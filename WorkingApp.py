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
	default=[True]*len(datasets)
	ids.append(dict(label="All" ,
		args=['visible',default]))
	default=[False]*len(datasets)
	for i in datasets:
		default[con]=True
		
		ids.append(dict(label="Graph %s" % (con),
			args=['visible',default
			]))

		sets.append(
			Scatter(y=i,line=Line(color='red'),
				name=con))
		con+=1
		default=[False]*len(datasets)
	data = Data(sets)
	
	layout = Layout(
	    title='Simple Graph',
	    annotations=[dict(text='Change data set',
	                      font=dict(size=18, color='#000000'),
	                      x=-0.19, y=0.85,
	                      xref='paper', yref='paper',
	                      showarrow=False)],
	    updatemenus=list([
	        dict(x=-0.1, y=0.7,
	             yanchor='middle',
	             bgcolor='c7c7c7',
	             buttons=list(ids)),
	    ]),
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