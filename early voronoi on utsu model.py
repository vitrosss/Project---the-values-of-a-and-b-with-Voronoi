import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, cKDTree
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.stats import norm
from math import exp
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from scipy.interpolate import griddata

data = pd.read_csv('EARTHQUAKE_DATA.csv')

Hasil = []
def proses_voronoi(Jumlah_Cell, data, iteration, Hasil):
    x_random = np.random.uniform(data['Long'].min(), data['Long'].max(), Jumlah_Cell)
    y_random = np.random.uniform(data['Lat'].min(), data['Lat'].max(), Jumlah_Cell)
    random_points = np.column_stack((x_random, y_random))

    if len(random_points) < 3:
        return None, None, None

    vor = Voronoi(random_points)

    voronoi_kdtree = cKDTree(random_points)
    _, cell = voronoi_kdtree.query(data[['Long', 'Lat']])
    data['Cell'] = cell

    result = []

    for cell_id in range(Jumlah_Cell):
        cell_data = data[data['Cell'] == cell_id]['Magnitude']

        if not cell_data.empty:
            M_obs = np.array(cell_data)
            M_min = M_obs.min()
            M_mean = M_obs.mean()
            M_std = M_obs.std()
            N = len(M_obs)

            if M_min > 0 and M_mean > 0 and M_std > 0:
                B = np.log(np.e) / (M_mean - M_min)
                A = np.log(N) + np.log(B*np.log(10))+M_min*B
                Beta = B * np.log(10)

                try:
                    log_cdf_values = np.log(norm.cdf(M_obs, M_mean, M_std))
                except ValueError as e:
                    print(f"Error in CDF calculation: {e}")
                    log_cdf_values = np.zeros_like(M_obs)  # Use zeros as fallback

                log_likelihood = (N * np.log(Beta) - (Beta * M_obs - log_cdf_values).sum() + N * Beta * M_mean - N / 2 * Beta**2 * M_std**2)


                result.append({
                    'Iteration': iteration,
                    'Cell_Count': Jumlah_Cell,
                    'Region': cell_id,
                    'Longitude': random_points[cell_id][0],
                    'Latitude': random_points[cell_id][1],
                    'Magnitudo': M_obs,
                    'M_min': M_min,
                    'M_mean': M_mean,
                    'M_std': M_std,
                    'Beta_init': Beta,
                    'B_value': B,
                    'A_value':A,
                    'Log_likelihood': log_likelihood
                })

    results_df = pd.DataFrame(result)
    Hasil.append(results_df)
    return vor, random_points, results_df

for iteration in range(1, 101):
    print(f"Starting iteration {iteration}")
    for Jumlah_Cell in range(2, 41):
        vor, random_points, results_df = proses_voronoi(Jumlah_Cell, data, iteration, Hasil,)
        if vor is not None:
            print(f"Processed {Jumlah_Cell} Voronoi cells in iteration {iteration}")

            
final_results = pd.concat(Hasil, ignore_index=True)
final_results.to_csv('Voronoi.csv', index=False)