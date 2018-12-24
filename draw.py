import numpy as np
#jhgjhgjhgjh
import cv2 as cv
import numpy as np
import os

file_list = os.listdir('.\\annotations')
for file_name in file_list:
    print(file_name)
    fp=open(".\\annotations\\"+file_name,"r")#打开文件读取所有内容
    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0
    while 1:
        line=fp.readline()          #一行一行的存储读取的文件
        if not line:
            break                   #line为空结束循环           
        if(line.find('xmin') > 0):
            xmin = int(line[line.find('xmin')+5:line.find('</xmin')])
        if(line.find('ymin') > 0):
            ymin = int(line[line.find('ymin')+5:line.find('</ymin')])
        if(line.find('xmax') > 0):
            xmax = int(line[line.find('xmax')+5:line.find('</xmax')])
        if(line.find('ymax') > 0):
            ymax = int(line[line.find('ymax')+5:line.find('</ymax')])
            print(xmin, ymin, xmax, ymax)
    #continue
    img_path = ".\\images\\"+file_name.replace('.xml', '.jpg')
    #print(img_path)
    path=cv.imread(img_path)         #待处理的图像名
    cv.rectangle(path,(xmin,ymin),(xmax,ymax),(0, 255, 0), 1, 1, 0)#画矩形框                 #str1的下一个矩形数据组
    cv.namedWindow("resultpicture") #打开显示图形界面
    cv.imshow("resultpicture",path) #显示结果图像
    cv.waitKey(2000)
    #cv.imwrite("./result_labelFace.jpg",path)#存储结果图像
