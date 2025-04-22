import jinja2
import pandas as pd
import os
import numpy as np
import datetime
import pathlib

# Get the project root directory (BD_food_security_simulation folder)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the output directory within the project
output_dir = os.path.join(project_root, 'results')
os.makedirs(output_dir, exist_ok=True)

# Set plots directory
plot_dir = os.path.join(output_dir, 'plots')
os.makedirs(plot_dir, exist_ok=True)

def generate_html_report(simulation_results, template_path, output_filename):
    """
    Generates an HTML report from simulation results using a Jinja2 template.

    Args:
        simulation_results (dict): A dictionary containing aggregated results
                                   (e.g., dataframes, key metrics).
                                   It should include:
                                   - plot_filenames: List of plot image filenames
                                   - dataframes: Dict of pandas DataFrames for summary tables
                                   - detailed_tables: Dict of pandas DataFrames for detailed scenario results
                                   - scenario_metrics: Dict of metrics for each scenario
                                   - scenario_names: List of scenario names
                                   - key_metrics: Dict of overall key metrics
                                   - main_takeaways: Dict of key takeaways and insights
        template_path (str): The path to the Jinja2 HTML template file.
        output_filename (str): The name for the output HTML report file (can be a full path).
    """
    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        return

    # Set up Jinja2 environment
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(os.path.basename(template_path))

    # Prepare context data for the template
    context = {
        'report_title': simulation_results.get('report_title', "Food Security Simulation Report"),
        'generation_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'simulation_period': simulation_results.get('simulation_period', 'N/A'),
        'key_metrics': simulation_results.get('key_metrics', {}), # e.g., final stunting rate
        'scenario_metrics': simulation_results.get('scenario_metrics', {}),  # Add scenario metrics to context
        'main_takeaways': simulation_results.get('main_takeaways', {}),  # Add main takeaways
        'summary_tables': {}, # Store dataframes as HTML tables
        'detailed_tables': simulation_results.get('detailed_tables', {}),  # Add detailed results tables
        'scenario_names': simulation_results.get('scenario_names', []),  # List of scenario names
        'scenario_plots': simulation_results.get('scenario_plots', {}),  # Individual scenario plots
        'plot_filenames': [], # Will be populated after validation
        'plot_dir': simulation_results.get('plot_dir', os.path.basename(plot_dir)) # Pass relative plot dir path
    }
    
    # Debug information
    print(f"Number of scenarios in metrics: {len(context['scenario_metrics'])}")
    for scenario, metrics in context['scenario_metrics'].items():
        print(f"Scenario: {scenario}, Metrics count: {len(metrics)}")

    # Convert pandas DataFrames to HTML tables
    for key, df in simulation_results.get('dataframes', {}).items():
        if isinstance(df, pd.DataFrame) and not df.empty:
            # Format numeric columns with 2 decimal places
            formatted_df = df.copy()
            for col in formatted_df.columns:
                if pd.api.types.is_numeric_dtype(formatted_df[col]) and col != 'year':
                    formatted_df[col] = formatted_df[col].round(2)
            context['summary_tables'][key] = formatted_df.to_html(classes='table table-striped table-hover', index=False)
        elif isinstance(df, pd.DataFrame) and df.empty:
            print(f"Warning: DataFrame '{key}' is empty. Skipping conversion.")
        else:
            print(f"Warning: Item '{key}' in dataframes is not a Pandas DataFrame. Skipping conversion.")


    # Get the plots directory (either from simulation_results or the default)
    plots_path = simulation_results.get('plots_path', '')
    scenario_name = simulation_results.get('scenario_name', '')
    
    # Verify and process plot filenames
    raw_plot_filenames = simulation_results.get('plot_filenames', [])
    print(f"Processing {len(raw_plot_filenames)} plot files for the report...")
    
    # Check all possible locations where plots might be stored
    potential_plot_dirs = [
        # Scenario-specific plot directory (preferred)
        plots_path,
        # Default locations
        os.path.join(os.path.dirname(output_filename), 'plots'),
        os.path.join(os.path.dirname(output_filename) if os.path.isabs(output_filename) else output_dir, 'plots'),
        plot_dir,
        os.path.join(output_dir, scenario_name, 'plots') if scenario_name else None,
        os.path.join(output_dir, 'plots')
    ]
    
    potential_plot_dirs = [d for d in potential_plot_dirs if d is not None]
    
    # Try to find each plot file
    for plot_file in raw_plot_filenames:
        found = False
        
        # First, check if it's an absolute path
        if os.path.isabs(plot_file) and os.path.exists(plot_file):
            context['plot_filenames'].append(os.path.basename(plot_file))
            found = True
            continue
        
        # Try all potential directories
        for plot_dir_path in potential_plot_dirs:
            if not plot_dir_path or not os.path.exists(plot_dir_path):
                continue
                
            # First try with the raw filename
            plot_path = os.path.join(plot_dir_path, plot_file)
            if os.path.exists(plot_path):
                context['plot_filenames'].append(plot_file)
                found = True
                print(f"Found plot: {plot_path}")
                break
                
            # Next try with scenario name prefix removed (if present)
            if scenario_name and plot_file.startswith(f"{scenario_name}_"):
                clean_name = plot_file[len(f"{scenario_name}_"):]
                plot_path = os.path.join(plot_dir_path, clean_name)
                if os.path.exists(plot_path):
                    context['plot_filenames'].append(clean_name)
                    found = True
                    print(f"Found plot: {plot_path}")
                    break
        
        if not found:
            print(f"Warning: Plot file not found in any location: {plot_file}")

    # Render the template
    html_content = template.render(context)

    # Handle output filename (can be a full path or just a filename)
    if os.path.isabs(output_filename):
        output_filepath = output_filename
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    else:
        output_filepath = os.path.join(output_dir, output_filename)
    
    # If we don't have any plots but should, give a clear message
    if not context['plot_filenames'] and raw_plot_filenames:
        print(f"WARNING: None of the {len(raw_plot_filenames)} plots could be found. The report will have empty plot sections.")
    
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report generated successfully: {output_filepath}")
        
        # Copy plots to the report's directory if needed
        report_dir = os.path.dirname(output_filepath)
        plots_output_dir = os.path.join(report_dir, context['plot_dir'])
        os.makedirs(plots_output_dir, exist_ok=True)
        
        # Ensure plots are in the right location for the HTML report
        for plot_file in context['plot_filenames']:
            for plot_dir_path in potential_plot_dirs:
                source_path = os.path.join(plot_dir_path, plot_file)
                if os.path.exists(source_path):
                    # Copy the plot file if it's not already in the right place
                    target_path = os.path.join(plots_output_dir, plot_file)
                    if not os.path.exists(target_path) or os.path.getsize(source_path) != os.path.getsize(target_path):
                        import shutil
                        shutil.copy2(source_path, target_path)
                        print(f"Copied plot from {source_path} to {target_path}")
                    break
        
        return output_filepath
    except Exception as e:
        print(f"Error writing HTML report file: {e}")
        return None

