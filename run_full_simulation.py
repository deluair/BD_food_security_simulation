# Full Bangladesh Food Security Simulation

import pandas as pd
import numpy as np
import os
import sys
import time
import json
import copy
import traceback

# Add project root to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change project_root to point to current working directory
project_root = os.getcwd()
sys.path.append(project_root)

# Import model classes and utility functions
try:
    from src.models.agricultural_production import AgriculturalProductionModel
    from src.models.climate_resilience import ClimateResilienceModel
    from src.models.food_supply_chain import FoodSupplyChainModel
    from src.models.socioeconomic_dynamics import SocioeconomicDynamicsModel
    from src.models.policy_interventions import PolicyInterventionsModel
    from src.models.nutritional_outcomes import NutritionalOutcomesModel
    from src.models.market_dynamics import MarketDynamicsModel
    from src.visualization.visualize import plot_time_series, plot_distribution, plot_correlation_heatmap
    from src.reporting.generate_report import generate_html_report
except ImportError as e:
    print(f"Error importing simulation components: {e}")
    print("Please ensure all model, visualization, and reporting files exist in the 'src' directory and dependencies are installed.")
    sys.exit(1)

# --- Simulation Configuration ---
START_YEAR = 2025
END_YEAR = 2035 # Simulate 11 years (2025-2035 inclusive)

# --- Realistic Data Placeholders (Bangladesh context) ---
INITIAL_POPULATION = 170e6
INITIAL_GDP_PER_CAPITA = 2600
INITIAL_STUNTING_RATE = 0.28
INITIAL_WASTING_RATE = 0.08
INITIAL_RICE_PRODUCTION = 38e6

# --- Scenario Definitions ---
BASE_CONFIG = {
    'simulation_name': 'BD_FoodSecurity_Scenario_Baseline',
    'start_year': START_YEAR,
    'end_year': END_YEAR,
    'initial_state': {
        'population': INITIAL_POPULATION,
        'gdp_per_capita': INITIAL_GDP_PER_CAPITA,
        'stunting_rate': INITIAL_STUNTING_RATE,
        'wasting_rate': INITIAL_WASTING_RATE,
        'rice_production': INITIAL_RICE_PRODUCTION,
    },
    'parameters': {
        'agricultural_production': {
            'yield_trends': {'rice': 0.01, 'wheat': 0.015, 'maize': 0.02},
            'climate_yield_sensitivity': {'rice': -0.05, 'wheat': -0.07}
        },
        'climate_resilience': {
            'temp_anomaly_trend': 0.03,
            'precip_change_trend': -0.005,
            'adaptation_effectiveness': 0.3
        },
        'food_supply_chain': {
            'storage_loss_rate': {'cereals': 0.06, 'perishables': 0.15},
            'transport_efficiency': 0.95
        },
        'socioeconomic_dynamics': {
            'population_growth_rate': 0.01,
            'gdp_growth_rate': 0.065,
            'income_elasticity_diet': 0.4
        },
        'policy_interventions': {
            'policy_scenario_active': 'baseline',
            'fertilizer_subsidy_level': 0.1,
            'safety_net_coverage': 0.2
        },
        'nutritional_outcomes': {
            'health_access_improvement_rate': 0.01,
            'base_nutrient_req': {'energy_kcal': 2100, 'protein_g': 50}
        },
        'market_dynamics': {
            'demand_elasticity': {'price': -0.3, 'income': 0.4},
            'price_transmission': {'producer_retail': 0.6},
            'world_prices': {'rice': 450, 'wheat': 350}
        }
    }
}

SCENARIOS = {
    "baseline": BASE_CONFIG,
    "high_climate_impact": copy.deepcopy(BASE_CONFIG),
    "enhanced_adaptation": copy.deepcopy(BASE_CONFIG),
    "policy_change_safety_net": copy.deepcopy(BASE_CONFIG),
}

# Modify specific parameters for non-baseline scenarios
SCENARIOS["high_climate_impact"]['simulation_name'] = 'BD_FoodSecurity_Scenario_HighClimateImpact'
SCENARIOS["high_climate_impact"]['parameters']['climate_resilience']['temp_anomaly_trend'] = 0.05
SCENARIOS["high_climate_impact"]['parameters']['climate_resilience']['precip_change_trend'] = -0.01

SCENARIOS["enhanced_adaptation"]['simulation_name'] = 'BD_FoodSecurity_Scenario_EnhancedAdaptation'
SCENARIOS["enhanced_adaptation"]['parameters']['climate_resilience']['adaptation_effectiveness'] = 0.6

