# -*- coding: utf-8 -*-
import cv2
import os
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree

# 计算单通道的直方图的相似值
def calculate_ext(image):
    (h, w) = image.shape[:2]
    image1 = image[0:h,0:int(w/2)]
    image2 = image[0:h,int(w/2):w]
    #cv2.imwrite("test\\image\\src_full1"+".jpg",(image))
    #cv2.imwrite("test\\image\\src_full2"+".jpg",(image1))
    #cv2.imwrite("test\\image\\src_full3"+".jpg",(image2))
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree

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

def find_tram(video_name, log_file = None):
    #获得视频的格式
    videoCapture = cv2.VideoCapture(video_name)
      
    #获得码率及尺寸
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 
            int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
     
     
    #读帧
    success, frame = videoCapture.read()
    frame_cnt = 0
    start_frame = 100
    end_frame = 10000
    rotate_angle = -3
    src_img = None
    judge_way = 1
    while success :
        #cv2.imshow('windows', frame) #显示
        #cv2.waitKey(1) #延迟
        frame_cnt += 1
        if(frame_cnt % 100) == 0:
            print("frame is "+str(frame_cnt))

        if judge_way == 0:
            if frame_cnt == start_frame:
                src_img = frame
                src_img = rotate(src_img, rotate_angle)
                cv2.imwrite("test\\image\\src"+".jpg",crop_img(src_img))
                cv2.imwrite("test\\image\\src_full"+".jpg",(src_img))
                src_img = crop_img(src_img)
            if (frame_cnt > start_frame) and (frame_cnt <= end_frame):
                frame = rotate(frame, rotate_angle)
                frame = crop_img(frame)
                degree=calculate(src_img, frame)
                if(degree < 0.65):
                    print("frame "+str(frame_cnt)+" degree is "+str(degree))
                    cv2.imwrite("test\\image\\img_"+str(frame_cnt)+".jpg", (frame))
                else:
                    pass
                    #if(frame_cnt > 700):
                    #    cv2.imwrite("test\\image\\img_"+str(frame_cnt)+".jpg", (frame)) #for test
                #break
            elif(frame_cnt > end_frame):
                break
        else:
            src_frame = frame
            frame = rotate(frame, rotate_angle)
            frame = crop_img(frame)
            degree=calculate_ext(frame)
            if(degree < 0.51):
                info_str = "frame "+str(frame_cnt)+" degree is "+str(degree)
                if log_file != None:
                    log_file.write(video_name+" "+info_str+"\n")
                print(info_str)
                cv2.imwrite("test\\image\\"+video_name[:-4]+"_img_"+str(frame_cnt)+".jpg", (src_frame))
            else:
                pass
            if(frame_cnt > end_frame):
                break
        success, frame = videoCapture.read() #获取下一帧
     
    videoCapture.release()

if __name__ == "__main__":
    #video_name = 'input0.mp4'
    log_file = open("log.txt", 'w')
    file_list = os.listdir('.')
    for file_name in file_list:
        if  os.path.splitext(file_name)[1] == '.mp4':
            video_name = file_name
            print(video_name)
            find_tram(video_name, log_file)
    log_file.close()
