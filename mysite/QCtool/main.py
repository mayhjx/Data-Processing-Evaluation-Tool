from math import fsum, pow, sqrt
from statistics import mean, stdev

from .models import QCframe, QCrecord, IonRatioFrame


class Evaluation(object):

    ''' 功能：数据处理质量评估
    对曲线回收率，线性，试剂空白，信噪比, 样品内标响应，保留时间，内标保留时间，质控值，定位孔值进行判断和评分'''

    # 返回包含分数和具体违反点的字典 
    # e.g. {'score': 10, 'violation': ["...","..."]} 
    
    # __slots__ = ()
    def __init__(self, 
                SampleName, 
                ActualConc, 
                Conc, 
                RT, 
                ISRT, 
                SN, 
                Area, 
                ISArea, 
                R, 
                USED, 
                ACCURACY, 
                IonRatio,
                LOCATE):
        self.SampleName = SampleName # 实验号
        self.ActualConc = ActualConc # 理论浓度
        self.CONC = Conc # 浓度
        self.RT = RT # 保留时间
        self.ISRT = ISRT # 内标保留时间
        self.SN = SN # 信噪比
        self.Area = Area # 峰面积
        self.ISArea = ISArea # 内标面积
        self.R = R # 相关系数
        self.USED = USED # 用于判断某个曲线点是否用于定量
        self.ACCURACY = ACCURACY # 曲线回收率
        self.IonRatio = IonRatio # 
        self.LOCATE = LOCATE  # 定位孔实验号前缀
        
        self.DEBUG = False # 调试开关

    def index(self, data, target):
        # 返回target在data[0]中的位置
        try:
            head = data[0]
            position = head.index(target)
        except Exception as e:
            if self.DEBUG: print(e)
            return
        else:
            return position

    def get_accuracy(self, data):

        ''' 1. 所有曲线点回收率都在(90%-110%)之间，得10分
        2. 当有一个曲线点回收率在[85%, 90%]或[110%, 115%]时，扣0.5分
        3. 某一个曲线点回收率小于85%或大于115%，得0分
        4. 舍去一个点扣1分，舍去两个点直接0分'''

        dic = dict()
        dic['score'] = 10
        dic['violation'] = list()
        numunUsed = 0

        samplename = self.index(data, self.SampleName)
        accuracy = self.index(data, self.ACCURACY)
        used = self.index(data, self.USED)

        if samplename is None or not accuracy or len(data) == 1:
            dic['score'] = None
            return dic

        for std in data[1:]:
            if "STD" in std[samplename].upper() and not std[samplename].endswith("0"):
                try:
                    acc = float(std[accuracy])
                except:
                    # =N/A
                    continue

                if acc < 85 or acc > 115:
                    dic['score'] = 0
                    dic['violation'].append('{}: {:.1f}%'.format(std[samplename], acc))
                elif 85 <= acc <= 90 or 110 <= acc <= 115:
                    dic['score'] -= 0.5
                    dic['violation'].append('{}: {:.1f}%'.format(std[samplename], acc))
                else:
                    if self.DEBUG:
                        dic['violation'].append('{}: {:.1f}%'.format(std[samplename], acc))

                if used and (std[used].upper() == "FALSE" or std[used] == '' or 'X' in std[used]):
                    if dic['score'] > 0: dic['score'] -= 1
                    dic['violation'].append('{} 去点'.format(std[samplename]))
                    numunUsed += 1
                    if numunUsed == 2:
                        dic['score'] = 0
        
        return dic

    def get_r(self, data):

        '''比较R²值：
        1. R²>0.999: 10分
        2. 0.997<R²<=0.999: 9分
        3. 0.995<R²<=0.997: 8分
        4. R²<=0.995: 0分'''

        dic = dict()
        dic['violation'] = list()

        
        r = self.index(data, self.R)
        
        if not r:
            dic['score'] = None
            # samplename = self.index(data, self.SampleName)
            # Ratio = self.index(data, self.Ratio)
            # ActualConc = self.index(data, self.ActualConc)

            # 没办法算得跟仪器的结果一模一样
            # if Ratio and ActualConc:
            #     # 通过ratio和actualconc计算r
            #     ratio = list()
            #     actualconc = list()
            #     for std in data[1:]:
            #         if std[samplename].upper().startswith("STD"):
            #             ratio.append(std[Ratio])
            #             actualconc.append(std[ActualConc])
                
            #     R2 = self.count_R2_value(ratio, actualconc)
            #     R2 = round(R2, 3)
            # else:
            #     # 无法计算r
            #     dic['score'] = None
            return dic
        else:
            for std in data[1:]:
                if "R2" in self.R:
                    R2 = round(float(std[r]), 3)
                    break
                else:
                    R2 = round(pow(float(std[r]), 2), 3)
                    break

        if self.DEBUG: print("R2", R2)

        if R2 > 0.999:
            dic['score'] = 10
            if self.DEBUG:
                dic['violation'].append('R²: {:.3f}'.format(R2))
        elif R2 > 0.997:
            dic['score'] = 9
            dic['violation'].append('R²: {:.3f}'.format(R2))
        elif R2 > 0.995:
            dic['score'] = 8
            dic['violation'].append('R²: {:.3f}'.format(R2))
        elif R2 <= 0.995:
            dic['score'] = 0
            dic['violation'].append('R²: {:.3f}'.format(R2))

        return dic
    
    # def count_R2_value(self, ratio, conc):
    #     # 普通最小二乘法
    #     # 返回相关系数r
    #     # 来源: https://wiki.mbalib.com/wiki/%E7%9B%B8%E5%85%B3%E7%B3%BB%E6%95%B0

    #     n = len(ratio)

    #     ratio = [float(x) for x in ratio]
    #     conc = [float(y) for y in conc]
    #     x = ratio
    #     y = conc
    #     x2 = [pow(x, 2) for x in ratio]
    #     y2 = [pow(y, 2) for y in conc]
    #     xy = [x*y for x, y in zip(ratio,conc)]

    #     r = (n * fsum(xy) - fsum(x) * fsum(y)) / (sqrt(n * fsum(x2) - pow(fsum(x), 2)) * (sqrt(n * fsum(y2) - pow(fsum(y), 2))))

    #     return pow(r,2)

    def get_LLMI(self, data):

        '''计算STD0峰面积与STD1峰面积的比值：
        1. 比值<10%: 10分
        2. 10%<=比值<15%: 9分
        3. 15%<=比值<20%: 8分
        4. 比值>=20%: 0分'''

        dic = dict()
        dic['score'] = 0
        dic['violation'] = list()

        samplename = self.index(data, self.SampleName)
        area = self.index(data, self.Area)

        if samplename is None or not area:
            dic['score'] = None
            return dic

        for std in data[1:]:
            if std[samplename].upper().startswith("STD") and std[samplename].upper().endswith("0"):
                std0_area = float(std[area])
                break

        for std in data[1:]:
            if std[samplename].upper().startswith("STD") and std[samplename].upper().endswith("1"):
                std1_area = float(std[area])
                break

        if std0_area is None or std1_area is None:
            dic['score'] = None
            return dic

        percent = round(std0_area / std1_area, 2)

        if percent < 0.1:
            dic['score'] = 10
            if self.DEBUG: dic['violation'].append('比值: {:.0%}'.format(percent))
        elif percent < 0.15:
            dic['score'] = 9
            dic['violation'].append('比值: {:.0%}'.format(percent))
        elif percent < 0.2:
            dic['score'] = 8
            dic['violation'].append('比值: {:.0%}'.format(percent))
        elif percent >= 0.2:
            dic['score'] = 0
            dic['violation'].append('比值: {:.0%}'.format(percent))

        return dic

    def get_sn(self, data):

        '''	比较STD1 SN的值：
        1. SN>30: 10分
        2. 20<SN<=30: 9分
        3. 10<SN<=20: 8分
        4. SN<=10: 0分'''

        dic = dict()
        dic['score'] = 0
        dic['violation'] = list()

        sn = self.index(data, self.SN)
        samplename = self.index(data, self.SampleName)

        if samplename is None or not sn:
            dic['score'] = None
            return dic

        for std in data[1:]:
            if std[samplename].upper().startswith("STD") and std[samplename].endswith("1"):
                std1 = float(std[sn])
                if std1 > 30:
                    dic['score'] = 10
                    if self.DEBUG:
                        dic['violation'].append('{}: {:.0f}'.format(std[samplename], std1))
                elif std1 > 20:
                    dic['score'] = 9
                    dic['violation'].append('{}: {:.0f}'.format(std[samplename], std1))
                elif std1 > 10:
                    dic['score'] = 8
                    dic['violation'].append('{}: {:.0f}'.format(std[samplename], std1))
                elif std1 <= 10:
                    dic['score'] = 0
                    dic['violation'].append('{}: {:.0f}'.format(std[samplename], std1))
                return dic
        else:
            dic['score'] = None

        return dic

    def get_isarea(self, data):

        '''比较当批临床样（不包括BLANK，TEST，曲线，质控和定位孔）内标的CV：
        1. CV<5%: 10分
        2. 5<=CV<10%: 9分
        3. 10%<=CV<15%: 8分
        4. CV>=15%: 0分
        5. 只要有一个内标信号超过批内平均信号的±30%, 则得0分'''

        dic = dict()
        dic['score'] = 0
        dic['violation'] = list()

        samplename = self.index(data, self.SampleName)
        istd = self.index(data, self.ISArea)

        if samplename is None or not istd:
            dic['score'] = None
            return dic

        exceptPreName = ('BLANK', 'TEST', 'STD', 'QC', 'X', 'WASH')

        name_list = list()
        is_list = list()
        for sample in data[1:]:
            if not sample[samplename].upper().startswith(exceptPreName):
                name_list.append(sample[samplename])
                is_list.append(float(sample[istd]))

        is_mean = mean(is_list)
        if len(is_list) > 1:
            is_std = stdev(is_list)
        else:
            is_std = 0
        is_cv = round(is_std / is_mean, 2)

        if is_cv < 0.05:
            dic['score'] = 10
            if self.DEBUG:
                dic['violation'].append("CV: {:.0%}".format(is_cv))
        elif is_cv < 0.10:
            dic['score'] = 9
            dic['violation'].append("CV: {:.0%}".format(is_cv))
        elif is_cv < 0.15:
            dic['score'] = 8
            dic['violation'].append("CV: {:.0%}".format(is_cv))
        elif is_cv >= 0.15:
            dic['score'] = 0
            dic['violation'].append("CV: {:.0%}".format(is_cv))

        for i, area in enumerate(is_list):
            if abs(area - is_mean) / is_mean > 0.3:
                dic['score'] = 0
                dic['violation'].append('{0} IS Area({1:.0f}) is abnormal'.format(name_list[i], area))

        return dic

    def get_rt(self, data):

        '''比较当批样品（不包括BLANK，TEST和定位孔）保留时间的CV：
        1. CV<=3%: 10分
        2. 3%<CV<=4%: 9分
        3. 4%<CV<=5%: 8分
        4. CV>5%: 0分
        5. 每当有一个样品保留时间与其均值的差异超过±0.1min时扣1分'''

        dic = dict()
        dic['score'] = 0
        dic['violation'] = list()

        samplename = self.index(data, self.SampleName)
        rt = self.index(data, self.RT)

        if samplename is None or not rt:
            dic['score'] = None
            return dic

        exceptPreName = ('BLANK', 'TEST', 'X', 'WASH')

        name_list = list()
        rt_list = list()
        for sample in data[1:]:
            if not sample[samplename].upper().startswith(exceptPreName):
                name_list.append(sample[samplename])
                rt_list.append(float(sample[rt]))

        rt_mean = mean(rt_list)
        if len(rt_list) > 1:
            rt_std = stdev(rt_list)
        else:
            rt_std = 0 # 无样或只有一个样时CV取0
        rt_cv = round(rt_std / rt_mean, 2)

        if rt_cv <= 0.03:
            dic['score'] = 10
            if self.DEBUG:
                dic['violation'].append("CV: {:.0%}".format(rt_cv))
        elif rt_cv <= 0.04:
            dic['score'] = 9
            dic['violation'].append("CV: {:.0%}".format(rt_cv))
        elif rt_cv <= 0.05:
            dic['score'] = 8
            dic['violation'].append("CV: {:.0%}".format(rt_cv))
        elif rt_cv > 0.05:
            dic['score'] = 0
            dic['violation'].append("CV: {:.0%}".format(rt_cv))

        for i, v in enumerate(rt_list):
            if abs(v - rt_mean) > 0.1:
                if dic['score'] > 0 : dic['score']  -= 1
                dic['violation'].append('{0} RT({1:.2f}) is abnormal'.format(name_list[i], v))

        return dic

    def get_isrt(self, data):

        '''比较当批样品（不包括BLANK，TEST和定位孔）内标保留时间的CV：
        1. CV<=3%: 10分
        2. 3%<CV<=4%: 9分
        3. 4%<CV<=5%: 8分
        4. CV>5%: 0分
        5. 每当有一个样品内标保留时间与其均值的差异超过±0.1min时扣1分'''

        dic = dict()
        dic['score'] = 0
        dic['violation'] = list()

        samplename = self.index(data, self.SampleName)
        isrt = self.index(data, self.ISRT)

        if samplename is None or not isrt:
            dic['score'] = None
            return dic

        exceptPreName = ('BLANK', 'TEST', 'X', 'WASH')

        name_list = list()
        isrt_list = list()
        for sample in data[1:]:
            if not sample[samplename].upper().startswith(exceptPreName):
                name_list.append(sample[samplename])
                isrt_list.append(float(sample[isrt]))

        isrt_mean = mean(isrt_list)

        if len(isrt_list) > 1:
            isrt_std = stdev(isrt_list)
        else:
            isrt_std = 0
        isrt_cv = round(isrt_std / isrt_mean, 2)

        if isrt_cv <= 0.03:
            dic['score'] = 10
            if self.DEBUG:
                dic['violation'].append("CV: {:.0%}".format(isrt_cv))
        elif isrt_cv <= 0.04:
            dic['score'] = 9
            dic['violation'].append("CV: {:.0%}".format(isrt_cv))
        elif isrt_cv <= 0.05:
            dic['score'] = 8
            dic['violation'].append("CV: {:.0%}".format(isrt_cv))
        elif isrt_cv > 0.05:
            dic['score'] = 0
            dic['violation'].append("CV: {:.0%}".format(isrt_cv))

        for i, v in enumerate(isrt_list):
            if abs(v - isrt_mean) > 0.1:
                if dic['score'] > 0 : dic['score']  -= 1
                dic['violation'].append('{0} RT({1}) is abnormal'.format(name_list[i], v))
                
        return dic


    def get_qc(self, data, instrument, item):
        
        # 根据质控前缀 name[:-1] 判断是否是同一种质控
        # 运行时存放同一种质控的水平一的rsd值，后续跟水平二rsd一起判断
        # 框架和RSD结果数据库里面的质控编号需要实际的对应

        # R4S 指对于两个水平的质控，同一组质控最高测量值与最低测量值一个大于+2S，一个小于-2S
         
        '''1. 将质控值与质控框架的mean和SD比较
        2. 所有质控值均在mean±2SD内: 10分
        3. 每当有一个质控值违反质控规则1-2S时扣1分
        4. 违反质控规则1-3S: 0分'''

        dic = dict()
        dic['score'] = 10
        dic['violation'] = list()
        # QC_prefix = None # 质控前缀
        # levelone_sd = 0 # 存放同一对质控的质控一 rsd值
        # isQC2 = False
        foundQC = False

        samplename = self.index(data, self.SampleName)
        conc = self.index(data, self.CONC)

        if samplename is None or not conc:
            dic['score'] = None
            return dic

        for sample in data[1:]: 
            qc_name = sample[samplename].upper().split("-")[0]
            if not qc_name.startswith("QC"): continue
            
            frame = QCframe.objects.filter(instrument=instrument, qc_name=qc_name, item=item)

            if frame.exists():
                foundQC = True
                mean = frame[0].mean
                sd = frame[0].sd
                rsd = round((float(sample[conc]) - mean) / sd,2)

                # if not QC_prefix:
                #     QC_prefix = qc_name
                #     levelone_name = sample[samplename]
                #     levelone_sd = rsd
                #     isQC2 = False
                # else:
                #     isQC2 = True

                # get latest qc record
                # last_record = QCrecord.objects.filter(instrument=instrument, qc_name=qc_name, item=item).last()
                
                if self.DEBUG: 
                    print("{} {} conc: {} rsd: {}".format(item, sample[samplename], sample[conc], rsd))
                    # print("上一个质控信息", last_record)
        
                # if last_record:
                #     last_rsd = last_record.qc_result
                # else:
                #     last_rsd = 0

                QCrecord.objects.create(instrument=instrument, item=item, qc_name=qc_name, qc_result=rsd)

                if self.DEBUG:
                    dic['violation'].append("{}: {} sd".format(sample[samplename], rsd))

                # 前一组2S判断，只在判断第一组质控的时候加入前一组质控信息
                # if abs(last_rsd) > 2 and abs(rsd) > 2:
                #     dic['violation'].append("(前一组 {}: {} sd)".format(last_record.qc_name, last_record.qc_result))

                if abs(rsd) > 3:
                    dic['score'] = 0
                    dic['violation'].append("{}: {} sd".format(sample[samplename], rsd))
                    dic['violation'].append("******13S******")
                elif abs(rsd) > 2:
                    if dic['score'] > 0: 
                        dic['score'] -= 1
                    dic['violation'].append("{}: {} sd".format(sample[samplename], rsd))
                    dic['violation'].append("******12S******")
                
                # # 前后组22S
                # if (last_rsd > 2 and rsd > 2) or (last_rsd < -2 and rsd < -2):
                #     dic['score'] = 0
                #     dic['violation'].append("******22S******")

                # # 同一组质控22S R4S判断
                # if isQC2:
                #     if (levelone_sd > 2 and rsd < -2) or (levelone_sd < -2 and rsd > 2):
                #         dic['score'] = 0
                #         # 显示违反R4S规则的质控信息
                #         if abs(levelone_sd) < 2:
                #             dic['violation'].append("{}: {} sd".format(levelone_name, levelone_sd))
                #         if abs(rsd) < 2:
                #             dic['violation'].append("{}: {} sd".format(sample[samplename], rsd))
                        
                #         dic['violation'].append("******R4S******")
                #     elif abs(levelone_sd) > 2 and abs(rsd) > 2:
                #         dic['score'] = 0
                #         dic['violation'].append("******22S******")
                #     isQC2 = False
                #     QC_prefix = None

        # 不存在质控
        if not foundQC:
            dic['score'] = None

        return dic

    def get_locate(self, data):

        '''判断定位孔浓度：
        1. >1：0分
        2. <=1:10分'''

        dic = dict()
        dic['violation'] = list()

        samplename = self.index(data, self.SampleName)
        conc = self.index(data, self.CONC)

        if samplename is None or not conc:
            dic['score'] = None
            return dic

        for sample in data[1:]:
            if sample[samplename].startswith(self.LOCATE):
                if sample[conc] == '< 0':
                    dic['score'] = 10
                    if self.DEBUG:
                        dic['violation'].append("{}: {}".format(sample[samplename], sample[conc]))
                elif float(sample[conc]) <= 1:
                    dic['score'] = 10
                    if self.DEBUG:
                        dic['violation'].append("{}: {:.2f}".format(sample[samplename], float(sample[conc])))
                elif float(sample[conc]) > 1:
                    dic['score'] = 0
                    dic['violation'].append("{}: {:.2f}".format(sample[samplename], float(sample[conc])))

        return dic

    def get_Ion_Ratio(self, data, LOQ, instrument, item):

        '''判断Ion Ratio值：
        先判断样品浓度是否大于某个值（自定义值或项目LOQ）
        再与仪器设定的Ion Raio标准值进行比较
        通过标准：比率<±20%'''

        dic = dict()
        dic['less_than_LOQ'] = 0
        dic['greater_than_LOQ'] = 0
        dic['Pass_num'] = 0
        dic['NoPass_num'] = 0

        dic['violation'] = list()

        samplename = self.index(data, self.SampleName)
        conc = self.index(data, self.CONC)
        ionRatio = self.index(data, self.IonRatio)

        greaterThanLOQ = 0
        lessThanLOQ = 0
        PassNum = 0
        NotPassNum = 0

        try:
            IonRatio = IonRatioFrame.objects.filter(instrument=instrument, item=item)[0]
        except:
            return dic

        if samplename is None or not conc or not ionRatio:
            dic['score'] = None
            return dic

        for sample in data[1:]:
            try:
                sampleconc = float(sample[conc])
                sampleIonRatio = float(sample[ionRatio])
            except:
                continue
            
            if sampleconc <= LOQ:
                lessThanLOQ += 1
            else:
                greaterThanLOQ += 1
                if abs(sampleIonRatio / IonRatio.IonRatio - 1) < 0.2:
                    PassNum += 1
                else:
                    NotPassNum += 1
                    dic['violation'].append(sample[samplename])
        
        dic['target_Ion_Ratio'] = IonRatio.IonRatio
        dic['less_than_LOQ'] = lessThanLOQ
        dic['greater_than_LOQ'] = greaterThanLOQ
        dic['Pass_num'] = PassNum
        dic['NoPass_num'] = NotPassNum
        return dic