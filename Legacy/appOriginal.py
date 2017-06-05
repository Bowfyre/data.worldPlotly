#This is the original file
import os
from io import BytesIO

# use matplotlib with the "Agg" backend for PNG generation, works on a "headless" server without
# some of the interactive UI libraries you'd expect on a personal machine
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.style as mstyle

# use the datadotworld python library to connect to data.world
from datadotworld.config import EnvConfig
from datadotworld.datadotworld import DataDotWorld

#use flask to run our web app
from flask import Flask, request, redirect, render_template, make_response

# create the Flask application
app = Flask(__name__)

# style the image
mstyle.use('fivethirtyeight')

# load the data.world API token from an environment variable
currently using my token directly in the code 
ddw = DataDotWorld(config=EnvConfig())

# grab and sort the list of all distinct names from the dataset
distinct_names_query = ddw.query('government/us-baby-names-by-yob',
                  ''' SELECT DISTINCT Name
                        FROM `babyNamesUSYOB-mostpopular.csv/babyNamesUSYOB-mostpopular`''')
names = sorted([x["Name"] for x in distinct_names_query.table])

# define the versus method to take the array of names
def versus(names):
    query = ddw.query('government/us-baby-names-by-yob',
                      '''SELECT * FROM `babyNamesUSYOB-mostpopular.csv/babyNamesUSYOB-mostpopular`
                                WHERE Name = "{}" OR Name = "{}" '''.format(*names))
    df = query.dataframe
    names = [i.lower() for i in names]
    nn = df.set_index('Name')
    nn.index = nn.index.str.lower()
    nn = nn.loc[names, ['YearOfBirth', 'Number']].reset_index()
    nn = nn.groupby(['Name', 'YearOfBirth']).agg('sum').unstack('Name')
    # create plot
    fig, ax = plt.subplots(figsize=(15, 7))
    nn.plot(ax=ax)
    plt.title('Name Popularity by Year', fontsize=20)
    plt.legend(title='', labels=sorted(names), fontsize='x-large')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Year of Birth', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    # save the fig into a BytesIO object as a png and return the PNG bytes
    output = BytesIO()
    fig.savefig(output, format='png')
    return output.getvalue()

# generate an image comparing names a and b over time
@app.route('/compare/<a>_vs_<b>.png', methods=['GET'])
def count(a, b):
    output = versus([a, b])
    response = make_response(output)
    response.mimetype = 'image/png'
    return response

# show the web form to generate image URLs
@app.route('/', methods=['GET'])
def form():
    return render_template("index.html", names=names)

# handle the form post and redirect to the image
@app.route('/', methods=['POST'])
def home():
    return redirect("/compare/{}_vs_{}.png".format(request.form['a'], request.form['b']))

@app.errorhandler(Exception)
def all_exception_handler(error):
    print(error)
    return error, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(debug=False, port=port, host='0.0.0.0')