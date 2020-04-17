import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:,[3,4]].values

'''
import scipy.cluster.hierarchy as sch

dendrogram = sch.dendrogram(sch.linkage(X,method = 'ward'))
plt.title('Dendrogram')
plt.show()
'''
GreaterClusters = 5

from sklearn.cluster import AgglomerativeClustering

hc = AgglomerativeClustering(n_clusters = 5, affinity = 'euclidean', linkage = 'ward')
y_hc = hc.fit_predict(X)





colors = ['g','b','r','c','m','y','k','w']
for i in range(0,GreaterClusters):
	plt.scatter(X[y_hc==i,0],X[y_hc==i,1],s = 15,c = colors[i],label = 'Cluster '+str(i))

plt.title('Clusters of clients')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()

