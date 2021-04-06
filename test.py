import numpy as np
from mantid.simpleapi import *

IPTS = 24655
exp = 724
scans = [183, 184] #34, 182

van_IPTS = 24612
van_exp = 722
van_scan = 220

Wavelength = 1.0008

# Adust detector
DetectorHeightOffset = 0
DetectorDistanceOffset = 0
OutputAsMDEventWorkspace = True
MergeInputs = False

min_values = [-10, -10, -10]
max_values = [10, 10, 10]

binning_0 = [-8.02, 8.02, 401]
binning_1 = [-2.52, 2.52, 126]
binning_2 = [-8.02, 8.02, 401]

# Find peaks
CellType = 'Orthorhombic'
Centering = 'F'
MaxPeaks = 1000
PeakDistanceThreshold = 0.25
DensityThresholdFactor = 2000

UseLattice = True
LatticeA = 5
LatticeB = 5
LatticeC = 5
LatticeAlpha = 90
LatticeBeta = 90
LatticeGamma = 90

# Integrate peaks
PeakRadius = 0.25
BackgroundInnerRadius = 0
BackgroundOuterRadius = 0
ApplyLorentz = True
OutputFormat = 'SHELX'
OutputFile = './integrated_peaks.hkl'

# Predict peaks
ReflectionCondition='B-face centred'

# Convert to HKL
h_extents = [-5.1, 5.1]
k_extents = [-2.1, 2.1]
l_extents = [-20.1, 20.1]
binning = [251, 101, 1001]

# ---

rootname = '/HFIR/HB3A/IPTS-'

filename = rootname+'{}/shared/autoreduce/HB3A_exp{:04}_scan{:04}.nxs'
data_files = ', '.join([filename.format(IPTS,exp,s) for s in scans])

vanfilename = rootname+'{}/shared/autoreduce/HB3A_exp{:04}_scan{:04}.nxs'.format(van_IPTS,van_exp,van_scan)

MinValues = str(min_values[0])+','+str(min_values[1])+','+str(min_values[2])
MaxValues = str(max_values[0])+','+str(max_values[1])+','+str(max_values[2])

BinningDim0 = str(binning_0[0])+','+str(binning_0[1])+','+str(binning_0[2])
BinningDim1 = str(binning_1[0])+','+str(binning_1[1])+','+str(binning_1[2])
BinningDim2 = str(binning_2[0])+','+str(binning_2[1])+','+str(binning_2[2])

Extents = str(h_extents[0])+','+str(h_extents[1])+','\
        + str(k_extents[0])+','+str(k_extents[1])+','\
        + str(l_extents[0])+','+str(l_extents[1])
        
Bins = str(binning[0])+','+str(binning[1])+','+str(binning[2])

from mantid import config
config['Q.convention'] = "Inelastic"
config['Q.convention'] = "Crystallography"


data = HB3AAdjustSampleNorm(Filename=data_files, 
#                            VanadiumFile=vanfilename,
                            DetectorHeightOffset=DetectorHeightOffset,
                            DetectorDistanceOffset=DetectorDistanceOffset,
                            OutputAsMDEventWorkspace=OutputAsMDEventWorkspace,
                            MergeInputs=MergeInputs,
                            MinValues=MinValues,
                            MaxValues=MaxValues,
                            BinningDim0=BinningDim0,
                            BinningDim1=BinningDim1,
                            BinningDim2=BinningDim2)
                         
peaks = HB3AFindPeaks(InputWorkspace=data,
                      CellType=CellType,
                      Centering=Centering,
                      PeakDistanceThreshold=PeakDistanceThreshold,
                      Wavelength=Wavelength)
