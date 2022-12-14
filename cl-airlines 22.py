# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 23:16:33 2022


@author: aditya
"""
#clustering on airlines 
import pandas as pd
data=pd.read_excel("EastWestAirlines.xlsx",sheet_name="data")
data.shape
data.dtypes
data.drop(["ID#"],axis=1,inplace=True)

x=data.iloc[:,1:12].values
x.shape
list(x)

#standardize the data
from sklearn.preprocessing import StandardScaler
SS=StandardScaler()
x_scale=SS.fit_transform(x)

#DB scan
from sklearn.cluster import DBSCAN
db=DBSCAN(eps=2,min_samples=7).fit(x_scale)
db.labels_

cl=pd.DataFrame(db.labels_,columns=['Cluster'])
cl
cl['Cluster'].value_counts()

data_new=pd.concat([pd.DataFrame(x_scale),cl],axis=1)

#noise data
nd=data_new[data_new['Cluster']==-1]
nd

#final data without outliers
fd=data_new[data_new['Cluster']==0]
fd.shape
data_new.mean()
fd.mean()
type(fd)
################################################################################################################
#K Means Clustering
#Initializing KMeans
from sklearn.cluster import KMeans
km=KMeans(n_clusters=6).fit(fd)
lab=km.predict(fd)
type(lab)

c=km.cluster_centers_
type(c)
km.inertia_

%matplotlib qt
fig=plt.figure()
ax=Axes3D(fig)
ax.scatter(fd.iloc[:,0],fd.iloc[:,1],fd.iloc[:,2])
ax.scatter(c[:,0],c[:,1],c[:,2],marker="*",c="Red",s=1000)

clust=[]
for i in range(1,11,1):
    km=KMeans(n_clusters=i).fit(fd)
    km.inertia_
    clust.append(km.inertia_)
    
#elbow plot
plt.plot(range(1,11),clust)
plt.title("Elbow Plot")
plt.xlabel("No of Clusters")
plt.ylabel("Cluster Inertia values")
plt.show()
#########################################################################################################
#(b)Hierarchial Clustering
#agglomerative Clustering
from sklearn.cluster import AgglomerativeClustering
ac=AgglomerativeClustering(n_clusters=3,affinity='euclidean',linkage='complete')
ac.fit_predict(fd)

plt.figure(figsize=(16,9))
plt.scatter(fd.iloc[:,0],fd.iloc[:,1],c=ac.labels_,cmap='rainbow')

#Dendogram
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
plt.figure(figsize=(16,9))
plt.title('Dendogram')
dend=shc.dendrogram(shc.linkage(fd,method='complete'))

'''
Inference: Firstly i have performed DB Scan to remove the outliers from the data
           Then using the data without outliers to perform both K-Means and 
           Hierarchial clustering.
The best clustering is found to be with K-Means clustering algorithm
'''