import numpy as np
import pandas as pd

class SocioeconomicDynamicsModel:
    """
    Models socioeconomic factors influencing food security.

    Includes population dynamics, economic growth, income distribution,
    social safety nets, and livelihood strategies.
    """
    def __init__(self, config):
        """
        Initializes the socioeconomic model with configuration parameters.

        Args:
            config (dict): Configuration dictionary. Expected keys:
                'population_params', 'economic_params', 'income_params',
                'safety_net_params', 'livelihood_params'.
        """
        self.population_params = config.get('population_params', {})
        self.economic_params = config.get('economic_params', {})
        self.income_params = config.get('income_params', {})
        self.safety_net_params = config.get('safety_net_params', {})
        self.livelihood_params = config.get('livelihood_params', {})
        self.historical_socioeconomic_data = {}
        print("SocioeconomicDynamicsModel initialized.")

    def load_historical_data(self, data_handler):
        """
        Loads historical socioeconomic data.

        Args:
            data_handler: An object capable of providing historical data.
                          Expected method: get_socioeconomic_data().
        """
        print("Loading historical socioeconomic data...")
        # self.historical_socioeconomic_data = data_handler.get_socioeconomic_data()
        # Placeholder data structure
        self.historical_socioeconomic_data = {
            'population': pd.DataFrame({'year': [2020, 2021, 2022], 'total_pop': [165e6, 167e6, 169e6]}),
            'gdp_per_capita': pd.DataFrame({'year': [2020, 2021, 2022], 'gdp_pc': [1900, 2000, 2100]})
        }
        print("Historical socioeconomic data loaded (placeholder).")

    def _simulate_population_dynamics(self, year, current_population_data):
        """Placeholder for simulating population changes."""
        print(f"Simulating population dynamics for {year}...")
        # Basic placeholder: simple growth rate
        growth_rate = self.population_params.get('annual_growth_rate', 0.01) # Example 1%
        
        # Handle different input formats safely
        last_pop = 170e6  # Default value if nothing else works
        
        if isinstance(current_population_data, dict):
            # Try to get total_population from dictionary
            if 'total_population' in current_population_data:
                last_pop_value = current_population_data.get('total_population')
                if isinstance(last_pop_value, (int, float)):
                    last_pop = last_pop_value
                else:
                    print(f"Warning: Non-numeric population value: {last_pop_value}, using default")
        
        # Calculate new population
        new_pop = last_pop * (1 + growth_rate)
        
        return {
            'total_population': new_pop,
            'urban_population': new_pop * 0.4, # Example split
            'rural_population': new_pop * 0.6,
            'age_distribution': {'0-14': 0.28, '15-64': 0.67, '65+': 0.05} # Placeholder distribution
        }

    def _simulate_economic_growth(self, year, current_economic_data):
        """Placeholder for simulating economic growth."""
        print(f"Simulating economic growth for {year}...")
        # Basic placeholder: simple GDP growth
        gdp_growth_rate = self.economic_params.get('gdp_growth_rate', 0.06) # Example 6%
        
        # Handle different input formats safely
        last_gdp_pc = 2200  # Default value if nothing else works
        
        if isinstance(current_economic_data, dict):
            # Try to get gdp_per_capita from dictionary
            if 'gdp_per_capita' in current_economic_data:
                last_gdp_value = current_economic_data.get('gdp_per_capita')
                if isinstance(last_gdp_value, (int, float)):
                    last_gdp_pc = last_gdp_value
                else:
                    print(f"Warning: Non-numeric GDP value: {last_gdp_value}, using default")
        
        # Calculate new GDP per capita
        new_gdp_pc = last_gdp_pc * (1 + gdp_growth_rate)
        
        return {
            'gdp_per_capita': new_gdp_pc,
            'sectoral_contribution': {'agriculture': 0.12, 'industry': 0.35, 'services': 0.53}, # Placeholder
            'inflation_rate': self.economic_params.get('inflation_rate', 0.055) # Example
        }

    def _simulate_income_distribution(self, year, population_data, economic_data):
        """Placeholder for simulating income distribution."""
        print(f"Simulating income distribution for {year}...")
        # Basic placeholder: fixed Gini or simple relation to GDP
        gini_coefficient = self.income_params.get('gini_coefficient', 0.33) # Example
        
        # Extract GDP per capita safely
        gdp_per_capita = 2200  # Default
        if isinstance(economic_data, dict):
            gdp_value = economic_data.get('gdp_per_capita', 2200)
            if isinstance(gdp_value, (int, float)):
                gdp_per_capita = gdp_value
            else:
                print(f"Warning: Non-numeric GDP value for income calculation: {gdp_value}, using default")
        
        # Calculate poverty rate using GDP
        poverty_headcount = max(0.1, 0.25 - (gdp_per_capita - 2200) / 5000) # Simplistic relation
        
        return {
            'gini_coefficient': gini_coefficient,
            'poverty_headcount_ratio': poverty_headcount, # National
            'income_quintiles': [0.08, 0.12, 0.16, 0.22, 0.42] # Placeholder shares
        }

    def _simulate_social_safety_nets(self, year, economic_data, governance_factors):
        """Placeholder for simulating social safety net impact."""
        print(f"Simulating social safety nets for {year}...")
        # Placeholder: coverage based on config and maybe economic state
        base_coverage = self.safety_net_params.get('base_coverage', 0.25) # Example 25% of poor
        effectiveness = self.safety_net_params.get('effectiveness', 0.7) # Example 70% effective transfer
        
        # Extract policy scaling factor safely
        policy_scaling = 1.0  # Default value
        
        if isinstance(governance_factors, dict):
            scaling_value = governance_factors.get('safety_net_investment_scale', 1.0)
            if isinstance(scaling_value, (int, float)):
                policy_scaling = scaling_value
            else:
                print(f"Warning: Non-numeric policy scaling value: {scaling_value}, using default")
        
        return {
            'coverage_rate': base_coverage * policy_scaling,
            'transfer_effectiveness': effectiveness,
            'program_types': ['cash_transfer', 'food_assistance', 'public_works'] # Placeholder
        }

    def _simulate_livelihoods(self, year, population_data, economic_data, climate_impacts):
        """Placeholder for simulating livelihood strategies."""
        print(f"Simulating livelihoods for {year}...")
        # Extract agri_labor_shift safely from potentially nested structure
        agri_labor_shift = 0.0  # Default value

        # Handle case when climate_impacts is a dictionary
        if isinstance(climate_impacts, dict):
            # Try to get agri_labor_shift from possible locations in the dictionary
            if 'agri_labor_shift' in climate_impacts:
                agri_labor_shift = climate_impacts.get('agri_labor_shift', 0.0)
            elif 'labor_impacts' in climate_impacts and isinstance(climate_impacts['labor_impacts'], dict):
                agri_labor_shift = climate_impacts['labor_impacts'].get('agri_labor_shift', 0.0)
            elif 'agricultural_impacts' in climate_impacts and isinstance(climate_impacts['agricultural_impacts'], dict):
                agri_labor_shift = climate_impacts['agricultural_impacts'].get('labor_shift', 0.0)

        # Make sure agri_labor_shift is a number
        if not isinstance(agri_labor_shift, (int, float)):
            print(f"Warning: Non-numeric agri_labor_shift value: {agri_labor_shift}, using 0.0")
            agri_labor_shift = 0.0

        # Placeholder: distribution based on broad sectors, potentially affected by climate
        agri_share = 0.40 - agri_labor_shift  # Example base, shifted by climate
        industry_share = 0.25
        services_share = 0.35 + agri_labor_shift
        # Ensure shares sum to 1 (simple normalization)
        total_share = agri_share + industry_share + services_share
        
        # Check for zero division
        if total_share == 0:
             print("Warning: total_share is zero, cannot normalize livelihood shares.", flush=True)
             agri_share = 1/3
             industry_share = 1/3
             services_share = 1/3
        else:
            agri_share /= total_share
            industry_share /= total_share
            services_share /= total_share

        return {
            'livelihood_distribution': {
                'agriculture': agri_share,
                'industry': industry_share,
                'services': services_share,
                'remittances_dependency': self.livelihood_params.get('remittance_dependency', 0.1) # Example
            },
            'migration_patterns': { # Placeholder
                'rural_urban_rate': 0.015,
                'international_rate': 0.002
            }
        }

    def simulate_socioeconomic_factors(self, year, current_state, governance_factors, climate_impacts):
        """
        Simulates the socioeconomic factors for a given year.

        Args:
            year (int): The simulation year.
            current_state (dict): Dictionary containing the current state
                                  (e.g., population, economy from previous year).
            governance_factors (dict): Factors related to policy and governance.
            climate_impacts (dict): Impacts from the climate model affecting livelihoods.

        Returns:
            dict: A dictionary containing the simulated socioeconomic factors for the year.
        """
        print(f"\n--- Simulating Socioeconomic Factors for Year {year} ---")

        # Ensure inputs are valid dictionaries
        if not isinstance(current_state, dict):
            print(f"Warning: current_state is not a dictionary, using empty dict. Type: {type(current_state)}")
            current_state = {}
            
        if not isinstance(governance_factors, dict):
            print(f"Warning: governance_factors is not a dictionary, using empty dict. Type: {type(governance_factors)}")
            governance_factors = {}
            
        if not isinstance(climate_impacts, dict):
            print(f"Warning: climate_impacts is not a dictionary, using empty dict. Type: {type(climate_impacts)}")
            climate_impacts = {}

        # Extract relevant current state data or use defaults/historical
        pop_data = current_state.get('population', self.historical_socioeconomic_data.get('population', {}))
        econ_data = current_state.get('economy', self.historical_socioeconomic_data.get('gdp_per_capita', {}))
        # If using pandas dataframes from historical, might need to extract latest year's values
        # For simplicity here, assume current_state holds the necessary scalar values or dicts

        # Simulate components
        population_results = self._simulate_population_dynamics(year, pop_data)
        economic_results = self._simulate_economic_growth(year, econ_data)
        income_results = self._simulate_income_distribution(year, population_results, economic_results)
        safety_net_results = self._simulate_social_safety_nets(year, economic_results, governance_factors)
        livelihood_results = self._simulate_livelihoods(year, population_results, economic_results, climate_impacts)

        # Combine results
        socioeconomic_state = {
            'year': year,
            'population': population_results,
            'economy': economic_results,
            'income_distribution': income_results,
            'social_safety_nets': safety_net_results,
            'livelihoods': livelihood_results
        }

        print(f"--- Finished Socioeconomic Simulation for Year {year} ---")
        return socioeconomic_state

