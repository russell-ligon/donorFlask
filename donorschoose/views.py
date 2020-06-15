from flask import render_template
from flask import request
from donorschoose import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from donorschoose.a_Model import ModelIt
################################################################
import pickle #for saving output files, pickles
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

##########################################################################
with open('/home/russell/Documents/GitHub/DonorBooster/testscripts/simplified_logistic_regression_scaler.pkl', 'rb') as handle:
    scaler = pickle.load(handle)

#don_num is a dictionary with key:value --> project id: # of donors
with open('/home/russell/Documents/GitHub/DonorBooster/testscripts/simplified_logistic_regression_model.pkl', 'rb') as handle:
    logistic_regression = pickle.load(handle)



# Python code to connect to Postgres
# You may need to modify this based on your OS,
# as detailed in the postgres dev setup materials.
# user = 'russell' #add your Postgres username here
# host = 'localhost'
# dbname = 'birth_db'

#######################################

#read in 'cleantrailer.pickle' from 'trailer_cleaning_inspection.ipynb'
#the resulting file, which we call 'trailers' is a list (of lists) in format for text analysis
# with open('/home/russell/Documents/DataScience/DonorsChoose/Data/trailers.pickle', 'rb') as handle:
#     trailers = pickle.load(handle)

#don_num is a dictionary with key:value --> project id: # of donors
# with open('/home/russell/Documents/DataScience/DonorsChoose/Data/donor_num.pickle', 'rb') as handle:
#     don_num = pickle.load(handle)

# trailers = list(trailers.values())
# #takes all *values* from _don_num_ dictionary, puts them in a list, then, turns all items in the list to int
# donor_list = [int(i) for i in list(don_num.values())]
#
# labels=[0, 1, 2]
# donor_categ = pd.cut(donor_list,bins=[0,2.9,8,1000],labels=labels, include_lowest=True)
#
# labels = donor_categ
#
# texts = trailers
#
# rest_texts, test_texts, rest_labels, test_labels = train_test_split(texts,
#                                                                     labels,
#                                                                     test_size=0.1,
#                                                                     random_state=1)
# train_texts, dev_texts, train_labels, dev_labels = train_test_split(rest_texts,
#                                                                     rest_labels,
#                                                                     test_size=0.1,
#                                                                     random_state=1)


# target_names = list(set(labels))
# label2idx = {label: idx for idx, label in enumerate(target_names)}
# train_labels = pd.Series(train_labels.astype('int')).rename("rating")
# print(type(train_labels))
# print(train_labels)



# pipeline = Pipeline([
#     ('vect', CountVectorizer()),
#     ('tfidf', TfidfTransformer()),
#     ('lr', LogisticRegression(multi_class="ovr", solver="lbfgs"))
# ])
#
# parameters = {'lr__C': [0.1, 0.5, 1, 2, 5, 10, 100, 1000]}
#
# best_classifier = GridSearchCV(pipeline, parameters, cv=5, verbose=0)
#
# best_classifier.fit(train_texts, train_labels)


##########################################
# db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
# con = None
# con = psycopg2.connect(database = dbname, user = user)

@app.route('/')
@app.route('/index')
def index():
   return render_template("index.html",
      title = 'Home', user = { 'nickname': 'Miguel' },
      )

# @app.route('/db')
# def birth_page():
#    sql_query = """
#                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean';
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
   return render_template("input.html")

# @app.route('/output')
# def cesareans_output():
#    return render_template("output.html")


@app.route('/output', methods=['POST','GET'])
def cesareans_output():

    projHook = request.args.get('projHook')
    projHook = [projHook]

    totalPrice = request.args.get('totalPrice')
    totalPrice = float(totalPrice)

    now_active = request.args.get('now_active')
    now_active = int(now_active)




    if request.method=='POST':

        for aKey in request.form:
            if aKey == 'resource':
                resource_type = request.form[aKey]
            if aKey == 'category':
                primary_focus_category = request.form[aKey]
            if aKey == 'metrop':
                school_metro = request.form[aKey]
            if aKey == 'month':
                good_month = request.form[aKey]

        # result=request.form
        # resource_type = result['resource']
        # primary_focus_category = result['category']
        # school_metro = result['metrop']
        # good_month = result['month']

        #is it a good month?
        if good_month == 'yup':
            goodmonth = 1
        else:
            goodmonth = 0
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

        fundingstring = "Likelihood of getting funded with 3 weeks of posting = "+str(FundedFast[0][1])
    else:
        error = 'Method was not POST'

    return render_template("output.html", the_result = fundingstring)
