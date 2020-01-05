import os, time
import sys
import cv2
import numpy as np

def check_for_idle_activity():
    while 1:
        #how frequent to check user idle time
        time.sleep(5)
        cmd = "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle}'"
        result = os.popen(cmd)
        str = result.read()
        idle_time = int(str.split(".")[0])
        print('user idle time', idle_time)

        if idle_time >= 10:
            print('going to check if teh user is sitting at their computer')
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0) 
            face_not_visible_x_seconds = 0

            while 1:
                ret, img = cap.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    print('face detected')
                    face_not_visible_x_seconds = 0

                cv2.imshow('img', img)

                if face_not_visible_x_seconds != 30:
                    print('number of seconds face not visible', face_not_visible_x_seconds)
                    face_not_visible_x_seconds += 1

                if face_not_visible_x_seconds > 29:
                    print('LOCK THE COMPUTER')
                    sleep_cmd = """osascript -e 'ignoring application responses' -e 'tell application "Finder" to sleep' -e end"""
                    os.system(sleep_cmd)

                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

check_for_idle_activity()
