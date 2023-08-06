# -*- coding: utf-8 -*-
# @ Description: 地理工具箱
# @ Contributor: https://github.com/wandergis/coordTransform_py
# @ Date: 2020-05-13 12: 46:00
# @ LastEditTime: 2020-8-5 10:05:11
# @ LastEditors: Li Jing
import math
import csv
import xlrd
from math import radians, cos, sin, asin, sqrt

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

def geodistance(lng1,lat1,lng2,lat2):
    """
    公式计算两点间距离（km）
    
    geodistance(111.79144963446,36.942999626245,111.79302778935,36.944967978826)
    
    :param lng1: 经度1
    :param lat1: 纬度1
    :param lng2: 经度2
    :param lat2: 纬度2
    :return: 两点间距离（km）
    """

    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=distance/1000
    return distance
    
def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    
    :param lng: 火星坐标经度
    :param lat: 火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德 
    
    :param bd_lat: 百度坐标纬度
    :param bd_lon: 百度坐标经度
    :return: 转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
     
    :param lng: WGS84坐标系的经度
    :param lat: WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84  
    
    :param lng: 火星坐标系的经度
    :param lat: 火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    
    :param lng:
    :param lat:
    :return:
    """
    return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)


def Converter(howtohow, infile, col_lng, col_lat, outfile, header):
    """
    坐标转换主程序
    jts.Converter(jts.gcj02_to_bd09,r'1.xlsx',1,2,r'2.csv',1)  
    
    :param howtohow:    gcj02_to_bd09
                        gcj02_to_bd09
                        bd09_to_gcj02
                        wgs84_to_gcj02
                        gcj02_to_wgs84
                        bd09_to_wgs84
                        wgs84_to_bd09
    :param infile:      输入文件
    :param col_lng:     经度所在的列
    :param col_lat:     纬度所在的列
    :param outfile:     输出文件  
    :param header:      表头标志位，有表头就是1 没有就是0
    :return:            XX.csv
    """
    # 读取数据
    alldata = xlrd.open_workbook(infile)
    table = alldata.sheets()[0] # 读取的sheet表为第0+1个
    lngall = table.col_values(col_lng - 1)[0:len(table.col_values(col_lng - 1))]
    latall = table.col_values(col_lat - 1)[0:len(table.col_values(col_lat - 1))]
    lng = []
    lat = []
    for i in range(header, len(lngall)):
        temp = howtohow(lngall[i], latall[i])
        lng.append(temp[0])
        lat.append(temp[1])
    data = []
    for i in range(len(lng)):
        data.append([lng[i], lat[i]])
    csvfile = open(outfile, 'w')
    writer = csv.writer(csvfile, lineterminator='\n')
    writer.writerow(['longitude', 'latitude'])
    writer.writerows(data)
    csvfile.close()


