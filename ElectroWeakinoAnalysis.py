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

from fastjet import *

#===================== define input/output here ===========================
OutputFile = "TTbar_nanoAOD_test_plots.root"
MaxEvents = 0        #set to 0 to run all events in each file
MaxFiles = -1        #set to -1 to run all files in file list
#MaxFiles = 1

#====================== define custome cuts here===========================
CheckMother = True

FatJetPtCut = 500
FatJetMassCut = 50
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
        self.LepGenMatch_h=ROOT.TH1F('LepGenMatch_h', '0: all. 1: gen match. 2: mother W', 3, 0, 3)
        self.addObject(self.LepGenMatch_h)

        #===================== AK12Jet SD mass =========================
        self.AK12JetHeavySDMass_h=ROOT.TH1F('AK12JetHeavySDMass_h', 'AK12Jet heavy SD mass', 100, 0, 500)
        self.addObject(self.AK12JetHeavySDMass_h)
        self.AK12JetLightSDMass_h=ROOT.TH1F('AK12JetLightSDMass_h', 'AK12Jet Light SD mass', 100, 0, 500)
        self.addObject(self.AK12JetLightSDMass_h)
        self.AK12JetLepLegSDMass_h=ROOT.TH1F('AK12JetLepLegSDMass_h', 'AK12Jet leptonic leg SD mass', 100, 0, 500)
        self.addObject(self.AK12JetLepLegSDMass_h)
        self.AK12JetHadLegSDMass_h=ROOT.TH1F('AK12JetHadLegSDMass_h', 'AK12Jet hadronic leg SD mass', 100, 0, 500)
        self.addObject(self.AK12JetHadLegSDMass_h)

        #===================== AK12Jet leptonic leg NSubJetness =========================
        self.AK12JetLepLegTau1_h=ROOT.TH1F('AK12JetLepLegTau1_h', 'AK12Jet leptonic leg tau1', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau1_h)
        self.AK12JetLepLegTau2_h=ROOT.TH1F('AK12JetLepLegTau2_h', 'AK12Jet leptonic leg tau2', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau2_h)
        self.AK12JetLepLegTau3_h=ROOT.TH1F('AK12JetLepLegTau3_h', 'AK12Jet leptonic leg tau3', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau3_h)
        self.AK12JetLepLegTau4_h=ROOT.TH1F('AK12JetLepLegTau4_h', 'AK12Jet leptonic leg tau4', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau4_h)
        self.AK12JetGenMatchLepLegTau3Tau1_h=ROOT.TH1F('AK12JetGenMatchLepLegTau3Tau1_h', 'AK12Jet gen match leptonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.AK12JetGenMatchLepLegTau3Tau1_h)
        self.AK12JetLepLegTau3Tau1_h=ROOT.TH1F('AK12JetLepLegTau3Tau1_h', 'AK12Jet leptonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau3Tau1_h)
        self.AK12JetLepLegTau4Tau2_h=ROOT.TH1F('AK12JetLepLegTau4Tau2_h', 'AK12Jet leptonic leg tau4/tau2', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau4Tau2_h)
        self.AK12JetLepLegTau4Tau1_h=ROOT.TH1F('AK12JetLepLegTau4Tau1_h', 'AK12Jet leptonic leg tau4/tau1', 100, 0, 1)
        self.addObject(self.AK12JetLepLegTau4Tau1_h)

        #===================== RecKT and AK12Jet leptonic leg cross check =========================
        self.AK12JetLepLegRawPt_h=ROOT.TH1F('AK12JetLepLegRawPt_h', 'AK12Jet leptonic leg raw pt', 100, 0, 1000)
        self.addObject(self.AK12JetLepLegRawPt_h)
        self.RecKT12JetLepLegPt_h=ROOT.TH1F('RecKT12JetLepLegPt_h', 'reclusted KT12Jet leptonic leg pt', 100, 0, 1000)
        self.addObject(self.RecKT12JetLepLegPt_h)

        #===================== RecKT12Jet leptonic leg NSubJetness =========================
        self.RecKT12JetLepLegTau1_h=ROOT.TH1F('RecKT12JetLepLegTau1_h', 'RecKT12Jet leptonic leg tau1', 100, 0, 1)
        self.addObject(self.RecKT12JetLepLegTau1_h)
        self.RecKT12JetLepLegTau2_h=ROOT.TH1F('RecKT12JetLepLegTau2_h', 'RecKT12Jet leptonic leg tau2', 100, 0, 1)
        self.addObject(self.RecKT12JetLepLegTau2_h)
        self.RecKT12JetLepLegTau3_h=ROOT.TH1F('RecKT12JetLepLegTau3_h', 'RecKT12Jet leptonic leg tau3', 100, 0, 1)
        self.addObject(self.RecKT12JetLepLegTau3_h)
        self.RecKT12JetLepLegTau4_h=ROOT.TH1F('RecKT12JetLepLegTau4_h', 'RecKT12Jet leptonic leg tau4', 100, 0, 1)
        self.addObject(self.RecKT12JetLepLegTau4_h)
        self.RecKT12JetLepLegTau3Tau1_h=ROOT.TH1F('RecKT12JetLepLegTau3Tau1_h', 'RecKT12Jet leptonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.RecKT12JetLepLegTau3Tau1_h)

        #===================== AK12Jet hadraonic leg NSubJetness =========================
        self.AK12JetHadLegTau1_h=ROOT.TH1F('AK12JetHadLegTau1_h', 'AK12Jet hadraonic leg tau1', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau1_h)
        self.AK12JetHadLegTau2_h=ROOT.TH1F('AK12JetHadLegTau2_h', 'AK12Jet hadraonic leg tau2', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau2_h)
        self.AK12JetHadLegTau3_h=ROOT.TH1F('AK12JetHadLegTau3_h', 'AK12Jet hadraonic leg tau3', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau3_h)
        self.AK12JetHadLegTau4_h=ROOT.TH1F('AK12JetHadLegTau4_h', 'AK12Jet hadraonic leg tau4', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau4_h)
        self.AK12JetGenMatchHadLegTau3Tau1_h=ROOT.TH1F('AK12JetGenMatchHadLegTau3Tau1_h', 'AK12Jet gen match hadraonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.AK12JetGenMatchHadLegTau3Tau1_h)
        self.AK12JetHadLegTau3Tau1_h=ROOT.TH1F('AK12JetHadLegTau3Tau1_h', 'AK12Jet hadraonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau3Tau1_h)
        self.AK12JetHadLegTau3Tau2_h=ROOT.TH1F('AK12JetHadLegTau3Tau2_h', 'AK12Jet hadraonic leg tau3/tau2', 100, 0, 1)
        self.addObject(self.AK12JetHadLegTau3Tau2_h)

        #===================== FatJet leptonic leg NSubJetness =========================
        self.FatJetLepLegTau1_h=ROOT.TH1F('FatJetLepLegTau1_h', 'FatJet leptonic leg tau1', 100, 0, 1)
        self.addObject(self.FatJetLepLegTau1_h)
        self.FatJetLepLegTau2_h=ROOT.TH1F('FatJetLepLegTau2_h', 'FatJet leptonic leg tau2', 100, 0, 1)
        self.addObject(self.FatJetLepLegTau2_h)
        self.FatJetLepLegTau3_h=ROOT.TH1F('FatJetLepLegTau3_h', 'FatJet leptonic leg tau3', 100, 0, 1)
        self.addObject(self.FatJetLepLegTau3_h)
        self.FatJetLepLegTau4_h=ROOT.TH1F('FatJetLepLegTau4_h', 'FatJet leptonic leg tau4', 100, 0, 1)
        self.addObject(self.FatJetLepLegTau4_h)
        self.FatJetLepLegTau3Tau1_h=ROOT.TH1F('FatJetLepLegTau3Tau1_h', 'FatJet leptonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.FatJetLepLegTau3Tau1_h)
        self.FatJetLepLegTau4Tau2_h=ROOT.TH1F('FatJetLepLegTau4Tau2_h', 'FatJet leptonic leg tau4/tau2', 100, 0, 1)
        self.addObject(self.FatJetLepLegTau4Tau2_h)
        self.FatJetLepLegTau4Tau1_h=ROOT.TH1F('FatJetLepLegTau4Tau1_h', 'FatJet leptonic leg tau4/tau1', 100, 0, 1)
        self.addObject(self.FatJetLepLegTau4Tau1_h)

        #===================== FatJet hadraonic leg NSubJetness =========================
        self.FatJetHadLegTau1_h=ROOT.TH1F('FatJetHadLegTau1_h', 'FatJet hadraonic leg tau1', 100, 0, 1)
        self.addObject(self.FatJetHadLegTau1_h)
        self.FatJetHadLegTau2_h=ROOT.TH1F('FatJetHadLegTau2_h', 'FatJet hadraonic leg tau2', 100, 0, 1)
        self.addObject(self.FatJetHadLegTau2_h)
        self.FatJetHadLegTau3_h=ROOT.TH1F('FatJetHadLegTau3_h', 'FatJet hadraonic leg tau3', 100, 0, 1)
        self.addObject(self.FatJetHadLegTau3_h)
        self.FatJetHadLegTau4_h=ROOT.TH1F('FatJetHadLegTau4_h', 'FatJet hadraonic leg tau4', 100, 0, 1)
        self.addObject(self.FatJetHadLegTau4_h)
        self.FatJetHadLegTau3Tau1_h=ROOT.TH1F('FatJetHadLegTau3Tau1_h', 'FatJet hadraonic leg tau3/tau1', 100, 0, 1)
        self.addObject(self.FatJetHadLegTau3Tau1_h)
        self.FatJetHadLegTau3Tau2_h=ROOT.TH1F('FatJetHadLegTau3Tau2_h', 'FatJet hadraonic leg tau3/tau2', 100, 0, 1)
        self.addObject(self.FatJetHadLegTau3Tau2_h)

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

    def pf_cand_in_fat_jet(self, JetPFCands, FatJet, FatJetSize):
        PFCandList = []
        FatJetTLV = FatJet.p4()
        for JetPFCand in JetPFCands:
            if JetPFCand.DeltaR(FatJetTLV) < FatJetSize:
                PFCandList.append(JetPFCand)
        return PFCandList

    def recluster_kt12_jet(self, JetPFCands):
        KT12JetDef = JetDefinition(kt_algorithm, 1.2)
        PseudoJetList = []
        for JetPFCand in JetPFCands:
            PseudoJetList.append(PseudoJet(JetPFCand.p4().Px(), JetPFCand.p4().Py(), JetPFCand.p4().Pz(), JetPFCand.p4().E()))
        RecKT12Jets = KT12JetDef(PseudoJetList)
        RecKT12Jet = RecKT12Jets[0]
        if len(RecKT12Jets) > 1:
            print "Warning! more than one reclustered KT12Jets"
            #Descend sort RecKT12Jets by pt
            RecKT12Jet = sorted(RecKT12Jets, key=lambda x: x.pt(), reverse=True)[0]
        return RecKT12Jet

    def decluster_rec_jet(self, RecJet):
        SubJetsList = []
        for i in range(4):
            SubJets = RecJet.exclusive_subjets_up_to(i+1)
            SubJetsList.append(SubJets)
        return SubJetsList

    def calc_nsubjetness(self, AxisList, JetPFCands, FatJetSize):
        Dist = 0
        Norm = 0
        for JetPFCand in JetPFCands:
            Pt = JetPFCand.pt
            dR = 999
            for Axis in AxisList:
                AxisTLV = ROOT.TLorentzVector(Axis.px(), Axis.py(), Axis.pz(), Axis.E())
                dRTemp = JetPFCand.DeltaR(AxisTLV)
                if dR > dRTemp:
                    dR = dRTemp
            Dist += Pt * dR
            Norm += Pt * FatJetSize
        return Dist / Norm

    def sel_gen_lep(self, GenParts):
        SelLepList = []
        for GenPart in GenParts:
            pdgId = abs(GenPart.pdgId)
            if pdgId == 11 or pdgId == 13:
                SelLepList.append(GenPart)
        return SelLepList

    def get_matched_gen_lep(self, GenLepList, HighPtLep):
        HighPtLepTLV = HighPtLep.p4()
        MatchedGenLep = None
        dR = 0.2
        for GenLep in GenLepList:
            dRTemp = GenLep.DeltaR(HighPtLepTLV)
            if dR > dRTemp:
                dR = dRTemp
                MatchedGenLep = GenLep
        return MatchedGenLep

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

    def sel_high_mass_fat_jet(self, FatJets, OriginFatJets):
        SelFatJetList = []
        for FatJet in FatJets:
            if FatJet.pt > FatJetPtCut and abs(FatJet.eta) < EtaCut:
                SelFatJetList.append(FatJet)
        if len(SelFatJetList) >= 2:
            FatJetSDMassLight = 0
            #Descend sort SelFatJetList by SD mass
            if OriginFatJets:
                SelFatJetList.sort(key=lambda x: x.msoftdrop, reverse=True)
                FatJetSDMassLight = SelFatJetList[1].msoftdrop
            else:
                SelFatJetList.sort(key=lambda x: x.softdropMass, reverse=True)
                FatJetSDMassLight = SelFatJetList[1].softdropMass
            if FatJetSDMassLight > FatJetMassCut: return SelFatJetList[0], SelFatJetList[1]
        return None, None

    def sel_fat_jets_lep_and_had_legs(self, HighPtLep, FatJetHeavy, FatJetLight, FatJetR):
        HighPtLepTLV = HighPtLep.p4()
        if FatJetHeavy.DeltaR(HighPtLepTLV) < FatJetR:
            return FatJetHeavy, FatJetLight
        if FatJetLight.DeltaR(HighPtLepTLV) < FatJetR:
            return FatJetLight, FatJetHeavy
        return None, None

    def analyze(self, event):
        #================ read needed collections/objects here ====================
        Electrons = Collection(event, "Electron")
        Muons = Collection(event, "Muon")
        AK12Jets = Collection(event, "selectedPatJetsAK12PFPuppi")
        FatJets = Collection(event, "FatJet")
        GenParts = Collection(event, "GenPart")
        JetPFCands = Collection(event, "JetPFCands")

        #================ analyze each event ======================================
        if CheckMother:
            IsTTbar, IsSignal = self.check_mother(GenParts)
            self.IsTTbar_h.Fill(IsTTbar)
            self.IsSignal_h.Fill(IsSignal)

        HighPtLep = self.sel_high_pt_lep(Muons, Electrons)
        AK12JetHeavy, AK12JetLight = self.sel_high_mass_fat_jet(AK12Jets, False)

        if HighPtLep is not None and AK12JetHeavy is not None and AK12JetLight is not None:
            self.AK12JetHeavySDMass_h.Fill(AK12JetHeavy.softdropMass)
            self.AK12JetLightSDMass_h.Fill(AK12JetLight.softdropMass)

            AK12JetLepLeg, AK12JetHadLeg = self.sel_fat_jets_lep_and_had_legs(HighPtLep, AK12JetHeavy, AK12JetLight, 1.2)
            if AK12JetLepLeg is not None and AK12JetHadLeg is not None:
                self.AK12JetLepLegSDMass_h.Fill(AK12JetLepLeg.softdropMass)
                self.AK12JetHadLegSDMass_h.Fill(AK12JetHadLeg.softdropMass)

                #=================== Njettiness by JetToolBox ======================
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

                #=================== recalculate Njettiness ======================
                AK12JetLepLegPFCands = self.pf_cand_in_fat_jet(JetPFCands, AK12JetLepLeg, 1.2)

                RecKT12JetLepLeg = self.recluster_kt12_jet(AK12JetLepLegPFCands)
                self.RecKT12JetLepLegPt_h.Fill(RecKT12JetLepLeg.pt())
                self.AK12JetLepLegRawPt_h.Fill(AK12JetLepLeg.pt * (1 - AK12JetLepLeg.rawFactor))
                RecKT12JetLepLegSubJetsList = self.decluster_rec_jet(RecKT12JetLepLeg)

                RecKT12JetLepLegTau1 = self.calc_nsubjetness(RecKT12JetLepLegSubJetsList[0], AK12JetLepLegPFCands, 1.2)
                RecKT12JetLepLegTau2 = self.calc_nsubjetness(RecKT12JetLepLegSubJetsList[1], AK12JetLepLegPFCands, 1.2)
                RecKT12JetLepLegTau3 = self.calc_nsubjetness(RecKT12JetLepLegSubJetsList[2], AK12JetLepLegPFCands, 1.2)
                RecKT12JetLepLegTau4 = self.calc_nsubjetness(RecKT12JetLepLegSubJetsList[3], AK12JetLepLegPFCands, 1.2)

                self.RecKT12JetLepLegTau1_h.Fill(RecKT12JetLepLegTau1)
                self.RecKT12JetLepLegTau2_h.Fill(RecKT12JetLepLegTau2)
                self.RecKT12JetLepLegTau3_h.Fill(RecKT12JetLepLegTau3)
                self.RecKT12JetLepLegTau4_h.Fill(RecKT12JetLepLegTau4)
                self.RecKT12JetLepLegTau3Tau1_h.Fill(RecKT12JetLepLegTau3 / RecKT12JetLepLegTau1)

                self.LepGenMatch_h.Fill(0)
                GenLepList = self.sel_gen_lep(GenParts)
                MatchedGenLep = self.get_matched_gen_lep(GenLepList, HighPtLep)
                if MatchedGenLep is not None:
                    self.LepGenMatch_h.Fill(1)
                    MatchedGenLepMother = GenParts[MatchedGenLep.genPartIdxMother]
                    #gen lep's mother is W
                    if abs(MatchedGenLepMother.pdgId) == 24:
                        self.LepGenMatch_h.Fill(2)
                        self.AK12JetGenMatchLepLegTau3Tau1_h.Fill(LepLegTau3 / LepLegTau1)
                        self.AK12JetGenMatchHadLegTau3Tau1_h.Fill(HadLegTau3 / HadLegTau1)

        FatJetHeavy, FatJetLight = self.sel_high_mass_fat_jet(FatJets, True)

        if HighPtLep is not None and FatJetHeavy is not None and FatJetLight is not None:
            FatJetLepLeg, FatJetHadLeg = self.sel_fat_jets_lep_and_had_legs(HighPtLep, FatJetHeavy, FatJetLight, 0.8)
            if FatJetLepLeg is not None and FatJetHadLeg is not None: 
                LepLegTau1 = FatJetLepLeg.tau1
                LepLegTau2 = FatJetLepLeg.tau2
                LepLegTau3 = FatJetLepLeg.tau3
                LepLegTau4 = FatJetLepLeg.tau4

                self.FatJetLepLegTau1_h.Fill(LepLegTau1)
                self.FatJetLepLegTau2_h.Fill(LepLegTau2)
                self.FatJetLepLegTau3_h.Fill(LepLegTau3)
                self.FatJetLepLegTau4_h.Fill(LepLegTau4)
                self.FatJetLepLegTau3Tau1_h.Fill(LepLegTau3 / LepLegTau1)
                self.FatJetLepLegTau4Tau2_h.Fill(LepLegTau4 / LepLegTau2)
                self.FatJetLepLegTau4Tau1_h.Fill(LepLegTau4 / LepLegTau1)

                HadLegTau1 = FatJetHadLeg.tau1
                HadLegTau2 = FatJetHadLeg.tau2
                HadLegTau3 = FatJetHadLeg.tau3
                HadLegTau4 = FatJetHadLeg.tau4

                self.FatJetHadLegTau1_h.Fill(HadLegTau1)
                self.FatJetHadLegTau2_h.Fill(HadLegTau2)
                self.FatJetHadLegTau3_h.Fill(HadLegTau3)
                self.FatJetHadLegTau4_h.Fill(HadLegTau4)
                self.FatJetHadLegTau3Tau1_h.Fill(HadLegTau3 / HadLegTau1)
                self.FatJetHadLegTau3Tau2_h.Fill(HadLegTau3 / HadLegTau2)

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
