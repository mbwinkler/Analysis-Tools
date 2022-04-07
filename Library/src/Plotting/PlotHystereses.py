# TODO: Plotter für Hysteresen aus Rohdaten
#   Parameter: Cycles = Array(0.1,0.5,0.9) --> plottet 3 mal bei 0.1,0.5 und 0.9 der max Zyklen
#   Restliche Plotting Parameter wie Style etc einfach übernehmen
#   Im Plot Spannungsmaxium, Minimum etc angeben


import numpy as np
import pandas as pd
import os
from tkinter.filedialog import askdirectory, askopenfilenames
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
import seaborn as sns
from matplotlib.colors import ListedColormap

matplotlib.use('TkAgg')


def plothystereses(Cycles=None, figurewidth='nature-singlecolumn', figureheight=None, plotstyle='seaborn-deep',
                   figurestyle='whitegrid', dpi=500, filetype='pdf', cols=None, normalize=False):
    """Reads multiple evaluated excel files, calculates mean amplitudes, then fits Ramberg Osgood equation to the
    amplitudes and returns a fitting plot.

    Keyword arguments:
        Cycles              -- List of Normalized cycles to plot the respective hystereses.
                                Will never plot the last, therefore the failing, cycle.
                                Defaults to [0.0, 0.25, 0.5, 0.75, 1.0]. Accepts:
                                    - numpy.array()
                                    - List
        figurewidth         -- Width of figure. Float value in cm or one of the following:
                                    - 'nature-singlecolumn' --> Default
                                    - 'nature-oneandhalfcolumn'
                                    - 'nature-doublecolumn'
                                    - 'elsevier-minimal'
                                    - 'elsevier-singlecolumn'
                                    - 'elsevier-oneandhalfcolumn'
                                    - 'elsevier-doublecolumn'
                                    - 'science-singlecolumn'
                                    - 'science-doublecolumn'
                               Defaults to 'nature-singlecolumn'
        figureheight        -- Height of figure. Float value in cm. Defaults to value of figurewidth.
        plotstyle           -- Style of plot. One of the following:
                                    - 'seaborn-default' --> Default
                                    - 'seaborn-colorblind'
                                    - 'seaborn-rocket'
                                    - 'seaborn-crest'
                                    - 'seaborn-spectral'
                                    - 'red-blue'
        figurestyle         -- Seaborn figure Style. One of the following:
                                    - 'whitegrid' --> Default
                                    - 'white'
                                    - 'darkgrid'
                                    - 'dark'
                                    - 'ticks'

        dpi                 -- Dpi to save figure with. Int Value.
        filetype            -- specify filetype as one of the following:
                                    - 'pdf' --> Default
                                    - 'png'
                                    - 'ps'
                                    - 'eps'
                                    - 'svg'
        cols                -- Columns of file that map to the data representing:
                            ['Total Time (s)', 'Elapsed Cycles', 'Strain (%)', 'Stress (MPa)']
                            Default concerning the data at the chair of metal structures is [0,3,8,10]
        normalize           -- True/False whether to set the first entry as 0 or not. Default is False

        """
    if Cycles is None:
        Cycles = [0.0, 0.25, 0.5, 0.75, 1.0]
    figurewidths = {'nature-singlecolumn': 8.9,
                    'nature-oneandhalfcolumn': 12,
                    'nature-doublecolumn': 18.3,
                    'elsevier-minimal': 3,
                    'elsevier-singlecolumn': 9,
                    'elsevier-oneandhalfcolumn': 14,
                    'elsevier-doublecolumn': 19,
                    'science-singlecolumn': 5.5,
                    'science-doublecolumn': 12}
    plotstyles = {'seaborn-deep': 'deep',
                  'seaborn-colorblind': 'colorblind',
                  'seaborn-rocket': 'rocket',
                  'seaborn-crest': 'crest',
                  'seaborn-spectral': 'Spectral',
                  'red-blue': ['r']}
    if figurestyle not in ['whitegrid', 'white', 'darkgrid', 'dark', 'ticks']:
        print('Figure style not in list\n run "help(rambergosgood)" for details')
        return
    sns.set_style(figurestyle)

    if filetype not in ['png', 'pdf', 'ps', 'eps', 'svg']:
        print('Filetype not in list\n run "help(rambergosgood)" for details')
        return

    if figurewidth not in ['nature-singlecolumn', 'nature-oneandhalfcolumn', 'nature-doublecolumn', 'elsevier-minimal',
                           'elsevier-singlecolumn', 'elsevier-oneandhalfcolumn', 'elsevier-doublecolumn',
                           'science-singlecolumn',
                           'science-doublecolumn'] and not np.issubdtype(type(figurewidth), np.number):
        print('Figurewidth not in list\n run "help(rambergosgood)" for details')
        return
    elif figurewidth not in ['nature-singlecolumn', 'nature-oneandhalfcolumn', 'nature-doublecolumn',
                             'elsevier-minimal',
                             'elsevier-singlecolumn', 'elsevier-oneandhalfcolumn', 'elsevier-doublecolumn',
                             'science-singlecolumn',
                             'science-doublecolumn'] and np.issubdtype(type(figurewidth), np.number):
        width = figurewidth
    else:
        width = figurewidths[figurewidth]

    if figureheight is None:
        figsize = (width / 2.54, width / 2.54)
    else:
        figsize = (width / 2.54, figureheight / 2.54)

    if cols is None:
        cols = [0, 3, 8, 10]

    sns.set_context('notebook')

    filepaths = askopenfilenames(filetypes=[("Excel and CSV Files", '*.csv *.xlsx *.xls')], title='Which files shall '
                                                                                                  'be evaluated?')
    savedirectory = askdirectory(title='Where to save the results?')

    for file in tqdm(filepaths):

        if file.endswith(".csv"):
            rawdata = pd.read_csv(file, usecols=cols)
        elif file.endswith(".xlsx"):
            rawdata = pd.read_excel(file, usecols=cols, engine='openpyxl')
        else:
            raise ValueError("Invalid file")

        rawdata.columns = ['Total Time (s)', 'Elapsed Cycles', 'Strain (%)', 'Stress (MPa)']
        if normalize:
            epsilonzero = rawdata['Strain (%)'][0]
            sigmazero = rawdata['Stress (MPa)'][0]

            rawdata['Strain (%)'] = rawdata['Strain (%)'].subtract(epsilonzero)
            rawdata['Stress (MPa)'] = rawdata['Stress (MPa)'].subtract(sigmazero)

        Data = pd.concat([rawdata.groupby('Elapsed Cycles')[['Strain (%)', 'Stress (MPa)']].min(),
                          rawdata.groupby('Elapsed Cycles')[['Strain (%)', 'Stress (MPa)']].max()], axis=1)

        Data.columns = ['Strain Min (%)', 'Stress Min (MPa)', 'Strain Max (%)', 'Stress Max (MPa)']

        Data[['Strain Max (%)', 'Strain Min (%)']] = Data[['Strain Max (%)', 'Strain Min (%)']].multiply(100)
        Data['Strain Amplitude (%)'] = (Data['Strain Max (%)'] - Data['Strain Min (%)']) / 2
        Data['Stress Amplitude (MPa)'] = (Data['Stress Max (MPa)'] - Data['Stress Min (MPa)']) / 2

        colormap = sns.color_palette(plotstyles[plotstyle], n_colors=len(Cycles)).as_hex()
        maxcycles = rawdata['Elapsed Cycles'].max()
        rawdata['Strain (%)'] = rawdata['Strain (%)'].multiply(100)
        plt.figure(figsize=figsize)

        for index, cycle in enumerate(Cycles):
            cycleindex = np.ceil(cycle * maxcycles)
            if cycle == 1.0:
                cycleindex = np.ceil(cycle * maxcycles) - 1
            elif cycle == 0.0:
                cycleindex = 1.0

            cycleframe = rawdata.loc[rawdata['Elapsed Cycles'] == cycleindex]
            stressamplitude = Data.loc[cycleindex]['Stress Amplitude (MPa)']
            strainamplitude = Data.loc[cycleindex]['Strain Amplitude (%)']
            plt.plot(cycleframe['Strain (%)'], cycleframe['Stress (MPa)'], color=colormap[index],
                     label=f'Cycle = {cycleindex:.0f},\n' + f'$\sigma_a$      = {stressamplitude:.2f}')

        plt.legend(loc='upper left')
        plt.xlabel('Strain [%]')
        plt.ylabel('Stress [MPa]')
        plt.title(f'Hystereses - $\epsilon_a = {strainamplitude:.2f}$ %')
        plt.tight_layout()
        filename = os.path.splitext(os.path.basename(file))[0]
        plt.savefig(savedirectory + '/' + filename + '_Hystereses.' + filetype, dpi=dpi)
        plt.show()
