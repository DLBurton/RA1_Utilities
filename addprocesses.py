#!/usr/bin/env python
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
    """ colate rootfiles into sample specific output"""

    for select,select_val in selections.iteritems():
        for jetpt,jetpt_val in thresholds.iteritems():
            for process,pathname in process_dictionary.iteritems():
                if glob.glob("{folder_prefix}{thresh_val}/*{sample_title}.root".format(folder_prefix=select_val,
                                                                  thresh_val=jetpt_val,sample_title=pathname)):
                    bashcommand = "hadd {sel_prefix}_{thresh_prefix}_{samplename}_tmp.root {folder_prefix}{thresh_val}/*{sample_title}.root".format(sel_prefix=select,
                                                                                    thresh_prefix=jetpt,samplename=process,folder_prefix=select_val,
                                                                                    thresh_val=jetpt_val,sample_title=pathname)
                    print bashcommand
                    os.system(bashcommand)

def Grab_Event_Number(file):
    """ get the event number from file """

    foldername = "count_total"
    histname = "count"
    number_events = 1
    hist = file.Get(foldername+"/"+histname)
    if type(hist) != type(r.TH1F()): 
        print "Histogram is not right Type Skipping"
        return -1

   number_events = hist.GetEntries()

   return number_events

def Reweight_Histograms(file_name,normalistation):
    """ reweight every histogram in a given file """

    file = r.TFile.Open(file_name, "update")

    n_events = Grab_Event_Number(file)

    for dir_name in file.GetListOfKeys():
        dir = file.Get(dir_name.GetName())
        for hist_name in dir.GetListOfKeys():
            hist = dir.Get(hist_name.GetName())
            
            if type(hist) != type(r.TH1D()): continue

            hist.Scale( float(1./n_events) )

    file.Write("",r.TObject.kOverwrite)

    file.Close()

def Produce_Reweighted_Files():
    """ reweight files according to nevents run over """

    file_list = glob.glob("*_tmp.root")

    if len(file_list) !> 0:
        print ">> Error: no intermediate *_tmp.root sample files found."
        print ">> Exiting. (You mug...)"
        os.exit()

    # loop over all the intermediate rootfiles for each sample
    # (this is gunna be slooowwwwww)
    for filename in glob.glob("*_tmp.root"):
        Reweight_Histograms(filename)

def Final_Addition():

    add_dict = {
            "Zinv":"ZJets*",  
            "TTbar":"TTJets*"
        }

    for select in selections:
        for entry,path in add_dict.iteritems():
            if glob.glob("{selection}*{processname}.root".format(selection=select,processname=path)):
                bashcommand = "hadd {selection}_{process}.root {selection}*{processname}_tmp.root".format(selection=select,process=entry,processname=path)
                removecommand = "rm {selection}*{processname}.root".format(selection=select,processname=path)
                os.system(bashcommand)
                os.system(removecommand)


if __name__ == "__main__":
    # Main Function Calls
    Make_Collated_Root_Files()
    Produce_Reweighted_Files()
    Final_Addition()
