import numpy as np
import pandas as pd
import os
from tkinter.filedialog import askdirectory, askopenfilenames
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use('TkAgg')


def plotcyclesstress(figurewidth='nature-singlecolumn', figureheight=None, plotstyle='seaborn-deep',
                     figurestyle='whitegrid', dpi=500, filetype='pdf', savedata=False, usestablezonedata=True,
                     logx=True):
    """Reads multiple evaluated excel files, calculates mean amplitudes, then fits Ramberg Osgood equation to the
    amplitudes and returns a fitting plot.

    Keyword arguments:
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
        savedata            -- True/False whether to save the Dataframe as Excel file.
        usestablezonedata   -- True/False whether the evaluation from fileevaluator() should be used.
        logx                -- True/False whether to set the x-axis scale to logarithmic.

        """
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

    sns.set_context('notebook')

    filepaths = askopenfilenames(filetypes=[("Excel Files", '*.xlsx')], title='Which files shall be evaluated?')
    savedirectory = askdirectory(title='Where to save the results?')

    Data = pd.DataFrame()

    for file in filepaths:
        Samplename = os.path.splitext(os.path.basename(file))[0]
        if Samplename.endswith('_cleaned_evaluated'):
            Samplename = Samplename[:-18]
        elif Samplename.endswith('_cleaned'):
            Samplename = Samplename[:-8]

        temp = pd.read_excel(file, engine='openpyxl')

        if 'Stable' in temp.columns and usestablezonedata:
            temp = temp.iloc[:int(temp.index[temp['Stable'] == 'Stable'].tolist()[-1]), :]
        else:
            print('This Excel file has not yet been evaluated by fileevaluator()')
        temp.insert(0, 'Sample', Samplename)
        Data = pd.concat([Data, temp])

    colormap = sns.color_palette(plotstyles[plotstyle], n_colors=len(Data['Sample'].unique()))

    Data.reset_index(drop=True, inplace=True)
    plt.figure(figsize=figsize)
    sns.lineplot(data=Data, x='Elapsed Cycles', y='Stress Max (MPa)', hue='Sample', palette=colormap)
    sns.lineplot(data=Data, x='Elapsed Cycles', y='Stress Min (MPa)', hue='Sample', palette=colormap, legend=False)

    if logx:
        plt.xscale('log')
    plt.title('Elapsed Cycles - Stress')
    plt.tight_layout()

    titles = Data.groupby("Sample")['Strain Amplitude (%)'].median()
    Legends = []
    for title in titles:
        Legends.append(r"$\varepsilon_a$ = {:10.1f} %".format(title))
    order = titles.reset_index().sort_values(by=["Strain Amplitude (%)"]).index.tolist()
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(labels=[Legends[idx] for idx in order], handles=[handles[idx] for idx in order],
               title='Dehnungsamplitude', loc='center left')

    plt.xlabel('Elapsed Cycles [-]')
    plt.ylabel('Stress [MPa]')
    plt.savefig(savedirectory + '/' + 'cycles-stress.' + filetype, dpi=dpi)
    plt.show()

    if savedata:
        Data.to_excel(savedirectory + '/' + 'Plot-Cycles-Stress.xlsx', index=False)
