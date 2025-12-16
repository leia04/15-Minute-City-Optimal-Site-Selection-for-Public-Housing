import json
import os
from typing import Any, Dict

import geopandas as gpd


def load_grid(path: str, crs: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs(crs)
    else:
        gdf = gdf.to_crs(crs)

    gdf = gdf.copy()
    gdf["centroid"] = gdf.geometry.centroid
    return gdf


def _convert_keys_to_int(obj: Any) -> Any:
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            try:
                ik = int(k)
                new[ik] = _convert_keys_to_int(v)
            except (ValueError, TypeError):
                new[k] = _convert_keys_to_int(v)
        return new
    if isinstance(obj, list):
        return [_convert_keys_to_int(x) for x in obj]
    return obj


def load_distances(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        distances = json.load(f)
    return _convert_keys_to_int(distances)


def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
