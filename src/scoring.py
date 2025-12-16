import math
from collections import defaultdict
from typing import Dict, Any, List, Tuple

import numpy as np
import geopandas as gpd
from tqdm import tqdm


def calculate_shannon_diversity_index(facility_count: Dict[str, int]) -> float:
    total = sum(facility_count.values())
    if total <= 0:
        return 0.0
    proportions = [c / total for c in facility_count.values() if c > 0]
    return float(-sum(p * math.log(p) for p in proportions))


def _count_accessible_facilities_for_grid(
    grid_id: int,
    facility_types: List[str],
    distances: Dict[str, Any],
    max_distance: int,
) -> Tuple[int, Dict[str, int]]:
    per_type_count = {}
    total = 0

    for ftype in facility_types:
        fdict = distances.get(ftype, {})
        entry = fdict.get(grid_id, [])

        if isinstance(entry, dict) and "distances" in entry:
            ds = entry["distances"]
        else:
            ds = entry

        if ds is None:
            ds = []

        # ds는 distance list라고 가정
        c = sum(1 for d in ds if d is not None and float(d) <= max_distance)
        per_type_count[ftype] = int(c)
        total += int(c)

    return total, per_type_count


def add_accessibility_and_diversity_scores(
    grid: gpd.GeoDataFrame,
    facility_types: List[str],
    distances: Dict[str, Any],
    max_distance: int = 1200,
    col_access: str = "accessible_facility_count",
    col_diversity: str = "diversity_index",
) -> gpd.GeoDataFrame:

    grid = grid.copy()

    access_scores = []
    diversity_scores = []

    idxs = list(grid.index)
    for grid_id in tqdm(idxs, desc="Scoring grid cells"):
        total, per_type = _count_accessible_facilities_for_grid(
            grid_id=grid_id,
            facility_types=facility_types,
            distances=distances,
            max_distance=max_distance,
        )
        access_scores.append(total)
        diversity_scores.append(calculate_shannon_diversity_index(per_type))

    grid[col_access] = access_scores
    grid[col_diversity] = diversity_scores
    return grid
