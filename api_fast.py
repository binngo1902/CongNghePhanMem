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


class hanghoa(BaseModel):
    id:str 
    ten_hang_hoa: str 
    so_luong: int
class sell_hanghoa(BaseModel):
    id:str 
    ten_hang_hoa: str 
    so_luong: int
    gia_tien: int
class list_hanghoa(BaseModel):
    danhsach: List[hanghoa]
class order(BaseModel):
    danhsach: List[sell_hanghoa]
    khach_hang: str
    thanh_toan:str
    tong_tien: int
    tong_sanpham:int

class update(BaseModel):
    id_hoadon: int
    status_vanchuyen: int
    status_thanhtoan: int
    flag_xuatkho: int 
    flag_thanhtoan: int
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

@app.get('/doanhthu')
async def doanhthu(date):
    cursor.execute('SELECT * FROM hoadon WHERE created_at BETWEEN 01/01/2022 AND 01/31/2022')
    result = cursor.fetchall()
    return result

@app.post('/hoadon/update')
async def update_hoadon(update: update):
    # try:
    sql1 = 'Select ct.id_hanghoa, ct.so_luong from chitiet_hoadon as ct where id_hoadon = %s '
    sql2 = "UPDATE hanghoa Set so_luong = %s WHERE id = %s"
    print("123",update.flag_thanhtoan)
    if (update.flag_xuatkho == 0):
        if(update.status_vanchuyen == 0):
            # print(update.status_vanchuyen,update.id_hoadon)
            sql ='UPDATE hoadon SET status_vanchuyen = %s,flag_xuatkho = %s WHERE id = %s'
            value = (update.status_vanchuyen,'0',update.id_hoadon)
            cursor.execute(sql,value)
            db.commit()
            value1 = (update.id_hoadon,)
            cursor.execute(sql1,value1)
            update_ = cursor.fetchall()
            for i in update_:
                cursor.execute('Select * from hanghoa where id="'+i[0]+'"')
                hanghoa = cursor.fetchone()
                value2 = (hanghoa[2]-i[1],i[0])
                print(value2)
                cursor.execute(sql2,value2)
            db.commit()
        elif(update.status_vanchuyen !=0):
            sql ='UPDATE hoadon SET status_vanchuyen = %s,flag_xuatkho = %s WHERE id = %s'
            value = (update.status_vanchuyen,1,update.id_hoadon)
            cursor.execute(sql,value)
            db.commit()
            print("ok123",value)
            value1 = (update.id_hoadon,)
            cursor.execute(sql1,value1)
            update_ = cursor.fetchall()
            for i in update_:
                cursor.execute('Select * from hanghoa where id="'+i[0]+'"')
                hanghoa = cursor.fetchone()
                value2 = (hanghoa[2]-i[1],i[0])
                print(value2)
                cursor.execute(sql2,value2)
            db.commit()
    elif (update.flag_xuatkho==1):
        if (update.status_vanchuyen == 0):
            sql ='UPDATE hoadon SET status_vanchuyen = %s,flag_xuatkho = %s WHERE id = %s'
            value = (update.status_vanchuyen,'0',update.id_hoadon)
            cursor.execute(sql,value)
            print("!@312312")
            db.commit()
            value1 = (update.id_hoadon,)
            cursor.execute(sql1,value1)
            update_ = cursor.fetchall()
            for i in update_:
                cursor.execute('Select * from hanghoa where id="'+i[0]+'"')
                hanghoa = cursor.fetchone()
                value2 = (hanghoa[2]+i[1],i[0])
                print(value2)
                cursor.execute(sql2,value2)
        else:
            sql ='UPDATE hoadon SET status_vanchuyen = %s,flag_xuatkho = %s WHERE id = %s'
            value = (update.status_vanchuyen,'1',update.id_hoadon)
            cursor.execute(sql,value)
            db.commit()


    if (update.flag_thanhtoan == 0):
        if (update.status_thanhtoan == 1):
            sql4 = 'UPDATE hoadon SET status_thanhtoan = %s,flag_thanhtoan = %s WHERE id = %s'
            value4 = (update.status_thanhtoan,'1',update.id_hoadon)
            cursor.execute(sql4,value4) 
            db.commit()
    elif (update.flag_thanhtoan == 1):
        if (update.status_thanhtoan == 0):
            sql4 = 'UPDATE hoadon SET status_thanhtoan = %s,flag_thanhtoan = %s WHERE id = %s'
            value4 = (update.status_thanhtoan,'0',update.id_hoadon)
            cursor.execute(sql4,value4) 
            db.commit()
    return {"Notify": "Cập nhật thành công"}
                # sql2 = 'UPDATE hanghoa SET so_luong = %s WHERE id in (SELECT id fro')
    # except Exception as e:
    #     db.rollback()
    #     return {"Notify": e}

