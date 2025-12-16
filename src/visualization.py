from typing import List, Optional
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from pyproj import Transformer
from shapely.geometry import Point


def plot_scores(grid: gpd.GeoDataFrame, col: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    grid.plot(column=col, cmap="viridis", linewidth=0.6, ax=ax, edgecolor="grey", legend=True)
    ax.set_title(title)
    ax.set_axis_off()
    plt.show()


def plot_candidates(grid: gpd.GeoDataFrame, candidates: List[int], title: str = "Candidates") -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    grid.plot(ax=ax, alpha=1, edgecolor="grey")
    pts = grid.loc[candidates].geometry.centroid
    ax.scatter(pts.x, pts.y, alpha=0.6, s=10, label="candidates")
    ax.set_title(title)
    ax.legend()
    ax.set_axis_off()
    plt.show()


def export_selected_sites_gpkg(
    grid: gpd.GeoDataFrame,
    selected_ids: List[int],
    out_path: str,
) -> gpd.GeoDataFrame:
    gdf = grid.loc[selected_ids].copy()
    gdf["selected_centroid"] = gdf.geometry.centroid
    gdf_point = gdf.set_geometry("selected_centroid")
    gdf_point.to_file(out_path, driver="GPKG")
    return gdf_point


def create_folium_map_selected_sites(
    selected_points: gpd.GeoDataFrame,
    out_html: str,
    crs_from: str = "EPSG:5179",
    crs_to: str = "EPSG:4326",
    zoom_start: int = 12,
):
    transformer = Transformer.from_crs(crs_from, crs_to, always_xy=True)

    def to_wgs84(pt: Point) -> Point:
        lon, lat = transformer.transform(pt.x, pt.y)
        return Point(lon, lat)

    gdf = selected_points.copy()
    gdf["geometry_wgs84"] = gdf.geometry.apply(to_wgs84)

    center = gdf["geometry_wgs84"].iloc[0]
    m = folium.Map(location=[center.y, center.x], zoom_start=zoom_start)

    for idx, row in gdf.iterrows():
        pt = row["geometry_wgs84"]
        folium.Marker(
            location=[pt.y, pt.x],
            popup=f"Selected site: {idx}",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    m.save(out_html)
    return m
