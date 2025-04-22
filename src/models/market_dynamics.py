import numpy as np
import pandas as pd

class MarketDynamicsModel:
    """
    Models market dynamics for key food commodities.

    Includes supply and demand simulation, price formation, and trade flows.
    """
    def __init__(self, config):
        """
        Initializes the market dynamics model with configuration parameters.

        Args:
            config (dict): Configuration dictionary. Expected keys:
                'supply_params', 'demand_params', 'price_params', 'trade_params'.
        """
        self.supply_params = config.get('supply_params', {}) # e.g., supply elasticities
        self.demand_params = config.get('demand_params', {}) # e.g., demand elasticities, preferences
        self.price_params = config.get('price_params', {}) # e.g., price transmission factors
        self.trade_params = config.get('trade_params', {}) # e.g., import/export costs, world prices
        self.historical_market_data = {}
        # Assume parameters define market characteristics for key commodities
        self.commodities = ['rice', 'wheat', 'pulses', 'vegetables', 'fish', 'meat', 'milk', 'eggs']
        print("MarketDynamicsModel initialized.")

    def load_historical_data(self, data_handler):
        """
        Loads historical market data (prices, quantities).

        Args:
            data_handler: An object capable of providing historical data.
                          Expected method: get_market_data().
        """
        print("Loading historical market data...")
        # self.historical_market_data = data_handler.get_market_data()
        # Placeholder data structure
        self.historical_market_data = {
            'prices': pd.DataFrame({
                'year': [2020, 2021, 2022],
                'rice_retail': [45, 48, 50],
                'wheat_retail': [35, 38, 40]
            }),
            'trade': pd.DataFrame({
                 'year': [2020, 2021, 2022],
                 'rice_imports': [0.5e6, 0.8e6, 0.6e6] # Example tonnes
            })
        }
        print("Historical market data loaded (placeholder).")

    def _simulate_supply(self, year, production_data, policy_effects):
        """Placeholder for simulating market supply based on production and policies."""
        print(f"Simulating market supply for {year}...")
        market_supply = {}
        # Start with production volumes (needs detailed breakdown)
        # Example: Aggregate rice production used as market supply
        total_rice = production_data.get('total_food',{}).get('cereals',{}).get('rice', 0)
        # Adjust based on policy effects (e.g., export restrictions)
        export_mod = policy_effects.get('trade_policy_effects', {}).get('export_volume_modifier', 1.0)

        # Simplistic supply: map production directly for key commodities
        # A real model would need more nuance (farm retention, marketed surplus)
        market_supply['rice'] = total_rice * export_mod # Example adjustment
        # Add other commodities based on production_data structure
        market_supply['wheat'] = production_data.get('total_food',{}).get('cereals',{}).get('wheat', 0) * export_mod
        market_supply['pulses'] = production_data.get('total_food',{}).get('pulses', 0) * export_mod
        # ... map other relevant production outputs ...
        market_supply['fish'] = production_data.get('total_food',{}).get('fish',{}).get('total', 0) * export_mod
        market_supply['meat'] = production_data.get('total_food',{}).get('meat',{}).get('beef_mutton', 0) + \
                                production_data.get('total_food',{}).get('meat',{}).get('poultry', 0) * export_mod
        market_supply['milk'] = production_data.get('total_food',{}).get('other_livestock',{}).get('milk', 0) * export_mod
        market_supply['eggs'] = production_data.get('total_food',{}).get('other_livestock',{}).get('eggs', 0) * export_mod

        # Consider storage changes if modeled

        return market_supply # Quantities available on the market

    def _simulate_demand(self, year, socioeconomic_state, policy_effects):
        """Placeholder for simulating market demand based on socioeconomics and policies."""
        print(f"Simulating market demand for {year}...")
        market_demand = {}
        # Base demand on population and income (needs elasticities from params)
        population = socioeconomic_state.get('population', {}).get('total_population', 170e6)
        gdp_pc = socioeconomic_state.get('economy', {}).get('gdp_per_capita', 2200)

        # Very simple placeholder demand (e.g., per capita constants scaled by population)
        # A real model uses demand systems (e.g., QUAIDS, AIDS) with price/income elasticities
        base_demand_per_cap = { # Example kg/person/year
            'rice': 150, 'wheat': 25, 'pulses': 8, 'vegetables': 65,
            'fish': 25, 'meat': 12, 'milk': 35, 'eggs': 6
        }

        for commodity, base_pc_demand in base_demand_per_cap.items():
            # Adjust based on income growth (using simple income elasticity placeholder)
            income_elasticity = self.demand_params.get(f'{commodity}_income_elasticity', 0.5) # Example
            # Need baseline GDP for comparison
            gdp_baseline = 2000 # Example baseline GDP
            income_effect = 1 + income_elasticity * ((gdp_pc - gdp_baseline) / gdp_baseline)
            
            # Apply policy effects (e.g., safety nets boosting food demand)
            # This is complex - safety nets might directly provide food or increase income
            # Simplified: Assume social policy modifier affects overall demand slightly
            demand_mod = policy_effects.get('social_protection_effects',{}).get('transfer_value_modifier', 1.0) * 0.1 + 0.9 # Example weak link

            market_demand[commodity] = base_pc_demand * income_effect * population * demand_mod

        return market_demand # Total desired quantities

    def _simulate_price_formation(self, year, market_supply, market_demand, policy_effects, trade_params):
        """Placeholder for simulating price formation considering supply, demand, trade, policies."""
        print(f"Simulating price formation for {year}...")
        prices = {}
        # Simple market clearing placeholder: price adjusts based on supply/demand gap
        # Needs price elasticities of supply and demand.

        # Assume base prices (needs historical data or calibration)
        base_prices = { # Example retail price/kg
            'rice': 50, 'wheat': 40, 'pulses': 100, 'vegetables': 40,
            'fish': 250, 'meat': 600, 'milk': 80, 'eggs': 120 # per dozen? -> needs consistent units
        }

        for commodity in self.commodities:
            supply = market_supply.get(commodity, 1e-6) # Avoid division by zero
            demand = market_demand.get(commodity, 1e-6)
            base_price = base_prices.get(commodity, 50) # Default base price

            # Calculate supply-demand gap ratio
            gap_ratio = (demand - supply) / ((supply + demand) / 2) if (supply + demand) > 0 else 0

            # Adjust price based on gap and placeholder elasticity factor
            # Higher gap means higher price. Elasticity determines sensitivity.
            price_elasticity_factor = self.price_params.get(f'{commodity}_elasticity_factor', -0.5) # Combined elasticity effect
            price_change_factor = 1 + gap_ratio / price_elasticity_factor if price_elasticity_factor != 0 else 1.0

            # Factor in trade policy effects (e.g., tariffs)
            trade_price_mod = policy_effects.get('trade_policy_effects', {}).get('import_price_modifier', 1.0)
            # Factor in world prices (if import/export occurs) - complex logic needed here
            # Example: if domestic price > world price + tariff, imports might occur, capping price.

            prices[commodity] = base_price * price_change_factor * trade_price_mod
            prices[commodity] = max(prices[commodity], 1.0) # Ensure positive price

        # Add different price levels (producer, wholesale, retail) using transmission factors
        prices_detailed = {'retail': prices.copy()}
        prices_detailed['wholesale'] = {c: p * self.price_params.get('wholesale_retail_margin', 0.85) for c,p in prices.items()}
        prices_detailed['producer'] = {c: p * self.price_params.get('producer_wholesale_margin', 0.7) for c,p in prices_detailed['wholesale'].items()}

        return prices_detailed # Dictionary with price levels

    def _simulate_trade_flows(self, year, domestic_prices, world_prices, trade_policies):
        """Placeholder for simulating import/export flows based on price gaps and policies."""
        print(f"Simulating trade flows for {year}...")
        trade_flows = {'imports': {}, 'exports': {}}
        # Logic: Compare domestic price to world price + transfer costs (tariffs, transport)
        # If world price + costs < domestic price -> potential import
        # If domestic price < world price - costs -> potential export

        for commodity in self.commodities:
            domestic_price = domestic_prices.get('producer', {}).get(commodity, 0) # Use producer price for trade decisions
            world_price = world_prices.get(commodity, domestic_price * 1.2) # Example world price (needs data)
            import_cost = trade_policies.get('import_tariff_rate', 0) * world_price + trade_policies.get('import_transport_cost', 5) # Example costs
            export_cost = trade_policies.get('export_subsidy_rate', 0) * domestic_price + trade_policies.get('export_transport_cost', 6) # Example costs

            if world_price + import_cost < domestic_price:
                # Potential import - quantity depends on demand elasticity, quotas etc.
                import_propensity = (domestic_price - (world_price + import_cost)) / domestic_price
                trade_flows['imports'][commodity] = import_propensity * market_demand.get(commodity,0) * 0.1 # Simplistic quantity
            elif domestic_price < world_price - export_cost:
                 # Potential export - quantity depends on supply elasticity, restrictions etc.
                 export_propensity = ((world_price - export_cost) - domestic_price) / domestic_price
                 export_restriction = trade_policies.get('export_restriction_level', 0) # From 0 to 1
                 trade_flows['exports'][commodity] = export_propensity * market_supply.get(commodity,0) * 0.1 * (1-export_restriction) # Simplistic

        return trade_flows


    def simulate_market_dynamics(self, year, production_data, socioeconomic_state, policy_effects):
        """
        Simulates market dynamics for a given year.

        Args:
            year (int): The simulation year.
            production_data (dict): Output from the agricultural production model.
            socioeconomic_state (dict): Output from the socioeconomic model.
            policy_effects (dict): Output from the policy interventions model.

        Returns:
            dict: A dictionary containing simulated market outcomes (supply, demand, prices, trade).
        """
        print(f"\n--- Simulating Market Dynamics for Year {year} ---")

        # 1. Simulate Market Supply
        market_supply = self._simulate_supply(year, production_data, policy_effects)

        # 2. Simulate Market Demand
        market_demand = self._simulate_demand(year, socioeconomic_state, policy_effects)

        # 3. Simulate Price Formation (Iterative process might be needed in a real model)
        market_prices = self._simulate_price_formation(year, market_supply, market_demand, policy_effects, self.trade_params)

        # 4. Simulate Trade Flows (Might influence prices and supply/demand balance in iterative model)
        world_prices = self.trade_params.get('world_prices', {}) # Need world price inputs
        trade_policies = policy_effects.get('trade_policy_effects', {}) # Extract relevant policy levers
        trade_flows = self._simulate_trade_flows(year, market_prices, world_prices, trade_policies)

        # Combine results
        market_state = {
            'year': year,
            'market_supply': market_supply,
            'market_demand': market_demand,
            'prices': market_prices, # Contains producer, wholesale, retail
            'trade_flows': trade_flows
        }

        print(f"--- Finished Market Dynamics Simulation for Year {year} ---")
        return market_state

