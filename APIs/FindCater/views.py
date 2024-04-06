import os.path
import os
from django.shortcuts import render
from django.http import HttpResponse
# from utils import get_nearby_cater
from .utils import get_nearby_cater, return_image, random_dish
import numpy as np
import pandas as pd
from django.http import JsonResponse, FileResponse
from .models import Dish
from django.conf import settings
from django.views.static import serve
# Create your views here.


def index(request):
    lat = float(request.GET.get('lat', default='31.229602'))
    lng = float(request.GET.get('lng', default='121.540706'))
    # df = get_nearby_cater(float(lat), float(lng))
    # df = pd.read_csv(r'D:\Projects\EatWhat\APIs\BaiduLocation\NearbyCater.csv')
    # choice = np.random.choice(len(df), 1)
    data = random_dish(request, lat, lng)
    print(f'data:{data}')

    return FileResponse(open(data, 'rb'), content_type='image/png')
