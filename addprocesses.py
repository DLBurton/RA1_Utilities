#!/usr/bin/env python

# jadd: like hadd, but for log files (JSON)
#
# usage: ./jadd.py out.log in_1.log in_2.log
# or   : ./jadd.py out.log in_*
#
# Robin Nandi, 30 October 2010

import os
import sys
import json
import math
import glob
import ROOT as r

selections = {
"Had":"Had_*NoSmear*",
"Muon":"Muon_*NoSmear*",
"Photon":"Photon_*NoSmear*"
}

thresholds = {
"Maps":"30*",
"200-325":"37*",
"325-375":"43*",
"375_upwards":"50*",
}

process_dictionary = {
"ZJets50":"ZJets*50*100*",
"ZJets100":"ZJets*100*200*",
"ZJets200":"ZJets*200*400*",
"ZJets400":"ZJets*400*inf*",
"TTJets":"TT_CT10*"
}

def Make_Collated_Root_Files():

  for select,select_val in selections.iteritems():
      for jetpt,jetpt_val in thresholds.iteritems():
          for process,pathname in process_dictionary.iteritems():
              if glob.glob("{folder_prefix}{thresh_val}/*{sample_title}.root".format(folder_prefix=select_val,thresh_val=jetpt_val,sample_title=pathname)):
                 bashcommand = "hadd {sel_prefix}_{thresh_prefix}_{samplename}.root {folder_prefix}{thresh_val}/*{sample_title}.root".format(sel_prefix=select,thresh_prefix=jetpt,samplename=process,folder_prefix=select_val,thresh_val=jetpt_val,sample_title=pathname)
                 print bashcommand
                 os.system(bashcommand)

def Grab_Event_Number(filename):

   foldername = "count_total"
   histname = "count"
   number_events = 1
   temp = r.TFile.Open(filename)
   hist = temp.Get(foldername+"/"+histname)
   if type(hist) != type(r.TH1F()): 
        print "Histogram is not right Type Skipping"
        return -1

   number_events = hist.GetEntries()

   return number_events

def Produce_Reweighted_Files():

    def Reweight_Histograms(filename,normalistation):

        print "This is where we create a new file filename+_reweighted then scale all histograms by 1/normalsation"

    for filename in glob.glob("*.root"):
        norm_number = Grab_Event_Number(filename)
        if norm_number < 0 : print " What is going on here you mug? "
        else:
           Reweight_Histograms(filename,norm_number)


def Final_Addition():

    add_dict = {

     "Zinv":"ZJets*",  
     "TTbar":"TTJets*"
     }

    for select in selections:
        for entry,path in add_dict.iteritems():
           if glob.glob("{selection}*{processname}.root".format(selection=select,processname=path)):
             bashcommand = "hadd {selection}_{process}.root {selection}*{processname}.root".format(selection=select,process=entry,processname=path)
             removecommand = "rm {selection}*{processname}.root".format(selection=select,processname=path)
             os.system(bashcommand)
             os.system(removecommand)


# Main Function Calls
Make_Collated_Root_Files()
Produce_Reweighted_Files()
Final_Addition()
