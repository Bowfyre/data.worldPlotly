from flask import Flask, render_template, Markup
from plotly.offline import plot

from plotly.graph_objs import *

app = Flask(__name__)
app.debug = True

if True: #So I can shrink it
	a=[1,5,10]
	b=[5,10,1]
	c=[10,1,5]
	datasets=[a,b,c]	
	sets=[]
	con=0
	ids=[]
	default=[False]*len(datasets)
	for i in datasets:
		default[con]=True
		ids.append(dict(label="Graph %s" % (con),args=['visible',default]))
		sets.append(
			Scatter(y=i,line=Line(color='red'),name=con)
		)
		con+=1
		default=[False]*len(datasets)
	data = Data(sets)
	
	layout = Layout(
	)

@app.route('/')
def test():
	fig = Figure(data=data, layout=layout)
	my_plot_div = plot(fig, output_type='div')
	return render_template('test.html',
                           div_placeholder=Markup(my_plot_div)
                          )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)