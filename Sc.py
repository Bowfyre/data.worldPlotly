import os
from io import BytesIO
from flask import Flask, render_template, Markup
from plotly.offline import plot
import pandas as pd
from plotly.graph_objs import *

# use the datadotworld python library to connect to data.world
from datadotworld.config import EnvConfig
from datadotworld.datadotworld import DataDotWorld

ddw = DataDotWorld(config=EnvConfig())
#ddw = DataDotWorld(config='eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJwcm9kLXVzZXItY2xpZW50OmJvd2Z5cmUiLCJpc3MiOiJhZ2VudDpib3dmeXJlOjpkN2NlYWQxNy0xN2E0LTRhMGYtYjg4MS1hNzZjZDA5MjBlYzAiLCJpYXQiOjE0OTM2NzU2NjYsInJvbGUiOlsidXNlcl9hcGlfd3JpdGUiLCJ1c2VyX2FwaV9yZWFkIl0sImdlbmVyYWwtcHVycG9zZSI6dHJ1ZX0.BNJwIEvf4bamLffbNYQdTohs1wcuU1XedFNI9QhmWgR9XxvDSs8tQMN449gFEqa6Og_pLn1qHlOeVuFgI5CoGw')


distinct_names_query = ddw.query('government/us-baby-names-by-yob',
                  ''' SELECT DISTINCT Name
                        FROM `babyNamesUSYOB-mostpopular.csv/babyNamesUSYOB-mostpopular`''')

names = sorted([x["Name"] for x in distinct_names_query.table])
names=names[1:10]
print names
counter=0
ids=[]
visList=[False]*len(names)
for n in names:
    visList[counter]=True
    print visList
    ids.append(dict(label='%s' % (n),
        args=['visible',visList]))
    visList[counter]=False
    #datasets(n,counter)
    counter+=1

#query = ddw.query('government/us-baby-names-by-yob',
#                      '''SELECT * FROM `babyNamesUSYOB-mostpopular.csv/babyNamesUSYOB-mostpopular`
#                                ''')
#
#df = query.dataframe
#print 'line 25'
##print df
#dfnum=[i for i in df['Number']]
##print dfnum
#names = [i.lower() for i in names]
#nn = df.set_index('Name')
#print 'Line 28'
#print nn
#nn.index = nn.index.str.lower()
#print 'Line 31'
##print nn
#nn = nn.loc[names, ['YearOfBirth', 'Number']].reset_index()
#print 'Line 34'
#print nn
#nn = nn.groupby(['Name', 'YearOfBirth']).agg('sum').unstack('Name')
#print 'Line 37'
##print nn







