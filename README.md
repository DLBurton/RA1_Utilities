Here contains all the utilities used to help produce the RA1 analysis

This will contain

1. PU Reweight Calculation Tool - Produce_PileUp_Weights

        - MC PU distribution is taken straight from twiki

        - Data PU distribution is taken from outputting filtered json in ICF code after applying Full Muon selection.
                . Use CMSSSW tools to merge jsons into single json
                . Tale Pileup json from json database. https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/PileUp/
                . Use pileupCalc.py tool from 
                        https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData
                        
                         ./pileupCalc.py -i MyAnalysisJSON.txt --pileupjson.txt --calcMode true --minBiasXsec 69300 --maxPileupBin 60 --numPileupBins 60  MyDataPileupHistogram.root


2. Calculating Btagging probabilities for event by event reweighting. Used in signal samples and Data/MC plots  - Make_Eta_Pt_Maps.py


        - Used to calculate the eta and pt dependant tagging efficiencies for b,c and light flavoured jets. Last measured in late 2012, probably needs remeasuring before new paper. 

        - Run analysis over all MC samples with the lowest jet thresholds in the analysis

        - Btagger effieicncy should be analysis independent for a given eta and pt but Run RA1 Selection anyway for completeness

        - Then running this script on the output root file will calculate the efficiency of each eta/pt bin and output them for you. Now place this within the ICF Btag Reweighting code to apply to MC in future.

3. Any other useful scripts I use
