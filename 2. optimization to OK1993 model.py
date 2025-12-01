import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.stats import norm
from tqdm import tqdm
from math import exp
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from scipy.interpolate import griddata
import ast

df = pd.read_csv("EARTHQUAKE_DATA.csv")
vor_model = pd.read_csv("VORONOI MODEL INFO.csv")

def ifmd(M, verbose=False):
    x = np.sort(M)
    y = np.arange(len(x)) / float(len(x))
    y[1:] -= y[:-1].copy()
    u, inv = np.unique(x, return_inverse=True)
    sums = np.zeros(len(u), dtype=y.dtype)
    np.add.at(sums, inv, y)
    x_value = np.arange(0, np.max(u), 0.1)
    if verbose:
        print(x, y, u, inv, sums)
    return u, sums, x_value

def density(M, theta, x_value):
    beta, mu, sigma = theta
    constant = (np.exp(-beta * M) * norm.cdf(M, mu, sigma)).sum()
    _, y_value, _ = ifmd(x_value)  
    return np.exp(-beta * M) * norm.cdf(M, mu, sigma) / constant, y_value

log_likelihood = lambda theta, M: (
    len(M) * np.log(theta[0]) -
    (theta[0] * M - np.log(norm.cdf(M, theta[1], theta[2]))).sum() +
    len(M) * theta[0] * theta[1] -
    len(M) / 2 * theta[0]**2 * theta[2]**2
)

hasil = []

for model_id in tqdm(range(len(vor_model))):
    m = vor_model.iloc[model_id, :]
    coord = np.array(eval(m.Koordinat))
    vor = cKDTree(coord)
    _, cell_id = vor.query(df[["Long", "Lat"]])

    b_list = eval(vor_model.loc[model_id, "B"])

    for sel_id in range(len(coord)):
        mask = cell_id == sel_id
        sel_df = df.iloc[mask, :]

        N = len(sel_df)  

        if N < 1:
            hasil.append({
                "Model_ID": model_id,
                "Cell_ID": sel_id,
                "Longitude": coord[sel_id][0],
                "Latitude": coord[sel_id][1],
                "N": N,
                "b_initial": b_list[sel_id],
                "Beta_init": np.nan,
                "M_mean": np.nan,
                "M_std": np.nan,
                "b_optimized": np.nan,
                "beta": np.nan,
                "mu": np.nan,
                "sigma": np.nan,
                "theta": np.nan,
                "log_likelihood": np.nan,
                "u": np.nan,
                "sums": np.nan,
                "x": np.nan,
                "y": np.nan
            })
            continue

        M = sel_df.Magnitude.to_numpy()
        M_mean = np.mean(M)
        M_std = np.std(M)
        b_value = b_list[sel_id]
        beta = b_value * np.log(10)

        theta = [beta, M_mean, M_std]

        u, sums, x_value = ifmd(M)
        density_value, y_value = density(M, theta, x_value)

        bounds = [
            [0.2 * np.log(10), 1.8 * np.log(10)],
            [np.min(M), np.max(M)],
            [0.01, 0.8],
        ]

        try:
            results = minimize(lambda theta: -log_likelihood(theta, M),
                               theta,
                               method="trust-constr",
                               bounds=bounds,
                               options=dict(xtol=1e-8, verbose=0, maxiter=10000))

            beta_opt, mu_opt, sigma_opt = results.x
            b_new = beta_opt / np.log(10)
            ll_value = log_likelihood(results.x, M)

            hasil.append({
                "Model_ID": model_id,
                "Cell_ID": sel_id,
                "Longitude": coord[sel_id][0],
                "Latitude": coord[sel_id][1],
                "N": N,
                "b_initial": b_value,
                "Beta_init": beta,
                "M_mean": M_mean,
                "M_std": M_std,
                "b_optimized": b_new,
                "beta": beta_opt,
                "mu": mu_opt,
                "sigma": sigma_opt,
                "theta": list(results.x),
                "log_likelihood": ll_value,
                "u": list(u),
                "sums": list(sums),
                "x": list(x_value),
                "y": list(y_value),
            })

        except Exception as e:
            hasil.append({
                "Model_ID": model_id,
                "Cell_ID": sel_id,
                "Longitude": coord[sel_id][0],
                "Latitude": coord[sel_id][1],
                "N": N,
                "b_initial": b_value,
                "Beta_init": beta,
                "M_mean": M_mean,
                "M_std": M_std,
                "b_optimized": np.nan,
                "beta": np.nan,
                "mu": np.nan,
                "sigma": np.nan,
                "theta": np.nan,
                "log_likelihood": np.nan,
                "u": list(u),
                "sums": list(sums),
                "x": list(x_value),
                "y": list(y_value),
            })

hasil_df = pd.DataFrame(hasil)
hasil_df.to_csv("1_OPT100.csv", index=False)
