#this program makes a tSNE visualization of data
#edited to make use of pca data
#currently using MinMaxScaler and learning rate of 1000.

import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
from sklearn.preprocessing import MinMaxScaler, Imputer
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt


net = pd.read_csv('~/PycharmProjects/network_classification/src/data/clean_data_with_new_chem.csv')

#data for use with pca file:
pca = pd.read_csv('~/PycharmProjects/network_classification/src/data/pca_for_tsne.csv')
#i need a list of the collections as numbers-useful in coloring tsne

collection_names = list(pca['Collection'])
pca['Collection'] = pca['Collection'].astype('category')
pca['Collection'] = pca['Collection'].cat.codes

#graph_categories = []
#all_categories = net['Collection'].values

#all_cat_names = list(net['Collection'].values)


#creates a list of the existing categories, no repeats
#for category in all_categories:
#    if not category in graph_categories:
#        graph_categories.append( category )
#re-assigns each collection name in all_categories to an integer, corresponding with its position in graph_categories
#for i in range(len( all_categories )):
#    all_categories[i] = graph_categories.index( all_categories[i] )

#all_graph_names = list(net['Graph'])

#del net['Graph']
#del net['Collection']


#net_array = net.values
pca_array = pca.values

#commented out scaler for pca stuff
#min_max_scale = MinMaxScaler()
#imp = Imputer(missing_values='NaN', strategy='most_frequent', axis=0)

tsne = TSNE()

#pipeline = make_pipeline(min_max_scale, tsne)
#tsne_features = pipeline.fit_transform(net_array)

tsne_features = tsne.fit_transform(pca_array)
xs = tsne_features[:,0]
ys = tsne_features[:,1]

plt.scatter(xs, ys, c=pca['Collection'])
plt.show()

#df = pd.DataFrame({"x" : xs, "y" : ys, "Category Number" : all_categories, "Category Name":all_cat_names, "Graph Name": all_graph_names})
#df.to_csv('~/PycharmProjects/network_classification/src/models/new_tsne_data.csv')