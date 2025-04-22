"""
Agricultural Production Systems Model for Bangladesh Food Security Simulation
"""
import numpy as np
import pandas as pd


class AgriculturalProductionModel:
    """Model diverse agricultural production systems in Bangladesh
    
    This class simulates the agricultural production systems in Bangladesh,
    including rice production, diversified crops, aquaculture, fisheries,
    and livestock systems.
    """
    
    def __init__(self, config):
        """Initialize agricultural production model with configuration parameters
        
        Args:
            config (dict): Configuration dictionary containing parameters for agricultural systems
        """
        # Core agricultural system parameters
        self.crop_systems = config.get('crop_systems', {})
        self.livestock_systems = config.get('livestock_systems', {})
        self.fisheries_systems = config.get('fisheries_systems', {})
        self.production_practices = config.get('production_practices', {})
        self.input_dependencies = config.get('input_dependencies', {})
        self.seasonal_patterns = config.get('seasonal_patterns', {})
        self.land_characteristics = config.get('land_characteristics', {})
        self.productivity_factors = config.get('productivity_factors', {})
        
        # Historical production data
        self.historical_data = {}
        
        # Initialize subsystems
        self._init_rice_production_systems()
        self._init_diversified_crop_systems()
        self._init_aquaculture_fisheries_systems()
        self._init_livestock_poultry_systems()
    
    def _init_rice_production_systems(self):
        """Initialize rice production systems for Bangladesh"""
        self.rice_systems = {
            'boro': {
                'base_yield_kg_ha': 4500,  # kg per hectare
                'base_area_ha': 4900000,  # hectares
                'yield_projections': {},
                'water_requirements': {},
                'input_sensitivity': {},
                'climate_vulnerability': {}
            },
            'aus': {
                'base_yield_kg_ha': 3000,  # kg per hectare
                'base_area_ha': 1100000,  # hectares
                'resilience_metrics': {},
                'input_sensitivity': {},
                'climate_vulnerability': {}
            },
            'aman': {
                'base_yield_kg_ha': 3800,  # kg per hectare
                'base_area_ha': 5500000,  # hectares
                'resilience_metrics': {},
                'input_sensitivity': {},
                'climate_vulnerability': {}
            },
            'hybrid_varieties': {
                'adoption_rates': {},
                'yield_advantage': {},
                'input_requirements': {}
            },
            'modern_varieties': {
                'adoption_rates': {},
                'yield_advantage': {},
                'input_requirements': {}
            }
        }
    
    def _init_diversified_crop_systems(self):
        """Initialize diversified crop production systems"""
        self.diversified_crops = {
            'wheat_maize': {
                'productivity_trends': {},
                'area_expansion': {},
                'market_integration': {}
            },
            'pulses_oilseeds': {
                'productivity_trends': {},
                'area_expansion': {},
                'market_integration': {}
            },
            'vegetables': {
                'productivity_trends': {},
                'area_expansion': {},
                'market_integration': {}
            },
            'fruits': {
                'productivity_trends': {},
                'area_expansion': {},
                'market_integration': {}
            },
            'potato_tubers': {
                'productivity_trends': {},
                'area_expansion': {},
                'market_integration': {}
            },
            'homestead_gardens': {
                'productivity_trends': {},
                'nutritional_contribution': {},
                'adoption_rates': {}
            }
        }
    
    def _init_aquaculture_fisheries_systems(self):
        """Initialize aquaculture and fisheries production systems"""
        self.aquaculture_fisheries = {
            'pond_aquaculture': {
                'productivity_trends': {},
                'area_expansion': {},
                'species_diversity': {}
            },
            'cage_pen_culture': {
                'productivity_trends': {},
                'area_expansion': {},
                'species_diversity': {}
            },
            'shrimp_prawn': {
                'productivity_trends': {},
                'area_expansion': {},
                'sustainability_metrics': {},
                'export_orientation': {}
            },
            'capture_fisheries': {
                'productivity_trends': {},
                'sustainability_metrics': {},
                'conservation_effectiveness': {}
            },
            'small_indigenous_fish': {
                'productivity_trends': {},
                'nutritional_contribution': {},
                'sustainability_metrics': {}
            },
            'integrated_rice_fish': {
                'productivity_trends': {},
                'adoption_rates': {},
                'synergy_benefits': {}
            }
        }
    
    def _init_livestock_poultry_systems(self):
        """Initialize livestock and poultry production systems"""
        self.livestock_poultry = {
            'dairy': {
                'productivity_trends': {},
                'herd_composition': {},
                'commercialization_levels': {}
            },
            'poultry': {
                'productivity_trends': {},
                'flock_composition': {},
                'commercialization_levels': {},
                'backyard_contribution': {}
            },
            'small_ruminants': {
                'productivity_trends': {},
                'herd_composition': {},
                'commercialization_levels': {}
            },
            'feed_systems': {
                'availability_trends': {},
                'quality_metrics': {},
                'price_dynamics': {}
            },
            'animal_health': {
                'disease_prevalence': {},
                'service_coverage': {},
                'vaccination_rates': {}
            }
        }
    
    def load_historical_data(self, data_handler):
        """Load historical production data from data handler
        
        Args:
            data_handler: Data handler object providing access to data sources
        """
        self.historical_data = data_handler.get_agricultural_production_data()
    
    def simulate_rice_production(self, year, climate_factors, input_availability, technology_adoption):
        """Simulate rice production for a specific year
        
        Args:
            year (int): Simulation year
            climate_factors (dict): Climate conditions affecting production (e.g., temp_anomaly, rainfall_deviation)
            input_availability (dict): Availability of agricultural inputs (e.g., water_ratio, fertilizer_ratio)
            technology_adoption (dict): Adoption rates of technologies (e.g., hybrid_adoption, modern_adoption)
            
        Returns:
            dict: Simulated rice production volumes by variety and season
        """
        # Debug prints
        print("DEBUG: Rice production inputs:")
        print(f"  year: {year}, type: {type(year)}")
        print(f"  climate_factors: {type(climate_factors)}")
        print(f"  input_availability: {type(input_availability)}")
        print(f"  technology_adoption: {type(technology_adoption)}")
        
        production = {}
        total_production = 0

        # --- Simulation for each rice type (Boro, Aus, Aman) ---
        for rice_type in ['boro', 'aus', 'aman']:
            print(f"DEBUG: Processing rice_type: {rice_type}")
            if rice_type not in self.rice_systems:
                print(f"DEBUG: rice_type {rice_type} not found in self.rice_systems")
                production[rice_type] = 0
                continue

            # Get baseline yield and area from initialized values
            base_yield = self.rice_systems[rice_type].get('base_yield_kg_ha', 3000)  # kg/ha
            base_area_ha = self.rice_systems[rice_type].get('base_area_ha', 100000)  # hectares
            print(f"DEBUG: base_yield: {base_yield}, type: {type(base_yield)}")
            print(f"DEBUG: base_area_ha: {base_area_ha}, type: {type(base_area_ha)}")

            # 1. Climate Impact Adjustment
            # Simplified climate impact calculation
            climate_impact_factor = 1.0
            # Robustness check for sensitivity value
            temp_sensitivity = self.rice_systems[rice_type].get('climate_vulnerability', {}).get('temp_sensitivity', -0.05)
            print(f"DEBUG: temp_sensitivity: {temp_sensitivity}, type: {type(temp_sensitivity)}")
            if not isinstance(temp_sensitivity, (int, float)):
                print(f"Warning: Non-numeric temp_sensitivity found for {rice_type}, using 0.")
                temp_sensitivity = 0 # Default to 0 effect if config is wrong
            temp_effect = climate_factors.get('temp_anomaly', 0) * temp_sensitivity
            print(f"DEBUG: climate_factors.get('temp_anomaly', 0): {climate_factors.get('temp_anomaly', 0)}, type: {type(climate_factors.get('temp_anomaly', 0))}")
            print(f"DEBUG: temp_effect: {temp_effect}, type: {type(temp_effect)}")

            # Robustness check for sensitivity value
            rain_sensitivity = self.rice_systems[rice_type].get('climate_vulnerability', {}).get('rain_sensitivity', 0.1)
            print(f"DEBUG: rain_sensitivity: {rain_sensitivity}, type: {type(rain_sensitivity)}")
            if not isinstance(rain_sensitivity, (int, float)):
                print(f"Warning: Non-numeric rain_sensitivity found for {rice_type}, using 0.")
                rain_sensitivity = 0 # Default to 0 effect if config is wrong
            rain_effect = climate_factors.get('rainfall_deviation', 0) * rain_sensitivity
            print(f"DEBUG: climate_factors.get('rainfall_deviation', 0): {climate_factors.get('rainfall_deviation', 0)}, type: {type(climate_factors.get('rainfall_deviation', 0))}")
            print(f"DEBUG: rain_effect: {rain_effect}, type: {type(rain_effect)}")

            climate_impact_factor += temp_effect + rain_effect
            # Add more complex factors: extreme events, sea level rise (for Aman), etc.
            # Ensure climate factor is reasonable (e.g., not negative)
            climate_impact_factor = max(0.1, climate_impact_factor) # Prevent zero or negative yield from climate alone
            print(f"DEBUG: climate_impact_factor: {climate_impact_factor}, type: {type(climate_impact_factor)}")
            
            # 2. Input Availability Adjustment
            input_factor = 1.0
            # Robustness check for sensitivity values
            water_sensitivity = self.rice_systems[rice_type].get('input_sensitivity', {}).get('water', 0.5)
            print(f"DEBUG: water_sensitivity: {water_sensitivity}, type: {type(water_sensitivity)}")
            if not isinstance(water_sensitivity, (int, float)):
                print(f"Warning: Non-numeric water sensitivity found for {rice_type}, using 0.")
                water_sensitivity = 0
            fert_sensitivity = self.rice_systems[rice_type].get('input_sensitivity', {}).get('fertilizer', 0.3)
            print(f"DEBUG: fert_sensitivity: {fert_sensitivity}, type: {type(fert_sensitivity)}")
            if not isinstance(fert_sensitivity, (int, float)):
                print(f"Warning: Non-numeric fertilizer sensitivity found for {rice_type}, using 0.")
                fert_sensitivity = 0

            # Calculate effect based on availability and sensitivity
            water_effect = input_availability.get('water_ratio', 1.0) * water_sensitivity
            print(f"DEBUG: input_availability.get('water_ratio', 1.0): {input_availability.get('water_ratio', 1.0)}, type: {type(input_availability.get('water_ratio', 1.0))}")
            print(f"DEBUG: water_effect: {water_effect}, type: {type(water_effect)}")
            
            fert_effect = input_availability.get('fertilizer_ratio', 1.0) * fert_sensitivity
            print(f"DEBUG: input_availability.get('fertilizer_ratio', 1.0): {input_availability.get('fertilizer_ratio', 1.0)}, type: {type(input_availability.get('fertilizer_ratio', 1.0))}")
            print(f"DEBUG: fert_effect: {fert_effect}, type: {type(fert_effect)}")
            
            # Adjust base factor (1.0) by weighted effect relative to full availability
            base_component = max(0, 1.0 - water_sensitivity - fert_sensitivity) # Ensure base is not negative
            input_factor = base_component + water_effect + fert_effect
            # Ensure input factor is reasonable
            input_factor = max(0.1, input_factor) # Prevent zero or negative yield from inputs alone
            print(f"DEBUG: input_factor: {input_factor}, type: {type(input_factor)}")
            
            # 3. Technology Adoption Impact
            # Weighted average yield based on adoption of modern/hybrid varieties
            tech_factor = 1.0
            modern_adoption = technology_adoption.get('modern_adoption', 0) 
            print(f"DEBUG: modern_adoption: {modern_adoption}, type: {type(modern_adoption)}")
            hybrid_adoption = technology_adoption.get('hybrid_adoption', 0)
            print(f"DEBUG: hybrid_adoption: {hybrid_adoption}, type: {type(hybrid_adoption)}")
            traditional_adoption = max(0, 1 - modern_adoption - hybrid_adoption)
            print(f"DEBUG: traditional_adoption: {traditional_adoption}, type: {type(traditional_adoption)}")

            modern_yield_advantage = self.rice_systems.get('modern_varieties', {}).get('yield_advantage', 1.2) # Example 20% advantage
            print(f"DEBUG: modern_yield_advantage: {modern_yield_advantage}, type: {type(modern_yield_advantage)}")
            # Check if modern_yield_advantage is a dictionary and provide a default value if it is
            if isinstance(modern_yield_advantage, dict):
                print(f"Warning: modern_yield_advantage is a dictionary, using default value 1.2")
                modern_yield_advantage = 1.2  # Default 20% advantage
            
            hybrid_yield_advantage = self.rice_systems.get('hybrid_varieties', {}).get('yield_advantage', 1.5) # Example 50% advantage
            print(f"DEBUG: hybrid_yield_advantage: {hybrid_yield_advantage}, type: {type(hybrid_yield_advantage)}")
            # Check if hybrid_yield_advantage is a dictionary and provide a default value if it is
            if isinstance(hybrid_yield_advantage, dict):
                print(f"Warning: hybrid_yield_advantage is a dictionary, using default value 1.5")
                hybrid_yield_advantage = 1.5  # Default 50% advantage

            avg_yield_advantage = (traditional_adoption * 1.0 + 
                                 modern_adoption * modern_yield_advantage + 
                                 hybrid_adoption * hybrid_yield_advantage)
            tech_factor = avg_yield_advantage
            print(f"DEBUG: tech_factor: {tech_factor}, type: {type(tech_factor)}")

            # 4. Calculate Final Adjusted Yield
            print(f"DEBUG: About to calculate adjusted_yield = {base_yield} * {climate_impact_factor} * {input_factor} * {tech_factor}")
            adjusted_yield = base_yield * climate_impact_factor * input_factor * tech_factor
            # Ensure yield doesn't go below zero
            adjusted_yield = max(0, adjusted_yield)
            print(f"DEBUG: adjusted_yield: {adjusted_yield}, type: {type(adjusted_yield)}")

            # 5. Calculate Production (Yield * Area)
            # Area might also be adjusted by climate, policy, etc. (simplified here)
            current_area = base_area_ha # Needs dynamic adjustment
            print(f"DEBUG: About to calculate type_production = {adjusted_yield} * {current_area}")
            # Convert kg/ha to tonnes total (divide by 1000 to convert kg to tonnes)
            type_production = (adjusted_yield * current_area) / 1000
            print(f"DEBUG: type_production: {type_production}, type: {type(type_production)}")

            # 6. Consider Post-Harvest Loss (Optional)
            post_harvest_loss_rate = self.production_practices.get('post_harvest_loss_rate', 0.1) # Example 10%
            print(f"DEBUG: post_harvest_loss_rate: {post_harvest_loss_rate}, type: {type(post_harvest_loss_rate)}")
            final_production = type_production * (1 - post_harvest_loss_rate)
            print(f"DEBUG: final_production: {final_production}, type: {type(final_production)}")

            production[rice_type] = final_production
            total_production += final_production

        production['total_production'] = total_production # Use 'total_production' key
        print(f"Simulated rice production for {year}: Total {total_production:.2f} tonnes")
        return production
    
    def simulate_crop_diversification(self, year, climate_factors, input_availability, 
                                     technology_adoption, market_prices):
        """Simulate diversified crop production for a specific year
        
        Args:
            year (int): Simulation year
            climate_factors (dict): Climate conditions affecting production
            input_availability (dict): Availability of agricultural inputs
            technology_adoption (dict): Adoption rates of technologies (e.g., improved seeds, practices)
            market_prices (dict): Market prices affecting production decisions (e.g., price_wheat, price_veg)
            
        Returns:
            dict: Simulated production volumes for diverse crops
        """
        production = {}
        total_diversified_production = 0

        # Define crop categories based on self.diversified_crops keys
        crop_categories = list(self.diversified_crops.keys())

        for category in crop_categories:
            if category not in self.diversified_crops:
                production[category] = 0
                continue
            
            category_params = self.diversified_crops[category]

            # Assume baseline yield and area (needs actual data/config)
            base_yield = category_params.get('base_yield_kg_ha', 2000) # Example
            base_area_ha = category_params.get('base_area_ha', 1e5) # Example

            # --- Apply Adjustments --- 
            # 1. Climate Impact (Simplified - different crops have different sensitivities)
            climate_impact_factor = 1.0 
            # Robustness checks
            temp_sens = category_params.get('climate_sensitivity', {}).get('temp', -0.03)
            if not isinstance(temp_sens, (int, float)):
                print(f"Warning: Non-numeric temp_sens found for crop {category}, using 0.")
                temp_sens = 0
            rain_sens = category_params.get('climate_sensitivity', {}).get('rain', 0.08)
            if not isinstance(rain_sens, (int, float)):
                print(f"Warning: Non-numeric rain_sens found for crop {category}, using 0.")
                rain_sens = 0

            climate_impact_factor += climate_factors.get('temp_anomaly', 0) * temp_sens
            climate_impact_factor += climate_factors.get('rainfall_deviation', 0) * rain_sens
            climate_impact_factor = max(0.1, climate_impact_factor) # Boundary check

            # 2. Input Availability (Simplified)
            input_factor = 1.0
            overall_input_ratio = input_availability.get('overall_input_ratio', 1.0)
            if not isinstance(overall_input_ratio, (int, float)):
                 print(f"Warning: Non-numeric overall_input_ratio found, using 1.0.")
                 overall_input_ratio = 1.0
            # Add specific input sensitivities if needed (water, fertilizer, pesticides)
            input_factor *= overall_input_ratio # General placeholder
            input_factor = max(0.1, input_factor) # Boundary check

            # 3. Technology Adoption (Improved seeds, practices, intensification)
            tech_factor = 1.0
            # Example: technology adoption increases yield by a certain percentage
            tech_adoption_rate = technology_adoption.get(f'{category}_tech_adoption', 0.1)
            # Robustness check
            tech_yield_boost = category_params.get('technology_yield_boost', 1.15)
            if not isinstance(tech_yield_boost, (int, float)):
                print(f"Warning: Non-numeric tech_yield_boost found for crop {category}, using 1.0.")
                tech_yield_boost = 1.0 # Default to no boost

            tech_factor = 1 + (tech_adoption_rate * (tech_yield_boost - 1))
            tech_factor = max(0.1, tech_factor) # Boundary check

            # 4. Market Prices (Influence on area allocation/intensity - very simplified)
            market_factor = 1.0
            # Robustness check
            price_sensitivity = category_params.get('market_sensitivity', 0.05)
            if not isinstance(price_sensitivity, (int, float)):
                print(f"Warning: Non-numeric price_sensitivity found for crop {category}, using 0.")
                price_sensitivity = 0
            
            # Example: Higher relative price increases area/intensity slightly
            # Needs relative price calculation based on market_prices dict
            # Placeholder logic:
            price_key = f'relative_price_{category}'
            relative_price_value = market_prices.get(price_key, 0)  # Assume 0 if not found
            
            # Safety check for non-numeric values
            if isinstance(relative_price_value, dict):
                print(f"Warning: price key {price_key} retrieved a dict instead of a number. Using default 0")
                relative_price_effect = 0
            elif not isinstance(relative_price_value, (int, float)):
                print(f"Warning: Non-numeric price value for {price_key}, using 0")
                relative_price_effect = 0
            else:
                relative_price_effect = relative_price_value
                
            market_factor += relative_price_effect * price_sensitivity 
            market_factor = max(0.1, market_factor) # Boundary check

            # 5. Calculate Final Adjusted Yield
            adjusted_yield = base_yield * climate_impact_factor * input_factor * tech_factor * market_factor # Include market factor
            adjusted_yield = max(0, adjusted_yield)

            # 6. Calculate Production (Yield * Area) 
            # Area might also be adjusted dynamically based on factors (esp. market price)
            current_area = base_area_ha # Simplified 
            category_production = adjusted_yield * current_area

            # 7. Post-Harvest Loss (Optional)
            post_harvest_loss_rate = self.production_practices.get(f'{category}_post_harvest_loss', 0.15) # Example
            final_production = category_production * (1 - post_harvest_loss_rate)

            production[category] = final_production
            total_diversified_production += final_production

        production['total_production'] = total_diversified_production
        print(f"Simulated diversified crops for {year}: Total {total_diversified_production:.2f} tonnes")
        return production
    
    def simulate_aquaculture_production(self, year, climate_factors, input_availability, 
                                       technology_adoption, market_prices):
        """Simulate aquaculture and fisheries production for a specific year
        
        Args:
            year (int): Simulation year
            climate_factors (dict): Climate conditions (temp, rainfall, salinity, river_flow)
            input_availability (dict): Availability of inputs (feed_ratio, water_quality)
            technology_adoption (dict): Adoption rates (improved_species, sustainable_practices)
            market_prices (dict): Market prices affecting production decisions (price_fish, price_shrimp)
            
        Returns:
            dict: Simulated production volumes for aquaculture and fisheries
        """
        production = {}
        total_aqua_fisheries_production = 0

        aqua_fisheries_types = list(self.aquaculture_fisheries.keys())

        for aqua_type in aqua_fisheries_types:
            if aqua_type not in self.aquaculture_fisheries:
                production[aqua_type] = 0
                continue
            
            params = self.aquaculture_fisheries[aqua_type]

            # Use different units/metrics based on type (yield/area for aqua, catch for capture)
            is_capture = (aqua_type == 'capture_fisheries')
            base_production = params.get('base_production', 1000) # Example kg/ha or tonnes/year
            base_unit_measure = params.get('base_unit_measure', 1e4) # Example ha or effort_units

            # --- Apply Adjustments --- 
            # 1. Climate Impact (Varies significantly by type)
            climate_impact_factor = 1.0
            if aqua_type == 'shrimp_prawn':
                # Robustness check
                salinity_sens = params.get('climate_sensitivity', {}).get('salinity', -0.1)
                if not isinstance(salinity_sens, (int, float)):
                    print(f"Warning: Non-numeric salinity_sens found for {aqua_type}, using 0.")
                    salinity_sens = 0
                climate_impact_factor += climate_factors.get('salinity_change', 0) * salinity_sens
            elif is_capture:
                # Robustness check
                flow_sens = params.get('climate_sensitivity', {}).get('river_flow', 0.15)
                if not isinstance(flow_sens, (int, float)):
                    print(f"Warning: Non-numeric flow_sens found for {aqua_type}, using 0.")
                    flow_sens = 0
                climate_impact_factor += climate_factors.get('river_flow_deviation', 0) * flow_sens
            else: # General temp/rain sensitivity for others
                # Robustness checks
                temp_sens = params.get('climate_sensitivity', {}).get('temp', -0.04)
                if not isinstance(temp_sens, (int, float)):
                    print(f"Warning: Non-numeric temp_sens found for {aqua_type}, using 0.")
                    temp_sens = 0
                rain_sens = params.get('climate_sensitivity', {}).get('rain', 0.06)
                if not isinstance(rain_sens, (int, float)):
                    print(f"Warning: Non-numeric rain_sens found for {aqua_type}, using 0.")
                    rain_sens = 0
                climate_impact_factor += climate_factors.get('temp_anomaly', 0) * temp_sens
                climate_impact_factor += climate_factors.get('rainfall_deviation', 0) * rain_sens

            climate_impact_factor = max(0.1, climate_impact_factor) # Boundary check

            # 2. Input Availability (More relevant for aquaculture)
            input_factor = 1.0
            if not is_capture:
                # Robustness checks
                feed_sens = params.get('input_sensitivity', {}).get('feed', 0.4)
                if not isinstance(feed_sens, (int, float)):
                    print(f"Warning: Non-numeric feed_sens found for {aqua_type}, using 0.")
                    feed_sens = 0
                wq_sens = params.get('input_sensitivity', {}).get('water_quality', 0.3)
                if not isinstance(wq_sens, (int, float)):
                    print(f"Warning: Non-numeric wq_sens found for {aqua_type}, using 0.")
                    wq_sens = 0
                feed_effect = input_availability.get('feed_ratio', 1.0) * feed_sens
                wq_effect = input_availability.get('water_quality_index', 1.0) * wq_sens
                # Calculate base component carefully
                base_component = max(0, 1.0 - feed_sens - wq_sens)
                input_factor = base_component + feed_effect + wq_effect
            
            input_factor = max(0.1, input_factor) # Boundary check

            # 3. Technology Adoption / Management Practices
            tech_factor = 1.0
            adoption_rate = technology_adoption.get(f'{aqua_type}_adoption', 0.1) # Example
            if is_capture:
                # e.g., adoption of sustainable fishing gear, conservation effectiveness
                # Robustness check
                sustainability_boost = params.get('sustainability_boost', 1.05)
                if not isinstance(sustainability_boost, (int, float)):
                    print(f"Warning: Non-numeric sustainability_boost found for {aqua_type}, using 1.0.")
                    sustainability_boost = 1.0
                tech_factor = 1 + (adoption_rate * (sustainability_boost - 1))
                 # Could also impose catch limits based on sustainability metrics
                max_sustainable_catch = params.get('max_sustainable_catch', base_production * 1.1) # Example
            else:
                # e.g., adoption of improved species, better feed, disease mgmt
                # Robustness check
                tech_yield_boost = params.get('technology_yield_boost', 1.20)
                if not isinstance(tech_yield_boost, (int, float)):
                    print(f"Warning: Non-numeric tech_yield_boost found for {aqua_type}, using 1.0.")
                    tech_yield_boost = 1.0
                tech_factor = 1 + (adoption_rate * (tech_yield_boost - 1))

            tech_factor = max(0.1, tech_factor) # Boundary check

            # 4. Market Prices (Influence on effort/intensity)
            market_factor = 1.0
            # Robustness check
            price_sensitivity = params.get('market_sensitivity', 0.08)
            if not isinstance(price_sensitivity, (int, float)):
                print(f"Warning: Non-numeric price_sensitivity found for {aqua_type}, using 0.")
                price_sensitivity = 0
            # Use appropriate price key (e.g., price_fish, price_shrimp)
            price_key = f'relative_price_{aqua_type}'
            
            # Safely extract a numeric value from market_prices
            relative_price_value = market_prices.get(price_key, 1.0)
            if isinstance(relative_price_value, dict):
                print(f"Warning: price key {price_key} retrieved a dict instead of a number. Using default 1.0")
                relative_price_change = 1.0
            elif not isinstance(relative_price_value, (int, float)):
                print(f"Warning: Non-numeric price value for {price_key}, using 1.0")
                relative_price_change = 1.0
            else:
                relative_price_change = relative_price_value
                
            market_factor = 1 + ( (relative_price_change - 1) * price_sensitivity )
            market_factor = max(0.1, market_factor) # Boundary check

            # 5. Calculate Final Adjusted Production Rate/Yield
            adjusted_production_rate = base_production * climate_impact_factor * input_factor * tech_factor * market_factor
            adjusted_production_rate = max(0, adjusted_production_rate)

            # 6. Calculate Total Production (Rate * Area/Effort)
            # Area/Effort could also be dynamic
            current_measure = base_unit_measure * market_factor # Simplistic adjustment
            aqua_type_production_val = adjusted_production_rate * current_measure

            # Apply sustainability cap for capture fisheries
            if is_capture:
                aqua_type_production_val = min(aqua_type_production_val, max_sustainable_catch * current_measure)

            # 7. Post-Harvest Loss (if applicable)
            phl_rate = params.get('post_harvest_loss_rate', 0.12) # Example 12%
            final_production = aqua_type_production_val * (1 - phl_rate)

            production[aqua_type] = final_production
            total_aqua_fisheries_production += final_production
            
        production['total_aqua_fisheries'] = total_aqua_fisheries_production
        return production
    
    def simulate_livestock_production(self, year, climate_factors, input_availability, 
                                     technology_adoption, market_prices):
        """Simulate livestock and poultry production for a specific year
        
        Args:
            year (int): Simulation year
            climate_factors (dict): Climate conditions (heat_stress_index, disease_risk_mod)
            input_availability (dict): Availability of inputs (feed_quality_ratio, water_stress)
            technology_adoption (dict): Adoption rates (breed_improvement, vaccination_coverage)
            market_prices (dict): Market prices (price_milk, price_meat, price_eggs)
            
        Returns:
            dict: Simulated production volumes for livestock products (milk, meat, eggs)
        """
        production = {}
        total_livestock_value = 0 # Placeholder for a potential aggregate value

        livestock_types = list(self.livestock_poultry.keys()) # ['dairy', 'poultry', 'small_ruminants', 'feed_systems', 'animal_health']
        production_types = ['dairy', 'poultry', 'small_ruminants']

        # --- Pre-calculate overall factors ---
        # Feed availability impact (from feed_systems)
        feed_params = self.livestock_poultry.get('feed_systems', {})
        base_feed_availability = feed_params.get('base_availability', 1.0)
        feed_trend_factor = 1.0 + feed_params.get('availability_trend', 0.01) * (year - 2025) # Example trend
        feed_quality_factor = input_availability.get('feed_quality_ratio', 1.0)
        current_feed_factor = base_feed_availability * feed_trend_factor * feed_quality_factor

        # Animal health impact (from animal_health)
        health_params = self.livestock_poultry.get('animal_health', {})
        base_disease_impact = health_params.get('base_disease_impact', 0.95) # e.g., 5% loss baseline
        vaccination_coverage = technology_adoption.get('vaccination_coverage', 0.5) # Example coverage
        service_coverage = technology_adoption.get('vet_service_coverage', 0.4) # Example
        disease_risk_modifier = climate_factors.get('disease_risk_mod', 1.0) # Climate effect on disease
        # Higher coverage reduces impact (closer to 1.0)
        health_factor = base_disease_impact + (1 - base_disease_impact) * (vaccination_coverage * 0.6 + service_coverage * 0.4)
        health_factor /= disease_risk_modifier # Increased risk reduces health factor
        health_factor = min(1.0, health_factor) # Cap at 1.0

        # --- Simulate each production type --- 
        for livestock_type in production_types:
            if livestock_type not in self.livestock_poultry:
                production[livestock_type] = {} # Initialize dict for this type
                continue
            
            params = self.livestock_poultry[livestock_type]
            production[livestock_type] = {} # Initialize dict for this type

            # Assume baseline productivity and herd/flock size (needs data/config)
            base_productivity = params.get('base_yield_per_animal', 100) # kg milk/cow, eggs/bird, kg meat/animal
            base_population = params.get('base_population', 1e6) # Number of animals

            # --- Apply Adjustments --- 
            # 1. Climate Impact (e.g., heat stress)
            climate_impact_factor = 1.0
            heat_stress_index = climate_factors.get('heat_stress_index', 0)
            heat_sensitivity = params.get('climate_sensitivity', {}).get('heat_stress', -0.05) # Example
            if not isinstance(heat_sensitivity, (int, float)):
                print(f"Warning: Non-numeric heat_sensitivity found for {livestock_type}, using 0.")
                heat_sensitivity = 0
            climate_impact_factor += heat_stress_index * heat_sensitivity
            
            # 2. Input Availability (Feed factor calculated above, add water stress etc.)
            input_factor = current_feed_factor # Start with feed
            water_stress_effect = climate_factors.get('water_stress', 0) * params.get('input_sensitivity', {}).get('water', -0.1)
            if not isinstance(water_stress_effect, (int, float)):
                print(f"Warning: Non-numeric water_stress_effect found for {livestock_type}, using 0.")
                water_stress_effect = 0
            input_factor *= (1 + water_stress_effect)

            input_factor = max(0.1, input_factor) # Boundary check

            # 3. Technology Adoption (Breed improvement, specific practices)
            tech_factor = 1.0
            breed_adoption = technology_adoption.get(f'{livestock_type}_breed_adoption', 0.2) # Example
            breed_yield_boost = params.get('breed_yield_boost', 1.25) # Example 25% boost
            if not isinstance(breed_yield_boost, (int, float)):
                print(f"Warning: Non-numeric breed_yield_boost found for {livestock_type}, using 1.0.")
                breed_yield_boost = 1.0
            tech_factor = 1 + (breed_adoption * (breed_yield_boost - 1))

            tech_factor = max(0.1, tech_factor) # Boundary check

            # 4. Animal Health (Factor calculated above)
            # Health factor is already calculated

            # 5. Market Prices (Influence on population size/intensity - simplified)
            market_factor = 1.0
            price_sensitivity = params.get('market_sensitivity', 0.06) # Example
            if not isinstance(price_sensitivity, (int, float)):
                print(f"Warning: Non-numeric price_sensitivity found for {livestock_type}, using 0.")
                price_sensitivity = 0
            # Use appropriate price key (e.g., price_milk, price_meat)
            price_key = f'relative_price_{params.get("market_product", livestock_type)}'
            
            # Safely extract a numeric value from market_prices
            relative_price_value = market_prices.get(price_key, 1.0)
            if isinstance(relative_price_value, dict):
                print(f"Warning: price key {price_key} retrieved a dict instead of a number. Using default 1.0")
                relative_price_change = 1.0
            elif not isinstance(relative_price_value, (int, float)):
                print(f"Warning: Non-numeric price value for {price_key}, using 1.0")
                relative_price_change = 1.0
            else:
                relative_price_change = relative_price_value
                
            market_factor = 1 + ( (relative_price_change - 1) * price_sensitivity )
            market_factor = max(0.1, market_factor) # Boundary check

            # 6. Calculate Final Adjusted Productivity per Animal
            adjusted_productivity = base_productivity * climate_impact_factor * input_factor * tech_factor * health_factor
            adjusted_productivity = max(0, adjusted_productivity)

            # 7. Calculate Total Production (Productivity * Population)
            # Area/Effort could also be dynamic
            current_population = base_population * market_factor # Simplistic adjustment
            type_total_production = adjusted_productivity * current_population

            # 8. Post-production considerations (e.g., losses, specific products)
            # Store raw production; further breakdown might happen in integration step
            # Assign specific product names based on type
            if livestock_type == 'dairy':
                production[livestock_type]['milk'] = type_total_production
                # Could also estimate meat from dairy herd cull rate etc.
                production[livestock_type]['meat_from_dairy'] = current_population * params.get('cull_rate_meat_yield', 5) # Example
            elif livestock_type == 'poultry':
                # Assume combined metric or split based on flock composition param
                egg_ratio = params.get('egg_production_ratio', 0.6) # Example 60% for eggs
                if not isinstance(egg_ratio, (int, float)):
                    print(f"Warning: Non-numeric egg_ratio found for {livestock_type}, using 0.")
                    egg_ratio = 0
                production[livestock_type]['eggs'] = type_total_production * egg_ratio
                production[livestock_type]['poultry_meat'] = type_total_production * (1 - egg_ratio)
            elif livestock_type == 'small_ruminants':
                # Assume primarily meat production
                production[livestock_type]['meat_small_ruminant'] = type_total_production
                # Could add milk component if relevant params exist

            # Accumulate a value metric (optional)
            # total_livestock_value += type_total_production * market_prices.get(price_key, 1.0) / relative_price_change # Approx value

        # Combine results into a flatter structure if needed for integration
        flat_production = {}
        for l_type, products in production.items():
            if isinstance(products, dict):
                flat_production.update(products)
        
        # production['total_value'] = total_livestock_value # Add if calculated
        return flat_production # Return the flattened dictionary
    
    def calculate_total_food_production(self, year, climate_factors, input_availability, 
                                       technology_adoption, market_prices):
        """Calculate total food production across all agricultural systems
        
        Args:
            year (int): Simulation year
            climate_factors (dict): Climate conditions affecting production
            input_availability (dict): Availability of agricultural inputs
            technology_adoption (dict): Adoption rates of technologies
            market_prices (dict): Market prices affecting production decisions
            
        Returns:
            dict: Consolidated food production volumes and caloric equivalent
        """
        # Calculate production for each subsystem
        rice_production = self.simulate_rice_production(
            year, climate_factors, input_availability, technology_adoption
        )
        
        crop_production = self.simulate_crop_diversification(
            year, climate_factors, input_availability, technology_adoption, market_prices
        )
        
        aqua_production = self.simulate_aquaculture_production(
            year, climate_factors, input_availability, technology_adoption, market_prices
        )
        
        livestock_production = self.simulate_livestock_production(
            year, climate_factors, input_availability, technology_adoption, market_prices
        )
        
        # Consolidate production data
        total_production = {
            'cereals': {
                'rice': rice_production,
                'other_cereals': {
                    'wheat': crop_production['wheat_maize'],
                    'maize': crop_production['wheat_maize']
                }
            },
            'non_cereal_crops': {
                'pulses': crop_production['pulses_oilseeds'],
                'oilseeds': crop_production['pulses_oilseeds'],
                'vegetables': crop_production['vegetables'],
                'fruits': crop_production['fruits'],
                'roots_tubers': {
                    'potato': crop_production['potato_tubers'],
                    'other_tubers': crop_production['potato_tubers']
                }
            },
            'animal_source_foods': {
                'fish_seafood': {
                    'aquaculture': aqua_production['total_aqua_fisheries'] - aqua_production.get('capture_fisheries', 0), # Crude split
                    'capture': aqua_production.get('capture_fisheries', 0)
                },
                'meat': {
                    'beef_mutton': livestock_production.get('meat_from_dairy', 0) + livestock_production.get('meat_small_ruminant', 0),
                    'poultry': livestock_production.get('poultry_meat', 0)
                },
                'other_livestock': {
                    'milk': livestock_production.get('milk', 0),
                    'eggs': livestock_production.get('eggs', 0)
                }
            }
        }
        
        # Calculate caloric and nutritional equivalents
        total_production['caloric_equivalent'] = self._calculate_caloric_equivalent(total_production)
        total_production['protein_equivalent'] = self._calculate_protein_equivalent(total_production)
        
        return total_production
    
    def _calculate_caloric_equivalent(self, production_data):
        """Calculate caloric equivalent of production
        
        Args:
            production_data (dict): Production volumes by food type
            
        Returns:
            float: Total caloric equivalent in kcal
        """
        # Caloric conversion factors (kcal per kg)
        caloric_factors = {
            'rice': 3600,
            'wheat': 3400,
            'maize': 3650,
            'pulses': 3400,
            'oilseeds': 8850,
            'vegetables': 250,
            'fruits': 550,
            'potato': 770,
            'other_tubers': 1180,
            'fish': 1050,
            'milk': 670,
            'meat': 2500,
            'eggs': 1550
        }
        
        total_calories = 0
        
        # Process each food category recursively
        def process_category(data, category=None):
            nonlocal total_calories
            
            if isinstance(data, dict):
                for key, value in data.items():
                    # Skip metadata keys
                    if key in ['caloric_equivalent', 'protein_equivalent', 'total_production']:
                        continue
                    
                    # Process nested dictionaries
                    if isinstance(value, dict):
                        process_category(value, key)
                    # Process numeric values directly
                    elif isinstance(value, (int, float)):
                        # If key exists in caloric_factors, use it directly
                        if key in caloric_factors:
                            total_calories += value * caloric_factors[key]
                        # If category exists in caloric_factors, use category
                        elif category in caloric_factors:
                            total_calories += value * caloric_factors[category]
                        # Special case for rice_production which has a 'total_production' key
                        elif key == 'total_production' and category == 'rice':
                            total_calories += value * caloric_factors['rice']
                        # Special handling for specific categories
                        elif category == 'fish_seafood' or key == 'fish_seafood':
                            total_calories += value * caloric_factors['fish']
                            
        # Start recursive processing
        process_category(production_data)
        
        return round(total_calories, 2)  # Round to 2 decimal places for readability
    
    def _calculate_protein_equivalent(self, production_data):
        """Calculate protein equivalent of production
        
        Args:
            production_data (dict): Production volumes by food type
            
        Returns:
            float: Total protein equivalent in kg
        """
        # Protein conversion factors (g per kg)
        protein_factors = {
            'rice': 75,
            'wheat': 120,
            'maize': 95,
            'pulses': 220,
            'oilseeds': 180,
            'vegetables': 13,
            'fruits': 8,
            'potato': 20,
            'other_tubers': 16,
            'fish': 180,
            'milk': 33,
            'meat': 250,
            'eggs': 130
        }
        
        total_protein = 0
        
        # Process each food category recursively
        def process_category(data, category=None):
            nonlocal total_protein
            
            if isinstance(data, dict):
                for key, value in data.items():
                    # Skip metadata keys
                    if key in ['caloric_equivalent', 'protein_equivalent', 'total_production']:
                        continue
                    
                    # Process nested dictionaries
                    if isinstance(value, dict):
                        process_category(value, key)
                    # Process numeric values directly
                    elif isinstance(value, (int, float)):
                        # If key exists in protein_factors, use it directly
                        if key in protein_factors:
                            total_protein += value * protein_factors[key]
                        # If category exists in protein_factors, use category
                        elif category in protein_factors:
                            total_protein += value * protein_factors[category]
                        # Special case for rice_production which has a 'total_production' key
                        elif key == 'total_production' and category == 'rice':
                            total_protein += value * protein_factors['rice']
                        # Special handling for specific categories
                        elif category == 'fish_seafood' or key == 'fish_seafood':
                            total_protein += value * protein_factors['fish']
                            
        # Start recursive processing
        process_category(production_data)
        
        # Convert grams to kg for final result
        return round(total_protein / 1000, 2)  # Convert from g to kg and round to 2 decimal places

    def simulate_production(self, year, climate_resilience_output, input_availability, technology_adoption, market_prices):
        """Orchestrates the simulation of all agricultural sub-sectors.

        Args:
            year (int): Simulation year.
            climate_resilience_output (dict): Output from the climate resilience model.
            input_availability (dict): Availability of inputs like fertilizer, water.
            technology_adoption (dict): Adoption rates of specific technologies.
            market_prices (dict): Market prices from the previous cycle, influencing planting decisions.

        Returns:
            dict: Aggregated production results across all sub-sectors.
        """
        print(f"\n--- Simulating Agricultural Production for Year {year} ---")

        # Ensure market_prices is a dict and not None
        if market_prices is None:
            market_prices = {}
        
        # If market_prices is a dict of dicts, flatten it for our models that expect a simple structure
        flattened_market_prices = {}
        if isinstance(market_prices, dict):
            # Check if the dict contains nested dicts (like prices.producer.rice)
            has_nested_values = any(isinstance(v, dict) for v in market_prices.values())
            
            if has_nested_values:
                # Flatten the nested structure
                for key, value in market_prices.items():
                    if isinstance(value, dict):
                        for inner_key, inner_value in value.items():
                            # Create keys like 'producer_rice', 'retail_wheat', etc.
                            flattened_key = f"{key}_{inner_key}"
                            flattened_market_prices[flattened_key] = inner_value
                    else:
                        flattened_market_prices[key] = value
                
                # Add in relative price keys that our models expect
                for crop in ['rice', 'wheat', 'maize', 'vegetables', 'fruits', 'fish', 'milk', 'meat', 'eggs']:
                    if f"producer_{crop}" in flattened_market_prices:
                        # Create relative price keys with default value 1.0
                        flattened_market_prices[f"relative_price_{crop}"] = 1.0
            else:
                # If it's already a flat structure, use it directly
                flattened_market_prices = market_prices
        else:
            # If market_prices is not a dict (unlikely), provide a default empty dict
            flattened_market_prices = {}

        # Extract relevant climate factors from the climate output dictionary
        # Adjust these keys based on the actual structure of climate_resilience_output
        climate_factors_for_rice = climate_resilience_output.get('agricultural_impacts', {})
        climate_factors_for_crops = climate_resilience_output.get('agricultural_impacts', {})
        climate_factors_for_aqua = climate_resilience_output.get('fisheries_impacts', {})
        climate_factors_for_livestock = climate_resilience_output.get('livestock_impacts', {})

        # 1. Simulate Rice Production
        rice_production = self.simulate_rice_production(
            year,
            climate_factors=climate_factors_for_rice,
            input_availability=input_availability,
            technology_adoption=technology_adoption
        )

        # 2. Simulate Diversified Crops
        diversified_crops_production = self.simulate_crop_diversification(
            year,
            climate_factors=climate_factors_for_crops,
            input_availability=input_availability,
            technology_adoption=technology_adoption,
            market_prices=flattened_market_prices # Market prices influence crop choices
        )

        # 3. Simulate Aquaculture and Fisheries
        aquaculture_fisheries_production = self.simulate_aquaculture_production(
            year,
            climate_factors=climate_factors_for_aqua,
            input_availability=input_availability, # e.g., feed availability
            technology_adoption=technology_adoption, # e.g., improved species adoption
            market_prices=flattened_market_prices
        )

        # 4. Simulate Livestock and Poultry
        livestock_poultry_production = self.simulate_livestock_production(
            year,
            climate_factors=climate_factors_for_livestock,
            input_availability=input_availability, # e.g., feed, health services
            technology_adoption=technology_adoption, # e.g., improved breeds
            market_prices=flattened_market_prices
        )

        # Aggregate results
        aggregated_production = {
            'year': year,
            'rice': rice_production,
            'diversified_crops': diversified_crops_production,
            'aquaculture_fisheries': aquaculture_fisheries_production,
            'livestock_poultry': livestock_poultry_production,
            # Potential: Calculate total food production in common units (e.g., calories, tonnes)
            'total_food_estimate': (
                rice_production.get('total_production', 0) +
                diversified_crops_production.get('total_production', 0) +
                aquaculture_fisheries_production.get('total_production', 0) +
                livestock_poultry_production.get('total_production', 0)
            ) # Simple sum, requires consistent 'total_production' keys in sub-outputs
        }

        print(f"--- Finished Agricultural Production Simulation for Year {year} ---")
        return aggregated_production