SCENARIOS["policy_change_safety_net"]['simulation_name'] = 'BD_FoodSecurity_Scenario_PolicyChangeSafetyNet'
SCENARIOS["policy_change_safety_net"]['parameters']['policy_interventions']['policy_scenario_active'] = 'enhanced_safety_nets'
SCENARIOS["policy_change_safety_net"]['parameters']['policy_interventions']['safety_net_coverage'] = 0.4

def run_simulation_scenario(scenario_name, config):
    """
    Runs the food security simulation for a specific scenario.
    
    Args:
        scenario_name (str): Name of the scenario (for output naming).
        config (dict): The configuration dictionary for this scenario.
        
    Returns:
        dict: A dictionary containing aggregated simulation results for the scenario.
              Returns None if initialization fails.
    """
    start_year = config['start_year']
    end_year = config['end_year']
    parameters = config['parameters']
    initial_state = config['initial_state']

    print(f"--- Initializing Models for Scenario: {scenario_name} ---")
    try:
        agri_model = AgriculturalProductionModel(parameters.get('agricultural_production', {}))
        climate_model = ClimateResilienceModel(parameters.get('climate_resilience', {}))
        fsc_model = FoodSupplyChainModel(parameters.get('food_supply_chain', {}))
        socio_model = SocioeconomicDynamicsModel(parameters.get('socioeconomic_dynamics', {}))
        policy_model = PolicyInterventionsModel(parameters.get('policy_interventions', {}))
        nutrition_model = NutritionalOutcomesModel(parameters.get('nutritional_outcomes', {}))
        market_model = MarketDynamicsModel(parameters.get('market_dynamics', {}))
    except Exception as e:
        print(f"Error initializing models for scenario '{scenario_name}': {e}")
        return None

    # Load historical/initial data (using placeholders within models)
    try:
        nutrition_model.load_historical_data(None)
        market_model.load_historical_data(None)
        # Add other models' data loading here if they implement it
    except Exception as e:
        print(f"Error loading historical data for scenario '{scenario_name}': {e}")

    # --- Data Storage Setup ---
    # Define base results path relative to the project root
    base_results_path = os.path.join(project_root, 'results')
    scenario_results_path = os.path.join(base_results_path, scenario_name)
    plots_path = os.path.join(scenario_results_path, 'plots')
    try:
        os.makedirs(scenario_results_path, exist_ok=True)
        os.makedirs(plots_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating results directories for scenario '{scenario_name}': {e}")
        return None # Cannot save results, treat as failure

    results = {'yearly_outputs': []}

    # Initialize state variables based on config/initial data
    current_socioeconomic_state = {
        'population': {'total_population': initial_state.get('population', 170e6)},
        'economy': {'gdp_per_capita': initial_state.get('gdp_per_capita', 2600)},
        'income_distribution': {'gini_coefficient': 0.32}
    }
    # Initialize other state vars (climate, health, policy) if they carry over year-to-year
    current_health_state = {'sanitation_coverage': 0.8, 'disease_burden_index': 1.0}

    print(f"\n--- Starting Simulation: {start_year} to {end_year} for Scenario: {scenario_name} ---")
    sim_start_time = time.time()

    for year in range(start_year, end_year + 1):
        print(f"\n--- {scenario_name} | Simulating Year: {year} ---", flush=True)
        yearly_data = {'year': year}
        try:
            # --- Model Execution Order ---

            # 1. Policy Interventions
            system_state_for_policy = {
                'socioeconomic': current_socioeconomic_state,
                'agricultural_production': results['yearly_outputs'][-1]['production_output'] if results['yearly_outputs'] else {},
                'market_dynamics': results['yearly_outputs'][-1]['market_state'] if results['yearly_outputs'] else {},
                'food_supply_chain': results['yearly_outputs'][-1]['supply_chain_output'] if results['yearly_outputs'] else {},
            }
            policy_impacts_for_year = policy_model.simulate_policy_impacts(year, scenario_name, system_state_for_policy)
            yearly_data['policy_impacts'] = policy_impacts_for_year

            # 2. Climate Simulation
            prev_agri_state = results['yearly_outputs'][-1]['production_output'] if results['yearly_outputs'] else {}
            climate_resilience_output = climate_model.simulate_climate_resilience(
                year,
                agricultural_systems=prev_agri_state,
                socioeconomic_factors=current_socioeconomic_state,
                governance_systems=policy_impacts_for_year
            )
            yearly_data['climate_resilience_output'] = climate_resilience_output

            # 3. Socioeconomic Dynamics
            current_socioeconomic_state = socio_model.simulate_socioeconomic_factors(
                year,
                current_state=current_socioeconomic_state,
                governance_factors=policy_impacts_for_year,
                climate_impacts=climate_resilience_output
            )
            yearly_data['socioeconomic_state'] = copy.deepcopy(current_socioeconomic_state)

            # 4. Agricultural Production
            print("--- Running Agricultural Production Model...", flush=True)
            input_availability = {'fertilizer_access': 0.9, 'irrigation_coverage': 0.6}
            technology_adoption = {'improved_seeds_rate': 0.7}
            prev_market_prices = results['yearly_outputs'][-1]['market_state']['prices']['producer'] if results['yearly_outputs'] else {}
            production_output = agri_model.simulate_production(
                year, climate_resilience_output, input_availability, technology_adoption, prev_market_prices
            )
            yearly_data['production_output'] = production_output
            print("--- Finished Agricultural Production Model.", flush=True)

            # 5. Food Supply Chain
            print("--- Running Food Supply Chain Model...", flush=True)
            supply_chain_output = fsc_model.simulate_supply_chains(year, production_output)
            yearly_data['supply_chain_output'] = supply_chain_output
            food_availability_market = supply_chain_output.get('available_supply', production_output.get('total_food', {}))
            print("--- Finished Food Supply Chain Model.", flush=True)

            # 6. Market Dynamics
            print("--- Running Market Dynamics Model...", flush=True)
            policy_effects_for_market = {
                'trade_policy_effects': policy_impacts_for_year.get('trade_policy_effects', {}),
                'social_protection_effects': policy_impacts_for_year.get('social_protection_effects', {})
            }
            market_state = market_model.simulate_market_dynamics(
                year, supply_chain_output, current_socioeconomic_state, policy_effects_for_market
            )
            yearly_data['market_state'] = market_state
            print("--- Finished Market Dynamics Model.", flush=True)

            # 7. Nutritional Outcomes
            print("--- Running Nutritional Outcomes Model...", flush=True)
            food_availability_nutrition = market_state.get('market_supply', {})
            population = current_socioeconomic_state['population']['total_population']
            food_availability_nutrition_pc = {k: (v / population) * 1000 if population > 0 else 0 for k, v in food_availability_nutrition.items()}
            nutritional_outcomes = nutrition_model.simulate_nutritional_outcomes(
                year, food_availability_nutrition_pc, market_state.get('prices', {}).get('retail',{}),
                current_socioeconomic_state, current_health_state
            )
            yearly_data['nutritional_outcomes'] = nutritional_outcomes
            print("--- Finished Nutritional Outcomes Model.", flush=True)

            # Store results for the year
            print("--- Appending results for the year...", flush=True)
            results['yearly_outputs'].append(yearly_data)
            print("--- Finished appending results.", flush=True)

        except Exception as e:
            print(f"ERROR during simulation for year {year} in scenario '{scenario_name}': {e}")
            print(f"Aborting scenario '{scenario_name}' due to error.")
            return None # Indicate failure

    sim_end_time = time.time()
    print(f"--- Simulation Finished for {scenario_name} ({sim_end_time - sim_start_time:.2f} seconds) ---", flush=True)

    # --- Post-processing and Aggregation ---
    print(f"\n--- Aggregating Results for {scenario_name} ---", flush=True)
    aggregated_results = {
        'scenario_name': scenario_name,
        'simulation_period': f"{start_year}-{end_year}",
        'config_summary': parameters # Store parameters used for reference
    }
    
    if results['yearly_outputs']:
        years_list = [res.get('year', np.nan) for res in results['yearly_outputs']]
        # Use .get() with defaults for robustness against missing keys in model outputs
        agg_data_dict = {
            'year': years_list,
            'total_population': [res.get('socioeconomic_state', {}).get('population', {}).get('total_population', np.nan) for res in results['yearly_outputs']],
            'gdp_per_capita': [res.get('socioeconomic_state', {}).get('economy', {}).get('gdp_per_capita', np.nan) for res in results['yearly_outputs']],
            'rice_production_total': [res.get('production_output', {}).get('total_food', {}).get('cereals', {}).get('rice', np.nan) for res in results['yearly_outputs']],
            'wheat_production_total': [res.get('production_output', {}).get('total_food', {}).get('cereals', {}).get('wheat', np.nan) for res in results['yearly_outputs']],
            'rice_price_retail': [res.get('market_state', {}).get('prices', {}).get('retail', {}).get('rice', np.nan) for res in results['yearly_outputs']],
            'stunting_prevalence': [res.get('nutritional_outcomes', {}).get('nutritional_status_indicators', {}).get('stunting_prevalence', np.nan) for res in results['yearly_outputs']],
            'wasting_prevalence': [res.get('nutritional_outcomes', {}).get('nutritional_status_indicators', {}).get('wasting_prevalence', np.nan) for res in results['yearly_outputs']],
            'avg_energy_intake': [res.get('nutritional_outcomes', {}).get('average_nutrient_intake_per_capita_day', {}).get('energy_kcal', np.nan) for res in results['yearly_outputs']],
        }

        try:
            agg_df = pd.DataFrame(agg_data_dict)
            csv_filepath = os.path.join(scenario_results_path, f'{scenario_name}_timeseries_summary.csv')
            agg_df.to_csv(csv_filepath, index=False)
            print(f"Saved aggregated data to {csv_filepath}")
            aggregated_results['dataframes'] = {'annual_summary': agg_df}

            # Extract key metrics (e.g., final year values or averages), checking for NaN
            final_row = agg_df.iloc[-1] if not agg_df.empty else None
            if final_row is not None:
                aggregated_results['key_metrics'] = {
                    'Final Population': f"{final_row.get('total_population', 0):,.0f}",
                    'Final GDP per Capita': f"${final_row.get('gdp_per_capita', 0):,.2f}",
                    'Final Stunting Rate': f"{final_row.get('stunting_prevalence', np.nan):.3f}" if pd.notna(final_row.get('stunting_prevalence')) else "N/A",
                    'Final Wasting Rate': f"{final_row.get('wasting_prevalence', np.nan):.3f}" if pd.notna(final_row.get('wasting_prevalence')) else "N/A",
                    'Avg Energy Intake (Final Year)': f"{final_row.get('avg_energy_intake', np.nan):.0f} kcal" if pd.notna(final_row.get('avg_energy_intake')) else "N/A",
                    'Avg Rice Production': f"{agg_df['rice_production_total'].mean() / 1e6:.2f} M Tonnes" if pd.notna(agg_df['rice_production_total'].mean()) else "N/A",
                }
            else:
                aggregated_results['key_metrics'] = {"Error": "No data to calculate final metrics"}

            # --- Visualization ---
            print(f"\n--- Generating Plots for {scenario_name} ---", flush=True)
            plot_filenames = []

            # Define plots to generate
            plots_to_make = []
            if 'rice_production_total' in agg_df.columns and not agg_df['rice_production_total'].isnull().all():
                plots_to_make.append({'func': plot_time_series, 'args': {'data': agg_df, 'y_column': ['rice_production_total', 'wheat_production_total'], 'title': f'{scenario_name}: Cereal Production', 'ylabel': 'Production (Tonnes)', 'filename': f'cereal_production_ts'}, 'filename_base': f'cereal_production_ts.png'})
            if 'stunting_prevalence' in agg_df.columns and not agg_df['stunting_prevalence'].isnull().all():
                plots_to_make.append({'func': plot_time_series, 'args': {'data': agg_df, 'y_column': 'stunting_prevalence', 'title': f'{scenario_name}: Stunting Rate', 'ylabel': 'Prevalence Rate', 'filename': f'stunting_rate_ts'}, 'filename_base': f'stunting_rate_ts.png'})
            if 'wasting_prevalence' in agg_df.columns and not agg_df['wasting_prevalence'].isnull().all():
                plots_to_make.append({'func': plot_time_series, 'args': {'data': agg_df, 'y_column': 'wasting_prevalence', 'title': f'{scenario_name}: Wasting Rate', 'ylabel': 'Prevalence Rate', 'filename': f'wasting_rate_ts'}, 'filename_base': f'wasting_rate_ts.png'})
            if 'avg_energy_intake' in agg_df.columns and not agg_df['avg_energy_intake'].isnull().all():
                plots_to_make.append({'func': plot_time_series, 'args': {'data': agg_df, 'y_column': 'avg_energy_intake', 'title': f'{scenario_name}: Average Energy Intake', 'ylabel': 'kcal/capita/day', 'filename': f'energy_intake_ts'}, 'filename_base': f'energy_intake_ts.png'})
            if 'rice_price_retail' in agg_df.columns and not agg_df['rice_price_retail'].isnull().all():
                plots_to_make.append({'func': plot_time_series, 'args': {'data': agg_df, 'y_column': 'rice_price_retail', 'title': f'{scenario_name}: Retail Price of Rice', 'ylabel': 'Price/kg', 'filename': f'rice_price_ts'}, 'filename_base': f'rice_price_ts.png'})
            
            # Correlation heatmap requires multiple non-null columns
            corr_cols = ['rice_production_total', 'stunting_prevalence', 'rice_price_retail', 'gdp_per_capita']
            valid_corr_cols = [col for col in corr_cols if col in agg_df.columns and not agg_df[col].isnull().all()]
            if len(valid_corr_cols) >= 2:
                plots_to_make.append({'func': plot_correlation_heatmap, 'args': {'data': agg_df[valid_corr_cols].dropna(), 'title': f'{scenario_name}: Indicator Correlations', 'filename': f'indicator_correlation'}, 'filename_base': f'indicator_correlation.png'})

            # Generate plots and collect filenames
            for plot_def in plots_to_make:
                try:
                    full_plot_path = os.path.join(plots_path, f"{scenario_name}_{plot_def['args']['filename']}.png")
                    plot_def['args']['filename'] = full_plot_path
                    plot_def['func'](**plot_def['args'])
                    plot_filenames.append(os.path.basename(full_plot_path))
                except Exception as e:
                    print(f"Error generating plot {plot_def['filename_base']}: {e}")

            aggregated_results['plot_filenames'] = plot_filenames

            # --- Reporting ---
            print(f"\n--- Generating HTML Report for {scenario_name} ---", flush=True)
            template_file = os.path.join(project_root, 'src', 'reporting', 'template.html')
            report_filename = f'{scenario_name}_simulation_report.html'
            report_filepath = os.path.join(scenario_results_path, report_filename)

            aggregated_results['plot_dir'] = 'plots'
            aggregated_results['report_title'] = f"Food Security Simulation Report: {scenario_name.replace('_', ' ').title()}"

            generate_html_report(
                simulation_results=aggregated_results,
                template_path=template_file,
                output_filename=report_filepath
            )

        except Exception as e:
            print(f"ERROR during post-processing for scenario '{scenario_name}': {e}")

    else:
        print(f"Warning: No yearly outputs generated for scenario {scenario_name}. Skipping aggregation, plots, and report.")
        aggregated_results = {}

    return aggregated_results

# Main function
if __name__ == "__main__":
    all_scenario_results = {}
    overall_start_time = time.time()
    
    print("\n--- Starting Full Scenario Simulations ---")
    
    for name, scenario_config in SCENARIOS.items():
        try:
            print(f"\n=== Running Scenario: {name} ===")
            results = run_simulation_scenario(name, scenario_config)
            if results:
                all_scenario_results[name] = results
                print(f"Scenario '{name}' completed successfully.")
            else:
                print(f"Scenario '{name}' failed to complete successfully.")
        except Exception as e:
            print(f"Error running scenario '{name}': {e}")
            traceback.print_exc()
    
    # Generate comprehensive HTML report if we have results
    if all_scenario_results and any(all_scenario_results.values()):
        try:
            template_file = os.path.join(project_root, 'src', 'reporting', 'template.html')
            report_path = os.path.join(project_root, 'results', 'bangladesh_food_security_report.html')
            generate_html_report(
                simulation_results=all_scenario_results,
                template_path=template_file,
                output_filename=report_path
            )
            print(f"Full HTML report generated at {report_path}")
        except Exception as e:
            print(f"Warning: Could not generate HTML report. Error: {e}")
        
    # --- Cross-Scenario Comparison ---
    print("\n--- Cross-Scenario Comparison ---", flush=True)
    comparison_data = []
    valid_scenarios = 0
    
    for name, results in all_scenario_results.items():
        if results and 'dataframes' in results and 'annual_summary' in results['dataframes'] and not results['dataframes']['annual_summary'].empty:
            df = results['dataframes']['annual_summary'].copy()
            df['scenario'] = name
            comparison_data.append(df)
            valid_scenarios += 1
        else:
            print(f"Warning: Results for scenario '{name}' are incomplete or missing 'annual_summary' DataFrame.")
    
    if comparison_data and valid_scenarios > 0:
        full_comparison_df = pd.concat(comparison_data, ignore_index=True)
        print(f"Comparison DataFrame created with data from {valid_scenarios} scenarios")
        
        comparison_results_dir = os.path.join(project_root, 'results', '_comparison')
        os.makedirs(comparison_results_dir, exist_ok=True)
        csv_comparison_filepath = os.path.join(comparison_results_dir, 'all_scenarios_summary.csv')
        
        try:
            full_comparison_df.to_csv(csv_comparison_filepath, index=False)
            print(f"Saved comparison data to {csv_comparison_filepath}")
        except Exception as e:
            print(f"Error saving comparison CSV: {e}")
    else:
        print("No valid results available for cross-scenario comparison.")
    
    overall_end_time = time.time()
    print(f"\nTotal simulation time: {overall_end_time - overall_start_time:.2f} seconds")
    print("\n--- Simulation Run Finished ---") 