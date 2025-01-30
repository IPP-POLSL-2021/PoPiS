# PoPiS: Polish Parliamentary Information System

## Overview

This project provides comprehensive Python tools for analyzing and accessing data from the Polish Sejm (Parliament) API, offering in-depth insights into parliamentary processes, voting patterns, and political dynamics.

## Features

- Detailed API wrappers for various parliamentary data
- Advanced analysis of:
  - MP statistics
  - Club compositions
  - Voting patterns
  - Legislative processes
  - Committee activities

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/PoPiS.git
cd PoPiS
pip install -r requirements.txt
```

## Quick Start

```python
from api_wrappers import MP, clubs, committees

# Get information about an MP
mp_details = MP.get_MP(10, 241)

# Find minimal coalitions
coalition_details = clubs.find_minimal_coalitions()

# Analyze committee statistics
committee_stats = committees.get_committee_stats(10)
```

## Available Modules

- Comprehensive API wrappers for:
  - Members of Parliament
  - Parliamentary Clubs
  - Committees
  - Votings
  - Interpellations
  - Legislative Processes
  - And more...

## Project Structure

- `api_wrappers/`: API interaction modules
- `Controller/`: Data processing and analysis scripts
- `View/`: Visualization and reporting components
- `Data/`: Election and parliamentary data

## Requirements

- Python 3.8+
- `requests`
- `pandas`
- `numpy`
- `plotly`
- `streamlit`

## Contributing

Contributions are welcome! Please read our contribution guidelines and submit pull requests.

## License

[Specify your project's license]