# Example usage (optional, for testing)
if __name__ == '__main__':
    # Dummy configuration
    config = {
        'population_params': {'annual_growth_rate': 0.011},
        'economic_params': {'gdp_growth_rate': 0.065, 'inflation_rate': 0.06},
        'income_params': {'gini_coefficient': 0.32},
        'safety_net_params': {'base_coverage': 0.30, 'effectiveness': 0.75},
        'livelihood_params': {'remittance_dependency': 0.12}
    }
    model = SocioeconomicDynamicsModel(config)
    model.load_historical_data(None) # Pass None as data_handler is not used in placeholder

    # Dummy initial state and factors for year 2025
    initial_state = {
         'population': {'total_population': 171e6},
         'economy': {'gdp_per_capita': 2300}
    }
    gov_factors = {'safety_net_investment_scale': 1.1}
    clim_impacts = {'agri_labor_shift': 0.01} # Example climate impact shifting labor

    # Simulate year 2025
    simulated_factors_2025 = model.simulate_socioeconomic_factors(2025, initial_state, gov_factors, clim_impacts)
    print("\nSimulated Socioeconomic Factors for 2025:")
    import json
    print(json.dumps(simulated_factors_2025, indent=2))

    # Simulate year 2026 using results from 2025
    simulated_factors_2026 = model.simulate_socioeconomic_factors(2026, simulated_factors_2025, gov_factors, clim_impacts)
    print("\nSimulated Socioeconomic Factors for 2026:")
    print(json.dumps(simulated_factors_2026, indent=2))
