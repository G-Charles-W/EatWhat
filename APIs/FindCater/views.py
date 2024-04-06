from django.shortcuts import render
from django.http import HttpResponse
# from utils import get_nearby_cater
from .utils import get_nearby_cater, return_image
import numpy as np
import pandas as pd
from django.http import JsonResponse, FileResponse
from .models import Dish


# Create your views here.


def index(request):
    lat = float(request.GET.get('lat', default='31.229602'))
    lng = float(request.GET.get('lng', default='121.540706'))
    # df = get_nearby_cater(float(lat), float(lng))
    # df = pd.read_csv(r'D:\Projects\EatWhat\APIs\BaiduLocation\NearbyCater.csv')
    # choice = np.random.choice(len(df), 1)
    data = return_image(lat, lng, 20)
    # print(f'choice:{choice}')
    # return HttpResponse(df.loc[choice]['name'])
    dishes = Dish.objects.all()
    for dish in dishes:
        dish_img = dish.image.url
    return FileResponse(open(dish_img, 'rb'), content_type='image/jfif')
