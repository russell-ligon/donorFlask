#####DONORSCHOOSE FUNCTIONS
import pandas as pd
import numpy as np

import datetime
from datetime import timedelta, date #for time duration calculations
from dateutil.parser import parse #for fuzzy finding year


def fixer(scaler,grd_boost4_model,
    dateDF2,total_price_excluding_optional_support,
    primary_focus_category,state_you_live,students_reached,
    resource_type,grade_level,school_metro,school_poverty):

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
    circlx=dateDF2.iloc[0,0]
    circly=dateDF2.iloc[0,1]
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
    funding100 = round(100*round(FundedFast[0][1],3),2) #times funded out of 100

    ###############################
    ###############################
    ###############################
    ###############################

    predictlist=[]
    listcopy=insertlist

    for index, row in dateDF2.iterrows():
        listcopy[2]=row['circlx']
        listcopy[3]=row['circly']
        valuearray=np.array([listcopy])
        valuearray=scaler.transform(valuearray)
        FundedFastFuture = grd_boost4_model.predict_proba((valuearray.reshape(1, -1)))
        predictlist.append(round(FundedFastFuture[0][1],4))

    dateDF2['probsuccess']=predictlist

    predictlistdrop15=[]
    for index, row in dateDF2.iterrows():
        listcopy[1]=total_price_excluding_optional_support*.75
        listcopy[2]=row['circlx']
        listcopy[3]=row['circly']
        valuearray=np.array([listcopy])
        valuearray=scaler.transform(valuearray)
        FundedFastFuture = grd_boost4_model.predict_proba((valuearray.reshape(1, -1)))
        predictlistdrop15.append(round(FundedFastFuture[0][1],4))

    dateDF2['drop25prob']=predictlistdrop15

    predictlistplus15=[]
    for index, row in dateDF2.iterrows():
        listcopy[1]=total_price_excluding_optional_support*1.25
        listcopy[2]=row['circlx']
        listcopy[3]=row['circly']
        valuearray=np.array([listcopy])
        valuearray=scaler.transform(valuearray)
        FundedFastFuture = grd_boost4_model.predict_proba((valuearray.reshape(1, -1)))
        predictlistplus15.append(round(FundedFastFuture[0][1],4))

    dateDF2['plus25prob']=predictlistplus15




    resources=['Books','Other','Supplies','Technology','Trips','Visitors']
    defaultresource = resources.index(resource_type)
    startresource = resources.index(resource_type) + 88 #find default resource type
    listcopy[startresource]=0 #and set it to zero
    rind=0

    toptwo=[]


    for rt in range(88,94): #loop through different resources, skip if de
        predictlistnewresource1=[]
        nameofresource=resources[rind]

        if rind!=defaultresource:
            for index, row in dateDF2.iterrows():
                listcopy[1]=total_price_excluding_optional_support
                listcopy[2]=row['circlx']
                listcopy[3]=row['circly']
                listcopy[rt]=1

                valuearray=np.array([listcopy])
                valuearray=scaler.transform(valuearray)
                FundedFastFuture = grd_boost4_model.predict_proba((valuearray.reshape(1, -1)))
                predictlistnewresource1.append(round(FundedFastFuture[0][1],4))
                listcopy[rt]=0#reset resource

            dateDF2[nameofresource]=predictlistnewresource1

        rind+=1





    return(fundingstring,funding100,dateDF2)














def elapseddays(posted, completed):
    formatuse = '%Y-%m-%d %H:%M:%S' # The format: see down this page:https://docs.python.org/3/library/datetime.html
    otherformat = '%Y-%m-%d'

    try:
        elapsed_days=completed-posted
    except:
        try:
            elapsed_days = datetime.datetime.strptime(completed,formatuse)-datetime.datetime.strptime(posted,formatuse)
        except:
            try:
                elapsed_days = datetime.datetime.strptime(completed,otherformat)-datetime.datetime.strptime(posted,otherformat)
            except:
                elapsed_days = 'error'


    return(elapsed_days)

