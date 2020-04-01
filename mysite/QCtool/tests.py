import os.path

from django.test import Client, TestCase

from .main import Evaluation
from .models import QCframe, QCrecord


# Create your tests here.
class QCtoolTest(TestCase):

    def setUp(self):

        self.ABfilepath = r'QCtool\testfile\AB-YZ04-test.txt'
        self.Agilentfilepath = r'QCtool\testfile\Agilent-YZ07-test.csv'
        self.daojinfilepath = r'QCtool\testfile\daojin-YZ21-test.txt'
        self.NAME = 'Sample Name'
        self.ActualConc = "Actual Concentration"
        self.CONC = 'Calculated Concentration'
        self.ACCURACY = 'Accuracy'
        self.SN = 'Signal / Noise'
        self.USED = 'Used'
        self.R = 'R2 Correlation Coefficient'
        self.Area = 'Area'
        self.ISArea = 'IS Area'
        self.Ratio = 'Area Ratio'
        self.RT = 'Retention Time'
        self.ISRT = 'IS Retention Time'
        self.LOCATE = 'X'  # 定位孔实验号前缀
        self.c = Client()

        # 初始化AB标题
        self.evaluation = Evaluation(SampleName=self.NAME, 
                                ActualConc=self.ActualConc,
                                Conc=self.CONC,
                                RT=self.RT,
                                ISRT=self.ISRT,
                                SN=self.SN,
                                Area=self.Area,
                                ISArea=self.ISArea,
                                Ratio=self.Ratio,
                                R=self.R,
                                USED=self.USED,
                                ACCURACY=self.ACCURACY,
                                LOCATE=self.LOCATE,
                            )
        
    def test_upload(self):
        
        def get_response(filepath):
            filename = os.path.basename(filepath).split('-')
            with open(filepath, 'rb') as f:
                arg = {'instrument_type': filename[0], 'instrument_num':filename[1], 'file':f}
                response = self.c.post('/', arg)
            return response
            
        filepath = self.ABfilepath
        response = get_response(filepath)
        self.assertEqual(response.status_code, 200)

        filepath = self.Agilentfilepath
        response = get_response(filepath)
        self.assertEqual(response.status_code, 200)

        filepath = self.daojinfilepath
        response = get_response(filepath)
        self.assertEqual(response.status_code, 200)


    def test_index(self):

        data = [[self.NAME, self.ActualConc, self.CONC, self.RT, self.ISRT, self.Area, self.ISArea, self.Ratio, self.ACCURACY, self.R],
                [0,1,2,3,4,5,6,7,8,9]]

        self.assertEqual(self.evaluation.index(data, self.NAME), 0)
        self.assertEqual(self.evaluation.index(data, self.R), 9)


    def test_accuracy(self):

        data_nodata = [
            [self.NAME, self.ACCURACY, self.USED],
        ]


        data_noName = [
            ["self.NAME", self.ACCURACY, self.USED],
            ['STD-1', '100', 'True'],
            ['STD-2', '100', 'True'],
            ['STD-3', '100', 'True'],
            ['STD-4', '100', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '100', 'True'],
        ]

        data_noAccuracy = [
            [self.NAME, "self.ACCURACY", self.USED],
            ['STD-1', '100', 'True'],
            ['STD-2', '100', 'True'],
            ['STD-3', '100', 'True'],
            ['STD-4', '100', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '100', 'True'],
        ]

        # 10分数据
        data_10 = [
            [self.NAME, self.ACCURACY, self.USED],
            ['STD-1', '100', 'True'],
            ['STD-2', '100', 'True'],
            ['STD-3', '100', 'True'],
            ['STD-4', '100', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '100', 'True'],
        ]
        # 9分数据
        data_9 = [
            [self.NAME, self.ACCURACY, self.USED],
            ['STD-1', '86', 'True'],
            ['STD-2', '114', 'True'],
            ['STD-3', '100', 'True'],
            ['STD-4', '100', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '100', 'True'],
        ]
        # 回收率大于115
        data_gt115 = [
            [self.NAME, self.ACCURACY, self.USED],
            ['STD-1', '100', 'True'],
            ['STD-2', '100', 'True'],
            ['STD-3', '100', 'True'],
            ['STD-4', '100', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '116', 'True'],
        ]
        # 回收率小于85
        data_lt85 = [
            [self.NAME, self.ACCURACY, self.USED],
            ['STD-1', '100', 'True'],
            ['STD-2', '100', 'True'],
            ['STD-3', '100', 'True'],
            ['STD-4', '84', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '100', 'True'],
        ]
        # 舍去一个点
        data_lost_one_point = [
            [self.NAME, self.ACCURACY, self.USED],
            ['STD-1', '100', 'False'],
            ['STD-2', '100', 'True'],
            ['STD-3', '100', 'True'],
            ['STD-4', '100', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '100', 'True'],
        ]
        # 舍去两个点
        data_lost_two_point = [
            [self.NAME, self.ACCURACY, self.USED],
            ['STD-1', '100', 'False'],
            ['STD-2', '100', 'False'],
            ['STD-3', '100', 'True'],
            ['STD-4', '100', 'True'],
            ['STD-5', '100', 'True'],
            ['STD-6', '100', 'True'],
        ]

        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)
        self.assertEqual(self.evaluation.get_accuracy(data_noName)['score'], None)
        self.assertEqual(self.evaluation.get_accuracy(data_noAccuracy)['score'], None)

        self.assertEqual(self.evaluation.get_accuracy(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_accuracy(data_9)['score'], 9)
        self.assertEqual(self.evaluation.get_accuracy(data_gt115)['score'], 0)
        self.assertEqual(self.evaluation.get_accuracy(data_lt85)['score'], 0)
        self.assertEqual(self.evaluation.get_accuracy(data_lost_one_point)['score'], 9)
        self.assertEqual(self.evaluation.get_accuracy(data_lost_two_point)['score'], 0)

    def test_r(self):

        data_10=[
            [self.NAME, self.R],
            ['STD-0', '1.000']
        ]

        data_9=[
            [self.NAME, self.R],
            ['STD-0', '0.999']
        ]

        data_8=[
            [self.NAME, self.R],
            ['STD-0', '0.997']
        ]

        data_0=[
            [self.NAME, self.R],
            ['STD-0', '0.995']
        ]

        data_nordata = [
            [self.NAME, self.CONC],
        ]

        self.assertEqual(self.evaluation.get_accuracy(data_nordata)['score'], None)

        self.assertEqual(self.evaluation.get_r(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_r(data_9)['score'], 9)
        self.assertEqual(self.evaluation.get_r(data_8)['score'], 8)
        self.assertEqual(self.evaluation.get_r(data_0)['score'], 0)

    # def test_count_R2_value(self):

    #     ratio = ['0', '0.02', '0.06', '0.18', '0.44', '0.80', '1.58']
    #     conc = ['0', '0.091', '0.325', '0.998', '3.000', '4.338', '9.11']

    #     self.assertAlmostEqual(self.evaluation.count_R2_value(ratio, conc), 0.9957, places=4)

    def test_LLMI(self):

        data_10 = [
            [self.NAME, self.Area],
            ['STD-0', '9'],
            ['STD-1', '100'],
        ]

        data_9 = [
            [self.NAME, self.Area],
            ['STD-0', '11'],
            ['STD-1', '100'],
        ]

        data_8 = [
            [self.NAME, self.Area],
            ['STD-0', '19'],
            ['STD-1', '100'],
        ]

        data_0 = [
            [self.NAME, self.Area],
            ['STD-0', '21'],
            ['STD-1', '100'],
        ]

        data_nodata = [
            [self.NAME, self.Area],
        ]

        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)

        self.assertEqual(self.evaluation.get_LLMI(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_LLMI(data_9)['score'], 9)
        self.assertEqual(self.evaluation.get_LLMI(data_8)['score'], 8)
        self.assertEqual(self.evaluation.get_LLMI(data_0)['score'], 0)
    
    def test_SN(self):
        
        data_10 = [
            [self.NAME, self.SN],
            ['STD-1', '31'],
        ]

        data_9 = [
            [self.NAME, self.SN],
            ['STD-1', '30'],
        ]

        data_8 = [
            [self.NAME, self.SN],
            ['STD-1', '20'],
        ]

        data_0 = [
            [self.NAME, self.SN],
            ['STD-1', '10'],
        ]

        data_nodata = [
            [self.NAME, self.SN],
        ]

        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)

        self.assertEqual(self.evaluation.get_sn(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_sn(data_9)['score'], 9)
        self.assertEqual(self.evaluation.get_sn(data_8)['score'], 8)
        self.assertEqual(self.evaluation.get_sn(data_0)['score'], 0)


    def test_isarea(self):
        
        # 比较当批临床样内标的CV
        # CV<5%: 10分
        # 5<=CV<10%: 9分
        # 10%<=CV<15%: 8分
        # CV>=15%: 0分
        # 只要有一个内标信号超过批内平均信号的±30%, 则得0分

        from statistics import mean, stdev
        samplename = [self.NAME, 'STD-0','X', 'QC1', 'QC2','1', '2', '3', '4','5','6','7', '8', '9','10']

        # 程序应忽略STD, X, QC，只计算后十个数据
        isarea_10 = [self.ISArea, 0, 0, 1,100,  9,10,10,10,10,10,10,10,10,10]
        isarea_9 =  [self.ISArea, 0, 0, 1,100,  8,10,10,10,10,10,10,10,10,10]
        isarea_8 =  [self.ISArea, 0, 0, 1,100,  7,10,10,10,10,10,10,10,10,10]
        isarea_0 =  [self.ISArea, 0, 0, 1,100,  5,10,10,10,10,10,10,10,10,10]

        data_10 = list(zip(samplename, isarea_10))
        data_9 = list(zip(samplename, isarea_9))
        data_8 = list(zip(samplename, isarea_8))
        data_0 = list(zip(samplename, isarea_0))

        def get_cv(data):
            return stdev(data) / mean(data)

        # 只计算后面10个样的CV
        cv_10 = get_cv(isarea_10[-10:])
        cv_9 =  get_cv(isarea_9[-10:])
        cv_8 =  get_cv(isarea_8[-10:])
        cv_0 =  get_cv(isarea_0[-10:])

        # 判断CV大小
        self.assertLess(cv_10, 0.05)
        self.assertLess(cv_9, 0.1)
        self.assertLess(cv_8, 0.15)
        self.assertGreaterEqual(cv_0, 0.15)

        self.assertEqual(self.evaluation.get_isarea(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_isarea(data_9)['score'], 9)
        self.assertEqual(self.evaluation.get_isarea(data_8)['score'], 8)
        self.assertEqual(self.evaluation.get_isarea(data_0)['score'], 0)

        # 判断最后一种情况：只要有一个内标信号超过批内平均信号的±30%, 则得0分
        samplename = [str(i) for i in range(1,51)]
        isarea_onesampleabnormal = [10 for area in range(1,50)]
        isarea_onesampleabnormal.append(4.5)

        cv = get_cv(isarea_onesampleabnormal)
        self.assertEqual(len(isarea_onesampleabnormal), 50)
        self.assertLess(cv, 0.1)

        samplename.insert(0,self.NAME)
        isarea_onesampleabnormal.insert(0,self.ISArea)
        data_0 = list(zip(samplename, isarea_onesampleabnormal))
        self.assertEqual(self.evaluation.get_isarea(data_0)['score'], 0)

        data_nodata = [
            [self.NAME, self.ISArea],
        ]
        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)

        
    def test_rt(self):

        # 比较当批临床样保留时间的CV
        # CV<=3%: 10分
        # 3%<CV<=4%: 9分
        # 4%<CV<=5%: 8分
        # CV>5%: 0分
        # 每当有一个样品保留时间与其均值的差异超过±0.1min时扣1分

        data_10 = [
            [self.NAME, self.RT],
            ['STD-0', 10],
            ['QC1', 2],
            ['X1', 2],
            ['1', 2],
            ['2', 2],
            ['3', 2],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 0%

        data_9 = [
            [self.NAME, self.RT],
            ['STD-0', 10],
            ['QC1', 2],
            ['X1', 2],
            ['1', 2.09],
            ['2', 2.15],
            ['3', 2],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 4%

        data_8 = [
            [self.NAME, self.RT],
            ['STD-0', 10],
            ['QC1', 2],
            ['X1', 2],
            ['1', 2.25],
            ['2', 2],
            ['3', 2],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 4% 一个异常数据

        data_0 = [
            [self.NAME, self.RT],
            ['STD-0', 10],
            ['QC1', 2],
            ['X1', 2],
            ['1', 2.4],
            ['2', 2],
            ['3', 2],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 8% 一个异常数据

        data_nodata = [
            [self.NAME, self.RT],
        ]
        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)

        self.assertEqual(self.evaluation.get_rt(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_rt(data_9)['score'], 9)
        self.assertEqual(self.evaluation.get_rt(data_8)['score'], 8)
        self.assertEqual(self.evaluation.get_rt(data_0)['score'], 0)


    def test_isrt(self):

        # 比较当批临床样内标保留时间的CV
        # CV<=3%: 10分
        # 3%<CV<=4%: 9分
        # 4%<CV<=5%: 8分
        # CV>5%: 0分
        # 每当有一个样品内标保留时间与其均值的差异超过±0.1min时扣1分
        
        data_10 = [
            [self.NAME, self.ISRT],
            ['STD-0', 2],
            ['QC1', 2],
            ['X1', 2],
            ['1', 2],
            ['2', 2],
            ['3', 2],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 0%

        data_9 = [
            [self.NAME, self.ISRT],
            ['STD-0', 2],
            ['QC1', 2],
            ['X1', 2],
            ['1', 2.09],
            ['2', 2.15],
            ['3', 2],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 4%

        data_8 = [
            [self.NAME, self.ISRT],
            ['1', 2.15],
            ['2', 2.15],
            ['3', 2.14],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 4% 一个异常数据

        data_0 = [
            [self.NAME, self.ISRT],
            ['1', 2.4],
            ['2', 2],
            ['3', 2],
            ['4', 2],
            ['5', 2],
            ['6', 2],
            ['7', 2],
            ['8', 2],
            ['9', 2],
            ['10', 2],
        ] # CV: 8% 一个异常数据

        data_nodata = [
            [self.NAME, self.ISRT],
        ]
        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)

        self.assertEqual(self.evaluation.get_isrt(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_isrt(data_9)['score'], 9)
        self.assertEqual(self.evaluation.get_isrt(data_8)['score'], 8)
        self.assertEqual(self.evaluation.get_isrt(data_0)['score'], 0)


    def test_qc(self):

        # 将质控值与质控框架的mean和SD比较
        # 所有质控值均在mean±2SD内: 10分
        # 每当有一个质控值违反质控规则1-2S时扣1分
        # 违反质控规则1-3S、2-2S或R4S(可识别前后批): 0分

        Instrument = 'FXS-YZ04'
        item = 'D2'
        QC1 = 'QC1'
        QC2 = 'QC2'

        QCframe.objects.create(instrument=Instrument, item=item, qc_name=QC1, mean=3.0, sd=1.0)
        QCframe.objects.create(instrument=Instrument, item=item, qc_name=QC2, mean=3.0, sd=1.0)

        QC68 = QCframe.objects.filter(instrument=Instrument, item=item, qc_name=QC1)[0]
        QC69 = QCframe.objects.filter(instrument=Instrument, item=item, qc_name=QC2)[0]

        self.assertEqual(QC68.instrument, Instrument)
        self.assertEqual(QC68.item, item)
        self.assertEqual(QC68.qc_name, QC1)
        self.assertEqual(QC68.mean, 3)
        self.assertEqual(QC68.sd, 1)

        data_10 = [
            [self.NAME, self.CONC],
            [QC68.qc_name, QC68.mean + QC68.sd],
            [QC69.qc_name, QC69.mean - QC69.sd],
        ]

        data_12S = [
            [self.NAME, self.CONC],
            [QC68.qc_name, QC68.mean + 2.1*QC68.sd],
            [QC69.qc_name, QC69.mean - QC69.sd],
            [QC68.qc_name, QC68.mean + QC68.sd],
            [QC69.qc_name, QC69.mean - 2.1*QC69.sd],
        ]

        data_13S = [
            [self.NAME, self.CONC],
            [QC68.qc_name, QC68.mean + QC68.sd],
            [QC69.qc_name, QC69.mean - QC69.sd],
            [QC68.qc_name, QC68.mean + 3.1*QC68.sd],
            [QC69.qc_name, QC69.mean + QC69.sd],
            [QC68.qc_name, QC68.mean + QC68.sd],
            [QC69.qc_name, QC69.mean - 3.1*QC69.sd],
        ]

        # 同一组22S
        data_22S = [
            [self.NAME, self.CONC],
            [QC68.qc_name, QC68.mean + QC68.sd],
            [QC69.qc_name, QC69.mean - QC69.sd],
            [QC68.qc_name, QC68.mean - 2.1*QC68.sd],
            [QC69.qc_name, QC69.mean + 1*QC69.sd],
            [QC68.qc_name, QC68.mean + 2.1*QC68.sd],
            [QC69.qc_name, QC69.mean + 2.1*QC69.sd],
        ]

        # 前后组同一水平22S
        data_22S_samelevel = [
            [self.NAME, self.CONC],
            [QC68.qc_name, QC68.mean + 2.1*QC68.sd],
            [QC69.qc_name, QC69.mean + QC69.sd],
            [QC68.qc_name, QC68.mean + 2.1*QC68.sd],
            [QC69.qc_name, QC69.mean + QC69.sd],
            [QC68.qc_name, QC68.mean + QC68.sd],
            [QC69.qc_name, QC69.mean + 2.1*QC69.sd],
            [QC68.qc_name, QC68.mean + QC68.sd],
            [QC69.qc_name, QC69.mean - 2.5*QC69.sd],
        ]

        data_R4S = [
            [self.NAME, self.CONC],
            [QC68.qc_name, QC68.mean - 2.5*QC68.sd],
            [QC69.qc_name, QC69.mean + 2.1*QC69.sd],
            [QC68.qc_name, QC68.mean - QC68.sd],
            [QC69.qc_name, QC69.mean - 2.5*QC69.sd],
            [QC68.qc_name, QC68.mean + 2.5*QC68.sd],
            [QC69.qc_name, QC69.mean - 2.6*QC69.sd],
        ]

        def test_normal():
            result = self.evaluation.get_qc(data_10, Instrument, item)
            print("test normal QC", result)
            self.assertEqual(result['score'], 10)

        def test_12S():
            result = self.evaluation.get_qc(data_12S, Instrument, item)
            print("test 12S", result)
            self.assertEqual(result['score'], 8)

        def test_13S():
            result = self.evaluation.get_qc(data_13S, Instrument, item)
            print("test 13S", result)
            self.assertEqual(result['score'], 0)
            self.assertIn('******13S******', result['violation'])

        def test_22S():
            result = self.evaluation.get_qc(data_22S, Instrument, item)
            print("test 22S in diffent level", result)
            self.assertEqual(result['score'], 0)
            self.assertIn('******22S******', result['violation'])
        
        def test_22S_samelevel():
            result = self.evaluation.get_qc(data_22S_samelevel, Instrument, item)
            print("test 22S in same level", result)
            self.assertEqual(result['score'], 0)
            self.assertIn('******22S******', result['violation'])

        def test_R4S():
            result = self.evaluation.get_qc(data_R4S, Instrument, item)
            print("test R4S", result)
            self.assertEqual(result['score'], 0)
            self.assertIn('******R4S******', result['violation'])

        test_normal()
        test_12S()
        test_13S()
        test_22S()
        test_22S_samelevel()
        test_R4S()

        data_nodata = [
            [self.NAME, self.CONC],
        ]
        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)

    
    def test_locate(self):
        
        # 比较定位孔的浓度
        # 浓度<=1: 10分
        # 浓度>1: 0分

        data_10 = [
            [self.NAME, self.CONC],
            ['X1', '0.999'],
        ]

        data_lt0 = [
            [self.NAME, self.CONC],
            ['X2', '< 0'],
        ]

        data_0 = [
            [self.NAME, self.CONC],
            ['X1', '1.001'],
        ]

        data_nodata = [
            [self.NAME, self.CONC],
        ]

        self.assertEqual(self.evaluation.get_accuracy(data_nodata)['score'], None)

        self.assertEqual(self.evaluation.get_locate(data_10)['score'], 10)
        self.assertEqual(self.evaluation.get_locate(data_lt0)['score'], 10)
        self.assertEqual(self.evaluation.get_locate(data_0)['score'], 0)