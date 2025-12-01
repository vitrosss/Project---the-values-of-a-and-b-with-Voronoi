file_path = "1 BestModel.csv"
best_100model = pd.read_csv(file_path)

grid_size = 0.1
lat_grid = np.arange(-20, 9, grid_size)
lon_grid = np.arange(92, 152, grid_size)

lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)
grid_points = np.column_stack((lon_mesh.ravel(), lat_mesh.ravel()))

B_values_grid = np.zeros((len(lon_grid), len(lat_grid)))
A_values_grid = np.zeros((len(lon_grid), len(lat_grid)))

all_coordinates = []
all_B_values = []
all_A_values = []

for _, row in best_100model.iterrows():
    coordinates = eval(row["Koordinat"])
    B_values = eval(row["B"])
    A_values = eval(row["A"])

    tree = cKDTree(coordinates)

    _, idx = tree.query(grid_points)

    all_coordinates.append(grid_points)
    all_B_values.append(np.array(B_values)[idx])
    all_A_values.append(np.array(A_values)[idx])

all_B_values = np.array(all_B_values)
all_A_values = np.array(all_A_values)

median_B_values = np.median(all_B_values, axis=0)
B_grid = median_B_values.reshape(lat_mesh.shape)

median_A_values = np.median(all_A_values, axis=0)
A_grid = median_A_values.reshape(lat_mesh.shape)

mad_values_B = np.median(np.abs(all_B_values - median_B_values), axis=0)
MAD_B = mad_values_B.reshape(lat_mesh.shape)

mad_values_A = np.median(np.abs(all_A_values - median_A_values), axis=0)
MAD_A = mad_values_A.reshape(lat_mesh.shape)

best_100model_grid = pd.DataFrame(grid_points, columns=['Longitude', 'Latitude'])
best_100model_grid['B_Value_Array'] = list(all_B_values.T)
best_100model_grid['B_Value_Array'] = list(all_A_values.T)
best_100model_grid['Median_B_Value'] = median_B_values
best_100model_grid['Median_A_Value'] = median_A_values
best_100model_grid['MAD_B'] = mad_values_B
best_100model_grid['MAD_A'] = mad_values_A

best_100model_grid.to_csv('VORONOI HASIL_GRID.csv', index=False)
