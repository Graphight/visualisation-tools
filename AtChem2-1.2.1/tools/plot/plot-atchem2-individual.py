# -----------------------------------------------------------------------------
#
# Copyright (c) 2017 Sam Cox, Roberto Sommariva
#
# This file is part of the AtChem2 software package.
#
# This file is covered by the MIT license which can be found in the file
# LICENSE.md at the top level of the AtChem2 distribution.
#
# -----------------------------------------------------------------------------

## Plotting tool for the AtChem2 model output
## --> Python version [requires numpy & matplotlib]
##
## Acknowledgements: M. Panagi
##
## ARGUMENT:
## - directory with the model output
##
## USAGE:
##   python ./tools/plot/plot-atchem2-numpy.py ./model/output/
## ---------------------------------------------- ##
from __future__ import print_function
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

os.chdir(sys.argv[1])
print(os.getcwd())

with open('speciesConcentrations.output') as f:
    var1 = f.readline().split()
with open('environmentVariables.output') as f:
    var2 = f.readline().split()
with open('photolysisRates.output') as f:
    var3 = f.readline().split()
with open('photolysisRatesParameters.output') as f:
    var4 = f.readline().split()

df1 = np.loadtxt('speciesConcentrations.output', skiprows=1, unpack=True)
df2 = np.loadtxt('environmentVariables.output', skiprows=1, unpack=True)
df3 = np.loadtxt('photolysisRates.output', skiprows=1, unpack=True)
df4 = np.loadtxt('photolysisRatesParameters.output', skiprows=1, unpack=True)

nc1 = df1.shape[0]
nc2 = df2.shape[0]
nc3 = df3.shape[0]
nc4 = df4.shape[0]

g_species = input("Enter variable to graph: ")

ind = 0
arr = 0
try:
    ind = var1.index(g_species.upper())
    arr = 1
except:
    try: 
        ind = var2.index(g_species.upper())
        arr = 2
    except:
        try:
            ind = var3.index(g_species.upper())
            arr = 3
        except:
            try:
                ind = var4.index(g_species.upper())
                arr = 4
            except:
                print('given species not found! Please check it exists in output')
                sys.exit(1)
     
arrs = [var1,var2,var3,var4]
dfs = [df1,df2,df3,df4]
var = arrs[arr-1]
df = dfs[arr-1]           

with PdfPages('atchem2_output_'+str(var[ind])+'.pdf') as pdf:

    fig, ax = plt.subplots(figsize=(11,7))
    ax.plot(df[0],df[ind],)
    ax.plot(df[0], df[ind], linestyle='-', color='black')
    ax.set(title=var[ind], xlabel='seconds', ylabel='')
    ax.set_xlim(left=172800)
    if g_species.upper() == 'NO2' or g_species.upper() == 'NO':
        ax.set_yscale('log')
    else:
        plt.ticklabel_format(style='sci', axis='y', useMathText=True)
    plt.tight_layout()
    pdf.savefig(fig)

print("graphing...")

## ---------------------------- ##

print("\n===> atchem2_output_individual.pdf created in directory:", sys.argv[1], "\n\n")
