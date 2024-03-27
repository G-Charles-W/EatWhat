from django.shortcuts import render
from django.http import HttpResponse
# from utils import get_nearby_cater
from .utils import get_nearby_cater
import numpy as np
import pandas as pd
# Create your views here.


def index(request):
    lat = float(request.GET.get('lat', default='31.229602'))
    lng = float(request.GET.get('lng', default='121.540706'))
    df = get_nearby_cater(float(lat), float(lng))
    # df = pd.read_csv(r'D:\Projects\EatWhat\APIs\BaiduLocation\NearbyCater.csv')
    choice = np.random.choice(len(df), 1)
    # print(f'choice:{choice}')
    return HttpResponse(df.loc[choice]['name'])
