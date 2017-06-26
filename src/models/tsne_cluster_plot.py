import pandas as pd
from bokeh.charts import Scatter, output_file, show
from bokeh.models import HoverTool

#read file
tsne = pd.read_csv('/Users/adrianaortiz/Downloads/tsne_plot_data_minmaxscale.csv')

#get each individual column and create new data frame
category = tsne['Category Name']
x = tsne['x']
y = tsne['y']
names = tsne['Graph']
idx = tsne.index.tolist()


d = {'x': x, 'y': y, 'Category Name' : category}
e = {'x': x, 'y': y, 'Category Name' : category, 'Graph': names}
f = {'x': x, 'y': y, 'Category Name' : category, 'Graph': names, 'index': idx}

df=pd.DataFrame(f)

#creating hover tool
hover = HoverTool()
hover.tooltips = [("Category", "@{Category Name}"), ("Graph", "@index")]

#creating the scatter plot
p =Scatter(x='x', y='y', color='Category Name', marker='Category Name', title='t-SNE using MinMaxScale',plot_width=1100, data = df)
p.add_tools(hover)
p.legend.click_policy="hide"

output_file('tsne_plot.html')
show(p)

#get all categories without repetitions
all_categories = category.unique().tolist()