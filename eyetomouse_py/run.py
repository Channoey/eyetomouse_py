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
import keyboard as k
from pynput import keyboard, mouse
import sys

#向数据库里插入消息
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

FLAG_START = True  # 是否为第一次标志
is_blink = False #眨眼功能是否开启
is_move = False #鼠标移动功能是否开启

insert_message("正在启动摄像头...")

#键盘绑定事件
def q():
    insert_message("q退出运行程序")
    time.sleep(1)
    os._exit(0)
k.add_hotkey('q', q)

def w(): #按w开启眨眼功能
    insert_message("开启眨眼功能")
    time.sleep(2)
    global is_blink
    is_blink = True
k.add_hotkey('w', w)

def e(): #按e关闭眨眼功能
    insert_message("关闭眨眼功能")
    time.sleep(2)
    global is_blink
    is_blink = False
k.add_hotkey('e', e)

def a(): #按a开启鼠标移动功能
    insert_message("开启鼠标移动功能")
    time.sleep(2)
    global is_move
    is_move = True
k.add_hotkey('a', a)

def s(): #按s关闭鼠标移动功能
    insert_message("关闭鼠标移动功能")
    time.sleep(2)
    global is_move
    is_move = False
k.add_hotkey('s', s)


username = sys.argv[1]
root = "/Users/amateur/project/eyetomouse/eyetomouse_py/image/" + username + "/"

eye_cascade = cv2.CascadeClassifier(
    "/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")
face_xml = cv2.CascadeClassifier(
    '/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
a = cv2.CascadeClassifier(
    "/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_lefteye_2splits.xml")  # 写入类型器的路径并给cv2.CascadeClassifier函数进行处理
b = cv2.CascadeClassifier(
    "/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_righteye_2splits.xml")  # 写入类型器的路径并给cv2.CascadeClassifier函数进行处理

video_capture = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

insert_message("摄像头启动成功，开始训练模型！")


def normalize(x):
    minn, maxx = x.min(), x.max()
    return (x - minn) / (maxx - minn)


def scan(image_size=(32, 32)):
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
        return (np.hstack(eyes) * 255).astype(np.uint8)
    else:
        return None


def scan2():
    is_left = False
    is_right = False
    ret, frame = video_capture.read()  # 读取视频，第一个参数ret 为True 或者False,代表有没有读取到图片，第二个参数frame表示截取到一帧的图片
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将每一帧图片转为灰色以便接下来处理
        face = face_xml.detectMultiScale(
            gray
        )
        for (x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绘制人脸方框
            face_gray = gray[y:y + h, x:x + w]
            face_color = frame[y:y + h, x:x + w]

            lefteye = a.detectMultiScale(
                face_gray,
                scaleFactor=1.1,
                minNeighbors=70,
                minSize=(3, 3),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if lefteye is not ():
                is_left = True
                # 通过cv2.CascadeClassifier(cascPath).detectMultiScale函数进行人眼识别处理
                for (x1, y1, w1, h1) in lefteye:
                    cv2.rectangle(face_color, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
                    cv2.putText(face_color, "lefteye", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2)
            righteye = b.detectMultiScale(
                face_gray,
                scaleFactor=1.1,
                minNeighbors=70,
                minSize=(3, 3),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if righteye is not ():
                is_right = True
                for (x2, y2, w2, h2) in righteye:
                    cv2.rectangle(face_color, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
                    cv2.putText(face_color, "righteye", (x2, y2 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 255, 0), 2)

        print("is_left:" + str(is_left))
        print("is_right:" + str(is_right))
            # 在原图的人脸上画出识别的矩形区域

        cv2.namedWindow("eyesFound", cv2.WINDOW_NORMAL)  # 给定可以拉伸的窗口
        cv2.resizeWindow("eyesFound", 640, 360) #16:9
        cv2.imshow('eyesFound', frame)  # 创造一个facesFound窗口来展示每一帧的图片，使其类似以视频方式播放
        cv2.waitKey(30)
        return is_left, is_right


width, height = 2560, 1600
try:
    filepaths = os.listdir(root)
except:
    insert_message("-6")  # 未训练模型
    time.sleep(1)
    insert_message("未训练模型，结束程序！")
    exit()

X, Y = [], []
for filepath in filepaths:
    try:
        x, y, _ = filepath.split(' ')
        x = float(x) / width
        y = float(y) / height
        X.append(cv2.imread(root + filepath))
        Y.append([x, y])
    except:
        continue

X = np.array(X) / 255.0
Y = np.array(Y)

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

print("model success")
insert_message("模型训练成功，开始程序！")

#主程序
while True:
    time.sleep(0.1)
    eyes = scan()
    is_left, is_right = scan2()

    if FLAG_START:
        if eyes is None:
            insert_message("-4")
            time.sleep(1)
            insert_message("未监测到眼睛，退出程序")
            cv2.destroyAllWindows()
            exit()
        FLAG_START = False
    else:
        if eyes is not None:
            if is_move:
                eyes = np.expand_dims(eyes / 255.0, axis=0)
                x, y = model.predict(eyes)[0]
                pyautogui.moveTo(x * width, y * height)
        else:
            if is_blink:
                pyautogui.click()
                insert_message("单击")
                time.sleep(1)
        if is_blink:
            if is_left is True and is_right is False:
                pyautogui.press("pagedown")
                insert_message("眨右眼，下滑")
                time.sleep(1)
            elif is_left is False and is_right is True:
                pyautogui.press("pageup")
                insert_message("眨左眼，上滑")
                time.sleep(1)
