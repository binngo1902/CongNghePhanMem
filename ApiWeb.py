import requests
import pprint
import json
from kivy.app import App

class ApiWeb():
    url = "http://localhost:8000"
    def get_hanghoa(self):
        api_hanghoa = "/hanghoa"
        endpoint = f"{self.url}{api_hanghoa}"
        res = requests.get(endpoint)
        print(res.ok)
        return res.json()['hanghoa']

    def get_hoadon(self):
        api_hoadon = "/hoadon"
        endpoint = f"{self.url}{api_hoadon}"
        res = requests.get(endpoint)
        print(res.ok)
        return res.json()['hoadon']

    def get_chitiet(self,id):
        api_hoadon = f"/chitiet/{id}"
        endpoint = f"{self.url}{api_hoadon}"
        res = requests.get(endpoint)
        print(res.ok)
        return res.json()

    def insert_hanghoa(self,json):
        print(json)
        api_hanghoa = "/hanghoa"
        endpoint = f"{self.url}{api_hanghoa}"
        res = requests.post(endpoint,data=json)
        if res.ok == True:
            return res.json()['Notify']
        else:
            return "error request"


    def update_hoadon(self,id_hoadon,status_vanchuyen,status_thanhtoan,flag_xuatkho,flag_thanhtoan):
        api_hanghoa = "/hoadon/update"
        endpoint = f"{self.url}{api_hanghoa}"
        data = {
            'id_hoadon': id_hoadon,
            'status_vanchuyen': int(status_vanchuyen),
            'status_thanhtoan': int(status_thanhtoan),
            'flag_xuatkho': flag_xuatkho,
            'flag_thanhtoan': flag_thanhtoan }
        print(data)
        res = requests.post(endpoint,data=json.dumps(data))
        if res.ok == True:
            return res.json()['Notify']
        else:
            return "error request"

    def check_hanghoa(self,json):
        api_hanghoa = "/kiemtra"
        endpoint = f"{self.url}{api_hanghoa}"
        res = requests.post(endpoint,data=json)
        if res.ok == True:
            return res.json()['Notify']
        else:
            return "error request"

    def order_hanghoa(self,json):
        api_hanghoa = "/dathang"
        endpoint = f"{self.url}{api_hanghoa}"
        res = requests.post(endpoint,data=json)
        if res.ok == True:
            return res.json()['Notify']
        else:
            return "error request"


        
        

    def logout(self,token): # api logout
        api_logout = '/api/logout'
        headers = {"Authorization": f"Bearer {token}"}
        endpoint = f"{self.url}{api_logout}"
        res = requests.post(endpoint,headers = headers)
        if res.ok == True:
            with open(self.file,'w') as f:
                f.write('')


    def all_zoom(self,token): # test render course
        api_zoom = f'/api/zoom?secret={self.secret_key}'
        endpoint= f"{self.url}{api_zoom}"

        res = requests.get(endpoint)
        return res.json()['meeting']

    def all_courses(self,token):
        api_course = f'/api/course?secret={self.secret_key}'
        endpoint = f"{self.url}{api_course}"
        res = requests.get(endpoint)
        return res.json()['course']