#!/usr/bin/env python

#case convention
#lowercase with underline for function names
#canmel case for variable/object names

import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

#===================== define input/output here ===========================
OutputFile = "TTbar_nanoAOD_test_plots.root"
MaxEvents = 0        #set to 0 to run all events in each file
MaxFiles = -1        #set to -1 to run all files in file list
#MaxFiles = 10

#====================== define custome cuts here===========================
CheckMother = False

FatJetPtCut = 500
LepPtCut = 10
EtaCut = 2.4
#muons have loose id by default
EleIdCut = 2 #cut-based ID Fall17 V2 (0:fail, 1:veto, 2:loose, 3:medium, 4:tight)

class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True
    
    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        #===================== cross check mother particles =============================
        self.IsTTbar_h=ROOT.TH1F('IsTTbar_h', 'is TTbar event', 2, 0, 2)
        self.addObject(self.IsTTbar_h)
        self.IsSignal_h=ROOT.TH1F('IsSignal_h', 'is Signal event', 2, 0, 2)
        self.addObject(self.IsSignal_h)

        #===================== AK12Jet leptonic leg NSubJetness =========================
        self.AK12JetLepLegTau1_h=ROOT.TH1F('AK12JetLepLegTau1_h', 'AK12Jet leptonic leg tau1', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau1_h)
        self.AK12JetLepLegTau2_h=ROOT.TH1F('AK12JetLepLegTau2_h', 'AK12Jet leptonic leg tau2', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau2_h)
        self.AK12JetLepLegTau3_h=ROOT.TH1F('AK12JetLepLegTau3_h', 'AK12Jet leptonic leg tau3', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau3_h)
        self.AK12JetLepLegTau4_h=ROOT.TH1F('AK12JetLepLegTau4_h', 'AK12Jet leptonic leg tau4', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau4_h)
        self.AK12JetLepLegTau3Tau1_h=ROOT.TH1F('AK12JetLepLegTau3Tau1_h', 'AK12Jet leptonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau3Tau1_h)
        self.AK12JetLepLegTau4Tau2_h=ROOT.TH1F('AK12JetLepLegTau4Tau2_h', 'AK12Jet leptonic leg tau4/tau2', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau4Tau2_h)
        self.AK12JetLepLegTau4Tau1_h=ROOT.TH1F('AK12JetLepLegTau4Tau1_h', 'AK12Jet leptonic leg tau4/tau1', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau4Tau1_h)

        #===================== AK12Jet hadraonic leg NSubJetness =========================
        self.AK12JetHadLegTau1_h=ROOT.TH1F('AK12JetHadLegTau1_h', 'AK12Jet hadraonic leg tau1', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau1_h)
        self.AK12JetHadLegTau2_h=ROOT.TH1F('AK12JetHadLegTau2_h', 'AK12Jet hadraonic leg tau2', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau2_h)
        self.AK12JetHadLegTau3_h=ROOT.TH1F('AK12JetHadLegTau3_h', 'AK12Jet hadraonic leg tau3', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau3_h)
        self.AK12JetHadLegTau4_h=ROOT.TH1F('AK12JetHadLegTau4_h', 'AK12Jet hadraonic leg tau4', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau4_h)
        self.AK12JetHadLegTau3Tau1_h=ROOT.TH1F('AK12JetHadLegTau3Tau1_h', 'AK12Jet hadraonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau3Tau1_h)
        self.AK12JetHadLegTau3Tau2_h=ROOT.TH1F('AK12JetHadLegTau3Tau2_h', 'AK12Jet hadraonic leg tau3/tau2', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau3Tau2_h)

    def check_mother(self, GenParts):
        IsTTbar = False
        IsSignal = False
        for GenPart in GenParts:
            pdgId = abs(GenPart.pdgId)
            if GenPart.genPartIdxMother == 0: #means current GenPart is mother
                if pdgId == 6:
                    IsTTbar = True
                    break
                if pdgId == 1000022 or pdgId == 1000024:
                    IsSignal = True
                    break
        return IsTTbar, IsSignal

    def sel_high_pt_lep(self, Muons, Electrons):
        SelLepList = []
        for Muon in Muons:
            if Muon.pt > LepPtCut and abs(Muon.eta) < EtaCut:
                SelLepList.append(Muon)
        for Electron in Electrons:
            if Electron.pt > LepPtCut and abs(Electron.eta) < EtaCut and Electron.cutBased >= EleIdCut:
                SelLepList.append(Electron)
        if len(SelLepList) > 0:
            #Descend sort SelLepList by pt
            SelLepList.sort(key=lambda x: x.pt, reverse=True)
            return SelLepList[0]
        return None

    def sel_high_mass_fat_jet(self, FatJets):
        SelFatJetList = []
        for FatJet in FatJets:
            if FatJet.pt > FatJetPtCut and abs(FatJet.eta) < EtaCut:
                SelFatJetList.append(FatJet)
        if len(SelFatJetList) >= 2:
            #Descend sort SelFatJetList by SD mass
            SelFatJetList.sort(key=lambda x: x.softdropMass, reverse=True)
            return SelFatJetList[0], SelFatJetList[1]
        return None, None

    def sel_AK12_jets_lep_and_had_legs(self, HighPtLep, AK12JetHeavy, AK12JetLight):
        HighPtLepTLV = HighPtLep.p4()
        if AK12JetHeavy.DeltaR(HighPtLepTLV) < 1.2:
            return AK12JetHeavy, AK12JetLight
        if AK12JetLight.DeltaR(HighPtLepTLV) < 1.2:
            return AK12JetLight, AK12JetHeavy
        return None, None

    def analyze(self, event):
        #================ read needed collections/objects here ====================
        Electrons = Collection(event, "Electron")
        Muons = Collection(event, "Muon")
        AK12Jets = Collection(event, "selectedPatJetsAK12PFPuppi")
        GenParts = Collection(event, "GenPart")

        #================ analyze each event ======================================
        if CheckMother:
            IsTTbar, IsSignal = self.check_mother(GenParts)
            self.IsTTbar_h.Fill(IsTTbar)
            self.IsSignal_h.Fill(IsSignal)

        HighPtLep = self.sel_high_pt_lep(Muons, Electrons)
        AK12JetHeavy, AK12JetLight = self.sel_high_mass_fat_jet(AK12Jets)

        if HighPtLep is not None and AK12JetHeavy is not None and AK12JetLight is not None:
            AK12JetLepLeg, AK12JetHadLeg = self.sel_AK12_jets_lep_and_had_legs(HighPtLep, AK12JetHeavy, AK12JetLight)
            if AK12JetLepLeg is not None and AK12JetHadLeg is not None: 
                LepLegTau1 = AK12JetLepLeg.NjettinessAK12Puppi_tau1
                LepLegTau2 = AK12JetLepLeg.NjettinessAK12Puppi_tau2
                LepLegTau3 = AK12JetLepLeg.NjettinessAK12Puppi_tau3
                LepLegTau4 = AK12JetLepLeg.NjettinessAK12Puppi_tau4

                self.AK12JetLepLegTau1_h.Fill(LepLegTau1)
                self.AK12JetLepLegTau2_h.Fill(LepLegTau2)
                self.AK12JetLepLegTau3_h.Fill(LepLegTau3)
                self.AK12JetLepLegTau4_h.Fill(LepLegTau4)
                self.AK12JetLepLegTau3Tau1_h.Fill(LepLegTau3 / LepLegTau1)
                self.AK12JetLepLegTau4Tau2_h.Fill(LepLegTau4 / LepLegTau2)
                self.AK12JetLepLegTau4Tau1_h.Fill(LepLegTau4 / LepLegTau1)

                HadLegTau1 = AK12JetHadLeg.NjettinessAK12Puppi_tau1
                HadLegTau2 = AK12JetHadLeg.NjettinessAK12Puppi_tau2
                HadLegTau3 = AK12JetHadLeg.NjettinessAK12Puppi_tau3
                HadLegTau4 = AK12JetHadLeg.NjettinessAK12Puppi_tau4

                self.AK12JetHadLegTau1_h.Fill(HadLegTau1)
                self.AK12JetHadLegTau2_h.Fill(HadLegTau2)
                self.AK12JetHadLegTau3_h.Fill(HadLegTau3)
                self.AK12JetHadLegTau4_h.Fill(HadLegTau4)
                self.AK12JetHadLegTau3Tau1_h.Fill(HadLegTau3 / HadLegTau1)
                self.AK12JetHadLegTau3Tau2_h.Fill(HadLegTau3 / HadLegTau2)

        #return true to move on to the next module. return false to go to the next event
        return True

def read_file_list(FileList, MaxFiles):
    f=open(FileList, "r")
    InputFiles = f.readlines()
    f.close()

    nInputFiles = len(InputFiles)
    if MaxFiles > nInputFiles:
        print "MaxFiles", MaxFiles, "> nInputFiles", nInputFiles
        quit()

    nOutputFiles = MaxFiles
    if MaxFiles == -1: nOutputFiles = nInputFiles

    for i in range(nInputFiles): InputFiles[i] = InputFiles[i].split("\n")[0]
    print InputFiles[0:nOutputFiles]
    return InputFiles[0:nOutputFiles]

FileList = sys.argv[1]
preselection=""
p=PostProcessor(".",read_file_list(FileList, MaxFiles),cut=preselection,branchsel=None,modules=[ExampleAnalysis()],noOut=True,histFileName=OutputFile,histDirName="plots",maxEntries=MaxEvents)
p.run()