# Example usage (can be run if this file is executed directly)
if __name__ == '__main__':
    print("Report generation functions defined.")

    # Create dummy results for testing
    years = range(2025, 2036)
    dummy_results_df = pd.DataFrame({
        'year': years,
        'rice_production': [35 + i * 0.5 for i in range(len(years))],
        'stunting_rate': [0.28 - i * 0.005 for i in range(len(years))],
        'energy_intake': [2050 + i * 20 for i in range(len(years))],
        'rice_price': [40 + np.sin(i) * 5 for i in range(len(years))],
        'market_stability_index': [0.7 + i * 0.02 for i in range(len(years))],
    })

    # Create scenario-specific detailed results
    scenarios = ['baseline', 'high_climate_impact', 'enhanced_adaptation', 'policy_change_safety_net']
    detailed_tables = {}
    
    for scenario in scenarios:
        # Create unique variations for each scenario
        modifier = 1.0
        if scenario == 'high_climate_impact':
            modifier = 0.8
        elif scenario == 'enhanced_adaptation':
            modifier = 1.2
        elif scenario == 'policy_change_safety_net':
            modifier = 1.3
        
        scenario_df = pd.DataFrame({
            'year': years,
            'rice_production': [35 * modifier + i * 0.5 for i in range(len(years))],
            'stunting_rate': [0.28 / modifier - i * 0.005 for i in range(len(years))],
            'energy_intake': [2050 * modifier + i * 20 for i in range(len(years))],
            'rice_price': [40 + np.sin(i) * 5 * (2-modifier) for i in range(len(years))],
            'nutrition_index': [0.65 * modifier + i * 0.02 for i in range(len(years))],
            'market_volatility': [0.2 / modifier - i * 0.005 for i in range(len(years))],
        })
        detailed_tables[scenario] = scenario_df
    
    # Create scenario metrics
    scenario_metrics = {}
    for scenario in scenarios:
        # Use the last year's values from detailed tables
        scenario_df = detailed_tables[scenario]
        scenario_metrics[scenario] = {
            'Stunting Rate': f"{scenario_df['stunting_rate'].iloc[-1]:.3f}",
            'Rice Production': f"{scenario_df['rice_production'].iloc[-1]:.1f} M Tonnes",
            'Energy Intake': f"{scenario_df['energy_intake'].iloc[-1]:.0f} kcal",
            'Market Stability': f"{scenario_df['nutrition_index'].iloc[-1]:.2f}"
        }

    dummy_data = {
        'simulation_period': f"{years[0]}-{years[-1]}",
        'key_metrics': {
            'Final Stunting Rate': f"{dummy_results_df['stunting_rate'].iloc[-1]:.3f}",
            'Average Rice Production': f"{dummy_results_df['rice_production'].mean():.2f} M Tonnes",
            'Energy Intake (2035)': f"{dummy_results_df['energy_intake'].iloc[-1]:.0f} kcal",
            'Market Stability Index': f"{dummy_results_df['market_stability_index'].iloc[-1]:.2f}"
        },
        'scenario_metrics': scenario_metrics,
        'scenario_names': scenarios,
        'dataframes': {
            'annual_summary': dummy_results_df
        },
        'detailed_tables': detailed_tables,
        'main_takeaways': {
            'nutrition': 'Child stunting rates show consistent improvement across all scenarios, with the most significant gains in the Policy Change scenario.',
            'production': 'Rice production is projected to increase, but climate impacts may reduce yields by up to 20% in high-impact scenarios.',
            'markets': 'Price stability improves with enhanced adaptation measures, reducing volatility by approximately 40%.',
            'overall': 'The simulation suggests that targeted safety net policies combined with climate adaptation measures could substantially improve food security outcomes.'
        },
        'plot_filenames': [ # Assumes these plots exist in results/plots/
            'cereal_production_ts.png',
            'stunting_rate_ts.png',
            'wasting_rate_ts.png',
            'energy_intake_ts.png',
            'price_ts.png',
            'market_dynamics.png',
            'indicator_correlation.png',
            'correlation_scatter.png',
            'income_distribution_hist.png'
        ],
        'scenario_plots': {
            scenario: [f"{scenario}_stunting_ts.png", f"{scenario}_production_ts.png"] for scenario in scenarios
        }
    }

    # Define paths relative to the script's location (assuming standard structure)
    script_dir = os.path.dirname(__file__)
    template_file = os.path.join(script_dir, 'template.html')
    output_file = 'simulation_report.html' # Will be saved in 'results/' directory

    # Check if template exists before generating
    if not os.path.exists(template_file):
         print(f"Creating dummy template file at: {template_file}")
         # Create a very basic dummy template if it doesn't exist for testing
         dummy_template_content = """
         <!DOCTYPE html><html><head><title>{{ report_title }}</title></head>
         <body><h1>{{ report_title }}</h1><p>Generated: {{ generation_time }}</p>
         <h2>Plots</h2> {% for plot in plot_filenames %} <img src="{{ plot_dir }}/{{ plot }}" alt="{{ plot }}"><br/> {% endfor %}
         <h2>Tables</h2> {% for name, table in summary_tables.items() %}<h3>{{ name }}</h3>{{ table|safe }}{% endfor %}
         </body></html>
         """
         os.makedirs(os.path.dirname(template_file), exist_ok=True)
         with open(template_file, 'w') as f:
             f.write(dummy_template_content)

    generate_html_report(dummy_data, template_file, output_file)

