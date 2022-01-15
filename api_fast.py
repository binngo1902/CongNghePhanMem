from fastapi import FastAPI,HTTPException, status, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector as mysql
import json
from datetime import datetime,timedelta
# from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
# from passlib.context import CryptContext
from mysql.connector import MySQLConnection,Error
import uvicorn
fake_user = {
    "username": "admin",
    "password": "123"
}


# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class Login(BaseModel):
#     email : str
#     password : str


class Course(BaseModel):
    id : str
    course_name : str
    teacher_id : str
    grade : int

# class CheckExist(BaseModel):
#     email : str

class RegisterAccount(BaseModel):
    username: str
    email: str
    password: str

class hanghoa(BaseModel):
    id:str 
    ten_hang_hoa: str 
    so_luong: int
class list_hanghoa(BaseModel):
    danhsach: List[hanghoa]
def connect():
    db_config = {
        'host' : 'localhost',
        'database': 'cnpm',
        'user': 'root',
        'password' : ''
    }

    try:
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            return conn
    except Error as err:
        print(err)
    return conn

db = connect()
cursor = db.cursor()
# cursor.execute('Select * from course')
# databases = cursor.fetchall()
# print(databases)

app = FastAPI()



@app.get('/hanghoa')
async def show_hanghoa():
    cursor.execute('Select * from hanghoa')
    hanghoa_table = cursor.fetchall()
    data_hanghoa = {}
    data_hanghoa['hanghoa'] = []
    for i in hanghoa_table:
       data_hanghoa['hanghoa'].append(i)
    return data_hanghoa

@app.get('/course')
async def show_course():
    cursor.execute('Select * from course')
    course = cursor.fetchall()
    data_full = {}
    data_full['Course'] = []
    for i in course:
        data = {}
        data['id'] = i[0]
        data['course_name'] = i[1]
        data['teacher_id'] = i[2]
        data['grade'] = i[3]
        data_full['Course'].append(data)
    return data_full

   
@app.delete('/courses/{course_id}')
async def delete_course(course_id: str):
    cursor.execute('Select * from course where ID ="'+course_id+'"')
    course = cursor.fetchall()
    if len(course) == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    cursor.execute('Delete from course where ID = "'+course_id+'"')
    db.commit()
    return {"Delete Succeed "+course_id}
        

@app.post('/hanghoa')
async def insert_hanghoa(list: list_hanghoa):
    try:
        sql = "INSERT INTO hanghoa Values (%s,%s,%s) "
        sql2 = "UPDATE hanghoa Set so_luong = %s WHERE id = %s"
        for i in list.danhsach:
            cursor.execute('Select * from hanghoa where id="'+i.id+'"')
            exist_hang = cursor.fetchone()
            print(len(exist_hang))
            if (exist_hang):
                
                value = (i.so_luong+exist_hang[2],i.id)
                print(value)
                cursor.execute(sql2,value)
            else:
                value = (i.id,i.ten_hang_hoa,i.so_luong)
                cursor.execute(sql,value)
        db.commit()
        return {"Notify": 1}
    except Exception as e:
        db.rollback()
        return {"Notify": e}
      

@app.get('/update')
async def check_update():
    dic = {
        "version" : "1.1",
        "link_update" : "https://codeload.github.com/fogleman/Minecraft/zip/master"
    }
    return dic

if __name__ == "__main__":
    print('oke')
    uvicorn.run("api_fast:app",host="localhost",reload=True)