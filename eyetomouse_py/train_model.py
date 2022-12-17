import time
import cv2
import numpy as np
import os
import shutil
import pymysql
from pynput import keyboard, mouse
import sys

root = "/Users/amateur/project/eyetomouse/eyetomouse_py/image/" + sys.argv[1] + "/"
if not os.path.isdir(root):
    os.mkdir(root)


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


def normalize(x):
    minn, maxx = x.min(), x.max()
    return (x - minn) / (maxx - minn)


# Eye cropping function
def scan(px,py,image_size=(32, 32)):
    global click_count
    msg = "当前训练次数：" + str(click_count)
    insert_message(msg)
    time.sleep(1)
    click_count = click_count + 1
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    boxes = cascade.detectMultiScale(gray, 1.3, 10)
    if len(boxes) == 2:
        eyes = []
        for box in boxes:
            x, y, w, h = box
            eye = frame[y:y + h, x:x + w]
            eye = cv2.resize(eye, image_size)
            eye = normalize(eye)
            eye = eye[10:-10, 5:-5]
            eyes.append(eye)
        cv2.namedWindow("click", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("click", 640, 360)
        text1 = "x:" + str(px) + " y:" + str(py)
        text2 = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, text1, (900, 560) , cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 2)
        cv2.putText(frame, text2, (900, 640), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 2)
        cv2.imshow('click', frame)
        cv2.waitKey(1)
        return (np.hstack(eyes) * 255).astype(np.uint8)
    else:
        return None


def on_press(key):
    insert_message("q退出模型训练程序")
    time.sleep(1)
    os._exit(0)


def on_click(x, y, button, pressed):
    if pressed:
        eyes = scan(x,y)
        if not eyes is None:
            filename = root + "{} {} {}.jpeg".format(x, y, button)
            cv2.imwrite(filename, eyes)

click_count = 1 #点击次数统计

insert_message("正在启动训练程序...")
time.sleep(1)

insert_message("正在启动摄像头...")
time.sleep(1)
cascade = cv2.CascadeClassifier(
    "/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")
video_capture = cv2.VideoCapture(0)

insert_message("启动成功，请开始点击！")
time.sleep(1)

with keyboard.Listener(on_press=on_press) as kl, \
        mouse.Listener(on_click=on_click) as ml:
    kl.join()
    ml.join()