import cv2
import pyautogui

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    print("1")
    print(frame.shape)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 下面这两个分类器文件替换成自己电脑上的。用everything搜索一下。
    xmlfile = r'/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml'
    xmlfile2 = r'/Users/amateur/opt/anaconda3/envs/ai_study_37/lib/python3.7/site-packages/cv2/data/haarcascade_lefteye_2splits.xml'

    face_cascade = cv2.CascadeClassifier(xmlfile)
    eyes = cv2.CascadeClassifier(xmlfile2)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(5, 5),
    )
    eyes = eyes.detectMultiScale(
        gray,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(5, 5),
    )
    print("发现{0}个目标!".format(len(faces)))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 2)
        xx = max(0, min(10 * (x - 100), 2560))
        yy = max(0, min(20 * (y - 100), 1440))
        pyautogui.moveTo(10 * (x - 100), 10 * (y - 100), duration=0.01)
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 2)
    print("{0} 个眼睛!".format(len(eyes)))
    print(eyes)
    if len(eyes) < 1:
        pyautogui.click()
    cv2.imshow("frame", frame)
    # Display the resulting frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
