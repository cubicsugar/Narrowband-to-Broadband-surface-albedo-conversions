# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 08:52:30 2019

@author: TX
"""
import subprocess  
import os
import numpy as np
import pandas as pd
import xlwt
from scipy.optimize import lsq_linear
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#查找文件夹下包含某个字符串的文件名
def search(path,name,c):
    num=0
    for file in os.listdir(a):
        if os.path.isfile(a+'\\'+file):
            if b in file:
#                print(file,'=>',a+'\\'+file)
                print(file)
                c.append(file)

                num=num+1
#        else:
#            search(a+'\\'+file,b,c)
    return num

#读取一个文本文件写入另一个文本文件
def inputfile(path1,path2):
    exec ("f=open('%s')"%(path1))
    exec ("f1=open('%s')"%(path2))
    content=f.readlines()
    f1. writelines(content)
    f1.close()
    f.close()

#进行辐射传输模拟
def runsbdart(path,fltname,refname,outname):
    sza_range=[0, 10, 20, 30, 40, 50, 60, 70, 75, 80, 85] 
    vis_range=[5, 10, 15, 20, 25, 30, 50, 70, 100]
    c=[]
    num=search(path,refname,c) #查找reflectance文件数量
    for i in range (1,num+1):
        exec ("path1='%s%s%s.txt'"%(path,fltname,i))
        exec ("path2='%sfilter.dat'"%(path))
        inputfile(path1,path2)
        exec ("file = open('%s%s%s.txt','a')"%(path,outname,i))     
        for sza in sza_range:       
            for vis in vis_range:            
                for j in range (1,376):
                    exec ("path1='%s%s%s.txt'"%(path,refname,j))
                    exec ("path2='%salbedo.dat'"%(path))
                    inputfile(path1,path2) 
                    exec ("file1 = open(r'%sINPUT','w')"%(path))
                    exec ("file1.write('&INPUT \n zout=0, 100 \n phi=0 \n\
                                uzen=0 \n sza=%s \n iout=10 \n\
                                isat=-1 \n isalb=-1 \n idatm=6 \n\
                                iaer=1 \n vis=vis \n/ \n')"%(sza,vis))
                    file1.close()
                    exec ("f1 = os.popen('%ssbdart.exe')"%(path)) 
                    r_v1=f1.read()  
                    file.write(r_v1)
        file.close()

#a = subprocess.call('df -hT',shell=True) #调用控制台

#由辐射传输模拟结果计算反照率        
def getalbedo(inpath,inname,outpath):
    c=[]

    num=search(inpath,inname,c) #查找lut
    
    print(c,num)
    print(c[1])

    ref = []

    #ad=inpath #文件路径
    xls = xlwt.Workbook()

    excel_ad=inname+'.xls'
    txt_ad=inname+'.txt'
    for j in range(0,num):
        ad1=inpath+c[j]
        sheet_name = os.path.basename(ad1)
        sheet = xls.add_sheet(sheet_name, cell_overwrite_ok=True)
        
        f = open(ad1)
        x = 0
        lut=[]

        while True:
            lines = f.readline()
            if not lines:
                break
            for line in lines:
         
                if line==' ':
                    lines=lines.strip();

                else:
                    break

            a=lines.split()
            data=map(float,a)
            data=list(data)
            data1=data[7]/data[6]
            data.append(data1)
            lut.append(data)
    #        sheet1.write(x,j,data[9])
            for i in range(len(a)):
    
                sheet.write(x,i,data[i])   # x,i,data 代表横、纵坐标和内容            
            x += 1 #另起一行
               
        f.close()
        lut1=np.array(lut)

        ref.append(lut1[:, 9])

    ref=np.array(ref)
    ref=ref.transpose()
    txt_path=outpath+txt_ad
    np.savetxt(txt_path,ref,fmt='%.9f')
    xlsname=outpath+excel_ad
    
    xls.save(xlsname)

def f_1(x, A, B):
    return A*x + B    
#散点图    
def plot_point(simulated_value,fitted_value,title):
    plt.xlabel('Simulated Value')
    plt.ylabel('Fitted Value')
    plt.xlim(xmax=1,xmin=0)
    plt.ylim(ymax=1,ymin=0)
    colors1 = '#054E9F'
    area = np.pi*2
    plt.plot([0,1],[0,1],linewidth = 0.5,color='black') 
    plt.scatter(simulated_value, fitted_value, s=area, c=colors1, alpha=0.4)

    plt.title(title,fontsize=20)

    residual = simulated_value - fitted_value
    RMSE=np.sqrt(np.sum(np.power(residual,2))/len(fitted_value))
    R2=1-RMSE*RMSE/np.var(simulated_value) 
    
    str1='R-squared='+str(R2)
    str2='RMSE='+str(RMSE)
    A1, B1 = curve_fit(f_1, simulated_value, fitted_value)[0]
    A1=format(A1,'.4f')
    B1=format(B1,'.4f')
    str3='y='+str(A1)+'x+'+str(B1)
    plt.text(0.05,0.95, str3, fontsize=8)
    plt.text(0.05,0.88, str1, fontsize=8)
    plt.text(0.05,0.81, str2,fontsize=8)

#多元线性回归
def simulation(narrow_inpath,broad_inpath,title):
    narrow_albedo=np.loadtxt(narrow_inpath,delimiter=' ')
    broad_albedo=np.loadtxt(broad_inpath,delimiter=' ')
    row=narrow_albedo.shape[0]
    col=narrow_albedo.shape[1]
    A=narrow_albedo
    inter=np.ones((row,1))
    A=np.column_stack((A,inter))
    
    
    b=broad_albedo
    
    l=col
    lb=[-1]*l
    lb.append(-0.01)
    #lb=-np.ones((col-3,1))
    #lb=np.insert(lb, col-3, values=-0.01, axis=0)
    ##lb=np.column_stack((lb,-0.01))
    #lb.reshape(-1,1)
    
    u=col
    ub=[1]*u
    ub.append(0.01)
    #ub=np.ones((col-3,1))
    #ub=np.insert(ub, col-3, values=0.01, axis=0)
    #ub.reshape(-1,1)
    
    res = lsq_linear(A, b, bounds=(lb, ub), tol=2.2204e-12, verbose=1)
    x = res['x']
    simulated=np.dot(A,x)
    residual = b - np.dot(A,x)
    RMSE=np.sqrt(np.sum(np.power(residual,2))/len(simulated))
    R2=1-RMSE*RMSE/np.var(b)
    print('The simulated coefficients are ',x)
    plot_point(simulated,b,title)
    
    return x

#验证    
def validation(narrow_inpath,broad_inpath,coefficient,title):
    narrow_albedo=np.loadtxt(narrow_inpath,delimiter=' ')
    broad_albedo=np.loadtxt(broad_inpath,delimiter=' ')
    row=narrow_albedo.shape[0]
    col=narrow_albedo.shape[1]
    A=narrow_albedo
    inter=np.ones((row,1))
    A=np.column_stack((A,inter))

    fitted_albedo=np.dot(A,coefficient) 
    plot_point(broad_albedo,fitted_albedo,title)
    

#radiance_path='F:/NTBtool/Narrowband-to-Broadband-surface-albedo-conversions/narrowband_fit/'
#radiance_name='landsat'  
#albedo_path='F:/NTBtool/Narrowband-to-Broadband-surface-albedo-conversions/narrowband_fit/albedo/'
#getalbedo(radiance_path,radiance_name,albedo_path)
#path='F:/NTBtool/sbdart/'
#ad='F:/NTBtool/Narrowband-to-Broadband-surface-albedo-conversions/narrowband_fit/albedo/'
#out='F:/NTBtool/Narrowband-to-Broadband-surface-albedo-conversions/broadband_fit/'
#ad2=ad+'landsat.txt'
#ad3=out+'visiblefit.txt'
#x=simulation(ad2,ad3,'Visible Broadband Albedo (Landsat)')  
#validation(ad2,ad3,x,'Landsat')
