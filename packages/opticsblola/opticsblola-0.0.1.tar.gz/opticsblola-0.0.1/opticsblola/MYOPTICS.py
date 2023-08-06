from sklearn.cluster import OPTICS
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import *
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'


def lonlat_distance(array1, array2):
    #'''
    #返回单位米，若要返回千米，半径取6371，米用6378137
    #array1, array2 list 分别为两对坐标
    #'''
    lon_1 = np.float64(array1[0])
    lat_1 = np.float64(array1[1])
    lon_2 = np.float64(array2[0])
    lat_2 = np.float64(array2[1])
    radlat1 = radians(lat_1)
    radlat2 = radians(lat_2)
    a = radlat1 - radlat2
    b = radians(lon_1) - radians(lon_2)
    s = 2 * asin(sqrt(pow(sin(a/2), 2) + cos(radlat1) * cos(radlat2) * pow(sin(b/2), 2)))
    earth_radius = 6371 
    s = s * earth_radius
    return s
    
def decide_minsample(df_lon_lat, maxeps, minsample_scale, low, up):
    #'''
    #df_lon_lat 二维坐标对DataFrame格式
    #minsample_scale [下限，上限，步长] 
    #maxeps 样本点邻居的最大涵盖半径
    #low/up 核心样本点邻居数量所满足的最小值low和最大值up(不包括)
    #'''
    mins = {}
    for minsamples in range(minsample_scale[0], minsample_scale[1], minsample_scale[2]):
        try:
            clust = OPTICS(min_samples = minsamples, max_eps = maxeps, xi = 0.5, metric = lonlat_distance).fit(df_lon_lat.iloc[:, :2])
        except ValueError:
            continue
        df_lon_lat['labels'] = clust.labels_
        ratio = len(df_lon_lat[df_lon_lat['labels'] != -1]) / len(df_lon_lat)
        if (ratio > low) and (ratio < up):
            mins[minsamples] = ratio
    return mins

class Myoptics:
    def __init__(self, df_lon_lat, minsamples, maxeps):
        self.data = df_lon_lat
        self.minsamples = minsamples
        self.maxeps = maxeps
        
    def my_optics(self):
        clust = OPTICS(min_samples = self.minsamples, max_eps = self.maxeps, xi = 0.5, metric = lonlat_distance).fit(self.data.iloc[:, :2])
        self.reachability = clust.reachability_[clust.ordering_] # clust.ordering_ 样本点聚类序号
        self.labels_ordering = clust.labels_[clust.ordering_]
        self.labels = clust.labels_
        return self  
        
# 样本点可达距离图
def reach_plot(df_lon_lat_labels_reachability_labelsordering, fsize = (16, 8)):
    da = df_lon_lat_labels_reachability_labelsordering
    L = len(set(da['labels']))
    total = len(da)
    ratio = len(da[da['labels'] != -1]) / total
    
    plt.figure(figsize = fsize)
    space = np.arange(total)
    for klass in range(0, L):
        xk = space[da['labels_ordering'] == klass]
        rk = da['reachability'][da['labels_ordering'] == klass]
        plt.scatter(xk, rk, alpha = 0.5)
    xk_outer = space[da['labels_ordering'] == -1]
    rk_outer = da['reachability'][da['labels_ordering'] == -1]
    plt.plot(xk_outer, rk_outer, 'k.', alpha = 0.5, marker = 10)
    plt.ylabel('Reachability(eps)')
    plt.title('Reachability Plot')
    plt.grid()
    plt.show()

# 聚类图
def clust_plot(df_lon_lat_labels_reachability_labelsordering, title, fsize = (16, 8)):
    da = df_lon_lat_labels_reachability_labelsordering
    L = len(set(da['labels']))
    total = len(da)
    ratio = len(da[da['labels'] != -1]) / total

    plt.figure(figsize = fsize)
    for klass in range(0, (L-1)):
        xk = da[da['labels'] == klass]
        plt.scatter(xk.iloc[:, 0], xk.iloc[:, 1], label = klass, s = 10, alpha = 1)
    xk_outer = da[da['labels'] == -1]
    plt.scatter(xk_outer.iloc[:, 0], xk_outer.iloc[:, 1], color = 'k', label = '-1', s = 50, alpha = 0.05, marker = '+')   
    plt.legend()
    plt.title(str(title) + ':  ' + str(total) + ', ' + '{:.2%}'.format(ratio))
    plt.grid()
    plt.show()