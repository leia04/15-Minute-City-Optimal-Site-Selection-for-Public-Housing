from typing import Dict, List, Tuple, Any

import geopandas as gpd
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpBinary, value


def solve_mclp(
    candidates_gdf: gpd.GeoDataFrame,
    demand_gdf: gpd.GeoDataFrame,
    demand_col: str,
    p: int = 3,
    max_distance: float = 750.0,
) -> Tuple[List[int], Dict[int, float]]:
    """
    MCLP (Maximal Covering Location Problem)
    - 후보지 i 중 p개 선택
    - 수요지 j가 후보지 i 중 하나라도 max_distance 내에 있으면 커버
    - 목적: 커버된 수요 합 최대화
    """
    candidates_gdf = candidates_gdf.copy()
    demand_gdf = demand_gdf.copy()

    if "centroid" not in candidates_gdf.columns:
        candidates_gdf["centroid"] = candidates_gdf.geometry.centroid
    if "centroid" not in demand_gdf.columns:
        demand_gdf["centroid"] = demand_gdf.geometry.centroid

    cand_ids = list(candidates_gdf.index)
    dem_ids = list(demand_gdf.index)

    neighbors: Dict[int, List[int]] = {j: [] for j in dem_ids}
    for j in dem_ids:
        cj = demand_gdf.loc[j, "centroid"]
        for i in cand_ids:
            ci = candidates_gdf.loc[i, "centroid"]
            if ci.distance(cj) <= max_distance:
                neighbors[j].append(i)

    # Model
    model = LpProblem("MCLP", LpMaximize)

    x = LpVariable.dicts("x", cand_ids, cat=LpBinary)  # select candidate
    y = LpVariable.dicts("y", dem_ids, cat=LpBinary)   # covered demand

    # objective: maximize covered demand
    model += lpSum(demand_gdf.loc[j, demand_col] * y[j] for j in dem_ids)

    # choose exactly p facilities
    model += lpSum(x[i] for i in cand_ids) == p

    # coverage constraints
    for j in dem_ids:
        if neighbors[j]:
            model += y[j] <= lpSum(x[i] for i in neighbors[j])
        else:
            model += y[j] == 0

    model.solve()

    selected = [i for i in cand_ids if value(x[i]) == 1]

    # coverage by selected location
    covered_by_loc: Dict[int, float] = {i: 0.0 for i in selected}
    for j in dem_ids:
        if value(y[j]) == 1:
            cj = demand_gdf.loc[j, "centroid"]
            best_i = None
            best_d = float("inf")
            for i in selected:
                ci = candidates_gdf.loc[i, "centroid"]
                d = ci.distance(cj)
                if d <= max_distance and d < best_d:
                    best_d = d
                    best_i = i
            if best_i is not None:
                covered_by_loc[best_i] += float(demand_gdf.loc[j, demand_col])

    return selected, covered_by_loc
