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
def search(a,b,c):
    for file in os.listdir(a):
        if os.path.isfile(a+'\\'+file):
            if b in file:
#                print(file,'=>',a+'\\'+file)
                print(file)
                c.append(file)
                global num
                num=num+1
        else:
            search(a+'\\'+file,b)
    return num

def inputfile(path1,path2):
    exec ("f=open('%s')"%(path1))
    exec ("f1=open('%s')"%(path2))
    content=f.readlines()
    f1. writelines(content)
    f1.close()
    f.close()


#file = open(r'F:\NTBtool\sbdart\INPUT','w') 
#file.write('&INPUT \n zout=0, 100 \n phi=0 \n uzen=0 \n sza=60 \n iout=10 \n isat=-1 \n isalb=-1 \n idatm=6 \n iaer=1 \n vis=50 \n/ \n')   
#file.close()
#main = "F:/NTBtool/sbdart/sbdart.exe"
#if os.path.exists(main):  
#    rc,out= subprocess.getstatusoutput(main)  
#    print (rc)
#    print ('*'*10)
#    print (out)
    
#f1 = os.popen("F:/NTBtool/sbdart/sbdart.exe") 
#r_v1=f1.read()   
#r_v = f1.readlines()    
#f1.close()

path='F:/NTBtool/sbdart/'

def runsbdart(path,fltname,refname,outname):
    sza_range=[0, 10, 20, 30, 40, 50, 60, 70, 75, 80, 85] 
    vis_range=[5, 10, 15, 20, 25, 30, 50, 70, 100]
    
    for i in range (1,num+1):
        exec ("path1='%s%s%s.txt'"%(path,fltname,i))
        exec ("path2='%sfilter.dat'"%(path))
        inputfile(path1,path2)
        exec ("file = open('%s%s.txt','a')"%(path,outname))    
    #    cat etm_srf_b$i.txt > filter.dat   
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

#                cat ./validate/validation$j.txt > albedo.dat
#                echo "
#                 &INPUT
#                  wlinf=0.35
#                	 wlsup=2.5
#                	 zout=0, 100
#                  phi=0
#                  uzen=0
#                  sza=$sza
#                  iout=10
#                  isat=0
#                  isalb=-1
#                  idatm=6
#                  iaer=1
#                  vis=$vis
#                 /" > INPUT
#                ./sbdart.exe >> shortwavevalidate3333.txt
    
#r_v =os.system("F:/NTBtool/sbdart/sbdart.exe") #调用外部exe程序
#os.system("F:/sbdart/sbdart/Release/atry.sh")
#
#os.system("pause")

#a = subprocess.call('df -hT',shell=True) #调用控制台
def getalbedo(inpath,inname,outpath,band_number):
    c=[]
    num=0
    search(inpath,inname,c) #查找lut
    
    print(c,num)
    print(c[1])
    ref=np.empty([24255, 10])
    #ref=np.zeros((3960, 4), dtype=np.float)
    ad=outpath #文件路径，要改成用户键盘输入的，用函数的形式
    xls = xlwt.Workbook()
    #sheet_name1 = 'summary'
    ad5='etm__lut.xls'
    ad6='etm__lut.txt'
    #ad4=inpath+ad5


    for j in range(0,num):
        ad1=ad+c[j]
    #    arr = np.loadtxt(ad1,delimiter='/n')
    #    print (arr)
        sheet_name = os.path.basename(ad1)
        sheet = xls.add_sheet(sheet_name, cell_overwrite_ok=True)
        
        f = open(ad1)
        x = 0
        lut=[]
                # 按行读取文本
        while True:
            lines = f.readline()
    #        print(lines)
            if not lines:
                break
            for line in lines:
    
     
                if line==' ':
                    lines=lines.strip();
    #            line = line.split()
                else:
                    break
    #                print(lines)
                    
    #                print(a)
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
                # 然后读取下一个文本
        f.close()
        lut1=np.array(lut)
        ref[:,j]=lut1[:, 9]
#        data = pd.DataFrame(lut1)
#        sheet=os.path.basename(ad1)
#        data.to_excel(writer, sheet, float_format='%.9f',index=False,index_label=None,header=False)	
    
    #ad2=ad+'broadbandvalidation.txt'
    #arr = np.loadtxt(ad2,delimiter='\t')
    #ref=np.column_stack((ref,arr))
    ref=np.around(ref, decimals=9)
    ad3=ad+ad6
    np.savetxt(ad3,ref)
    xlsname=ad+ad5
    
    xls.save(xlsname)  
            
#    data = pd.DataFrame(ref)
    
    #writer = pd.ExcelWriter('F:/sbdart/sbdart/Release/artificial/test.xls')		# 写入Excel文件
