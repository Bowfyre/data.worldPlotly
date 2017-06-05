#This file is intended for testing purposes only

import os
from flask import Flask, render_template, Markup
from plotly.offline import plot

from plotly.graph_objs import *
import plotly

# use the datadotworld python library to connect to data.world
from datadotworld.config import EnvConfig
from datadotworld.datadotworld import DataDotWorld

#use flask to run our web app
from flask import Flask, request, render_template

# create the Flask application
app = Flask(__name__)
app.debug = True

# load the data.world API token from an environment variable
ddw = DataDotWorld(config=EnvConfig())

# grab and sort the list of all distinct names from the dataset
distinct_names_query = ddw.query('government/us-baby-names-by-yob',
                  ''' SELECT DISTINCT Name
                        FROM `babyNamesUSYOB-mostpopular.csv/babyNamesUSYOB-mostpopular`''')
names = sorted([x["Name"] for x in distinct_names_query.table])
#because of the inefficency of the datasets method
names=names[1:5]

#Global Variables

ids=[]
ids2=[]
graphData=[]


def graphingSetup (listofnames):
    global ids
    counter=0
    vis=[True]*len(listofnames)
    ids.append(dict(label='All',
        args=['visible',vis]))
    ids.append(dict(label='None',
        args=['visible',[False,False,False]]))#Even though there are 4 plots, this makes everything, not shown
    ids.append(dict(label='Only 1',
        args=['visible',[False,'',True]]))#for some reason it takes '' as True and disregards the extra
    ids.append(dict(label='Change 1',
        args=['visible',[False]]))#As if you set them all to false

    vis=[True]*len(listofnames)
    ids.append(dict(label='All',args=['visible',vis]))
    for nam in listofnames:
        visList=[False]*len(listofnames)
        visList[counter]=True
        ids.append(dict(label='%s' % (nam),
            args=['visible',visList]))
        ids2.append(dict(label='%s' % (nam),
            args=['visible',visList]))
        datasets(nam,counter)
        counter+=1

    #for nam in listofnames:
    #    #visList[counter]=True
    #    datasets(nam,counter)
    #    ids.append(dict(label='%s' % (nam),
    #        args=[ dict(visible=True, **graphData[counter]) ]))
    #    counter+=1

def datasets(nam,num):
    global graphData
    query = ddw.query('government/us-baby-names-by-yob',
                      '''SELECT * FROM `babyNamesUSYOB-mostpopular.csv/babyNamesUSYOB-mostpopular`
                                WHERE Name = "{}"'''.format(nam))
    df = query.dataframe
    numdf=[i for i in df['Number']]
    yeardf=[i for i in df['YearOfBirth']]
    graphData.append(
        Scatter(y=numdf,x=yeardf,line=Line(color='red'),name='%s' % (nam)))

#For readability
def layoutFormat():
    layout = Layout(
        title='Simple Graph',
        annotations=[dict(text='Change data set',
                          font=dict(size=18, color='#000000'),
                          x=-0.19, y=0.85,
                          xref='paper', yref='paper',
                          showarrow=False)
        ],
        updatemenus=list([
            dict(x=-0.1, y=0.7,
                 yanchor='middle',
                 bgcolor='c7c7c7',
                 buttons=list(ids)),
            dict(x=-0.1,y=.1,
            	yanchor='middle',
                 bgcolor='c7c7c7',
                 buttons=list(ids2))
        ]),
    )
    return layout

if False:# An atempt at buttons
	shape1 = {
	            'type': 'circle',
	            'xref': 'x', 'yref': 'y',
	            'x0': 0, 'y0': 0, 'x1': 1, 'y1': 1,
	            'line': {'color': 'rgb(0, 0, 255)'}
	        }
	shape2 = {
	            'type': 'circle',
	            'xref': 'x', 'yref': 'y',
	            'x0': 0, 'y0': 0, 'x1': 0.5, 'y1': 0.5,
	            'line': {'color': 'rgb(255, 0, 255)'}
	        }
	
	trace0 = plotly.graph_objs.Scatter(
	    x= [0.2, 0.2, 0.3, 0.4, 0.2],
	    y= [0.2, 0.5, 0.8, 0.3, 0.2]
	)
	
	data = plotly.graph_objs.Data([trace0])
	layout = plotly.graph_objs.Layout(shapes=[shape1, shape2])
	fig = plotly.graph_objs.Figure(data=data, layout=layout)
	fig['layout']['shapes'].append(dict(visible=True, **shape1))
	fig['layout']['shapes'].append(dict(visible=True, **shape2))
	
	
	fig['layout']['updatemenus'] = [dict(
	        x=-0.05, y=0.8,
	        buttons=[
	            dict(args=['shapes.visible', [False, True]], label='Hide big - does not work', method='relayout'),
	            dict(args=['shapes.visible', [True, False]], label='Hide small - does not work', method='relayout'),
	            dict(args=['shapes[0].visible', False], label='Hide big - might work', method='relayout'),
	            dict(args=['shapes[1].visible', False], label='Hide small - might work', method='relayout'),
	            dict(args=['shapes[0].visible', True], label='Show big', method='relayout'),
	            dict(args=['shapes[1].visible', True], label='Show small', method='relayout'),
	            dict(args=['shapes', [dict(visible=True, **shape1), dict(visible=True, **shape2)]], label='Show all', method='relayout'),
	            dict(args=['shapes', [dict(visible=False, **shape1), dict(visible=False, **shape2)]], label='Hide all', method='relayout'),
	            dict(args=['shapes', [dict(visible=True, **shape1), dict(visible=False, **shape2)]], label='Show big, hide small', method='relayout'),
	            dict(args=['shapes', [dict(visible=False, **shape1), dict(visible=True, **shape2)]], label='Hide big, show small', method='relayout')
	        ]
	    )]

#Using plotly to take the data and make the graph and using flask to display it to the screen 
@app.route('/')
def form():
    global names
    graphingSetup(names)
    layout=layoutFormat()
    data=Data(graphData)
    fig = Figure(data=data, layout=layout)
    my_plot_div = plot(fig, output_type='div')
    return render_template('test.html',div_placeholder=Markup(my_plot_div))

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')