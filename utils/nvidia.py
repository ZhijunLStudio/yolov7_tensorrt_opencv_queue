import pynvml
from utils.myPrint import customPrint


UNIT = 1024 * 1024

def indexGPU():
    pynvml.nvmlInit() #初始化
    gpuDeviceCount = pynvml.nvmlDeviceGetCount()#获取Nvidia GPU块数
    gpudir = {}
    for i in range(gpuDeviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i) #获取GPU i的handle，后续通过handle来处理
        memoryInfo = pynvml.nvmlDeviceGetMemoryInfo(handle)#通过handle获取GPU i的信息

        customPrint(f"显存空闲率：{memoryInfo.free/memoryInfo.total}")
        gpudir[i] = memoryInfo.free/memoryInfo.total
        gpumin = max(gpudir.keys(),key=(lambda k:gpudir[k]))

    pynvml.nvmlShutdown() #最后关闭管理工具
    customPrint(f"选择第{gpumin}号GPU")
    return gpumin
