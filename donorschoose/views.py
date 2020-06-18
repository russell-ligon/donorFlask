from flask import render_template
from flask import request
from donorschoose import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from donorschoose.a_Model import *
################################################################
import pickle #for saving output files, pickles
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
####################
import requests
import json
url="https://www.donorschoose.org/common/json_feed.html?showFacetCounts=true&APIKey=H9v7hCeN&max=10&index=0"
r = requests.get(url)
dataj = json.loads(r.text)
current_active_proposals = int(dataj['totalProposals'])
##########################################################################
import plotly
import plotly.graph_objs as go
import json

############################
with open('/home/russell/Documents/GitHub/DonorBooster/testscripts/simplified_logistic_regression_scaler.pkl', 'rb') as handle:
    scaler = pickle.load(handle)

#don_num is a dictionary with key:value --> project id: # of donors
with open('/home/russell/Documents/GitHub/DonorBooster/testscripts/simplified_logistic_regression_model.pkl', 'rb') as handle:
    logistic_regression = pickle.load(handle)






def create_line_plot():

    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/')
@app.route('/index')
def index():

    liney = create_line_plot()

    return render_template("index.html",
    title = 'Home', user = { 'nickname': 'Miguel' }, plot = liney)

# @app.route('/db')
# def birth_page():
#    sql_query = """
#                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean'
#                """
#    query_results = pd.read_sql_query(sql_query,con)
#    births = ""
#    for i in range(0,10):
#        births += query_results.iloc[i]['birth_month']
#        births += "<br>"
#    return births

# @app.route('/db_fancy')
# def cesareans_page_fancy():
#    sql_query = """
#               SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
#                """
#    query_results=pd.read_sql_query(sql_query,con)
#    births = []
#    for i in range(0,query_results.shape[0]):
#        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
#    return render_template('cesareans.html',births=births)

@app.route('/input')
def cesareans_input():
    c_a_p = current_active_proposals
    return render_template("input.html", CURRACT = c_a_p)


# @app.route('/output')
# def cesareans_output():
#    return render_template("output.html")


@app.route('/output', methods=['POST'])
def output():

    #projHook = request.form.get('projHook')
    #projHook = [projHook]

    totalPrice = request.form.get('totalPrice')
    totalPrice = float(totalPrice)

    #now_active = request.form.get('now_active')
    #now_active = int(now_active)
    now_active = current_active_proposals


    if request.method=='POST':

        result=request.form
        resource_type = result['resource']
        primary_focus_category = result['category']
        school_metro = result['metrop']
        good_month = result['month']

        #is it a good month?
        # if good_month == 'yup':
        #     goodmonth = 1
        # else:
        #     goodmonth = 0
        #######
        #Is the school in a metro area?
        if school_metro == 'metro':
            school_metro_urban = 1
        else:
            school_metro_urban = 0

        #######
        #What is the subject area?
        if primary_focus_category == 'HW':
            primary_focus_HW = 1
            primary_focus_Nut = 0
        elif primary_focus_category == 'Nut':
            primary_focus_HW = 0
            primary_focus_Nut = 1
        else:
            primary_focus_HW = 0
            primary_focus_Nut = 0
        ################
        #What are the resources requested?
        if resource_type == 'trip':
            resource_type_Trip = 1
            resource_type_Tech = 0
            resource_type_Book = 0
        elif resource_type == 'tech':
            resource_type_Trip = 0
            resource_type_Tech = 1
            resource_type_Book = 0
        elif resource_type == 'book':
            resource_type_Trip = 0
            resource_type_Tech = 0
            resource_type_Book = 1
        else:
            resource_type_Trip = 0
            resource_type_Tech = 0
            resource_type_Book = 0

        ####################################

        valuearray=np.array([[now_active,totalPrice,goodmonth,school_metro_urban,primary_focus_HW,
                primary_focus_Nut,resource_type_Trip,resource_type_Tech,resource_type_Book]])

        valuearray=scaler.transform(valuearray)

        FundedFast = logistic_regression.predict_proba((valuearray.reshape(1, -1)))

        fundingstring = str(round(FundedFast[0][1],3))
        funding100 = round(100*round(FundedFast[0][1],3),3)
        ###############################
        ###############################
        ###############################
        ###############################
        alternative_dict = {}

        #all possible resources
        resource_options=['trip','tech','book','otherresource']
        #remove the resource selected by the user
        resource_options.remove(resource_type)

        for r in resource_options:
            if r == 'trip':
                #tech instead
                resource_type_Trip = 1
                resource_type_Tech = 0
                resource_type_Book = 0
            if r == 'tech':
                resource_type_Trip = 0
                resource_type_Tech = 1
                resource_type_Book = 0
            if r == 'book':
                resource_type_Trip = 0
                resource_type_Tech = 0
                resource_type_Book = 1
            if r == 'otherresource':
                resource_type_Trip = 0
                resource_type_Tech = 0
                resource_type_Book = 0

            resource_instead=np.array([[now_active,totalPrice,goodmonth,school_metro_urban,primary_focus_HW,
                        primary_focus_Nut,resource_type_Trip,resource_type_Tech,resource_type_Book]])
            resource_instead=scaler.transform(resource_instead)
            ResourceMod = logistic_regression.predict_proba((resource_instead.reshape(1, -1)))

            alternative_dict[r]=round(ResourceMod[0][1],3)






    else:
        error = 'Method was not POST'




    return render_template("output.html", the_result = fundingstring, hundo = funding100, additional_opportunities = alternative_dict)

if __name__ == '__main__':
    app.run()
