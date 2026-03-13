# Skill: Spatial Cartography for Airbnb Paris (AirBnB_NLP4socialscience)

## Goal
Produce consistent spatial maps for Airbnb listings in Paris using the local arrondissement boundaries and reproducible geospatial transformations.

## When to use
- Any request for a Paris map based on listing coordinates (`latitude`, `longitude`).
- Any choropleth, KDE contour map, or local price/density surface.
- Any notebook or script that needs arrondissement boundaries, Paris masking, or map exports in `data/`.

## Required Inputs
- A dataframe with `latitude` and `longitude`.
- A local Paris boundary file: `data/map/arrondissements.zip`.
- For price surfaces, a numeric nightly price column such as `price_numeric`, `price_clean`, or `price`.

## Core Geospatial Rules
1. Never hardcode absolute paths. Use `DATA_DIR / 'map' / 'arrondissements.zip'`.
2. Build points in `EPSG:4326`, then project both points and polygons to `EPSG:2154` before any area, KDE, or metric-distance computation.
3. Filter to broad Paris geographic bounds before projection to remove invalid points:
   - latitude between `48.75` and `48.95`
   - longitude between `2.20` and `2.50`
4. For final rendering, mask the surface strictly to Paris using the union of arrondissement geometries.
5. Use arrondissement boundaries as the visual reference layer.

## Boundary And Styling Rules
- Arrondissement boundaries should default to grey: `#999999`.
- Boundary linewidth should stay light and publication-friendly: around `0.8`.
- Keep the map clean: no axis ticks, no grid, no basemap.
- Prefer readable sequential colormaps:
  - Density: `YlGnBu`
  - Price: `YlOrRd`
- Use thin darker isolines above filled contours when contour readability matters.

## Standard Choropleth Workflow
1. Load `arrondissements.zip` with GeoPandas.
2. Rename ambiguous columns only if needed for readability.
3. Reproject polygons and points to `EPSG:2154`.
4. Spatially join points to arrondissements.
5. Aggregate the target metric by arrondissement.
6. If using area-normalized metrics, compute `area_ha = geometry.area / 10000`.
7. Export summary CSV to `data/` and figure PNG to `data/`.

## Standard KDE Density Workflow
Use this for continuous listing density maps.

1. Fit an unweighted KDE on projected point coordinates.
2. Evaluate KDE on a regular grid covering `arr_m.total_bounds`.
3. Convert probability density to listings per hectare:

```python
density_prob = kde(grid_coords).reshape(xx.shape)
density_per_ha = density_prob * len(points_m) * 10000.0
```

4. If requested, clip display values to a fixed range.
5. Render with `contourf` plus a few thin isolines.
6. Mask outside Paris before plotting or set outside cells to `np.nan`.

## Standard KDE Mean Price Workflow
Use this for a local mean nightly price surface, not a price sum.

1. Fit two KDEs on projected coordinates:
   - unweighted KDE for local spatial density
   - price-weighted KDE for local price mass
2. Compute the local conditional mean price:

```python
kde_density = gaussian_kde(np.vstack([xs, ys]))
kde_price = gaussian_kde(np.vstack([xs, ys]), weights=price_weights)

density_prob = kde_density(grid_coords).reshape(xx.shape)
price_density_prob = kde_price(grid_coords).reshape(xx.shape)
safe_density = np.where(density_prob > density_prob.max() * 1e-6, density_prob, np.nan)
mean_price_surface = (price_density_prob * price_weights.sum()) / (safe_density * float(len(xs)))
```

3. Mask outside Paris using the arrondissement union.
4. Use fixed display bounds when the user specifies a target scale, for example `50` to `500` EUR.
5. Use a colorbar label such as `Mean nightly price (EUR)`.

## Paris Mask Pattern
Prefer this masking logic for any interpolated surface:

```python
from shapely.ops import unary_union

paris_union = unary_union(arr_m.geometry)
try:
    from shapely.vectorized import contains as shp_contains
    inside_mask = shp_contains(paris_union, xx.ravel(), yy.ravel()).reshape(xx.shape)
except ImportError:
    import shapely
    inside_mask = shapely.contains_xy(paris_union, xx.ravel(), yy.ravel()).reshape(xx.shape)

surface = np.where(inside_mask, surface, np.nan)
```

