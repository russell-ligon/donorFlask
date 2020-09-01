from flask import render_template
from flask import request
from donorschoose import app
import pandas as pd
import psycopg2
import donorschoose.a_Model as DonorsChooseFunx
################################################################
import io
import base64
###############
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
########
import datetime
from datetime import date
from datetime import timedelta, date #for time duration calculations

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
# @app.route('/index')
# def index():
#     return render_template("index.html",
#     title = 'Home', user = { 'nickname': 'Miguel' })
#

@app.route('/input')
def cesareans_input():
    import requests
    import json
    url="https://www.donorschoose.org/common/json_feed.html?showFacetCounts=true&APIKey=H9v7hCeN&max=10&index=0"
    r = requests.get(url)
    dataj = json.loads(r.text)
    current_active_proposals = int(dataj['totalProposals'])
    c_a_p = current_active_proposals
    return render_template("input.html", CURRACT = c_a_p)


@app.route('/output', methods=['POST'])

def output():
    import datetime
    from datetime import date
    from datetime import timedelta, date #for time duration calculations
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

    #projHook = request.form.get('projHook')
    #projHook = [projHook]

    totalPrice = request.form.get('totalPrice')
    total_price_excluding_optional_support = float(totalPrice)


    state_you_live = request.form.get('state')


    students_reached = request.form.get('numstudents')
    students_reached = int(students_reached)



    if request.method=='POST':

        result=request.form
        primary_focus_category = result['category']
        resource_type = result['resource']
        grade_level = result['grade']
        school_metro = result['metrop']
        school_poverty = result['poverty']

        interestinglist=DonorsChooseFunx.fixer(scaler,grd_boost4_model,
        dateDF,total_price_excluding_optional_support,
        primary_focus_category,state_you_live,students_reached,
        resource_type,grade_level,school_metro,school_poverty)

        fundingstring = interestinglist[0]
        funding100 = interestinglist[1]
        dateDF3 = interestinglist[2]




        ##############################################################
        # create figure and axis objects with subplots()
        plt.rcParams["figure.figsize"] = (20,12)

        index_range=max(dateDF3["probsuccess"])-min(dateDF["probsuccess"])

        index_max = max(range(len(dateDF3["probsuccess"])), key=dateDF3["probsuccess"].__getitem__)

        try:
            if(len(index_max)>1):
                index_max=index_max[0]
        except:
            index_max=index_max



        # Generate plot
        fig = Figure()
        # axis = fig.add_subplot(1, 1, 1)
        # axis.set_title("title")
        # axis.set_xlabel("x-axis")
        # axis.set_ylabel("y-axis")
        # axis.grid()
        # axis.plot(range(5), range(5), "ro-")

        # create figure and axis objects with subplots()
        fig,ax = plt.subplots()
        # make a plot
        ax.plot(dateDF3.calendardate, dateDF3["probsuccess"],alpha=0.61,color="blue",marker="o")
        #set x-axis limits
        #ax.set_xlim(r[0],r[-1])
        #ax.set_ylim(0,1)
        ax.set_ylim(0,None)
        # set x-axis label
        ax.set_xlabel("Date",fontsize=30)
        # set y-axis label
        ax.set_ylabel("Probability of funding fast",color="blue",fontsize=30)

        ax.tick_params(axis='both', which='major', labelsize=20)
        plt.xticks(rotation=35)


        ax.annotate('Today', xy=(dateDF3["calendardate"][0],dateDF3["probsuccess"][0]),
                    xycoords='data',
                    xytext=(dateDF3["calendardate"][0]+timedelta(days=3),
                    dateDF3["probsuccess"][0]+index_range*.15),
                    size=13, ha='right', va="center",
                    bbox=dict(boxstyle="round", alpha=0.51,color='orange'),
                    arrowprops=dict(arrowstyle="wedge,tail_width=0.5", facecolor='orange',alpha=0.1))


        ax.annotate(('Best likelihood'+'\n'+str(dateDF3["calendardate"][index_max].date())), xy=(dateDF3["calendardate"][index_max],dateDF3["probsuccess"][index_max]),
                    xycoords='data',
                    xytext=(dateDF3["calendardate"][index_max]+timedelta(days=3),
                            dateDF3["probsuccess"][index_max]-index_range*.45),
                    size=13, ha='right', va="center",
                    bbox=dict(boxstyle="round", alpha=0.51,color='green'),
                    arrowprops=dict(arrowstyle="wedge,tail_width=0.5",facecolor='green',alpha=0.1))

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        ################################################################
        ########################################################
        ##############################################################
        # create figure and axis objects with subplots()
        plt.rcParams["figure.figsize"] = (20,12)

        index_range=max(dateDF3["probsuccess"])-min(dateDF["probsuccess"])

        index_max = max(range(len(dateDF3["probsuccess"])), key=dateDF3["probsuccess"].__getitem__)

        try:
            if(len(index_max)>1):
                index_max=index_max[0]
        except:
            index_max=index_max

        # Generate plot
        fig = Figure()
        # axis = fig.add_subplot(1, 1, 1)
        # axis.set_title("title")
        # axis.set_xlabel("x-axis")
        # axis.set_ylabel("y-axis")
        # axis.grid()
        # axis.plot(range(5), range(5), "ro-")

        # create figure and axis objects with subplots()
        fig,ax = plt.subplots()
        # make a plot
        ax.plot(dateDF.calendardate, dateDF["probsuccess"],alpha=0.61,
            color="blue",marker="o",label=('current request: $'+str(round(total_price_excluding_optional_support,3))))

        ax.plot(dateDF.calendardate, dateDF["drop25prob"],alpha=0.61,
                color="red",marker="o",
                label='reduced request (-25%): $'+str(round(total_price_excluding_optional_support*.75,3)))

        ax.plot(dateDF.calendardate, dateDF["plus25prob"],alpha=0.61,
            color="green",marker="o",
            label='increased request (+25%): $'+str(round(total_price_excluding_optional_support*1.25,3)))
        #set x-axis limits
        #ax.set_xlim(r[0],r[-1])
        ax.set_ylim(0,None)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, prop={"size":20},loc='lower left')


        # set x-axis label
        ax.set_xlabel("Date",fontsize=30)
        # set y-axis label
        ax.set_ylabel("Probability of funding fast",color="blue",fontsize=30)

        ax.tick_params(axis='both', which='major', labelsize=20)
        plt.xticks(rotation=35)


        ax.annotate('Today', xy=(dateDF3["calendardate"][0],dateDF3["probsuccess"][0]),
                    xycoords='data',
                    xytext=(dateDF3["calendardate"][0]+timedelta(days=3),
                    dateDF3["probsuccess"][0]+index_range*.15),
                    size=13, ha='right', va="center",
                    bbox=dict(boxstyle="round", alpha=0.51,color='orange'),
                    arrowprops=dict(arrowstyle="wedge,tail_width=0.5", facecolor='orange',alpha=0.1))


        # ax.annotate(('Best likelihood'+'\n'+str(dateDF3["calendardate"][index_max].date())), xy=(dateDF3["calendardate"][index_max],dateDF3["probsuccess"][index_max]),
        #             xycoords='data',
        #             xytext=(dateDF3["calendardate"][index_max]+timedelta(days=3),
        #                     dateDF3["probsuccess"][index_max]-index_range*.45),
        #             size=13, ha='right', va="center",
        #             bbox=dict(boxstyle="round", alpha=0.51,color='green'),
        #             arrowprops=dict(arrowstyle="wedge,tail_width=0.5",facecolor='green',alpha=0.1))

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64StringMONEY = "data:image/png;base64,"
        pngImageB64StringMONEY += base64.b64encode(pngImage.getvalue()).decode('utf8')

        ##################################################################################
        newrs = list(dateDF.iloc[:,7:].max().sort_values(ascending=False)[0:3].index)
        # create figure and axis objects with subplots()
        plt.rcParams["figure.figsize"] = (20,12)

        index_range=max(dateDF3["probsuccess"])-min(dateDF["probsuccess"])

        index_max = max(range(len(dateDF3["probsuccess"])), key=dateDF3["probsuccess"].__getitem__)

        try:
            if(len(index_max)>1):
                index_max=index_max[0]
        except:
            index_max=index_max

        # Generate plot
        fig = Figure()
        # axis = fig.add_subplot(1, 1, 1)
        # axis.set_title("title")
        # axis.set_xlabel("x-axis")
        # axis.set_ylabel("y-axis")
        # axis.grid()
        # axis.plot(range(5), range(5), "ro-")

        # create figure and axis objects with subplots()
        fig,ax = plt.subplots()
        # make a plot
        ax.plot(dateDF.calendardate, dateDF["probsuccess"],alpha=0.61,
                color="blue",marker="o",label=(str(resource_type)+"(current)"))
        ax.plot(dateDF.calendardate, dateDF[newrs[0]],alpha=0.61,
                color="red",marker="o",
                label=newrs[0])

        ax.plot(dateDF.calendardate, dateDF[newrs[1]],alpha=0.61,
                color="green",marker="o",
                label=newrs[1])
        ax.plot(dateDF.calendardate, dateDF[newrs[2]],alpha=0.61,
                color="orange",marker="o",
                label=newrs[2])

        ax.set_ylim(0,None)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, prop={"size":20},loc='lower left')

        # set x-axis label
        ax.set_xlabel("Date",fontsize=30)
        # set y-axis label
        ax.set_ylabel("Probability of funding fast",color="blue",fontsize=30)

        ax.tick_params(axis='both', which='major', labelsize=20)
        plt.xticks(rotation=35)


        ax.annotate('Today', xy=(dateDF3["calendardate"][0],dateDF3["probsuccess"][0]),
                    xycoords='data',
                    xytext=(dateDF3["calendardate"][0]+timedelta(days=3),
                    dateDF3["probsuccess"][0]+index_range*.15),
                    size=13, ha='right', va="center",
                    bbox=dict(boxstyle="round", alpha=0.51,color='orange'),
                    arrowprops=dict(arrowstyle="wedge,tail_width=0.5", facecolor='orange',alpha=0.1))


        # ax.annotate(('Best likelihood'+'\n'+str(dateDF3["calendardate"][index_max].date())), xy=(dateDF3["calendardate"][index_max],dateDF3["probsuccess"][index_max]),
        #             xycoords='data',
        #             xytext=(dateDF3["calendardate"][index_max]+timedelta(days=3),
        #                     dateDF3["probsuccess"][index_max]-index_range*.45),
        #             size=13, ha='right', va="center",
        #             bbox=dict(boxstyle="round", alpha=0.51,color='green'),
        #             arrowprops=dict(arrowstyle="wedge,tail_width=0.5",facecolor='green',alpha=0.1))

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64StringRES = "data:image/png;base64,"
        pngImageB64StringRES += base64.b64encode(pngImage.getvalue()).decode('utf8')


        ############################################





    else:
        error = 'Method was not POST'


    maxD=round(100*round(dateDF3["probsuccess"][index_max],3),3) #times funded out of 100
    maxdate = str(dateDF3["calendardate"][index_max].date())

    return render_template("output.html", the_result = fundingstring,
    hundo = funding100, maxdefault=maxD,maxDdate = maxdate,
    imagenow=pngImageB64String, alternativefunding = pngImageB64StringMONEY,
    alternativematerials=pngImageB64StringRES)

if __name__ == '__main__':
    app.run()
