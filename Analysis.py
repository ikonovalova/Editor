from PyQt5 import QtCore, QtGui, QtWidgets
import json

def try_except(function):
    """
    https://www.blog.pythonlibrary.org/2016/06/09/python-how-to-create-an-exception-logging-decorator/
    """
    import functools

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print("Exception in " + function.__name__ + ": " + repr(e))
            raise
    return wrapper


class Analysis(QtWidgets.QWidget):
    def __init__(self, elements, path, parent):
        super().__init__()
        self.data = elements #json
        self.filename = path  #current file
        self.parent = parent

        self.Precision = 0
        self.Recall = 0
        self.Av_Pr = 0
        self.Av_Recall = 0

        Analysis.load_data(self)
        Analysis.check_elem(self, self.report_data)
        Analysis.check_elem(self, self.data)
        Analysis.matching(self,self.data)
        Analysis.count_metrics(self,self.data)
        Analysis.count_Av_metrics(self,self.data)

        self.setWindowTitle("Analysis")
        vbox = QtWidgets.QVBoxLayout(self)

        hbox1 = QtWidgets.QHBoxLayout()
        text1 = QtWidgets.QLabel("Precision ")
        rez1 = QtWidgets.QLabel(str(self.Precision))
        hbox1.addWidget(text1)
        hbox1.addWidget(rez1)

        hbox2 = QtWidgets.QHBoxLayout()
        text2 = QtWidgets.QLabel("Recall ")
        rez2 = QtWidgets.QLabel(str(self.Recall))
        hbox2.addWidget(text2)
        hbox2.addWidget(rez2)

        hbox3 = QtWidgets.QHBoxLayout()
        text3 = QtWidgets.QLabel("Average Precision ")
        rez3 = QtWidgets.QLabel(str(self.Av_Pr))
        hbox3.addWidget(text3)
        hbox3.addWidget(rez3)

        hbox4 = QtWidgets.QHBoxLayout()
        text4 = QtWidgets.QLabel("Average Recall ")
        rez4 = QtWidgets.QLabel(str(self.Av_Recall))
        hbox4.addWidget(text4)
        hbox4.addWidget(rez4)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

    def load_data(self):
        if self.filename:
            report_filename = self.filename + '.report.json'
            with open(report_filename, "r+", encoding='utf-8') as r_file:
                self.report_data = json.load(r_file)

    @try_except
    def check_elem(self, elements):
        i = 0;
        while i < len(elements["Benchmarks"]):
            j = 0
            while j < len(elements["Benchmarks"][i]["group_ids"]):
                elements["Benchmarks"][i]["group_ids"][j]["check"] = 0
                elements["Benchmarks"][i]["group_ids"][j]["intersection"] = 0
                elements["Benchmarks"][i]["group_ids"][j]["FP_dupl"] = 1000000
                elements["Benchmarks"][i]["group_ids"][j]["FN_dupl"] = 1000000
                elements["Benchmarks"][i]["group_ids"][j]["F"] = 0
                elements["Benchmarks"][i]["group_ids"][j]["Prec_Dupl"] = 0
                elements["Benchmarks"][i]["group_ids"][j]["Recall_Dupl"] = 0

                j = j + 1
            i = i + 1

    @try_except
    def matching(self, elements):
        intersection = 0
        FP_dupl = 0
        FN_dupl = 0
        for text in elements["Benchmarks"]:
            child = text["group_ids"]
            for bench in child:
                for text1 in self.report_data["Benchmarks"]:
                    for report in text1["group_ids"]:
                        if (bench["position"][0] < report["position"][1]) and (bench["position"][1] > report["position"][0]):
                            report["check"] = 1
                            bench["check"] = 1

                            if (bench["position"][0] < report["position"][0]) and (bench["position"][1] < report["position"][1]):
                                intersection= bench["position"][1] - report["position"][0] + 1
                                FP_dupl = report["position"][1] - bench["position"][1]
                                FN_dupl = report["position"][0] - bench["position"][0]

                            if (report["position"][0] < bench["position"][0]) and (report["position"][1] < bench["position"][1]):
                                intersection = report["position"][1] - bench["position"][0] + 1
                                FP_dupl = bench["position"][0] - report["position"][0]
                                FN_dupl = bench["position"][1] - report["position"][1]

                            if (bench["position"][0] >= report["position"][0]) and (bench["position"][1] <= report["position"][1]):
                                intersection = bench["position"][1] - bench["position"][0] + 1
                                FP_dupl = (report["position"][1] - report["position"][0]) - (bench["position"][1] - bench["position"][0])
                                FN_dupl = 0

                            if (bench["position"][0] <= report["position"][0]) and (report["position"][1] <= bench["position"][1]):
                                intersection = report["position"][1] - report["position"][0] + 1
                                FP_dupl = 0
                                FN_dupl = (bench["position"][1] - bench["position"][0]) - (
                                        report["position"][1] - report["position"][0])

                            if (bench["position"][0] == report["position"][0]) and (report["position"][1] == bench["position"][1]):
                                # полное совпадение
                                intersection = bench["position"][1] - bench["position"][0]
                                FN_dupl = 0
                                FP_dupl = 0

                            Pres = intersection/(intersection + FP_dupl)
                            Rec = intersection/(intersection + FN_dupl)
                            F = 2*(Pres*Rec)/(Pres+Rec)

                            if (bench["F"]<F):
                                bench["FN_dupl"] = FN_dupl
                                bench["FP_dupl"] = FP_dupl
                                bench["intersection"] = intersection
                                bench["F"] = F

                                bench["Prec_Dupl"] = Pres
                                bench["Recall_Dupl"] = Rec

    @try_except
    def count_metrics(self, elements):
        TP = 0
        FP = 0
        FN = 0
        for text in elements["Benchmarks"]:
            for text1 in text["group_ids"]:
                if text1["check"] == 1:
                    TP = TP + 1
                if text1["check"] == 0:
                    FN = FN + 1

        for text in self.report_data["Benchmarks"]:
            for text1 in text["group_ids"]:
                if text1["check"] == 0:
                    FP = FP + 1

        self.Precision = "{0:.2f}".format(TP / (TP+FP))
        self.Recall = "{0:.2f}".format(TP / (TP+FN))

    def count_Av_metrics(self, elements):
        Av_Prec = 0
        Av_Recall = 0
        count_d = 0

        for text in elements["Benchmarks"]:
            for text1 in text["group_ids"]:
                if text1["check"] == 1:
                    count_d = count_d + 1
                    Av_Prec = Av_Prec + text1["Prec_Dupl"]
                    Av_Recall = Av_Recall + text1["Recall_Dupl"]

        Av_Prec = Av_Prec/count_d
        Av_Recall = Av_Recall/count_d

        self.Av_Pr = "{0:.2f}".format(Av_Prec)
        self.Av_Recall = "{0:.2f}".format(Av_Recall)




