# Bangladesh Food Security Simulation Framework (2025-2035)

A comprehensive simulation framework for modeling and projecting food security dynamics in Bangladesh from 2025-2035. This system models the complex interplay between agricultural production, climate impacts, supply chains, nutrition, governance, and socioeconomic factors with advanced visualization and reporting capabilities.

## Overview

This framework simulates Bangladesh's food security ecosystem, capturing interactions between:

- Agricultural production systems
- Climate resilience and adaptation
- Food supply chains and market dynamics
- Food access and affordability
- Nutrition security and diet quality
- Food safety and quality
- Agricultural technology and innovation
- Land use and resource management
- Food trade and self-sufficiency
- Governance and policy frameworks
- Food-energy-water nexus
- System resilience and transformation

## Project Structure

```text
├── config/               # Configuration files and simulation parameters
├── src/                  # Source code
│   ├── models/           # Core simulation model components
│   ├── data/             # Data handling and processing modules
│   ├── utils/            # Utility functions and helpers
│   ├── visualization/    # Data visualization components
│   └── reporting/        # HTML report generation using Jinja2 templates
├── results/              # Simulation results and reports
│   ├── plots/            # Generated visualizations
│   └── [scenario_name]/  # Scenario-specific outputs
├── tests/                # Unit and integration tests
└── data/                 # Data directory (not included in repository)
    ├── raw/              # Raw data files
    └── processed/        # Processed data ready for simulation
```

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/deluair/BD_food_security_simulation.git

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running a Simulation

```bash
# Run the main simulation script
python run_simulation.py
```

This will:
1. Run multiple scenarios (baseline, high climate impact, enhanced adaptation, policy change safety net)
2. Generate visualizations for each scenario
3. Create detailed HTML reports with interactive elements
4. Generate a comprehensive comparison report of all scenarios

## Features

### Modeling Components

- Climate resilience and adaptation simulation
- Agricultural production systems with crop diversification
- Market dynamics and price forecasting
- Nutritional outcomes and food security metrics
- Policy intervention impact analysis
- Socioeconomic dynamics modeling

### Visualization & Reporting

- Interactive HTML reports with Bootstrap styling
- Time series visualizations of key indicators
- Correlation analysis between food security metrics
- Market dynamics plots with dual-axis visualization
- Scenario comparison with color-coded metrics
- Detailed tabular results with searchable interfaces

## Data Sources

This simulation integrates data from multiple Bangladesh institutions:

- Bangladesh Bureau of Statistics
- Bangladesh Agricultural Research Council
- Department of Agricultural Extension
- Bangladesh Meteorological Department
- Food Planning and Monitoring Unit
- Institute of Public Health Nutrition
- And many other governmental and non-governmental sources

## Scenarios

The framework includes multiple simulation scenarios:

1. **Baseline**: Represents continuation of current trends and policies
2. **High Climate Impact**: Models more severe climate effects on agriculture and livelihoods
3. **Enhanced Adaptation**: Simulates increased agricultural technology adoption and infrastructure improvements
4. **Policy Change Safety Net**: Models expanded social protection policies focused on food security

## License

MIT License

## Contributors

- University of Tennessee Research Team
- Food Security Analysis Working Group