## Reusable Python Template
Use this compact template as a starting point in notebooks or scripts.

```python
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import gaussian_kde
from shapely.ops import unary_union

DATA_DIR = Path("data")
MAP_FILE = DATA_DIR / "map" / "arrondissements.zip"

source_df = df.copy()
source_df["latitude"] = pd.to_numeric(source_df["latitude"], errors="coerce")
source_df["longitude"] = pd.to_numeric(source_df["longitude"], errors="coerce")
source_df = source_df.dropna(subset=["latitude", "longitude"])
source_df = source_df[
  source_df["latitude"].between(48.75, 48.95)
  & source_df["longitude"].between(2.20, 2.50)
].copy()

points_gdf = gpd.GeoDataFrame(
  source_df,
  geometry=gpd.points_from_xy(source_df["longitude"], source_df["latitude"]),
  crs="EPSG:4326",
)
arr_gdf = gpd.read_file(MAP_FILE)

arr_m = arr_gdf.to_crs(epsg=2154)
points_m = points_gdf.to_crs(epsg=2154)

xs = points_m.geometry.x.to_numpy()
ys = points_m.geometry.y.to_numpy()

minx, miny, maxx, maxy = arr_m.total_bounds
xi = np.linspace(minx, maxx, 220)
yi = np.linspace(miny, maxy, 220)
xx, yy = np.meshgrid(xi, yi)
grid_coords = np.vstack([xx.ravel(), yy.ravel()])

# Example: listing density per hectare
kde = gaussian_kde(np.vstack([xs, ys]))
surface = kde(grid_coords).reshape(xx.shape) * len(points_m) * 10000.0

# Strict Paris mask
paris_union = unary_union(arr_m.geometry)
try:
  from shapely.vectorized import contains as shp_contains
  inside_mask = shp_contains(paris_union, xx.ravel(), yy.ravel()).reshape(xx.shape)
except ImportError:
  import shapely
  inside_mask = shapely.contains_xy(paris_union, xx.ravel(), yy.ravel()).reshape(xx.shape)
surface = np.where(inside_mask, surface, np.nan)

display_min, display_max = 0.0, 40.0
surface_display = np.clip(surface, display_min, display_max)

fig, ax = plt.subplots(figsize=(10, 10))
cf = ax.contourf(
  xx,
  yy,
  surface_display,
  levels=np.linspace(display_min, display_max, 9),
  cmap="YlGnBu",
  extend="max",
  alpha=0.85,
)
ax.contour(
  xx,
  yy,
  surface_display,
  levels=[5, 10, 20, 30, 40],
  colors="#1d3557",
  linewidths=0.8,
)
arr_m.boundary.plot(ax=ax, color="#999999", linewidth=0.8)

cbar = fig.colorbar(cf, ax=ax, fraction=0.036, pad=0.02)
cbar.set_label("Apartments per hectare", rotation=90)
ax.set_axis_off()
plt.tight_layout()
plt.show()
```

## Export Rules
- Save figure outputs in `data/` with explicit names tied to the notebook/script section.
- Save derived arrondissement summaries in `data/` as UTF-8 CSV.
- Keep naming stable and descriptive, for example:
  - `data/P00c_density_by_arrondissement.csv`
  - `data/P00c_paris_density2d_contourf_clean_per_hectare.png`
  - `data/P00c_paris_price2d_contourf_clean_per_hectare.png`

## Notebook And Script Integration Rules
- Add a markdown section immediately before any new mapping code cell.
- The markdown must explain the goal, the transformation, and the output in 2-3 simple sentences.
- Reuse `POWER_WATTS`, `FR_GRID_KGCO2_PER_KWH`, and final runtime reporting conventions when the map is part of a full pipeline script.

## Validation Checklist
- The map uses only points with valid numeric coordinates.
- The polygons and points are projected to `EPSG:2154` before metric computations.
- The final rendered surface is strictly masked to Paris.
- The plotted metric matches the requested interpretation:
  - density per hectare
  - local mean nightly price
  - arrondissement aggregate
- The display scale matches the user's requested bounds when specified.
- The arrondissement boundaries are visible but visually secondary.