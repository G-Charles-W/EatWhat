import requests
import urllib
import hashlib
import pandas as pd


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


if __name__ == '__main__':
    # get_nearby_cater()
    df = pd.read_csv(r'D:\Projects\EatWhat\APIs\BaiduLocation\NearbyCater.csv')
    import numpy as np
    choice = np.random.choice(len(df), 1)
    breakpoint()