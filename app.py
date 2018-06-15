from flask import Flask, render_template, request
import quandl
from bokeh.plotting import figure, show, output_file
import pandas as pd
from bokeh.palettes import Spectral4
from bokeh.embed import components

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/graph')
def generate_plot(ticker_name, value_choices, df):
    df['date'] = pd.to_datetime(df['date'])
    p = figure(plot_width=800, plot_height=600, x_axis_type="datetime")
    p.xaxis.axis_label = 'date'
    for choice, color in zip(value_choices, Spectral4):
        p.line(df['date'], df[choice], color=color, alpha=0.8,
               line_width=2.5, legend=ticker_name+": "+choice)
    show(p)
    script, div = components(p)
    return render_template('graph.html', script=script, div=div, ticker_name=ticker_name)

@app.route('/index', methods=['POST'])
def get_data_from_quandl():
    ticker_name = request.form["ticker"]
    value_choices = request.form.getlist("features")
    if ticker_name is None or value_choices is None:
        return
    quandl.ApiConfig.api_key = 'rSYiMRCK6UBqXxsLTqL-'
    df = quandl.get_table('WIKI/PRICES',
                          qopts={'columns': ['ticker', 'date', 'close', 'adj_close', 'open', 'adj_open']},
                          ticker=[ticker_name],
                          date={'gte': '2017-01-01', 'lte': '2017-12-31'})
    return generate_plot(ticker_name, value_choices, df)



if __name__ == '__main__':
    app.run(port=33507)
