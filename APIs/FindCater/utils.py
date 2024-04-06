import requests
import urllib
import hashlib
import pandas as pd
from .models import Restaurant, Dish
import random
import os
from django.conf import settings

class BaiduMapConfig:

    def __init__(self, lat=31.23, lng=121.539, page_num=0):
        self.host = "https://api.map.baidu.com"
        self.uri = "/place/v2/search"
        self.ak = "6383llGMRDZwFUKXn6tpMAj1wCLV6LLa"
        self.sk = "YjGvH37AFeONJu2ulGwuUC1ScC0ygW74"
        self.params = {"query": "饭店",
                       "location": f"{lat},{lng}",
                       "radius": "2500",
                       "scope": "2",
                       "output": "json",
                       "ak": self.ak,
                       "page_size": "20",
                       "industry_type": "cater",
                       "page_num": str(page_num)}

    def generate_request(self):
        paramsArr = []
        for key in self.params:
            paramsArr.append(key + "=" + self.params[key])

        queryStr = self.uri + "?" + "&".join(paramsArr)

        encodedStr = urllib.request.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

        rawStr = encodedStr + self.sk
        sn = hashlib.md5(urllib.parse.quote_plus(rawStr).encode("utf8")).hexdigest()
        queryStr = queryStr + "&sn=" + sn
        url = self.host + queryStr
        return url

    @staticmethod
    def send_request(url):
        response = requests.get(url)
        if response:
            print(response.json())
        return response.json()


class CaterMsgParser:

    def __init__(self, msg_list):
        self.msg_list = msg_list
        self.df = pd.DataFrame(columns=['name', 'lat', 'lng', 'address', 'label'])

    def parse_msg(self):
        total_index = 0
        for msg in self.msg_list:
            status = msg['message']
            assert status == 'ok'

            results = msg['results']

            for i in range(len(results)):
                print(results[i])
                name = results[i]['name']
                lat = results[i]['location']['lat']
                lng = results[i]['location']['lng']
                address = results[i]['address']
                label = results[i]['detail_info']['label']
                self.df.loc[total_index] = [name, lat, lng, address, label]
                total_index += 1
            print(self.df)
        # self.df.to_csv('NearbyCater.csv')
        return self.df


def get_nearby_cater(lat_=31.23, lgt_=121.539):
    baiduMap = BaiduMapConfig(lat_, lgt_)
    msg = baiduMap.send_request(baiduMap.generate_request())
    total = msg['total']
    msg_list = [msg]
    if total > 20:
        times = total // 20

        for i in range(times):
            this_baiduMap = BaiduMapConfig(lat_, lgt_, 1 + i)
            msg = this_baiduMap.send_request(this_baiduMap.generate_request())
            msg_list.append(msg)
    parser = CaterMsgParser(msg_list)
    df = parser.parse_msg()
    return df


def return_image(lat, lng, radius=1):
    lat_min = lat - radius
    lat_max = lat + radius
    lng_max = lng + radius
    lng_min = lng - radius
    resturants = Restaurant.objects.filter(latitude__gte=lat_min, latitude__lte=lat_max)
    data = []
    for resturant in resturants:
        resturant_data = {
            'name': resturant.name,
            'latitude': resturant.latitude,
            'longtitude': resturant.longitude,
            'dishes': []
        }
        for dish in resturant.dish_set.all():
            dish_data = {
                'name': dish.name,
                'image_url': dish.image.url
            }
            resturant_data['dishes'].append(dish_data)
        data.append(resturant_data)
    return data


def random_dish(request, latitude, longitude):
    # 根据提供的经纬度坐标随机选择一家店铺
    restaurants = Restaurant.objects.all()
    random_restaurant = random.choice(restaurants)
    print(f'random_restaurant:{random_restaurant}')

    # 获取该店铺的所有菜品
    dishes = Dish.objects.filter(Restaurant=random_restaurant)
    if not dishes.exists():
        return None

        # 从店铺里面随机选择一道菜名
    random_dish = random.choice(dishes)

    print(f'random_dish:{random_dish}')
    return os.path.join(settings.BASE_DIR, random_dish.image.name)


if __name__ == '__main__':
    # get_nearby_cater()
    df = pd.read_csv(r'D:\Projects\EatWhat\APIs\BaiduLocation\NearbyCater.csv')
    import numpy as np

    choice = np.random.choice(len(df), 1)
    breakpoint()