#    data.to_excel(writer, 'summary', float_format='%.9f',index=False,index_label=None,header=False)		# ‘page_1’是写入excel的sheet名
#    writer.save()
#    
#    writer.close()


    
#对得到的文件计算反照率    
#c=[]
#num=0
#search('F:/etm/','etm__lutb',c) #查找lut
#
#print(c,num)
#print(c[1])
#ref=np.empty([24255, 10])
##ref=np.zeros((3960, 4), dtype=np.float)
#ad='F:/etm/' #文件路径，要改成用户键盘输入的，用函数的形式
#xls = xlwt.Workbook()
#sheet_name1 = 'summary'
#ad5='etm__lut.xls'
#ad6='etm__lut.txt'
#ad4=ad+ad5
#sheet1 = xls.add_sheet(sheet_name1, cell_overwrite_ok=True)
#writer = pd.ExcelWriter(ad4)
#for j in range(0,num):
#    ad1=ad+c[j]
##    arr = np.loadtxt(ad1,delimiter='/n')
##    print (arr)
#    sheet_name = os.path.basename(ad1)
#    sheet = xls.add_sheet(sheet_name, cell_overwrite_ok=True)
#    
#    f = open(ad1)
#    x = 0
#    lut=[]
#            # 按行读取文本
#    while True:
#        lines = f.readline()
##        print(lines)
#        if not lines:
#            break
#        for line in lines:
#
# 
#            if line==' ':
#                lines=lines.strip();
##            line = line.split()
#            else:
#                break
##                print(lines)
#                
##                print(a)
#        a=lines.split()
#        data=map(float,a)
#        data=list(data)
#        data1=data[7]/data[6]
#        data.append(data1)
#        lut.append(data)
##        sheet1.write(x,j,data[9])
#        for i in range(len(a)):
#
#            sheet.write(x,i,data[i])   # x,i,data 代表横、纵坐标和内容            
#        x += 1 #另起一行
#            # 然后读取下一个文本
#    f.close()
#    lut1=np.array(lut)
#    ref[:,j]=lut1[:, 9]
#    data = pd.DataFrame(lut1)
#    sheet=os.path.basename(ad1)
#    data.to_excel(writer, sheet, float_format='%.9f',index=False,index_label=None,header=False)	
#
##ad2=ad+'broadbandvalidation.txt'
##arr = np.loadtxt(ad2,delimiter='\t')
##ref=np.column_stack((ref,arr))
#np.around(ref, decimals=9)
#ad3=ad+ad6
#np.savetxt(ad3,ref)
#xlsname=ad+ad5
#
#xls.save(xlsname)  
#        
#data = pd.DataFrame(ref)
#
##writer = pd.ExcelWriter('F:/sbdart/sbdart/Release/artificial/test.xls')		# 写入Excel文件
#data.to_excel(writer, 'summary', float_format='%.9f',index=False,index_label=None,header=False)		# ‘page_1’是写入excel的sheet名
#writer.save()
#
#writer.close()
#
#        # 最后保存到文件 
##        xls.save(xlspath)
#
##    sheet = xls.add_sheet(sheetname='sheet 1')
#    
#    # 在指定单元格 (第一行第二列) 写入数据
#
##files = dir(strcat(inpath,'*.txt'));
##len=length(files);

#多元线性回归

#ad='F:/sbdart/sbdart/Release/artificial/'
#ad3=ad+'gf1拟合.txt'
#input1=np.loadtxt(ad3,delimiter='\t')
#row=input1.shape[0]
#col=input1.shape[1]
#for i in range(0,col-3):
#    exec ("x%s=input1[:,%s]"%(i+1,i)) #将模拟的传感器窄波段反照率存到x
#for i in range(col-3,col):
#    exec ("y%s=input1[:,%s]"%(i-3,i)) #将模拟的宽波段反照率存到x
##x1=input1[:,0]
##x2=input1[:,1]
##x3=input1[:,2]
##x4=input1[:,3]
##x5=input1[:,4]
##x6=input1[:,5]
##x7=input1[:,6]
##x8=input1[:,7]
###x1=input1[:,0:4]
##y1=input1[:,8]
##y2=input1[:,9]
##y3=input1[:,10]
#
##for i in range(0,col):
##    x
##curve_fit非线性最小二乘拟合
#from scipy.optimize import curve_fit
#def func(X,a0,a1,a2,a3,a4):
#    x1,x2,x3,x4=X
#    return a0+a1*x1+a2*x2+a3*x3+a4*x4
#param_bounds=([-0.01,-1.,-1.,-1.,-1.],[0.01,1.,1.,1.,1.])
#fitParams, fitCovariances = curve_fit(func,(x1,x2,x3,x4),y1,bounds=param_bounds)
#
##线性最小二乘拟合lsq_linear
#from scipy.optimize import lsq_linear
##可见光
#A=input1[:,0:col-3]
#inter=np.ones((row,1))
#A=np.column_stack((A,inter))
#
#
#b=input1[:,col-3]
#
#l=col-3
#lb=[-1]*l
#lb.append(-0.01)
##lb=-np.ones((col-3,1))
##lb=np.insert(lb, col-3, values=-0.01, axis=0)
###lb=np.column_stack((lb,-0.01))
##lb.reshape(-1,1)
#
#u=col-3
#ub=[1]*l
#ub.append(0.01)
##ub=np.ones((col-3,1))
##ub=np.insert(ub, col-3, values=0.01, axis=0)
##ub.reshape(-1,1)
#
#res = lsq_linear(A, b, bounds=(lb, ub), tol=2.2204e-12, verbose=1) 
##,lsmr_tol='auto'
