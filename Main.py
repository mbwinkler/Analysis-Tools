from TUMMET.Fatigue.Analysis import filereader, fileevaluator
from TUMMET.Fatigue.Plotting import plothystereses, plotcyclesstress
from TUMMET.Fatigue.Fitting import rambergosgood

# filereader()
# fileevaluator(save=True, filetype='svg')
# rambergosgood(YoungsModulus=70000, dpi=500, hue=True, save=True, filetype='pdf', plotstyle='seaborn-spectral', figurewidth='nature-doublecolumn')
#plotcyclesstress(normalizecycles=True, figurewidth='nature-doublecolumn', plotstyle='seaborn-deep', savedata=True,
#                 usestablezonedata=True)
plothystereses(Cycles=[0.0, 0.5, 1.0],useabsolutecycles=False, figurewidth='nature-doublecolumn', plotstyle='seaborn-rocket')
