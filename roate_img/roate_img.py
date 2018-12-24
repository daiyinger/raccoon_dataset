# -*- coding: utf-8 -*-
import cv2
import os

def rotate(image, angle, center=None, scale=1.0):
    # 
    (h, w) = image.shape[:2]

    # 
    if center is None:
        center = (w / 2, h / 2)

    # 
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # 
    return rotated

def crop_img(image):
    img_size = image.shape
    return image[290:img_size[1]-312, 50:img_size[0]-50] # Y-start:Y-End, X-start:X-end

def roate_image(dir_str, image_name, log_file):
    pass
    img = cv2.imread(image_name)
    img = rotate(img, -3.9)
    cv2.imwrite(dir_str+"\\"+image_name[:-4]+"_1.jpg", img)

if __name__ == "__main__":
    #video_name = 'input0.mp4'
    log_file = open("log.txt", 'w')
    file_list = os.listdir('.')
    os.mkdir("output")
    for file_name in file_list:
        if  os.path.splitext(file_name)[1] == '.jpg':
            image_name = file_name
            print(image_name)
            roate_image("output",image_name, log_file)
    log_file.close()
