#lowercase with underline for function/class names
#canmel case for variables

import ROOT as rt

class process:
    def __init__(self, ProcessName, Hist, Lumi, TotEvent, Leg, Color):
        self.ProcessName  = ProcessName
        self.Hist = Hist
        self.Lumi = Lumi
        self.TotEvent = TotEvent
        self.Color = Color
        self.Leg = Leg

        self.FileNameList = []
        self.XsecDic = {}
        self.IsSignal = ("Signal" in ProcessName)

    def add_file(self, FileName, Xsec):
        self.FileNameList.append(FileName)
        self.XsecDic[FileName] = Xsec

    def return_process(self):
        if len(self.FileNameList) == 0:
            print "no input file for process ", self.ProcessName
            return None
        else:
            InitFile = rt.TFile.Open(self.FileNameList[0])
            InitHist = InitFile.Get(self.Hist)
            ResultProcess = InitHist.Clone(self.ProcessName)
            ResultProcess.Reset()    #clone the frame for later add
            print "====================", self.ProcessName, "========================"
            for FileName in self.FileNameList:
                iFile = rt.TFile.Open(FileName)
                iHist = iFile.Get(self.Hist)
                iTotEvent = iFile.Get(self.TotEvent)
                TotEvent = iTotEvent.GetBinContent(1)
                iHist.Scale(self.Lumi * self.XsecDic[FileName] * 1000 / TotEvent)
                ResultProcess.Add(iHist)
                print FileName, ", TotEvent", TotEvent, ", Xsec", self.XsecDic[FileName]

            ResultProcess.SetDirectory(0)    #return objects ownership to user
            TotBins = ResultProcess.GetSize() - 2
            print "LastBinContent", ResultProcess.GetBinContent(TotBins)

            if self.IsSignal:
                ResultProcess.SetLineColor(self.Color)
                ResultProcess.SetLineWidth(2)
                self.Leg.AddEntry(ResultProcess, self.ProcessName, "l")
            else:
                ResultProcess.SetFillColor(self.Color)
                self.Leg.AddEntry(ResultProcess, self.ProcessName, "f")
            return ResultProcess

MyHist = "BaseLineTest_h"
MyHistDir = "plots/"
MyTotEvent = "BaseLineTest_h"
MyTotEventDir = "plots/"
MyLumi = 140
ResultsDir = ""

MyLeg = rt.TLegend(0.5,0.65,0.89,0.89)

TTbarProcess = process("TTbar", MyHistDir + MyHist, MyLumi, MyTotEventDir + MyTotEvent, MyLeg, rt.kYellow - 9)
TTbarProcess.add_file(ResultsDir + "nanoAOD_2017_TTJets_SingleLeptFromT_plots.root", 182.7 * 2)

QCDProcess = process("QCD", MyHistDir + MyHist, MyLumi, MyTotEventDir + MyTotEvent, MyLeg, rt.kOrange - 3)
QCDProcess.add_file(ResultsDir + "nanoAOD_2017_QCD_HT1000to1500_plots.root", 1064)
#QCDProcess.add_file("QCD_HT1500toInf_plots.root", 121.5 + 25.42)

MyHS = rt.THStack()
MyHS.Add(TTbarProcess.return_process())
MyHS.Add(QCDProcess.return_process())

SignalProcessList = []
SignalProcess_1 = process("Signal(100,110)", MyHistDir + MyHist, MyLumi, MyTotEventDir + MyTotEvent, MyLeg, rt.kRed)
SignalProcess_1.add_file(ResultsDir + "nanoAOD_2017_mn1_100_mx1_110_plots.root", 1807.39 / 1000)
SignalProcessList.append(SignalProcess_1.return_process())

SignalProcess_2 = process("Signal(300,310)", MyHistDir + MyHist, MyLumi, MyTotEventDir + MyTotEvent, MyLeg, rt.kBlue)
SignalProcess_2.add_file(ResultsDir + "nanoAOD_2017_mn1_300_mx1_310_plots.root", 20.1372 / 1000)
SignalProcessList.append(SignalProcess_2.return_process())

SignalProcess_3 = process("Signal(300,350)", MyHistDir + MyHist, MyLumi, MyTotEventDir + MyTotEvent, MyLeg, rt.kGreen)
SignalProcess_3.add_file(ResultsDir + "nanoAOD_2017_mn1_300_mx1_350_plots.root", 13.7303 / 1000)
SignalProcessList.append(SignalProcess_3.return_process())

MyCanvas = rt.TCanvas("MyCanvas", "MyCanvas", 600, 600)
rt.gStyle.SetOptStat(rt.kFALSE)
rt.gPad.SetLogy()

MyHS.SetMinimum(10)
MyHS.SetMaximum(1E9)
MyHS.Draw("hist")

for SignalProcess in SignalProcessList: SignalProcess.Draw("histsame")
MyLeg.Draw("same")

MyCanvas.SaveAs("plots_temp/" + MyHist + "_stack.png")
