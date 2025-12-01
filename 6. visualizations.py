plt.figure(figsize=(12, 6))

ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='green')
ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=1)

pcm = plt.pcolormesh(lon_mesh, lat_mesh, B_grid, shading='auto', cmap='jet')

cbar = plt.colorbar(pcm, orientation='horizontal', fraction=0.04, pad=0.05)
cbar.set_label('B Value')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title(' B-Value Distribution Map')
plt.savefig('B-Value Distribution Map', dpi=1600)
plt.show()

plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='green')
ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=1)

pcm = plt.pcolormesh(lon_mesh, lat_mesh, MAD_B, shading='auto', cmap='coolwarm')

cbar = plt.colorbar(pcm, orientation='horizontal', fraction=0.04, pad=0.05)
cbar.set_label('MAD B Value')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Median Absolute Deviation (MAD)- B Value')
plt.savefig('Median Absolute Deviation (MAD)- B Value', dpi=1600)
plt.show()


#########################################################
plt.figure(figsize=(12, 6))

ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='green')
ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=1)

pcm = plt.pcolormesh(lon_mesh, lat_mesh, A_grid, shading='auto', cmap='jet')

cbar = plt.colorbar(pcm, orientation='horizontal', fraction=0.04, pad=0.05)
cbar.set_label('A Value')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('A-Value Distribution Map')
plt.savefig('A-Value Distribution Map', dpi=1600)
plt.show()

plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='green')
ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=1)

pcm = plt.pcolormesh(lon_mesh, lat_mesh, MAD_A, shading='auto', cmap='coolwarm')

cbar = plt.colorbar(pcm, orientation='horizontal', fraction=0.04, pad=0.05)
cbar.set_label('MAD A Value')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Median Absolute Deviation (MAD) - A Value')
plt.savefig('Median Absolute Deviation (MAD) - A Value', dpi=1600)
plt.show()
cbar = plt.colorbar(pcm, orientation='horizontal', fraction=0.04, pad=0.05)
cbar.set_label('A Value')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('A-Value Distribution Map')
plt.savefig('A-Value Distribution Map', dpi=1600)
plt.show()

plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='green')
ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=1)

pcm = plt.pcolormesh(lon_mesh, lat_mesh, MAD_A, shading='auto', cmap='coolwarm')

cbar = plt.colorbar(pcm, orientation='horizontal', fraction=0.04, pad=0.05)
cbar.set_label('MAD A Value')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Median Absolute Deviation (MAD) - A Value')
plt.savefig('Median Absolute Deviation (MAD) - A Value', dpi=1600)
plt.show()