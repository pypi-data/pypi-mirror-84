import requests


class POI:
    def __init__(self):
        self.url = 'http://datahub.wtf/api/'
    
    def get_pois(lon,lat,page=1,page_size=10):
        resp = requests.get(self.url+'/MapPoiRouter/getPoiList?page={}&pageSize={}&lon={}&lat={}'.format(page,page_size,lon,lat))
        return resp.json()