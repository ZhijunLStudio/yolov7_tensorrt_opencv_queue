import os
import cv2
import datetime
from utils.myPrint import customPrint

class GenerateJpgAndXml:
    """
    参数名含义：
    parentName:存放jpg和xml上一级文件夹名字,如person

    """
    def __init__(self, parentName, labelDict):
        self.parentName = parentName
        # 存放所有文件的主文件夹路径
        self.parentPath = os.path.join(os.getcwd(), "JpgAndXml")
        self.midPath = os.path.join(self.parentPath, self.parentName)
        # 存放jpg文件夹名字
        self.jpgName = "JPEGImages"
        # 存放xml文件夹名字
        self.xmlName = "Annotations"
        # 存放标签的字典
        self.labelDict = labelDict
        # 第一次进来，需要判断下文件夹是否存在
        self.isExist()

    def isExist(self):
        # 存放jpg文件的文件夹
        self.jpgPath = os.path.join(self.midPath, self.jpgName)
        # 存放xml文件的文件夹
        self.xmlPath = os.path.join(self.midPath, self.xmlName)
        # 判断jpg和xml文件夹是否存在，不存在则创建
        for perPath in [self.jpgPath, self.xmlPath]:
            # 判断所在目录下是否有该文件名的文件夹
            if not os.path.exists(perPath):
                # 创建多级目录用mkdirs
                print(f"创建成功，已创建文件夹{perPath}")
                os.makedirs(perPath)
            else:
                print(f"创建失败，已存在文件夹{perPath}")


    def generatr_xml(self, frame, result):
        # print('开始写xml')
        # 获取当前时间戳
        xmlPrefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        # print(xmlPrefix)
        hwc = frame.shape
        # jpg名字
        jpgName = xmlPrefix + ".jpg"
        # jpg路径
        jpgPath = os.path.join(self.jpgPath, jpgName)
        # 写图片
        cv2.imwrite(jpgPath, frame)
        # xml路径
        xmlPath = os.path.join(self.xmlPath, xmlPrefix + ".xml")
        with open(xmlPath, 'w') as xml_file:
            xml_file.write('<annotation>\n')
            xml_file.write('\t<folder>' + self.parentName +'</folder>\n')
            xml_file.write('\t<filename>' + jpgName + '</filename>\n')
            xml_file.write('\t<path>' + jpgPath + '</path>\n')
            xml_file.write('\t<source>\n')
            xml_file.write('\t\t<database>' + 'Unknown' + '</database>\n')
            xml_file.write('\t</source>\n')
            xml_file.write('\t<size>\n')
            xml_file.write('\t\t<width>' + str(hwc[1]) + '</width>\n')
            xml_file.write('\t\t<height>' + str(hwc[0]) + '</height>\n')
            xml_file.write('\t\t<depth>'+str(hwc[2])+'</depth>\n')
            xml_file.write('\t</size>\n')
            xml_file.write('\t<segmented>0</segmented>\n')

            for re in result:
                ObjName = self.labelDict[re[0]]

                xmin = int(re[2])
                ymin = int(re[3])
                xmax = int(re[4])
                ymax = int(re[5])

                xml_file.write('\t<object>\n')
                xml_file.write('\t\t<name>' + ObjName + '</name>\n')
                xml_file.write('\t\t<pose>Unspecified</pose>\n')
                xml_file.write('\t\t<truncated>0</truncated>\n')
                xml_file.write('\t\t<difficult>0</difficult>\n')
                xml_file.write('\t\t<bndbox>\n')
                xml_file.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                xml_file.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                xml_file.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                xml_file.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                # xml_file.write('\t\t\t<angle>' + str(4) + '</angle>\n')
                xml_file.write('\t\t</bndbox>\n')
                # xml_file.write('\t\t<extra/>\n')
                xml_file.write('\t</object>\n')
            xml_file.write('</annotation>')
        customPrint(f"{jpgPath}的jpg和xml已写入")






# NEW = GenerateJpgAndXml("PERSON")
