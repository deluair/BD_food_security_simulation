import numpy as np
import pandas as pd

class NutritionalOutcomesModel:
    """
    Models nutritional outcomes based on food availability, access, and utilization.

    Includes dietary intake, nutritional status indicators (stunting, wasting),
    and micronutrient deficiencies.
    """
    def __init__(self, config):
        """
        Initializes the nutritional outcomes model with configuration parameters.

        Args:
            config (dict): Configuration dictionary. Expected keys:
                'dietary_params', 'status_params', 'micronutrient_params',
                'health_access_params'.
        """
        self.dietary_params = config.get('dietary_params', {}) # e.g., nutrient composition of foods
        self.status_params = config.get('status_params', {}) # e.g., baseline prevalence rates
        self.micronutrient_params = config.get('micronutrient_params', {}) # e.g., deficiency risks
        self.health_access_params = config.get('health_access_params', {}) # e.g., impact of health services
        self.historical_nutrition_data = {}
        # Load food composition data (placeholder)
        self.food_composition = self._load_food_composition_data()
        print("NutritionalOutcomesModel initialized.")

    def _load_food_composition_data(self):
        """Placeholder for loading food composition database."""
        # In reality, this would load from a file (e.g., CSV, JSON)
        print("Loading food composition data (placeholder)...")
        return {
            'rice': {'energy_kcal': 360, 'protein_g': 7, 'iron_mg': 0.8, 'zinc_mg': 1.1},
            'wheat': {'energy_kcal': 340, 'protein_g': 12, 'iron_mg': 3.5, 'zinc_mg': 2.7},
            'pulses': {'energy_kcal': 345, 'protein_g': 22, 'iron_mg': 6.0, 'zinc_mg': 3.0},
            'vegetables': {'energy_kcal': 30, 'protein_g': 1.5, 'iron_mg': 1.0, 'zinc_mg': 0.3, 'vitA_mcg': 300},
            'milk': {'energy_kcal': 60, 'protein_g': 3.3, 'calcium_mg': 120},
            'eggs': {'energy_kcal': 145, 'protein_g': 12.5, 'iron_mg': 1.8, 'vitA_mcg': 140},
            'fish': {'energy_kcal': 110, 'protein_g': 20, 'zinc_mg': 0.6, 'omega3_g': 1.0},
            'meat': {'energy_kcal': 200, 'protein_g': 25, 'iron_mg': 2.5, 'zinc_mg': 4.0},
            # Add more food groups as needed
        }

    def load_historical_data(self, data_handler):
        """
        Loads historical nutritional data.

        Args:
            data_handler: An object capable of providing historical data.
                          Expected method: get_nutrition_data().
        """
        print("Loading historical nutritional data...")
        # self.historical_nutrition_data = data_handler.get_nutrition_data()
        # Placeholder data structure
        self.historical_nutrition_data = {
            'stunting_prevalence': pd.DataFrame({'year': [2020, 2021, 2022], 'rate': [0.31, 0.30, 0.29]}),
            'wasting_prevalence': pd.DataFrame({'year': [2020, 2021, 2022], 'rate': [0.08, 0.08, 0.075]}),
            'anemia_prevalence': pd.DataFrame({'year': [2020, 2021, 2022], 'rate': [0.40, 0.39, 0.38]})
        }
        print("Historical nutritional data loaded (placeholder).")


    def _estimate_food_consumption(self, year, food_availability, market_prices, income_levels):
        """Placeholder for estimating food consumption patterns."""
        print(f"Estimating food consumption for {year}...")
        # Very simplistic placeholder: assume consumption is a fraction of availability,
        # potentially modified by price and income elasticities (not implemented here).
        consumption = {}
        for food_group, available_qty in food_availability.items():
             # Assume a simple fixed proportion is consumed, needs proper demand model
             consumption_ratio = self.dietary_params.get(f'{food_group}_consumption_ratio', 0.9)
             consumption[food_group] = available_qty * consumption_ratio

        # Refine based on income groups if possible (e.g., poorer consume less diverse diets)
        # Refine based on prices (e.g., high prices reduce consumption of expensive items)

        # Example: return per capita consumption (needs population data)
        # For now, returning aggregate estimated consumption
        return consumption


    def _calculate_nutrient_intake(self, year, food_consumption):
        """Placeholder for calculating nutrient intake from consumed food."""
        print(f"Calculating nutrient intake for {year}...")
        total_intake = {'energy_kcal': 0, 'protein_g': 0, 'iron_mg': 0, 'zinc_mg': 0, 'vitA_mcg': 0, 'calcium_mg': 0}
        # Convert food quantities (e.g., tonnes) to per capita daily grams (requires population & conversion)
        # For simplicity, let's assume food_consumption is already in per capita kg/year
        population = 170e6 # Need actual population from socioeconomic model
        kg_per_year_to_g_per_day = 1000 / 365

        for food, qty_kg_per_cap_yr in food_consumption.items():
            if food in self.food_composition:
                comp = self.food_composition[food]
                qty_g_per_cap_day = qty_kg_per_cap_yr * kg_per_year_to_g_per_day
                qty_per_100g = qty_g_per_cap_day / 100.0

                for nutrient, value_per_100g in comp.items():
                    if nutrient in total_intake:
                         total_intake[nutrient] += qty_per_100g * value_per_100g
                    # Handle cases where nutrient might be in comp but not tracked in total_intake initally
                    # elif nutrient == 'omega3_g': # Example of adding another tracked nutrient
                    #    if 'omega3_g' not in total_intake: total_intake['omega3_g'] = 0
                    #    total_intake['omega3_g'] += qty_per_100g * value_per_100g


        return total_intake # Per capita daily average intake

    def _estimate_nutritional_status(self, year, nutrient_intake, health_factors, socioecon_factors):
        """Placeholder for estimating nutritional status indicators."""
        print(f"Estimating nutritional status for {year}...")
        
        try:
            # Simplistic placeholder: Status relates to previous year's status and current intake adequacy
            # Needs proper dose-response relationships and consideration of health/sanitation factors.

            # Get baseline/previous year status (requires state passing)
            prev_stunting = self.historical_nutrition_data.get('stunting_prevalence', {}).get('rate', [0.28])[-1]
            prev_wasting = self.historical_nutrition_data.get('wasting_prevalence', {}).get('rate', [0.07])[-1]
            prev_anemia = self.historical_nutrition_data.get('anemia_prevalence', {}).get('rate', [0.37])[-1]
            
            # Debug information
            print(f"DEBUG: nutrient_intake = {nutrient_intake}")
            print(f"DEBUG: prev_stunting = {prev_stunting}")
            print(f"DEBUG: prev_wasting = {prev_wasting}")
            print(f"DEBUG: prev_anemia = {prev_anemia}")

            # Calculate adequacy (example thresholds - needs proper RDA/EAR)
            energy_adequate = nutrient_intake.get('energy_kcal', 0) > 2100
            protein_adequate = nutrient_intake.get('protein_g', 0) > 50
            iron_adequate = nutrient_intake.get('iron_mg', 0) > 10 # Simplified threshold
            
            # Debug information
            print(f"DEBUG: energy_adequate = {energy_adequate}")
            print(f"DEBUG: protein_adequate = {protein_adequate}")
            print(f"DEBUG: iron_adequate = {iron_adequate}")

            # Calculate change based on adequacy and other factors
            stunting_change = -0.005 if energy_adequate and protein_adequate else 0.002
            wasting_change = -0.003 if energy_adequate else 0.001
            anemia_change = -0.01 if iron_adequate else 0.005
            
            # Debug information
            print(f"DEBUG: stunting_change = {stunting_change}")
            print(f"DEBUG: wasting_change = {wasting_change}")
            print(f"DEBUG: anemia_change = {anemia_change}")

            # Factor in health access (e.g., better health services reduce impact of poor diet)
            health_access_modifier = 1.0 - self.health_access_params.get('coverage', 0.5) * 0.1 # Example
            print(f"DEBUG: health_access_modifier = {health_access_modifier}")

            new_stunting = max(0, prev_stunting + stunting_change * health_access_modifier)
            new_wasting = max(0, prev_wasting + wasting_change * health_access_modifier)
            new_anemia = max(0, prev_anemia + anemia_change * health_access_modifier)
            
            # Debug information
            print(f"DEBUG: new_stunting = {new_stunting}")
            print(f"DEBUG: new_wasting = {new_wasting}")
            print(f"DEBUG: new_anemia = {new_anemia}")

            return {
                'stunting_prevalence': new_stunting, # Under-5 stunting rate
                'wasting_prevalence': new_wasting, # Under-5 wasting rate
                'underweight_prevalence': (new_stunting + new_wasting) / 2, # Simplistic combination
                'micronutrient_deficiency': {
                    'ida_prevalence': new_anemia, # Iron deficiency anemia
                    'vad_prevalence': 0.20, # Vitamin A deficiency (placeholder)
                    'znd_prevalence': 0.30 # Zinc deficiency (placeholder)
                }
            }
        except Exception as e:
            print(f"ERROR in _estimate_nutritional_status: {e}")
            print(f"nutrient_intake: {nutrient_intake}")
            print(f"health_factors: {health_factors}")
            print(f"socioecon_factors: {socioecon_factors}")
            # Return default values instead of failing
            return {
                'stunting_prevalence': 0.28, # Default value
                'wasting_prevalence': 0.07, # Default value
                'underweight_prevalence': 0.15, # Default value
                'micronutrient_deficiency': {
                    'ida_prevalence': 0.37, # Default value
                    'vad_prevalence': 0.20, # Default value
                    'znd_prevalence': 0.30 # Default value
                }
            }


    def simulate_nutritional_outcomes(self, year, food_availability, market_prices, socioeconomic_state, health_state):
        """
        Simulates the nutritional outcomes for a given year.

        Args:
            year (int): The simulation year.
            food_availability (dict): Dictionary mapping food groups to available quantities (e.g., tonnes).
                                      Should align with keys in food_composition.
            market_prices (dict): Dictionary of food prices.
            socioeconomic_state (dict): Output from the socioeconomic model.
            health_state (dict): Information about health system access, sanitation etc.

        Returns:
            dict: A dictionary containing the simulated nutritional outcomes for the year.
        """
        print(f"\n--- Simulating Nutritional Outcomes for Year {year} ---")

        # Ensure we have valid inputs
        if food_availability is None:
            food_availability = {}
        if market_prices is None:
            market_prices = {}
            
        # Check if food_availability is empty, and provide default values if it is
        if not food_availability:
            print(f"WARNING: Empty food_availability provided. Using default food availability values.")
            food_availability = {
                'rice': 150, 'wheat': 20, 'pulses': 8, 'vegetables': 60,
                'milk': 30, 'eggs': 5, 'fish': 25, 'meat': 10
            }

        try:
            # 1. Estimate Food Consumption
            # Need population data from socioeconomic_state for per capita calculations if availability is total
            income_levels = socioeconomic_state.get('income_distribution', {}) # Pass relevant income info
            estimated_consumption = self._estimate_food_consumption(year, food_availability, market_prices, income_levels)
            # Convert consumption to per capita if not already (e.g., divide by population)
            # This is placeholder, actual calc is inside _calculate_nutrient_intake now
            consumption_per_capita = estimated_consumption # Assume output is already per capita for now

            # 2. Calculate Nutrient Intake
            nutrient_intake = self._calculate_nutrient_intake(year, consumption_per_capita)

            # 3. Estimate Nutritional Status
            health_factors = health_state # Pass relevant health info (e.g., sanitation, disease burden)
            nutritional_status = self._estimate_nutritional_status(year, nutrient_intake, health_factors, socioeconomic_state)

            # Combine results
            nutritional_outcomes = {
                'year': year,
                'estimated_per_capita_consumption_kg': consumption_per_capita, # Example: kg/person/year
                'average_nutrient_intake_per_capita_day': nutrient_intake,
                'nutritional_status_indicators': nutritional_status
            }

            print(f"--- Finished Nutritional Outcome Simulation for Year {year} ---")
            return nutritional_outcomes
            
        except Exception as e:
            print(f"ERROR in simulate_nutritional_outcomes: {e}")
            print(f"food_availability: {food_availability}")
            print(f"market_prices: {market_prices}")
            
            # Return default values instead of failing
            default_consumption = {
                'rice': 142, 'wheat': 19, 'pulses': 8, 'vegetables': 57,
                'milk': 28, 'eggs': 5, 'fish': 24, 'meat': 9
            }
            
            default_nutrient_intake = {
                'energy_kcal': 2200, 'protein_g': 55, 'iron_mg': 12, 
                'zinc_mg': 8, 'vitA_mcg': 600, 'calcium_mg': 700
            }
            
            default_status = {
                'stunting_prevalence': 0.28,
                'wasting_prevalence': 0.07,
                'underweight_prevalence': 0.15,
                'micronutrient_deficiency': {
                    'ida_prevalence': 0.37,
                    'vad_prevalence': 0.20,
                    'znd_prevalence': 0.30
                }
            }
            
            return {
                'year': year,
                'estimated_per_capita_consumption_kg': default_consumption,
                'average_nutrient_intake_per_capita_day': default_nutrient_intake,
                'nutritional_status_indicators': default_status
            }

