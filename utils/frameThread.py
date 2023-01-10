import cv2
import threading
import redis
import queue
from utils.myPrint import customPrint


class FrameThread(threading.Thread):
    def __init__(self, rtsp_url, q):
        super(FrameThread, self).__init__()
        self.rtsp_url = rtsp_url
        self.q = q
        self.thread_exit = False
        # self.run()


    def run(self):
        customPrint('已进入取图循环')
        # 用来记录异常次数的标记
        exit_frame_num = 0
        exit_cap_num = 0


        cap = cv2.VideoCapture(self.rtsp_url)
        while not self.thread_exit:
            ret, frame = cap.read()
            if ret:
                exit_frame_num = 0
                exit_cap_num = 0
                try:
                    self.q.put(frame, block=True, timeout=3)

                except queue.Full:
                    customPrint('队列已满，写入失败')
                # print(self.q.qsize())
            else:
                exit_frame_num += 1
                # 异常5次则重新读一下流
                if exit_frame_num >= 5:
                    customPrint(f"读流异常，已经开始{exit_frame_num}:{exit_cap_num}重新读流")
                    cap = cv2.VideoCapture(self.rtsp_url)
                    exit_cap_num += 1
                    # 读流异常5次则退出
                    if exit_cap_num == 5:
                        self.thread_exit = True

        customPrint(f'摄像头已经退出')
        cap.release()

