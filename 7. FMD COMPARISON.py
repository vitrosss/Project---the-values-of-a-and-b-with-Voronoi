df = pd.read_csv("1 MODEL.csv")

def parse_array(array_str):
    return [float(val) for val in ast.literal_eval(array_str.replace('np.float64', ''))]

#SAMPEL
iterasi = 100
Cell_Count = 40

row = df[(df['Iteration'] == iterasi) & (df['Cell_Count'] == Cell_Count)].iloc[0]
u = np.array(parse_array(row['u']))
sums = np.array(parse_array(row['sums']))
x  = np.arange(0, np.max(u), 0.1)


Beta_init = np.array(row['Beta_init'])    
M_mean = np.array(row['M_mean'])
M_std = np.array(row['M_std'])

beta = np.array(row['beta'])
mu = np.array(row['mu'])
sigma = np.array(row['sigma'])

def utsu(M, utsu):
    Beta_init = utsu[0]
    M_mean = utsu[1]
    M_std = utsu[2]
    constant = (np.exp(-Beta_init*M)*norm.cdf(M, M_mean, M_std)).sum()
    return np.exp(-Beta_init*M)*norm.cdf(M, M_mean, M_std)/constant

def density(M, theta):
    beta = theta[0]
    mu = theta[1]
    sigma = theta[2]
    constant = (np.exp(-beta*M)*norm.cdf(M, mu, sigma)).sum()
    return np.exp(-beta*M)*norm.cdf(M, mu, sigma)/constant

y1 = utsu(x,[Beta_init,M_mean,M_std])
y2 = density(x,[beta,mu,sigma])


print (Beta_init/np.log(10))
print (beta/np.log(10))

plt.scatter(u,sums, marker='+', color='black')
plt.plot(x, y1, label="sebelum = model Utsu")
plt.plot(x, y2, label="sesudah = model OK1993")
plt.semilogy()
plt.ylabel("Frequency")
plt.xlabel("Magnitude")
plt.ylim(bottom=0.0001)
plt.title(f'Kurva Frequency Magnitude Distribution (FMD) \nIterasi ke-{iterasi}, Cell ke-{Cell_Count}')
plt.legend()