from flask import render_template
from flask import request
from donorschoose import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import donorschoose.a_Model as DonorsChooseFunx
################################################################
import datetime
from datetime import date

today = date.today()
day_of_year = today.timetuple().tm_yday #get day of year

list_o_days=[]
list_o_day_coords=[]
j=0

if (day_of_year+90) <= 364:
    for d in range(day_of_year,day_of_year+91):
        list_o_days.append(d)
        list_o_day_coords.append(DonorsChooseFunx.getxy(d))

else:
    for d in range(day_of_year,day_of_year+91):
        if d<=364:
            list_o_days.append(d)
            list_o_day_coords.append(DonorsChooseFunx.getxy(d))
        else:
            list_o_days.append(j)
            list_o_day_coords.append(DonorsChooseFunx.getxy(j))
            j += 1

dateDF = pd.DataFrame(list_o_day_coords,columns=['circlx','circly'])
dateDF['dayOFyear']=list_o_days
dateDF.astype({'dayOFyear':'int'}).dtypes
dateDF['calendardate']=dateDF.apply(lambda row: (datetime.datetime.strptime('{} {}'.format(int(row['dayOFyear']), today.year),'%j %Y')),axis=1)


################################################
import pickle #for saving output files, pickles
import joblib
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
############################
with open('/home/russell/Documents/GitHub/donorFlask/donorschoose/static/grd_boost4_model.pkl', 'rb') as handle:
    grd_boost4_model = joblib.load(handle)

#don_num is a dictionary with key:value --> project id: # of donors
with open('/home/russell/Documents/GitHub/donorFlask/donorschoose/static/thorough_modeleval_scaler.pkl', 'rb') as handle:
    scaler = joblib.load(handle)