def elapsedseconds(posted, completed):

    formatuse = '%Y-%m-%d %H:%M:%S' # The format: see down this page:https://docs.python.org/3/library/datetime.html
    otherformat = '%Y-%m-%d'

    if isinstance(posted, datetime.datetime) or (type(posted) is pd.Timestamp):
        clock = completed
    else:
        try:
            clock = datetime.datetime.strptime(completed,formatuse)
        except:
            clock = datetime.datetime.strptime(completed,otherformat)

    if isinstance(completed, datetime.datetime) or (type(completed) is pd.Timestamp):
        startclock = completed
    else:
        try:
            startclock = datetime.datetime.strptime(posted,formatuse)
        except:
            startclock = datetime.datetime.strptime(posted,otherformat)

    elapsed = (clock-startclock).total_seconds()

    return(elapsed)


intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

# Function convert seconds into day.decimal
def ConvertSectoDay(n):
    day = n // (24 * 3600)
    #print(day) #keep day
    n = n % (24 * 3600)
    daydec=(n/86400) # add this to day
    addem=day+daydec
    #https://stackoverflow.com/a/48812729/1602288
    holder='{:g}'.format(float('{:.{p}g}'.format(addem, p=5)))
    return(float(holder))

def projectover(posted, completed,expiration):
    formatuse = '%Y-%m-%d %H:%M:%S' # The format: see down this page:https://docs.python.org/3/library/datetime.html
    otherformat = '%Y-%m-%d'

    #failed projects were never completed, so in those cases, use the expiration date
    # if variable is None:
    if completed is None:
        try:
            clock = datetime.datetime.strptime(expiration,formatuse)
        except:
            try:
                clock = datetime.datetime.strptime(expiration,otherformat)
            except:
                clock = datetime.datetime.strptime('1900-01-01',otherformat)
    else:
        try:
            clock = datetime.datetime.strptime(completed,formatuse)
        except:
            try:
                clock = datetime.datetime.strptime(completed,otherformat)
            except:
                clock = datetime.datetime.strptime('1900-01-01',otherformat)

    return(clock)

def makedate(posted):
    formatuse = '%Y-%m-%d %H:%M:%S' # The format: see down this page:https://docs.python.org/3/library/datetime.html
    otherformat = '%Y-%m-%d'

    try:
        clock = datetime.datetime.strptime(posted,formatuse)
    except:
        try:
            clock = datetime.datetime.strptime(posted,otherformat)
        except:
            clock = datetime.datetime.strptime('1900-01-01',otherformat)

    return(clock)

def Convert_to_clock_x(m):
    m=int(m)
    if m == 1:
        a = 1
    if m == 2:
        a = 2
    if m == 3:
        a = 3
    if m == 4:
        a = 2
    if m == 5:
        a = 1
    if m == 6:
        a = 0
    if m == 7:
        a = -1
    if m == 8:
        a = -2
    if m == 9:
        a = -3
    if m == 10:
        a = -2
    if m == 11:
        a = -1
    if m == 12:
        a = 0
    return(a)

def Convert_to_clock_y(m):
    m=int(m)
    if m == 1:
        a = 2
    if m == 2:
        a = 1
    if m == 3:
        a = 0
    if m == 4:
        a = -1
    if m == 5:
        a = -2
    if m == 6:
        a = -3
    if m == 7:
        a = -2
    if m == 8:
        a = -1
    if m == 9:
        a = 0
    if m == 10:
        a = 1
    if m == 11:
        a = 2
    if m == 12:
        a = 3
    return(a)

import matplotlib.pyplot as plt
import seaborn as sns

#function for producing nice, smoothed line plots sorted by categorical variable, of a continues (var_dist) variable
def comp_dist(df_to_use, cat_to_subset, var_dist, figw,figh,linew):
    plt.figure(figsize=(figw,figh))
    sns.set_context( rc={"lines.linewidth": linew})

    for grp in sorted(df_to_use[cat_to_subset].unique()):
        grp_df = df_to_use.loc[df_to_use[cat_to_subset] == grp]

        sns.distplot(grp_df[var_dist], hist=False, label=grp)
        plt.xlim(0, 90)
    plt.show()

import math

def getxy(day):
    x = math.sin((180 - day * 0.9849521203830369)/180 * 3.141)
    y = math.cos((180 - day * 0.9849521203830369)/180 * 3.141)
    return x, y