# Example Usage (for testing)
if __name__ == "__main__":
    # Initialize model with example configuration
    config = {
        'crop_systems': {},
        'livestock_systems': {},
        'fisheries_systems': {},
        'production_practices': {},
        'input_dependencies': {},
        'seasonal_patterns': {},
        'land_characteristics': {},
        'productivity_factors': {}
    }
    model = AgriculturalProductionModel(config)

    # Example inputs for simulation
    year = 2025
    climate_resilience_output = {
        'agricultural_impacts': {
            'temp_anomaly': 0.5,
            'rainfall_deviation': 0.2
        },
        'fisheries_impacts': {
            'salinity_change': 0.1,
            'river_flow_deviation': 0.3
        },
        'livestock_impacts': {
            'heat_stress_index': 0.4,
            'disease_risk_mod': 1.1
        }
    }
    input_availability = {
        'water_ratio': 0.9,
        'fertilizer_ratio': 0.8,
        'feed_ratio': 0.95,
        'water_quality_index': 0.9
    }
    technology_adoption = {
        'modern_adoption': 0.2,
        'hybrid_adoption': 0.1,
        'improved_species_adoption': 0.15,
        'breed_improvement_adoption': 0.1
    }
    market_prices = {
        'relative_price_rice': 1.1,
        'relative_price_wheat_maize': 1.05,
        'relative_price_fish': 1.2,
        'relative_price_milk': 1.1,
        'relative_price_meat': 1.15
    }

    # Run simulation
    results = model.simulate_production(year, climate_resilience_output, input_availability, technology_adoption, market_prices)
    print(results)
