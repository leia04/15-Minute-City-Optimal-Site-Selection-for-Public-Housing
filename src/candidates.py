from typing import List, Tuple
import geopandas as gpd


def select_candidates_and_demand_points(
    grid: gpd.GeoDataFrame,
    access_col: str,
    diversity_col: str,
    quantile: float = 0.85,
) -> Tuple[List[int], List[int]]:

    access_thr = grid[access_col].quantile(quantile)
    div_thr = grid[diversity_col].quantile(quantile)

    top_access = grid[grid[access_col] >= access_thr].index.tolist()
    top_div = grid[grid[diversity_col] >= div_thr].index.tolist()

    candidates = list(set(top_access) & set(top_div))
    demand_points = grid.index.tolist()
    return candidates, demand_points