# Example usage (optional, for testing)
if __name__ == '__main__':
    # Dummy configuration
    config = {
        'demand_params': {'rice_income_elasticity': 0.2, 'meat_income_elasticity': 0.8},
        'price_params': {'wholesale_retail_margin': 0.8, 'producer_wholesale_margin': 0.65},
        'trade_params': {'world_prices': {'rice': 400, 'wheat': 300}} # $/tonne example
    }
    model = MarketDynamicsModel(config)
    model.load_historical_data(None)

    # Dummy inputs for year 2025
    # Production data needs to align with the expected structure
    prod_data = {
        'total_food': {
            'cereals': {'rice': 35e6, 'wheat': 1e6}, # Tonnes
            'pulses': 0.8e6,
            'fish': {'total': 4e6},
            'meat': {'beef_mutton': 1.5e6, 'poultry': 2e6},
            'other_livestock': {'milk': 10e6, 'eggs': 15e9} # Milk tonnes, eggs number? needs units
        }
    }
    socio_state = {
        'population': {'total_population': 171e6},
        'economy': {'gdp_per_capita': 2300}
    }
    # Assume baseline policy effects (modifiers are 1.0 or 0)
    policy_eff = {
         'trade_policy_effects': {'export_volume_modifier': 1.0, 'import_price_modifier': 1.0},
         'social_protection_effects': {'transfer_value_modifier': 1.0}
    }

    # Simulate year 2025
    simulated_market_2025 = model.simulate_market_dynamics(2025, prod_data, socio_state, policy_eff)
    print("\nSimulated Market Dynamics for 2025:")
    import json
    # Convert numpy types if they appear
    print(json.dumps(simulated_market_2025, indent=2, default=lambda x: str(x) if isinstance(x, (np.int64, np.float64)) else x))