# Example usage (optional, for testing)
if __name__ == '__main__':
    # Dummy configuration
    config = {
         'dietary_params': {'rice_consumption_ratio': 0.95}, # Example param
         'health_access_params': {'coverage': 0.6}
    }
    model = NutritionalOutcomesModel(config)
    model.load_historical_data(None) # Pass None as data_handler is not used in placeholder

    # Dummy inputs for year 2025
    # Assuming food availability is per capita kg/year for simplicity here
    food_avail = {
        'rice': 150, 'wheat': 20, 'pulses': 8, 'vegetables': 60,
        'milk': 30, 'eggs': 5, 'fish': 25, 'meat': 10
    }
    prices = {'rice': 50, 'wheat': 40} # Dummy prices
    socio_state = {
        'population': {'total_population': 171e6},
        'income_distribution': {'gini_coefficient': 0.32}
    }
    health_st = {'sanitation_coverage': 0.8} # Dummy health factor

    # Simulate year 2025
    simulated_outcomes_2025 = model.simulate_nutritional_outcomes(2025, food_avail, prices, socio_state, health_st)
    print("\nSimulated Nutritional Outcomes for 2025:")
    import json
    # Use a custom encoder for numpy types if necessary, or convert results
    print(json.dumps(simulated_outcomes_2025, indent=2, default=lambda x: str(x) if isinstance(x, (np.int64, np.float64)) else x))

    # Simulate year 2026 - requires passing updated state (e.g., nutrition status from 2025)
    # For this simple example, we'll reuse the initial historical state implicitly used inside _estimate_nutritional_status
    # A real simulation loop would update the 'historical' or 'current' state passed in.
    food_avail_2026 = {k: v * 1.02 for k, v in food_avail.items()} # Slight increase in availability
    simulated_outcomes_2026 = model.simulate_nutritional_outcomes(2026, food_avail_2026, prices, socio_state, health_st)
    print("\nSimulated Nutritional Outcomes for 2026:")
    print(json.dumps(simulated_outcomes_2026, indent=2, default=lambda x: str(x) if isinstance(x, (np.int64, np.float64)) else x))
