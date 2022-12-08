import datetime
import numpy as np
import os
import cv2
import pyautogui
import pymysql
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *
import time
import keyboard
import sys


def insert_message(msg):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    con = pymysql.connect(host='localhost', password='123456', port=3306, user='root', charset='utf8')
    cur = con.cursor()
    sql = "insert into demo.message(message,time) values(\"" + msg + "\",\"" + now + "\");"
    print(sql)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

insert_message("正在启动摄像头...")

# username = sys.argv[1]
# root = "/Users/amateur/project/eyetomouse/image/" + username + "/"
root = "/Users/amateur/project/eyetomouse/image/" + "admin" + "/"

eye_cascade = cv2.CascadeClassifier(
    "/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")
face_cascade = cv2.CascadeClassifier(
    '/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

insert_message("摄像头启动成功，开始训练模型！")


def normalize(x):
    minn, maxx = x.min(), x.max()
    return (x - minn) / (maxx - minn)


def scan(image_size=(32, 32)):
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    cv2.waitKey(30)

    boxes = eye_cascade.detectMultiScale(gray, 1.3, 10)
    if len(boxes) == 2:
        eyes = []
        for box in boxes:
            x, y, w, h = box
            eye = frame[y:y + h, x:x + w]
            eye = cv2.resize(eye, image_size)
            eye = normalize(eye)
            eye = eye[10:-10, 5:-5]
            eyes.append(eye)
            # try:
            if keyboard.is_pressed('Q'):
                insert_message("q退出")
                break
        return (np.hstack(eyes) * 255).astype(np.uint8)
    else:
        return None


width, height = 2560, 1600
try:
    filepaths = os.listdir(root)
except:
    insert_message("-6") #未训练模型
    time.sleep(1)
    insert_message("未训练模型，结束程序！")
    exit()

X, Y = [], []
for filepath in filepaths:
    x, y, _ = filepath.split(' ')
    x = float(x) / width
    y = float(y) / height
    X.append(cv2.imread(root + filepath))
    Y.append([x, y])
    # try:
    if keyboard.is_pressed('Q'):
        insert_message("q退出")
        break
X = np.array(X) / 255.0
Y = np.array(Y)
# print (X.shape, Y.shape)

model = Sequential()
model.add(Conv2D(32, 3, 2, activation='relu', input_shape=(12, 44, 3)))
model.add(Conv2D(64, 2, 2, activation='relu'))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(2, activation='sigmoid'))
model.compile(optimizer="adam", loss="mean_squared_error")
model.summary()

epochs = 200
for epoch in range(epochs):
    model.fit(X, Y, batch_size=32)
    # try:
    # if keyboard.is_pressed('Q'):
    #     insert_message("q退出")
    #     break

print("model success")
insert_message("模型训练成功，开始程序！")
time.sleep(1)

FLAG = -1  # 记录当前状态 0-五次推出 1-三次开启眨眼监测 2-三次关闭眨眼监测 3-双击 4-单击
FLAG_START = True  # 是否为第一次标志
is_blink = False  # 是否开启眨眼监测
blink_list = []  # 记录无眼睛时间点
blink_list_second = []  # 精确到秒的记录无时间眼睛点
count1 = 0  # 记录是否五次结束

while True:

    FLAG = -1

    # try:
    if keyboard.is_pressed('Q'):
        insert_message("q退出运行程序")
        cv2.destroyAllWindows()
        exit()

    eyes = scan()
    if FLAG_START:
        if eyes is None:
            print("未监测到眼睛，退出程序")
            insert_message("-4")
            time.sleep(1)
            insert_message("未监测到眼睛，退出程序")
            cv2.destroyAllWindows()
            exit()
        time.sleep(2)
        FLAG_START = False

    time_now = datetime.datetime.now()

    if eyes is None and not is_blink:  # 监测到眨眼但没有开启眨眼监测
        blink_list.append(time_now)
        for i in range(len(blink_list)):
            data = blink_list[i]
            data_second = datetime.datetime(data.year, data.month, data.day, data.hour, data.minute, data.second)
            if data_second not in blink_list_second and eyes is None:
                blink_list_second.append(data_second)
        if len(blink_list) > 3:
            delta = datetime.timedelta(seconds=1)
            count2 = 0
            time_now_temp = time_now
            for i in range(4):
                time_now_temp = time_now_temp - delta
                temp = datetime.datetime(time_now_temp.year, time_now_temp.month, time_now_temp.day,
                                         time_now_temp.hour, time_now_temp.minute, time_now_temp.second)
                if temp in blink_list_second:
                    count2 += 1
            if count2 >= 3:
                # print("三次开启眨眼监测")
                FLAG = 1


    elif is_blink:  # 监测到眨眼并开启眨眼监测
        blink_list.append(time_now)
        # 闭眼五秒关闭程序
        for i in range(len(blink_list)):
            data = blink_list[i]
            data_second = datetime.datetime(data.year, data.month, data.day, data.hour, data.minute, data.second)
            if data_second not in blink_list_second and eyes is None:
                blink_list_second.append(data_second)
        if len(blink_list) > 5:
            delta = datetime.timedelta(seconds=1)
            count1 = 0
            time_now_temp = time_now
            for i in range(6):
                time_now_temp = time_now_temp - delta
                temp = datetime.datetime(time_now_temp.year, time_now_temp.month, time_now_temp.day,
                                         time_now_temp.hour, time_now_temp.minute, time_now_temp.second)
                if temp in blink_list_second:
                    count1 += 1
                print(blink_list_second)
            print("count1:" + str(count1))
            print("count2:" + str(count2))
            if count1 >= 5:
                # print("闭眼五秒关闭程序")
                FLAG = 0
            elif count1 >= 4:
                FLAG = 2
            elif count1 >= 3:
                FLAG = 3
            elif count1 >= 2:
                FLAG = 4
    if eyes is not None:
        eyes = np.expand_dims(eyes / 255.0, axis=0)
        x, y = model.predict(eyes)[0]
        pyautogui.moveTo(x * width, y * height)

    if FLAG == 0:
        print("五次退出")
        insert_message("五次退出")
        FLAG = -1
        exit(0)
    elif FLAG == 1:
        print("开启眨眼功能")
        insert_message("开启眨眼功能")
        FLAG = -1
        is_blink = True
        blink_list.clear()
        blink_list_second.clear()
        time.sleep(3)
    elif FLAG == 2:
        print("关闭眨眼功能")
        insert_message("关闭眨眼功能")
        FLAG = -1
        is_blink = False
        blink_list.clear()
        blink_list_second.clear()
        time.sleep(3)
    elif FLAG == 3:
        print("双击")
        insert_message("双击")
        FLAG = -1
        pyautogui.click()
        pyautogui.click()
        blink_list.clear()
        blink_list_second.clear()
        time.sleep(3)
    elif FLAG == 4:
        print("单击")
        insert_message("单击")
        FLAG = -1
        pyautogui.click()
        blink_list.clear()
        blink_list_second.clear()
        time.sleep(3)
    time.sleep(0.1)
    # except:
    #     print("-3") #数据库异常
    #     exit()
