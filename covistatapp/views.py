import json
from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime as dt


def indexview(request):
    url=requests.get('https://data.covid19india.org/v4/min/timeseries.min.json')
    json_data=url.json()

    user_input_state=''
    user_input_date_from='2020-03-26'
    user_input_date_to='2021-10-31'
    user_data_type=''
    user_required_type=''
    if request.method == 'POST': 
        user_input_state=request.POST.get('state') 
        user_input_date_from=request.POST['date_from']
        user_input_date_to=request.POST['date_to']
        user_data_type=request.POST.get('data_period') #cumulative or daily
        user_required_type=request.POST.get('required_type') #confirmed, recovered.....
        #To store dates list
    start_date =user_input_date_from
    end_date = user_input_date_to
    start_date_object = dt.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_date_object = dt.datetime.strptime(end_date,"%Y-%m-%d").date()
    days = end_date_object - start_date_object
    dates=[]
    otp=[]
    for i in range(days.days+1):
        dates.append(str(start_date_object+dt.timedelta(days=i)))
    
    for i in dates:
        try:
            otp.append(json_data[user_input_state]['dates'][i][user_data_type][user_required_type])
        except KeyError:
            otp.append(0)

    chart_list = [list(a) for a in zip(dates,otp)]
    #chart_list.insert(0,['Dates','Values'])
    chart_list_json=json.dumps(chart_list)
    user_input_state_json=json.dumps(user_input_state)
    user_required_type_json=json.dumps(user_required_type)
    dict_pass={
        'dates':dates,
        'otp':otp,
        'chart_list':chart_list,
        'chart_list_json':chart_list_json,
        'user_input_state_json':user_input_state_json,
        'user_required_type_json':user_required_type_json
        }
    return render(request,'index.html',dict_pass)
    

