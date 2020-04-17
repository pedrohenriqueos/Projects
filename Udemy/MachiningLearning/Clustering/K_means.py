import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:,[3,4]].values

from sklearn.cluster import KMeans

WCSS = []

for i in range(1,11):#optimize with binary search
	kmeans = KMeans(n_clusters = i,init = 'k-means++',max_iter = 300, n_init = 10,random_state = 0)
	kmeans.fit(X)
	WCSS.append(kmeans.inertia_)
''' #See the optimal amount of clusters
plt.plot(range(1,11),WCSS)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
'''
GreaterWCSS = 5
kmeans = KMeans(n_clusters = GreaterWCSS,init = 'k-means++',max_iter = 300,n_init = 10,random_state = 0)
y_kmeans = kmeans.fit_predict(X)

colors = ['g','b','r','c','m','y','k','w']
for i in range(0,GreaterWCSS):
	plt.scatter(X[y_kmeans==i,0],X[y_kmeans==i,1],s = 15,c = colors[i],label = 'Cluster '+str(i))
plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],s=20,label = 'Centroids',c = colors[GreaterWCSS])

plt.title('Clusters of clients')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()

