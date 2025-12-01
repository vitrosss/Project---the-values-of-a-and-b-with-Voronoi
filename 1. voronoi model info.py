model_info = []
for (iteration, cell_count), group in final_results.groupby(['Iteration', 'Cell_Count']):
    points_filtered = group[['Longitude', 'Latitude']].values.tolist()
    Mag = group['Magnitudo'].tolist()
    b_values_filtered = group['B_value'].tolist()
    A_values_filtered = group['A_value'].tolist()
    Log_model = group['Log_likelihood'].sum()
    
    N = len(Mag)
    k = 5
    k=5
    BIC = -Log_model + (k / 2) * np.log(N)

    model_info.append({
        'Iteration': iteration,
        'Cell_Count': cell_count,
        'B': b_values_filtered,
        'A': A_values_filtered,
        'Koordinat': points_filtered,
        'BIC': BIC
    })

    print(f"Model for Iteration {iteration} and Cell Count {cell_count} saved.")

model_info_df = pd.DataFrame(model_info)

csv_filename = 'VORONOI MODEL INFO.csv'
model_info_df.to_csv(csv_filename, index=False)