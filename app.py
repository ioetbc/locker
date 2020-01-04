import os, time

def main_loop():
    while 1:
        #how frequent to get the idle time
        time.sleep(5)
        cmd = "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle}'"
        result = os.popen(cmd)
        str = result.read()
        idle_time = int(str.split(".")[0])
        print('user idle time', idle_time)

        if idle_time >= 10:
            print('going to check if teh user is sitting at their computer')
            sleep_cmd = """osascript -e 'ignoring application responses' -e 'tell application "Finder" to sleep' -e end"""
            os.system(sleep_cmd)

main_loop()
