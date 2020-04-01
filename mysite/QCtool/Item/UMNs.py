from statistics import mean, stdev
from datetime import date
import xml.dom.minidom as dom

from QCtool.main import Evaluation
from QCtool.models import QCframe, QCrecord

class UMNs(Evaluation):

    def __init__(self, f, instrument_num, instrument_type):
        self.f = f
        self.instrument_num = instrument_num
        self.instrument_type = instrument_type
        self.instrument_prefix = 'FXS-'
        self.MN = "MN" # 包含3个项目 MN NMN 3-MT
        self.NMN = "NMN"
        self.MT = "3-MT"
        if self.instrument_type == "WATERS":
            self.delimiter = '\t'
            self.Component = "Component Name" 
            self.NAME = 'Sample Name'
            self.ActualConc = "Actual Concentration"
            self.CONC = 'Calculated Concentration'
            self.ACCURACY = 'Accuracy'
            self.SN = 'Signal / Noise'
            self.USED = 'Used'
            self.R = 'R2'
            self.Area = 'Area'
            self.ISArea = 'IS Area'
            self.IonRatio = None
            self.RT = 'Retention Time'
            self.ISRT = 'IS Retention Time'
            self.LOCATE = None  # 定位孔实验号前缀

        super().__init__(self.NAME,
                         self.ActualConc,
                         self.CONC,
                         self.RT,
                         self.ISRT,
                         self.SN,
                         self.Area,
                         self.ISArea,
                         self.R,
                         self.USED,
                         self.ACCURACY,
                         self.IonRatio,
                         self.LOCATE,
                         )

    def reader(self, decoding='utf-8'):

        # InMemoryFile to list
        data = ""
        for line in self.f:
            data = data + line.decode()
        return data

    def WATERS_data_format(self):
        # WATERS数据转换
        data = self.reader()
        
        with dom.parseString(data) as DOMTree:
            collection = DOMTree.documentElement
            samples = collection.getElementsByTagName("SAMPLE") # 样品信息元素
            calibration = collection.getElementsByTagName("CALIBRATIONDATA")[0] # 曲线信息元素

            # 项目
            items = ['MN', 'NMN', '3-MT']
            # 标题 
            head = [self.NAME,
                    self.Component,
                    self.ActualConc,
                    self.CONC,
                    self.ACCURACY,
                    self.SN,
                    self.USED,
                    self.Area,
                    self.RT,
                    self.ISArea,
                    self.ISRT,
                    self.R,
                    ]

            dic = dict()
            dic[items[0]] = list()
            dic[items[1]] = list()
            dic[items[2]] = list()
            dic[items[0]].append(head)
            dic[items[1]].append(head)
            dic[items[2]].append(head)

            for sample in samples:
                for i in range(len(items)):
                    info = []

                    # 化合物元素
                    curCompound = sample.getElementsByTagName("COMPOUND")[i]
                    # 待测物峰元素
                    curPeak = curCompound.getElementsByTagName("PEAK")[0]
                    # 内标峰元素
                    curISPeak = curCompound.getElementsByTagName("ISPEAK")[0]

                    info.append(sample.getAttribute("sampleid")) # 实验号

                    info.append(curCompound.getAttribute("name")) # 化合物名称
                    info.append(curCompound.getAttribute("stdconc")) # 理论浓度
    
                    info.append(curPeak.getAttribute("analconc")) # 实际浓度
                    info.append(curPeak.getAttribute("percrecovery")) # 回收率
                    info.append(curPeak.getAttribute("signoise")) # SN
                    info.append(curPeak.getAttribute("pkflags")) # 曲线去点信息
                    info.append(curPeak.getAttribute("area")) # 峰面积
                    info.append(curPeak.getAttribute("foundrt")) # 样品RT
                    info.append(curISPeak.getAttribute("area")) # IS Area
                    info.append(curISPeak.getAttribute("foundrt")) # IS RT

                    info.append(calibration.getElementsByTagName("COMPOUND")[i]
                                            .getElementsByTagName("CURVE")[0]
                                            .getElementsByTagName("DETERMINATION")[0]
                                            .getAttribute("rsquared")) # 线性

                    dic[items[i]].append(info)    

        return dic


    def get_dic_data(self):

        if self.instrument_type == "WATERS":
            dic = self.WATERS_data_format()

        return dic

    def output(self):

        dic = self.get_dic_data()

        if not dic: 
            raise IOError("无法识别原始数据格式")
        
        output = dict()

        output["accuracy_doc"] = self.get_accuracy.__doc__
        output["r_doc"] = self.get_r.__doc__
        output["LLMI_doc"] = self.get_LLMI.__doc__
        output["sn_doc"] = self.get_sn.__doc__
        output["isarea_doc"] = self.get_isarea.__doc__
        output["rt_doc"] = self.get_rt.__doc__
        output["isrt_doc"] = self.get_isrt.__doc__
        output["qc_doc"] = self.get_qc.__doc__
        
        output["MN_accuracy"] = self.get_accuracy(dic[self.MN])
        output["MN_r"] = self.get_r(dic[self.MN])
        output["MN_LLMI"] = self.get_LLMI(dic[self.MN])
        output["MN_sn"] = self.get_sn(dic[self.MN])
        output["MN_isarea"] =self.get_isarea(dic[self.MN])
        output["MN_rt"] = self.get_rt(dic[self.MN])
        output["MN_isrt"] = self.get_isrt(dic[self.MN])
        output["MN_qc"] = self.get_qc(dic[self.MN],  self.instrument_prefix + self.instrument_num, self.MN)

        output["NMN_accuracy"] = self.get_accuracy(dic[self.NMN])
        output["NMN_r"] = self.get_r(dic[self.NMN])
        output["NMN_LLMI"] = self.get_LLMI(dic[self.NMN])
        output["NMN_sn"] = self.get_sn(dic[self.NMN])
        output["NMN_isarea"] =self.get_isarea(dic[self.NMN])
        output["NMN_rt"] = self.get_rt(dic[self.NMN])
        output["NMN_isrt"] = self.get_isrt(dic[self.NMN])
        output["NMN_qc"] = self.get_qc(dic[self.NMN],  self.instrument_prefix + self.instrument_num, self.NMN)

        output["MT_accuracy"] = self.get_accuracy(dic[self.MT])
        output["MT_r"] = self.get_r(dic[self.MT])
        output["MT_LLMI"] = self.get_LLMI(dic[self.MT])
        output["MT_sn"] = self.get_sn(dic[self.MT])
        output["MT_isarea"] =self.get_isarea(dic[self.MT])
        output["MT_rt"] = self.get_rt(dic[self.MT])
        output["MT_isrt"] = self.get_isrt(dic[self.MT])
        output["MT_qc"] = self.get_qc(dic[self.MT],  self.instrument_prefix + self.instrument_num, self.MT)

        output["total_MN_score"] = 0
        output["total_NMN_score"] = 0
        output["total_MT_score"] = 0

        for k, v in output.items():
            if k.startswith(self.MN) and v['score']:
                output["total_MN_score"] += float(v['score'])
            elif k.startswith(self.NMN) and v['score']:
                output["total_NMN_score"] += float(v['score'])
            elif k.startswith("MT") and v['score']:
                output["total_MT_score"] += float(v['score'])

        return output