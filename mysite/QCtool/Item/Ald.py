from statistics import mean, stdev
from datetime import date

from QCtool.main import Evaluation
from QCtool.models import QCframe, QCrecord

class Ald(Evaluation):

    def __init__(self, f, instrument_num, instrument_type):
        self.f = f
        self.instrument_num = instrument_num
        self.instrument_type = instrument_type
        self.instrument_prefix = 'FXS-'
        self.Ald = "Ald"

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
            conc = head.index(self.CONC)
            comp = head.index(self.Component)
        except:
            return

        dic = dict()
        for d in data[-1:0:-1]:
            if "ALD-QUAN" not in d[comp]:
                data.remove(d)

        dic[self.Ald] = list()
        dic[self.Ald].append(head)
        dic[self.Ald].extend([d for d in data[1:]])

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

        output["ALD_accuracy"] = self.get_accuracy(dic[self.Ald])
        output["ALD_r"] = self.get_r(dic[self.Ald])
        output["ALD_LLMI"] = self.get_LLMI(dic[self.Ald])
        output["ALD_sn"] = self.get_sn(dic[self.Ald])
        output["ALD_isarea"] =self.get_isarea(dic[self.Ald])
        output["ALD_rt"] = self.get_rt(dic[self.Ald])
        output["ALD_isrt"] = self.get_isrt(dic[self.Ald])
        output["ALD_qc"] = self.get_qc(dic[self.Ald],  self.instrument_prefix + self.instrument_num, self.Ald)

        output["total_ALD_score"] = 0

        for k, v in output.items():
            if k.startswith(self.Ald.upper()) and v['score']:
                output["total_ALD_score"] += float(v['score'])
        return output
