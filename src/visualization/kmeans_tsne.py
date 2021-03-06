# This program creates plots using data ran on tsne and
# plots it with bokeh using kmeans to get the clusters

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import d3
import matplotlib.pyplot as plt
from bokeh.io import export_svgs


# Read file
tsne_data = pd.read_csv('../data/new_tsne_data.csv', index_col=0)

tsne_data = tsne_data[tsne_data['Category Name'] != 'Temporal Reachability']


# Make a copy of the data
tsne_new = pd.DataFrame.copy(tsne_data)


# Delete categorical columns
del tsne_new['Category Name']
del tsne_new['Graph Name']
del tsne_new['Category Number']


# Create array of data (only numerical columns)
tsne_array = tsne_new.values



#**************************
# Getting inertia graph
#**************************
def inertia_plot(data_array):
    ks = range(1, 20)
    inertias = []

    for k in ks:
        # Create a KMeans instance with k clusters: model
        model = KMeans(n_clusters=k)

        # Fit model to samples
        # Change to the data we need to check
        model.fit(data_array)

        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)

    # Plot ks vs inertias
    plt.plot(ks, inertias, '-o')
    plt.title('Inertia vs. k')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()



#**************************
# Creating plot of kmeans
# using tsne data in bokeh
#**************************

# Create KMeans with 8 clusters and fit data to model
kmeans = KMeans(n_clusters = 8)
kmeans.fit_transform(tsne_array)
labels = kmeans.predict(tsne_array)
centroids = kmeans.cluster_centers_

#**************************
#write out labels for use in boxplots/table
#**************************

#tsne_data['Label'] = labels
#tsne_data.to_csv('~/PycharmProjects/network_classification/src/data/tsne_label_data.csv')

# Assign the columns of centroids: centroids_x, centroids_y
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]

df_labels = pd.read_csv('../data/tsne_label_data.csv')

# Create cross tabulation of tsne data and print
df1 = pd.DataFrame({'labels':df_labels['Label'], 'Collection':df_labels['Category Name']})
print("Crosstab for t-SNE data:\n")
ct = pd.crosstab(df1['Collection'], df1['labels'])
print(ct)

# Get category and graph names for new dataframe
category = tsne_data['Category Name']
names = tsne_data['Graph Name']

# Get all categories without repetitions
all_categories = category.unique().tolist()

# Assign the columns of tsne_array
xs = tsne_array[:,0]
ys = tsne_array[:, 1]
data = {'x': xs, 'y': ys, 'Category Name' : category, 'Graph': names, 'Label' : labels}

# Create new pandas dataframe
df=pd.DataFrame(data)

# Create hover tool
hover = HoverTool()
hover.tooltips = [("Graph", "@Graph"),("Category", "@{Category Name}"), ("Cluster", "@Label")]

# Creating the figure for the scatter plot
p=figure(title = 't-Distributed Stochastic Neighbor Embedding', plot_width=1000)
p.title.text_font_size = '25pt'

# Create scatter points and color the plot by collection
#for i, graph in enumerate(all_categories):
#    source = ColumnDataSource(df[df['Category Name'] == graph])
#    p.circle(x='x', y='y', source = source, color = d3['Category20'][17][i], size = 8, legend = graph)



#Color by label
#for label in range(14):
#    source = ColumnDataSource(df[df['Label'] == label])
#    p.circle(x='x', y='y', source = source, color = d3['Category20'][17][label], size = 8)


colormap = {'Web Graphs':d3['Category20'][16][0], 'Technological Networks':d3['Category20'][16][1],
            'Facebook Networks':d3['Category20'][16][2], 'Social Networks':d3['Category20'][16][3],
            'Scientific Computing':d3['Category20'][16][4], 'Retweet Networks':d3['Category20'][16][5],
            'Recommendation Networks':d3['Category20'][16][6], 'Massive Network Data':d3['Category20'][16][7],
            'Infrastructure Networks':d3['Category20'][16][8], 'Interaction Networks':d3['Category20'][16][9],
            'Ecology Networks': d3['Category20'][16][10], 'Collaboration Networks':d3['Category20'][16][11],
            'Brain Networks': d3['Category20'][16][12], 'Biological Networks':d3['Category20'][16][13],
            'Cheminformatics': d3['Category20'][16][14],}



#colors = [colormap[x] for x in df['Category Name']]
#colors = [colormap[x] for all_categories(x).index in (for x in df['Category Name']) ]
df = df.assign(colors = [colormap[x] for x in df['Category Name']])

source0=df[df['Label']==0]
source1=df[df['Label']==1]
source2=df[df['Label']==2]
source3=df[df['Label']==3]
source4=df[df['Label']==4]
source5=df[df['Label']==5]

#p.circle(x='x', y='y', source=ColumnDataSource(df[df['Label'] == 0]), legend='Category Name', size=8)
p.triangle(x='x', y='y', source=ColumnDataSource(source0), legend='Category Name',color='colors', size=8)
#p.triangle(x='x', y='y', source=ColumnDataSource(df[df['Label'] == 1]), color=colors, legend='Category Name', size=8)
p.circle(x='x', y='y', source=ColumnDataSource(source1), legend='Category Name', color='colors', size=8)
p.diamond(x='x', y='y', source=ColumnDataSource(source2), color='colors', legend='Category Name', size=8)
p.asterisk(x='x', y='y', source=ColumnDataSource(df[df['Label'] == 3]), color='colors', legend='Category Name', size=8)
p.cross(x='x', y='y', source=ColumnDataSource(df[df['Label'] == 4]), color='colors', legend='Category Name', size=8)
p.square(x='x', y='y', source=ColumnDataSource(df[df['Label'] == 5]), color='colors', legend='Category Name', size=8)
p.inverted_triangle(x='x', y='y', source=ColumnDataSource(df[df['Label'] == 6]), color='colors', legend='Category Name', size=8)
p.square(x='x', y='y', source=ColumnDataSource(df[df['Label'] == 7]), color='colors', legend='Category Name', size=8)


# Creating scatter points of centroids
p.square(centroids_x, centroids_y, color ='black', size = 12, legend = 'Centroid')

# Add tools and interactive legend
p.add_tools(hover)
p.legend.location = "top_left"
p.legend.click_policy="hide"
#p.output_backend="svg"
#export_svgs(p, filename="tsnesvg.svg")
#p.legend.label_text_font_size = "16pt"
#p.legend.background_fill_alpha = 0

# Save file and show plot
output_file('kmeans_centroids_plot.html')
show(p)

