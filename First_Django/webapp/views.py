import json,random
from dimaag.handler import handle
from django.shortcuts import render
from django.http import HttpResponse

HAND = handle()
# Create your views here.

def about(request):
    #return HttpResponse("<H2>Hi this page is called about</H2>")
    return render(request, 'about.html')


def IOT_data(request):
    categories = list()
    voltage = list()
    current = list()


    for x in range(50):
        dataw = HAND.get_data()
        categories.append(dataw['timestamp'])
        voltage.append(dataw['voltage'])
        current.append(dataw['current'])

    voltage = {
        'name': 'voltage',
        'data': voltage,
        'color': 'orange'
    }
    current = {
        'name': 'current',
        'data': current,
        'color': 'red'
    }
    date = HAND.get_data()
    chart = {
        'chart': {'type': 'spline','animation': 'Highcharts.svg','marginRight':'10'},
        'title': {'text': '(SDM120 ENERGY METER) DATE -:'+str(date['datestamp'])},
        'xAxis': {'categories': categories},
        'series': [voltage, current]
    }

    dump = json.dumps(chart)
    #dump1 = json.dumps(chart)
    return render(request,'index.html',{'chart': dump})#'chart1':dump1})