import os
import cv2
from cv2 import getTickCount, getTickFrequency
from queue import Queue
import queue

from algorithm.yolov7_trt import TRT_engine
from algorithm.yolov7_trt import visualize
from utils.myPrint import customPrint
from utils.generateXml import GenerateJpgAndXml
from utils.nvidia import indexGPU
from utils.frameThread import FrameThread


if __name__ == '__main__':
    # 根据自己模型和摄像头信息，修改1、2、3即可
    # 1.放在model文件夹下tensorrt引擎的名字
    trt_name = "best.engine"
    # 2.rtsp地址，如果使用的是USB摄像头或者其他板载摄像头，可以更改为0（没有引号）
    RtspUrl = "rtsp://admin:ztt12345@20.21.43.104:554/Streaming/Channels/101"
    # 3.自动生成xml配置——标签字典，需要按照{"配置后的文件夹名": {0: "标签1", 1: "标签2", 2: "标签3"...}}进行配置
    label_dict = {'person': {0: 'person'}}
    # 根据gpu使用情况获取占用率低的GPU编号
    gpu_id = indexGPU()

    # 获取当前路径
    trt_path = os.path.join(os.getcwd(), "model", trt_name)
    # 第一个参数为预测图的大小，第二个参数为模型路径，第三个参数为选用第几号GPU
    trt_engine = TRT_engine(imgsz=640, weight=trt_path, GPUId=0)
    # trt_engine = TRT_engine(imgsz=640, weight=trt_path, GPUId=gpu_id)

    # 新建保存xml的文件夹
    label_dict_key = list(label_dict.keys())[0]
    label_dict_value = list(label_dict.values())[0]
    car_write_xml = GenerateJpgAndXml(label_dict_key, label_dict_value)

    # 新建一个队列，用来存放图像数组
    q = Queue()
    # 多线程对象
    thread = FrameThread(RtspUrl, q)
    # 设置读图线程为守护线程
    thread.setDaemon(True)
    # 启动读图线程
    thread.start()
    while True:
        try:
            loop_start = getTickCount()
            # 获取一帧图像
            frame = q.get(block=True, timeout=3)
            results = trt_engine.predict(frame, threshold=0.5)
            # 结果可视化
            frame = visualize(frame, results)
            # FPS计时
            loop_time = getTickCount() - loop_start
            total_time = loop_time / (getTickFrequency())
            FPS = 1 / total_time

            # 左上角文字信息
            cv2.putText(frame, f"FPS: {int(FPS)}", (0, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 2)
            cv2.putText(frame, "Press q to exit", (0, 200), cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 100, 200), 2)

            out_win = "yolov7_trt_output"
            cv2.namedWindow(out_win, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(out_win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(out_win, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except queue.Empty:
            print('队列为空，get失败')

    customPrint("----------------------所有程序已结束----------------------")