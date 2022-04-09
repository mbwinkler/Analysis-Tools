from TUMMET.Fatigue.Analysis import evaluate_raw_data, evaluate_stable_zone
from TUMMET.Fatigue.Plotting import plot_cycles_stress, plot_hystereses
from TUMMET.Fatigue.Fitting import fit_ramberg_osgood

# filereader()
# fileevaluator(save=True, filetype='svg')
# rambergosgood(YoungsModulus=70000, dpi=500, hue=True, save=True, filetype='pdf', plotstyle='seaborn-spectral', figurewidth='nature-doublecolumn')
#plotcyclesstress(normalizecycles=True, figurewidth='nature-doublecolumn', plotstyle='seaborn-deep', savedata=True,
#                 usestablezonedata=True)
plot_hystereses(Cycles=[0.0, 0.5, 1.0],useabsolutecycles=False, figurewidth='nature-doublecolumn', plotstyle='seaborn-rocket')