@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
    title = 'Home', user = { 'nickname': 'Miguel' })



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
    total_price_excluding_optional_support = float(totalPrice)


    state_you_live = request.form.get('state')


    students_reached = request.form.get('numstudents')
    students_reached = int(students_reached)
    #now_active = request.form.get('now_active')
    #now_active = int(now_active)
    #now_active = current_active_proposals


    if request.method=='POST':

        result=request.form
        primary_focus_category = result['category']
        resource_type = result['resource']
        grade_level = result['grade']
        school_metro = result['metrop']
        school_poverty = result['poverty']

        #DEFAULTS
        primary_focus_subject_AppliedSciences = 0
        primary_focus_subject_CharacterEducation = 0
        primary_focus_subject_Civics_Government = 0
        primary_focus_subject_College_CareerPrep = 0
        primary_focus_subject_CommunityService = 0
        primary_focus_subject_ESL = 0
        primary_focus_subject_EarlyDevelopment = 0
        primary_focus_subject_Economics = 0
        primary_focus_subject_EnvironmentalScience = 0
        primary_focus_subject_Extracurricular = 0
        primary_focus_subject_FinancialLiteracy = 0
        primary_focus_subject_ForeignLanguages = 0
        primary_focus_subject_Gym_Fitness = 0
        primary_focus_subject_Health_LifeScience = 0
        primary_focus_subject_Health_Wellness = 0
        primary_focus_subject_History_Geography = 0
        primary_focus_subject_Literacy = 0
        primary_focus_subject_Literature_Writing = 0
        primary_focus_subject_Mathematics = 0
        primary_focus_subject_Music = 0
        primary_focus_subject_Nutrition = 0
        primary_focus_subject_Other = 0
        primary_focus_subject_ParentInvolvement = 0
        primary_focus_subject_PerformingArts = 0
        primary_focus_subject_SocialSciences = 0
        primary_focus_subject_SpecialNeeds = 0
        primary_focus_subject_Sports = 0
        primary_focus_subject_TeamSports = 0
        primary_focus_subject_VisualArts = 0

        resource_type_Books = 0
        resource_type_Other = 0
        resource_type_Supplies = 0
        resource_type_Technology = 0
        resource_type_Trips = 0
        resource_type_Visitors = 0

        grade_level_Grades3_5 = 0
        grade_level_Grades6_8 = 0
        grade_level_Grades9_12 = 0
        grade_level_GradesPreK_2 = 0

        school_metro_none = 0
        school_metro_rural = 0
        school_metro_suburban = 0
        school_metro_urban = 0

        poverty_level_high = 0
        poverty_level_highest = 0
        poverty_level_low = 0
        poverty_level_minimal = 0
        poverty_level_moderate = 0
        poverty_level_unknown = 0

        #######################
        #Then use user input decides which one is 'active'
        if primary_focus_category == "AppliedSciences":
            primary_focus_subject_AppliedSciences = 1
        if primary_focus_category == "CharacterEducation":
            primary_focus_subject_CharacterEducation = 1
        if primary_focus_category == "Civics_Government":
            primary_focus_subject_Civics_Government = 1
        if primary_focus_category == "College_CareerPrep":
            primary_focus_subject_College_CareerPrep = 1
        if primary_focus_category == "CommunityService":
            primary_focus_subject_CommunityService = 1
        if primary_focus_category == "ESL":
            primary_focus_subject_ESL = 1
        if primary_focus_category == "EarlyDevelopment":
            primary_focus_subject_EarlyDevelopment = 1
        if primary_focus_category == "Economics":
            primary_focus_subject_Economics = 1
        if primary_focus_category == "EnvironmentalScience":
            primary_focus_subject_EnvironmentalScience = 1
        if primary_focus_category == "Extracurricular":
            primary_focus_subject_Extracurricular = 1
        if primary_focus_category == "FinancialLiteracy":
            primary_focus_subject_FinancialLiteracy = 1
        if primary_focus_category == "ForeignLanguages":
            primary_focus_subject_ForeignLanguages = 1
        if primary_focus_category == "Gym_Fitness":
            primary_focus_subject_Gym_Fitness = 1
        if primary_focus_category == "Health_LifeScience":
            primary_focus_subject_Health_LifeScience = 1
        if primary_focus_category == "Health_Wellness":
            primary_focus_subject_Health_Wellness = 1
        if primary_focus_category == "History_Geography":
            primary_focus_subject_History_Geography = 1
        if primary_focus_category == "Literacy":
            primary_focus_subject_Literacy = 1
        if primary_focus_category == "Literature_Writing":
            primary_focus_subject_Literature_Writing = 1
        if primary_focus_category == "Mathematics":
            primary_focus_subject_Mathematics = 1
        if primary_focus_category == "Music":
            primary_focus_subject_Music = 1
        if primary_focus_category == "Nutrition":
            primary_focus_subject_Nutrition = 1
        if primary_focus_category == "Other":
            primary_focus_subject_Other = 1
        if primary_focus_category == "ParentInvolvement":
            primary_focus_subject_ParentInvolvement = 1
        if primary_focus_category == "PerformingArts":
            primary_focus_subject_PerformingArts = 1
        if primary_focus_category == "SocialSciences":
            primary_focus_subject_SocialSciences = 1
        if primary_focus_category == "SpecialNeeds":
            primary_focus_subject_SpecialNeeds = 1
        if primary_focus_category == "Sports":
            primary_focus_subject_Sports = 1
        if primary_focus_category == "TeamSports":
            primary_focus_subject_TeamSports = 1
        if primary_focus_category == "VisualArts":
            primary_focus_subject_VisualArts = 1

        #######################
        #What resources being requested
        if resource_type == "Books":
            resource_type_Books = 1
        if resource_type == "Other":
            resource_type_Other = 1
        if resource_type == "Supplies":
            resource_type_Supplies = 1
        if resource_type == "Technology":
            resource_type_Technology = 1
        if resource_type == "Trips":
            resource_type_Trips = 1
        if resource_type == "Visitors":
            resource_type_Visitors = 1
        #######################
        #What grade level?
        if grade_level == 'pk2':
            grade_level_GradesPreK_2 = 1
        if grade_level == 'g35':
            grade_level_Grades3_5 = 1
        if grade_level == 'g68':
            grade_level_Grades6_8 = 1
        if grade_level == 'g912':
            grade_level_Grades9_12 = 1
        #######################
        #Is the school in a metro area?
        if school_metro == 'metro':
            school_metro_urban = 1
        if school_metro == 'suburban':
            school_metro_suburban = 1
        if school_metro == 'rural':
            school_metro_rural = 1
        if school_metro == 'other':
            school_metro_none = 1
        #######################
        #What is the school's poverty level?
        if school_poverty == 'highest':
            poverty_level_highest = 1
        if school_poverty == 'high':
            poverty_level_high = 1
        if school_poverty == 'moderate':
            poverty_level_moderate = 1
        if school_poverty == 'low':
            poverty_level_low = 1
        if school_poverty == 'minimal':
            poverty_level_minimal = 1
        if school_poverty == 'unknown':
            poverty_level_unknown = 1
        #######
        circlx=dateDF.iloc[0,0]
        circly=dateDF.iloc[0,1]
        ####################################
        scst=['school_state_AK', 'school_state_AL','school_state_AR',
                 'school_state_AZ',
                 'school_state_CA',
                 'school_state_CO',
                 'school_state_CT',
                 'school_state_DC',
                 'school_state_DE',
                 'school_state_FL',
                 'school_state_GA',
                 'school_state_HI',
                 'school_state_IA',
                 'school_state_ID',
                 'school_state_IL',
                 'school_state_IN',
                 'school_state_KS',
                 'school_state_KY',
                 'school_state_LA',
                 'school_state_MA',
                 'school_state_MD',
                 'school_state_ME',
                 'school_state_MI',
                 'school_state_MN',
                 'school_state_MO',
                 'school_state_MS',
                 'school_state_MT',
                 'school_state_NC',
                 'school_state_ND',
                 'school_state_NE',
                 'school_state_NH',
                 'school_state_NJ',
                 'school_state_NM',
                 'school_state_NV',
                 'school_state_NY',
                 'school_state_OH',
                 'school_state_OK',
                 'school_state_OR',
                 'school_state_PA',
                 'school_state_RI',
                 'school_state_SC',
                 'school_state_SD',
                 'school_state_TN',
                 'school_state_TX',
                 'school_state_UT',
                 'school_state_VA',
                 'school_state_VT',
                 'school_state_WA',
                 'school_state_WI',
                 'school_state_WV',
                 'school_state_WY']

        school_state = dict()
        for s in scst:
            if state_you_live in s:
                school_state[s] = 1
            else:
                school_state[s] = 0
        ####################################
        startingvals = [students_reached,total_price_excluding_optional_support,
                        circlx,circly]
        for key, value in school_state.items():
            startingvals.append(value)

        insertlist=startingvals+[school_metro_none,
        school_metro_rural,
        school_metro_suburban,
        school_metro_urban,
        primary_focus_subject_AppliedSciences,
        primary_focus_subject_CharacterEducation,
        primary_focus_subject_Civics_Government,
        primary_focus_subject_College_CareerPrep,
        primary_focus_subject_CommunityService,
        primary_focus_subject_ESL,
        primary_focus_subject_EarlyDevelopment,
        primary_focus_subject_Economics,
        primary_focus_subject_EnvironmentalScience,
        primary_focus_subject_Extracurricular,
        primary_focus_subject_FinancialLiteracy,
        primary_focus_subject_ForeignLanguages,
        primary_focus_subject_Gym_Fitness,
        primary_focus_subject_Health_LifeScience,
        primary_focus_subject_Health_Wellness,
        primary_focus_subject_History_Geography,
        primary_focus_subject_Literacy,
        primary_focus_subject_Literature_Writing,
        primary_focus_subject_Mathematics,
        primary_focus_subject_Music,
        primary_focus_subject_Nutrition,
        primary_focus_subject_Other,
        primary_focus_subject_ParentInvolvement,
        primary_focus_subject_PerformingArts,
        primary_focus_subject_SocialSciences,
        primary_focus_subject_SpecialNeeds,
        primary_focus_subject_Sports,
        primary_focus_subject_TeamSports,
        primary_focus_subject_VisualArts,
        resource_type_Books,
        resource_type_Other,
        resource_type_Supplies,
        resource_type_Technology,
        resource_type_Trips,
        resource_type_Visitors,
        poverty_level_high,
        poverty_level_highest,
        poverty_level_low,
        poverty_level_minimal,
        poverty_level_moderate,
        poverty_level_unknown,
        grade_level_Grades3_5,
        grade_level_Grades6_8,
        grade_level_Grades9_12,
        grade_level_GradesPreK_2]
        #################################
        valuearray=np.array([insertlist])

        valuearray=scaler.transform(valuearray)

        FundedFast = grd_boost4_model.predict_proba((valuearray.reshape(1, -1)))

        fundingstring = str(round(FundedFast[0][1],3))
        funding100 = round(100*round(FundedFast[0][1],3),3) #times funded out of 100
        ###############################
        ###############################
        ###############################
        ###############################
        alternative_dict = {}










    else:
        error = 'Method was not POST'


    return render_template("output.html", the_result = fundingstring,
    hundo = funding100, additional_opportunities = alternative_dict)

if __name__ == '__main__':
    app.run()
