from statistics import mean, stdev
from datetime import date

from QCtool.main import Evaluation
from QCtool.models import QCframe, QCrecord

class PMNs(Evaluation):

    def __init__(self, f, instrument_num, instrument_type):
        self.f = f
        self.instrument_num = instrument_num
        self.instrument_type = instrument_type
        self.instrument_prefix = 'FXS-'
        self.MN = "MN" # 包含3个项目 MN NMN 3-MT
        self.NMN = "NMN"
        self.MT = "3-MT"
        if self.instrument_type == "AB":
            self.delimiter = '\t'
            self.Component = "Component Name" 
            self.NAME = 'Sample Name'
            self.ActualConc = "Actual Concentration"
            self.CONC = 'Calculated Concentration'
            self.ACCURACY = 'Accuracy'
            self.SN = 'Signal / Noise'
            self.USED = 'Used'
            self.R = 'Correlation Coefficient'
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
        data = list()
        for line in self.f.read().splitlines():
            data.append(line.decode(decoding).split(self.delimiter))
        return data

    def AB_data_format(self):

        data = self.reader()
        try:
            head = data[0]
            comp = head.index(self.Component)
        except:
            return

        dic = dict()

        Q = "-Q"
        dic[self.MN] = list()
        dic[self.MN].append(head)
        dic[self.MN].extend([d for d in data if d[comp].startswith(self.MN + Q)])

        dic[self.NMN] = list()
        dic[self.NMN].append(head)
        dic[self.NMN].extend([d for d in data if d[comp].startswith(self.NMN + Q)])

        dic[self.MT] = list()
        dic[self.MT].append(head)
        dic[self.MT].extend([d for d in data if d[comp].startswith(self.MT + Q)])

        return dic

    def get_dic_data(self):

        if self.instrument_type == "AB":
            dic = self.AB_data_format()

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