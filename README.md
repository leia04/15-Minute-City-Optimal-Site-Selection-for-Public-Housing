# Optimal Site Selection for Public Housing (15-Minute Walkable City)

## Abstract
This project analyzes optimal locations for youth public rental housing in Changwon, South Korea, based on the 15-minute walkable city concept.  
Conducted as part of the 2024 Gyeongsangnam-do Big Data Analysis Competition, the analysis focuses on translating policy goals into quantifiable spatial metrics and optimization-based decision making.

## Problem
Changwon City faces a decline in its youth population, threatening its status as a special metropolitan city.  
Public statistics indicate that housing conditions are a major driver of youth outmigration, highlighting the need for well-located public rental housing.

The challenge is to identify housing locations that allow residents to access essential daily-life infrastructure within walking distance, under limited site selection constraints.


## Key Findings
- Three optimal locations were identified within Changwon City, each providing access to diverse daily-life infrastructure within walking distance.  
- The optimization-based approach ensures transparent and reproducible site selection compared to heuristic placement.



## Approach
The analysis follows a structured pipeline:

#### Data Preparation
- Aggregated youth population at a 500m grid level to define spatial demand.
- Geocoded daily-life facilities from public datasets.

#### Walkability-Based Distance Calculation
- Constructed a pedestrian road network.
- Computed walking distances from grid centroids, defining a 15-minute threshold as 1,200 meters.

#### Accessibility and Diversity Scoring
- Quantified accessibility by counting facilities within walking distance.
- Measured facility balance using the Shannon Diversity Index.

#### Candidate Site Selection
- Selected candidate locations from the intersection of top 15% accessibility and diversity scores.

#### Optimization
- Formulated the problem as a Maximal Covering Location Problem (MCLP).
- Selected three sites to maximize covered youth population within a 750m distance constraint.

#### Optimization
The final site selection was formulated as a Maximal Covering Location Problem (MCLP):
- Objective: maximize covered youth population
- Coverage distance: 750 meters
- Number of sites: 3

Binary decision variables were used to model site selection.


## Code
- `io.py`: Loads and preprocesses spatial grid data and precomputed facility distance data.
- `scoring.py`: Computes accessibility scores and Shannon diversity indices for each grid cell.
- `candidates.py`: Selects candidate sites based on accessibility and diversity thresholds.
- `optimization.py`: Implements the MCLP formulation and solves the site selection problem using integer programming.
- `visualization.py`: Provides optional spatial visualization and result export utilities.

## Tools and Libraries
- Python
- pandas, numpy
- geopandas, shapely, pyproj
- osmnx, networkx
- PuLP
- matplotlib, folium
- tqdm

## Contribution
- Designed the full spatial analysis and optimization pipeline.
- Defined accessibility and diversity metrics aligned with the 15-minute city concept.
- Implemented integer programming for optimal site selection.
- Translated policy-oriented objectives into a reproducible, data-driven framework.
