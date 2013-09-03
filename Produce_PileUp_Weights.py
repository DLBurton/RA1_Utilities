#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging,itertools
import os,fnmatch,sys
import glob, errno
from time import strftime
from optparse import OptionParser
import array, ast
from math import *


# This is the pileup distribution that Summer 2013 PU Scenario 10 is produced with

Summer2012 =  [ 2.560E-06,   5.239E-06,  1.420E-05,   5.005E-05,  1.001E-04,  2.705E-04,   1.999E-03,  6.097E-03, 1.046E-02,   1.383E-02,  1.685E-02, 2.055E-02, 2.572E-02, 3.262E-02,   4.121E-02,   4.977E-02,  5.539E-02,  5.725E-02,   5.607E-02,  5.312E-02, 5.008E-02,  4.763E-02, 4.558E-02,  4.363E-02,  4.159E-02, 3.933E-02,  3.681E-02, 3.406E-02, 3.116E-02,    2.818E-02, 2.519E-02, 2.226E-02, 1.946E-02,  1.682E-02,  1.437E-02,  1.215E-02,  1.016E-02,  8.400E-03, 6.873E-03, 5.564E-03, 4.457E-03,  3.533E-03,  2.772E-03, 2.154E-03,1.656E-03, 1.261E-03, 9.513E-04,  7.107E-04,   5.259E-04,  3.856E-04,  2.801E-04, 2.017E-04, 1.439E-04,  1.017E-04,   7.126E-05,    4.948E-05, 3.405E-05,2.322E-05, 1.570E-05,  5.005E-06  ]

# Create empty file to fill with histograms
Pileup_Root = r.TFile("ParkedData_Pileup.root","RECREATE")

# Fill histogram with MC distribution Summmer2012
mcplot_noselection = TH1F("pileup","pileup",60,0,60)

for num,entry in enumerate(Summer2012): mcplot_noselection.SetBinContent(num+1,entry)
c1 = r.TCanvas("canvas","mycanvas")
c1.cd()
c1.SetLogy(0)


"""
Normalises the Data to unit area 1. Like the MC
"""
def Normalise_Data(file_name,file_path,file_type):
  file = r.TFile.Open(file_name)
  data_plot = file.Get(file_path)
  data_integral = data_plot.Integral()
  datanumbers = []
  print "Data number of bins %s " %data_plot.GetNbinsX()
  for bin in range(1,data_plot.GetNbinsX()+1): 
    datanumbers.append((data_plot.GetBinContent(bin)/data_integral))
    data_plot.SetBinContent(bin,(data_plot.GetBinContent(bin)/data_integral))
  integral_test = data_plot.Integral()
  data_plot.Draw("HIST")
  c1.SaveAs("pu_%s.png"%file_type)
  return data_plot

def Normalise_MC(plot):
  plotintegral = plot.Integral()
  print "Number of bins %s " %plot.GetNbinsX()
  for bin in range(1,plot.GetNbinsX()+1):
    plot.SetBinContent(bin,(plot.GetBinContent(bin)/plotintegral))
  return plot  


# This is Data File you read in and normalise
normalise_data_selection =  Normalise_Data("./PileUp_Muon_Selection.root",'pileup','data_selection')

"""
Divide the two histograms by each other Data/MC to produce factor MC must be corrected by
"""
make_weights_after_selection = normalise_data_selection.Clone()
default_pu_distribution = mcplot_noselection.Clone()

make_weights_after_selection.Divide(pu_distribution_with_selection)
make_weights_after_selection.Draw("HIST")
c1.SaveAs("mc_weights_derived_after_selection.png")

weights_selection = []
for bin in range(1,make_weights_after_selection.GetNbinsX()+1):
  weights_selection.append(make_weights_after_selection.GetBinContent(bin))

print weights_selection

