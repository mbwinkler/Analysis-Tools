import importlib
#TODO: Johannes nach TUM Style ja/nein mit Logo etc fragen
#   Axenbeschriftung Stress in MPa → anpassen
#       -Parameter Beschriftungssstil
#   Plothysterese Cyclenporzent angeben in Label
#   Plotcyclestress Parameter um die Zyklen auf Maxzykles 0,1 zu normieren

from TUM-MET.Fatigue.Analysis.FatigueTest import filereader, fileevaluator
from Library.src.Fitting.RambergOsgood import rambergosgood
from Library.src.Plotting.PlotCyclesStress import plotcyclesstress
from Library.src.Plotting.PlotHystereses import plothystereses


#filereader()
#fileevaluator(save=True, filetype='svg')
#rambergosgood(YoungsModulus=70000, dpi=500, hue=True, save=True, filetype='pdf', plotstyle='seaborn-spectral', figurewidth='nature-doublecolumn')
plotcyclesstress(normalizecycles=True,figurewidth='nature-doublecolumn', plotstyle='seaborn-deep', savedata=True, usestablezonedata=True)
#plothystereses(Cycles=[0.0, 0.5, 1.0], figurewidth='nature-doublecolumn', plotstyle='seaborn-rocket')

