model_info = []

for (iteration, cell_count), group in merged_df.groupby(['Iteration', 'Cell_Count']):
    points_filtered = group[['Longitude', 'Latitude']].values.tolist()
    
    N = group['N']
    M_min = group['M_min']
    b = group['b_optimized']
    
    A_values_filtered = np.log(N) + np.log(b * np.log(10)) + b * M_min
    A_values_filtered = A_values_filtered.tolist()
    
    Log_model = group['log_likelihood'].sum()

    k = 5
    BIC = -Log_model + (k / 2) * np.log(len(group))

    model_info.append({
        'Iteration': iteration,
        'Cell_Count': cell_count,
        'B': b.tolist(),
        'A': A_values_filtered,
        'Koordinat': points_filtered,
        'BIC': BIC
    })

    print(f"Model for Iteration {iteration} and Cell Count {cell_count} saved.")

model_info_df = pd.DataFrame(model_info)
csv_filename = '1 MODEL INFO.csv'
model_info_df.to_csv(csv_filename, index=False)


best_100 = model_info_df.sort_values(by='BIC').head(100)

cell_counts = model_info_df['Cell_Count']
bic_values = model_info_df['BIC']

Best100_Cell = best_100['Cell_Count']
Best100_BIC = best_100['BIC']

Med_BIC = model_info_df.groupby('Cell_Count')['BIC'].median()

plt.figure(figsize=(6, 5))
plt.scatter(cell_counts, bic_values, color='gray', alpha=0.5, label='All Models')
plt.scatter(Best100_Cell, Best100_BIC, color='red', label='Best 100 Models')
plt.plot(Med_BIC.index, Med_BIC.values, color='Black', linestyle='--', linewidth=2, label='Median BIC')

best_100model = pd.DataFrame(best_100)

csv_filename = '1 BestModel.csv'
best_100model.to_csv(csv_filename, index=False)

plt.title('BIC vs Number of Effective Cells')
plt.xlabel('Number of Effective Cells (Nv)')
plt.ylabel('BIC')
plt.xlim(min(cell_counts)-1, max(cell_counts)+1)
plt.ylim(min(bic_values)-5000, max(bic_values)+5000 )
plt.legend()
plt.grid(True)
plt.savefig('BIC', dpi=1600)
plt.show()
