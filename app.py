import os, time
import cv2
import numpy as np

def run():
    while True:
        time.sleep(1)
        cmd = "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle}'"
        result = os.popen(cmd)
        str = result.read()
        idle_time = int(str.split(".")[0])
        print('user idle time', idle_time)
        seconds_face_not_detected = 0

        if idle_time >= 5:
            while True:
                front_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                profile_face_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

                cap = cv2.VideoCapture(0)
                ret, img = cap.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                front_face = front_face_cascade.detectMultiScale(gray, 1.3, 5)
                profile_face = profile_face_cascade.detectMultiScale(gray, 1.3, 5)

                face_detected = False

                for (x, y, w, h) in front_face:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    face_detected = True
                    print('face_detected front face', face_detected)
                    seconds_face_not_detected = 0
                    cap.release()
                    cv2.destroyAllWindows()
                    print('waiting 5 seconds tobe called again if no activity')
                    time.sleep(5)
                    run()
                    break

                for (x, y, w, h) in profile_face:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    face_detected = True
                    print('face_detected profile face', face_detected)
                    seconds_face_not_detected = 0
                    cap.release()
                    cv2.destroyAllWindows()
                    print('waiting 5 seconds tobe called again if no activity')
                    time.sleep(5)
                    run()
                    break

                if not face_detected:
                    seconds_face_not_detected += 1

                    if seconds_face_not_detected > 10:
                        print('LOCK SCREEN')
                        cap.release()
                        cv2.destroyAllWindows()
                        sleep_cmd = """osascript -e 'ignoring application responses' -e 'tell application "Finder" to sleep' -e end"""
                        os.system(sleep_cmd)
                        break

                cv2.imshow('img', img)
                print('FACE_DETECTED', face_detected)
                print('seconds_face_not_detected', seconds_face_not_detected)

                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break

run()
