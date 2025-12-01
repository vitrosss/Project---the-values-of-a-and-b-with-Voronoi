model_utsu = pd.read_csv("Voronoi.csv")
optimasi = pd.read_csv("1_OPT100.csv")

merged_df = pd.merge(
    optimasi,
    model_utsu[['Longitude', 'Latitude','Iteration','Cell_Count', 'M_min']],
    on=['Longitude', 'Latitude'],
    how='left'
)

merged_df.to_csv("1 MODEL.csv", index=False)
print(merged_df.head())  