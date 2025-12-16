from location_opt.config import Config
from location_opt.io import load_grid, load_distances, ensure_dir
from location_opt.scoring import add_accessibility_and_diversity_scores
from location_opt.candidates import select_candidates_and_demand_points
from location_opt.optimization import solve_mclp
from location_opt.visualization import (
    plot_scores,
    plot_candidates,
    export_selected_sites_gpkg,
    create_folium_map_selected_sites,
)

def main():
    cfg = Config()

    ensure_dir(cfg.output_gpkg)
    ensure_dir(cfg.output_html)

    # 1) load inputs
    grid = load_grid(cfg.grid_path, cfg.crs_grid)
    distances = load_distances(cfg.distances_path)

    # 2) scoring
    grid = add_accessibility_and_diversity_scores(
        grid=grid,
        facility_types=list(cfg.facility_types),
        distances=distances,
        max_distance=cfg.max_access_distance_m,
        col_access="accessible_facility_count",
        col_diversity="diversity_index",
    )


    # 3) candidates / demand
    candidates, demand_points = select_candidates_and_demand_points(
        grid=grid,
        access_col="accessible_facility_count",
        diversity_col="diversity_index",
        quantile=cfg.candidate_quantile,
    )


    # 4) optimization (MCLP)
    selected_ids, coverage_by_loc = solve_mclp(
        candidates_gdf=grid.loc[candidates],
        demand_gdf=grid.loc[demand_points],
        demand_col=cfg.demand_col,
        p=cfg.p_facilities,
        max_distance=float(cfg.max_cover_distance_m),
    )

    print("Selected site IDs:", selected_ids)
    print("Coverage by selected site:", coverage_by_loc)

    # 5) outputs
    selected_points = export_selected_sites_gpkg(grid, selected_ids, cfg.output_gpkg)

    # folium map
    create_folium_map_selected_sites(
        selected_points=selected_points,
        out_html=cfg.output_html,
        crs_from=cfg.crs_grid,
        crs_to=cfg.crs_web,
        zoom_start=12,
    )

if __name__ == "__main__":
    main()