@app.get('/hoadon')
async def show_hoadon():
    cursor.execute('Select id,id_daily,tong_tien,tong_sanpham,thanh_toan,status_vanchuyen,status_thanhtoan,created_at from hoadon')
    hoadon_table = cursor.fetchall()
    data_hoadon = {}
    data_hoadon['hoadon'] = []
    for i in hoadon_table:
        i = list(i)
        if i[5] == 0:
            i[5] = "Mới tạo"
        elif i[5] == 1:
            i[5] = "Xuất kho"
        elif i[5] == 2:
            i[5] = "Đã giao"
        if i[6] == 0:
            i[6] = "Chưa thanh toán"
        elif i[6] == 1:
            i[6] =="Đã thanh toán"
        data_hoadon['hoadon'].append(i)
    print(data_hoadon)
    return data_hoadon

@app.get('/chitiet/{id}')
async def show_chitiet(id:int):
    cursor.execute('Select hd.id,dl.ten_daily,hd.tong_tien,hd.tong_sanpham,hd.thanh_toan,hd.status_vanchuyen,hd.status_thanhtoan,hd.flag_xuatkho,hd.flag_thanhtoan  from hoadon as hd,daily as dl where hd.id = "'+str(id)+'" and hd.id_daily = dl.id')
    chitiet_table1 = cursor.fetchone()
    cursor.execute('Select ct.id_hanghoa, hh.ten_hang_hoa,ct.so_luong,ct.gia_tien from chitiet_hoadon as ct,hanghoa as hh where ct.id_hoadon = "'+str(id)+'" and ct.id_hanghoa = hh.id')
    chitiet_table2 = cursor.fetchall()
    return {"table1":chitiet_table1,"table2":chitiet_table2}


@app.post('/hanghoa')
async def insert_hanghoa(list: list_hanghoa):
    try:
        sql = "INSERT INTO hanghoa Values (%s,%s,%s) "
        sql2 = "UPDATE hanghoa Set so_luong = %s WHERE id = %s"
        print(list)
        for i in list.danhsach:
            print(i)
            cursor.execute('Select * from hanghoa where id="'+i.id+'"')
            exist_hang = cursor.fetchone()
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
        print(e)
        db.rollback()
        return {"Notify": e}
      
@app.post('/kiemtra')
async def check_hanghoa(order: order):
    try:
        error = ""
        for i in order.danhsach:
            cursor.execute('Select * from hanghoa where id="'+i.id+'"')
            exist_item = cursor.fetchone()
            if (exist_item):
                if exist_item[2] < i.so_luong:
                    error += str(i.id)+'-'+i.ten_hang_hoa+' không đủ hàng ( chỉ còn '+str(exist_item[2])+' sản phẩm )\n'
            else:
                error += 'Không tồn tại sản phẩm '+i.ten_hang_hoa+'-'+i.id+'\n'
        if error == "":
            return {"Notify": 1}
        else:
            return {"Notify": error}
    except Exception as e:
        print(e)
        return {"Notify": e}

      
@app.post('/dathang')
async def order_hanghoa(order: order):
    try:
        # kiểm tra đại lý tồn tại hay chưa
        cursor.execute('SELECT * FROM daily WHERE ten_daily="'+order.khach_hang+'"')
        exist_khachhang = cursor.fetchone()

        if not (exist_khachhang): # chưa tồn tại thêm mới
            sql  = 'INSERT INTO daily (ten_daily) Values (%s) '
            value = (order.khach_hang,) # thêm dấu phẩy để tạo kiểu tuple
            cursor.execute(sql,value)
        # lấy id đại lý
        cursor.execute('SELECT id FROM daily WHERE ten_daily="'+order.khach_hang+'"')
        id_khachhang = cursor.fetchone()[0]
        # tạo hóa đơn
        sql1 = 'INSERT INTO hoadon (id_daily,tong_tien,tong_sanpham,thanh_toan,status_vanchuyen,status_thanhtoan) Values (%s,%s,%s,%s,%s,%s)'
        if order.thanh_toan == "Chuyển khoản":
            status_thanhtoan = 1
        else:
            status_thanhtoan = 0

        value1 = (id_khachhang,order.tong_tien,order.tong_sanpham,order.thanh_toan,0,status_thanhtoan)

        cursor.execute(sql1,value1)
        
        # lấy id hóa đơn
        sql2 = 'Select id from hoadon where id_daily= %s and tong_tien = %s and tong_sanpham = %s and thanh_toan = %s and status_vanchuyen = %s and status_thanhtoan = %s'
        value2 = (id_khachhang,order.tong_tien,order.tong_sanpham,order.thanh_toan,0,status_thanhtoan)
        cursor.execute(sql2,value2)
        id_hoadon = cursor.fetchone()[0]
        # thêm hàng vào chi tiết hóa đơn
        sql3 = "INSERT INTO chitiet_hoadon (id_hanghoa,id_hoadon,so_luong,gia_tien) Values (%s,%s,%s,%s)"
        for i in order.danhsach:
            value3 = (i.id,id_hoadon,i.so_luong,i.gia_tien)
            cursor.execute(sql3,value3)
        db.commit()
        return {"Notify": 1}
    except Exception as e:
        db.rollback()
        print(e)
        return {"Notify": e}


if __name__ == "__main__":
    print('oke')
    uvicorn.run("api_fast:app",host="localhost",reload=True)