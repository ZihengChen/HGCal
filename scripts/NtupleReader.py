from pylab import *
import pandas as pd
from root_pandas import read_root
from RechitCalibrator import *
import common

class NtupleReader():
    def __init__(self,fileName):

        self.baseDir = common.getBaseDir( isLocal=False )
        self.fileName = fileName
        self.ntupleFileName    = self.baseDir + 'data/ntuples/' + fileName + ".root"
        self.dataframeFileName = self.baseDir + 'data/pickles/' + fileName + ".pkl"

        self.sigmaNoiseCut = 3

        self.variableNames = ['l','e','t','x','y','z','gen_e','gen_vx','gen_vy','gen_vz','gen_id','gen_tag']
        
        self.variableNamesInNtuple = ['rechit_thickness', # need for calibration purpose
            'rechit_layer','rechit_energy','rechit_time','rechit_x','rechit_y','rechit_z', 
            'genpart_energy','genpart_dvx','genpart_dvy','genpart_dvz','genpart_pid','genpart_gen'
            ]


    def getDataFrame(self, savePickle=False):
        
        ntuple = read_root( self.ntupleFileName, 'ana/hgc', columns=self.variableNamesInNtuple )

        rc = RecHitCalibration()
        df = pd.DataFrame(columns=self.variableNames)

        for index, row in ntuple.iterrows():

            thick  = (row["rechit_thickness"]/100 - 1).astype(int)
            layer  = row['rechit_layer']
            energy = row['rechit_energy']

            # ask rechit calibrator for noise threshold
            sigmaNoise = rc.sigmaNoiseGeV(layer, thick) 
            threshold  = self.sigmaNoiseCut * sigmaNoise

            # define selection critera for hit and gen
            hitAboveTreshold = energy >= sigmaNoise
            hitOnPosSide = row['rechit_z'] > 0
            genOnPosSide = row['genpart_dvz'] > 0

            # positive side ## 
            hitslt = hitOnPosSide & hitAboveTreshold
            genslt = genOnPosSide

            # fill this event record in dataframe 
            df.loc[index] = [
                layer[hitslt],
                energy[hitslt],
                row['rechit_time'][hitslt]
                row['rechit_x'][hitslt],
                row['rechit_y'][hitslt],
                row['rechit_z'][hitslt],
                row['genpart_energy'][genslt],
                row['genpart_dvx'][genslt],
                row['genpart_dvy'][genslt],
                row['genpart_dvz'][genslt],
                row['genpart_pid'][genslt],
                row['genpart_gen'][genslt]
            ]
        self.df = df
        if savePickle:
            df.to_pickle(self.dataframeFileName)

            




                  


        