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


    def insert_hanghoa(self,json):
        print(json)
        api_hanghoa = "/hanghoa"
        endpoint = f"{self.url}{api_hanghoa}"
        res = requests.post(endpoint,data=json)
        if res.ok == True:
            return res.json()['Notify']
        else:
            return "error request"


    def user_profile(self,token): # get profile user
        a= 0
        api_show = f"/api/show/profile?secret={self.secret_key}"
        headers = {"Authorization": f"Bearer {token}"}
        endpoint = f"{self.url}{api_show}"
        res = requests.post(endpoint,headers = headers)
        if (hasattr(res, 'json')):
            return res.json()
        else:
            return False

        
        

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