#####DONORSCHOOSE FUNCTIONS

import datetime
from datetime import timedelta, date #for time duration calculations
from dateutil.parser import parse #for fuzzy finding year




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
