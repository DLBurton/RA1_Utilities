#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array
import math as m

#================================== Preamble
print " Selecting tdr style"
r.gROOT.ProcessLine(".L tdrstyle.C")
r.setstyle()
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)


"""
Normally measured for Z0 and Z2

Z0 : WJets, DY , Zinv
Z2 : TTbar, SingleTop DiBoson

However using the BtagPOG recommend jet identifier. The btag and mistag rates for Z0 and Z2 are the same. Therefore a single efficnecy can be measured if desired

To produce efficiencies take :

        1.  GenJetPt_vs_GenJetEta_noB_all   - Number of light jets binned in eta and pt
        2.  Matched_GenJetPt_vs_GenJetEta_noB_all - Number of light jets that also fire the b-tagger (I know the name is a bit screwy)

Divide the two histograms and you have the efficiencies. Then when fed back into the ICF code now jets are matched to an eta/pt bin and the efficiency read off. Any reweighting factors are applied to this probability to pull out the 'real' tagging efficiency of this jet in data and the weight of the event is adjusted accordingly

"""
name = "Z0"

file = r.TFile.Open("Muon_"+name+".root")

#Light Jets
mistag = file.Get("OneMuon_Template_275/GenJetPt_vs_GenJetEta_noB_all")
mistag_matched = file.Get("OneMuon_Template_275/Matched_GenJetPt_vs_GenJetEta_noB_all")

#B Jets
btag = file.Get("OneMuon_Template_275/GenJetPt_vs_GenJetEta_all")
btag_matched = file.Get("OneMuon_Template_275/Matched_GenJetPt_vs_GenJetEta_all")

#C Jets
ctag = file.Get("OneMuon_Template_275/GenJetPt_vs_GenJetEta_c_all")
ctag_matched = file.Get("OneMuon_Template_275/Matched_GenJetPt_vs_GenJetEta_c_all")


mistag_matched.Divide(mistag)
btag_matched.Divide(btag)
ctag_matched.Divide(ctag)

c1 = r.TCanvas("canvas","canname",1200,1200)
c1.cd()
 
mistag_matched.Draw("COLZTEXT")
c1.SaveAs("Mistag_Pt_Eta.png")
btag_matched.Draw("COLZTEXT")
c1.SaveAs("Btag_Pt_Eta.png")
ctag_matched.Draw("COLZTEXT")
c1.SaveAs("charm_Pt_Eta.png")


btag_txt = open('Btag_%s_Efficiency.txt'%name,'w')
s = ""
mistag_txt = open('Mistag_%s_Efficiency.txt'%name,'w')
t = ""
ctag_txt = open('Charm_%s_Efficiency.txt'%name,'w')
u = ""

for i in range (1,btag_matched.GetNbinsX()+2):
  print i
  for j in range(1,btag_matched.GetNbinsY()+2):
    s += "BtagEfficiency_%s_%s %s\n" %(btag_matched.GetXaxis().GetBinLowEdge(i),btag_matched.GetYaxis().GetBinLowEdge(j),btag_matched.GetBinContent(i,j))

print "Btag Efficiency Done"

for i in range (1,btag_matched.GetNbinsX()+2):
  for j in range(1,btag_matched.GetNbinsY()+2):
    t += "BtagMistagEfficiency_%s_%s %s\n" %(mistag_matched.GetXaxis().GetBinLowEdge(i),mistag_matched.GetYaxis().GetBinLowEdge(j),mistag_matched.GetBinContent(i,j))

print "Mistag Efficiency Done"

for i in range (1,ctag_matched.GetNbinsX()+2):
  for j in range(1,ctag_matched.GetNbinsY()+2):
    u += "BtagCharmEfficiency_%s_%s %s\n" %(ctag_matched.GetXaxis().GetBinLowEdge(i),ctag_matched.GetYaxis().GetBinLowEdge(j),ctag_matched.GetBinContent(i,j))

btag_txt.write(s)
btag_txt.close()   

mistag_txt.write(t)
mistag_txt.close()   

ctag_txt.write(u)
ctag_txt.close()   




