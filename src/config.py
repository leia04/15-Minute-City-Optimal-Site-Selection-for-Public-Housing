from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Config:
    # input paths
    grid_path: str = "data/raw/grid_data.gpkg"
    distances_path: str = "data/raw/merged_distances.json"

    # output paths
    output_gpkg: str = "data/outputs/selected_sites.gpkg"
    output_html: str = "data/outputs/selected_sites_map.html"

    # data columns
    demand_col: str = "val"  
    crs_grid: str = "EPSG:5179"   
    crs_web: str = "EPSG:4326"    

    # scoring
    max_access_distance_m: int = 1200

    # candidate selection 
    candidate_quantile: float = 0.85

    # optimization (MCLP)
    p_facilities: int = 3
    max_cover_distance_m: int = 750

    facility_types: List[str] = (
        "park",
        "laundry",
        "health",
        "bus",
        "subway",
        "cafe",
    )
