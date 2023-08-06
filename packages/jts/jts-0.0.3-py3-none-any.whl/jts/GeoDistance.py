from math import radians, cos, sin, asin, sqrt

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

