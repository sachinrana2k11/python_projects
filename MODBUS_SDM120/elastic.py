# Python program to illustrate the concept 
# of threading 
import threading
import os
import time
lock = threading.Lock()

def task1():
    while 1:
        #lock.acquire()
        print("Task-1")
        #time.sleep(1)
        #lock.release()
        time.sleep(5)


def task2():
    while 1:
        print("\t\tTask-2")
        time.sleep(2)


if __name__ == "__main__":
    t1 = threading.Thread(target=task1, name='t1')
    t2 = threading.Thread(target=task2, name='t2')
    t1.start()
    t2.start()