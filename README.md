# ElectroWeakino nanoAOD analysis
This is a git repo for the ElectroWeakino analysis using nanoAOD ntuples  
The ntuple production steps can be found in this repo  
https://github.com/wang-hui/electroWeakino_NanoAOD

1. setup CMSSW. Any 10xx should work
```
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
cmsenv
```

2. checkout nanoAOD-tools
```
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j 8
```

3. checkout this repo
```
git clone https://github.com/wang-hui/electroWeakino_analysis.git
```

4. local test
```
cd electroWeakino_analysis
python ElectroWeakinoAnalysis.py FileList/nanoAOD_2017_TTJets_SingleLeptFromT.list
```
