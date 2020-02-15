import os, time
import cv2
import numpy as np

while True:
    time.sleep(1)
    cmd = "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle}'"
    result = os.popen(cmd)
    str = result.read()
    idle_time = int(str.split(".")[0])
    print('user idle time', idle_time)
    seconds_face_not_detected = 0

    if idle_time >= 10:
        while True:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0)
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print(1)

            for (x, y, w, h) in faces:
                print('FACE DETECTED')
                seconds_face_not_detected = 0
                # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cap.release()
                cv2.destroyAllWindows()

            else:
                seconds_face_not_detected += 1
                print('seconds_face_not_detected', seconds_face_not_detected)
                if seconds_face_not_detected > 10:
                    print('LOCK SCREEN')
                    sleep_cmd = """osascript -e 'ignoring application responses' -e 'tell application "Finder" to sleep' -e end"""
                    os.system(sleep_cmd)
                    break

            # cv2.imshow('img', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

