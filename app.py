import os
from flask import Flask, render_template, Markup
from plotly.offline import plot

from plotly.graph_objs import *

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
names=names[1:10]

#Global Variables

ids=[]
graphData=[]

#this should take the list of all the names and adds to 'ids' and 'graphData'
def graphingSetup (listofnames):
    global ids
    counter=0
    visList=[True]*len(listofnames)
    ids.append(dict(label='All',
        args=['visible',visList]))

    visList=[False]*len(listofnames)
    for nam in listofnames:
        visList[counter]=True
        ids.append(dict(label='%s' % (nam),
            args=['visible',visList],method='restyle'))
        visList[counter]=False
        datasets(nam,counter)
        counter+=1

#TODO: This is probably very inefficent because it has to query each time.
#I've been trying to work out how to avoid this but I don't have enough experience with either the dataframes or the data.world api to figure it out yet
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
        ]),
    )
    return layout

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