import time

import pandas as pd


def filereader(filepath: str, savepath: str, cols: list):
    """Reads excel or csv file, calculates material data, writes to pandas df and saves as excel to be imported later.

    Keyword arguments:
        filepath            -- path to excel/csv file
        savepath            -- path where to save the file
        cols                -- Columns of file that map to the data representing:
                            ['Total Time (s)', 'Elapsed Cycles', 'Strain (%)', 'Stress (MPa)']
                            -> example [0,3,5,8]

    Additional arguments:

        """

    if filepath.endswith(".csv"):
        rawdata = pd.read_csv(filepath, usecols=cols)
    elif filepath.endswith(".xlsx"):
        rawdata = pd.read_excel(filepath, usecols=cols, engine='openpyxl')
    else:
        raise ValueError("Invalid file")

    rawdata.columns = ['Total Time (s)', 'Elapsed Cycles', 'Strain (%)', 'Stress (MPa)']

    # TODO: Write function to normalise the data the desired way

    while True:
        # case = input("normalize data around first (y/n)")
        case = 'y'
        if case in (["Y", "y"]):
            epsilonzero = rawdata['Strain (%)'][0]
            sigmazero = rawdata['Stress (MPa)'][0]

            rawdata['Strain (%)'] = rawdata['Strain (%)'].subtract(epsilonzero)
            rawdata['Stress (MPa)'] = rawdata['Stress (MPa)'].subtract(sigmazero)
            break
        elif case in (["N", "n"]):
            break
        else:
            continue

    Data = pd.concat([rawdata.groupby('Elapsed Cycles')[['Strain (%)', 'Stress (MPa)']].min(),
                      rawdata.groupby('Elapsed Cycles')[['Strain (%)', 'Stress (MPa)']].max()], axis=1)

    Data.columns = ['Strain Min (%)', 'Stress Min (MPa)', 'Strain Max (%)', 'Stress Max (MPa)']

    Data[['Strain Max (%)', 'Strain Min (%)']] = Data[['Strain Max (%)', 'Strain Min (%)']].multiply(100)
    Data['Strain Amplitude (%)'] = (Data['Strain Max (%)'] - Data['Strain Min (%)']) / 2
    Data['Stress Amplitude (MPa)'] = (Data['Stress Max (MPa)'] - Data['Stress Min (MPa)']) / 2

    # plotstablezone(Data)
    Data.to_excel(savepath)
    return Data


def fileevaluator():
    import os
    import numpy as np
    from tkinter import Tk
    from tkinter.filedialog import askdirectory, askopenfilenames
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('TkAgg')
    # matplotlib.interactive(True)
    import seaborn as sns
    sns.set()
    from matplotlib.widgets import RangeSlider, Button, RadioButtons

    filepaths = askopenfilenames()
    savedirectory = askdirectory()

    for file in filepaths:
        Data = pd.read_excel(file, engine='openpyxl')
        Data["Stable"] = 'Stable'

        fig, ax = plt.subplots(figsize=(16, 9))
        plt.subplots_adjust(bottom=0.25)

        slider_ax = plt.axes([0.20, 0.1, 0.60, 0.03])
        slider = RangeSlider(ax=slider_ax, label="Stable Zone", valmin=0, valmax=Data["Elapsed Cycles"].max(),
                             valstep=1, valfmt='%0.0f')

        donebuttonax = plt.axes([0.8, 0.025, 0.1, 0.04])
        button = Button(donebuttonax, 'Done', hovercolor='0.975')

        start = 10
        end = Data['Elapsed Cycles'].max()-10

        s, = ax.plot(Data.loc[(Data['Elapsed Cycles'] > start) & (Data['Elapsed Cycles'] < end)]["Elapsed Cycles"],
                   Data.loc[(Data['Elapsed Cycles'] > start) & (Data['Elapsed Cycles'] < end)]["Stress Amplitude (MPa)"],'o',Data.loc[(Data['Elapsed Cycles'] < start) & (Data['Elapsed Cycles'] > end)]["Elapsed Cycles"],Data.loc[(Data['Elapsed Cycles'] < start) & (Data['Elapsed Cycles'] > end)]["Stress Amplitude (MPa)"],'d')

        #TODO: u und s zu einem zusammenfassen!!
        #u, = ax.plot(Data.loc[(Data['Elapsed Cycles'] < start) & (Data['Elapsed Cycles'] > end)]["Elapsed Cycles"],
        #           Data.loc[(Data['Elapsed Cycles'] < start) & (Data['Elapsed Cycles'] > end)]["Stress Amplitude (MPa)"],'d')

        #sns.scatterplot(data=Data, x="Elapsed Cycles", y='Stress Amplitude (MPa)', hue="Stable", ax=ax)

        def update(val):
            #Data.loc[Data["Elapsed Cycles"] < int(val[0]), 'Stable'] = 'Unstable'
            #Data.loc[Data["Elapsed Cycles"] > int(val[1]), 'Stable'] = 'Unstable'



            #time.sleep(0.5)
            #matplotlib.axes.Axes.clear(ax)
            # sns.scatterplot(data=Data, x="Elapsed Cycles", y='Stress Amplitude (MPa)', hue="Stable", ax=ax)
            s.set_xdata(Data.loc[(Data['Elapsed Cycles'] > int(val[0])) & (Data['Elapsed Cycles'] < int(val[1]))]["Elapsed Cycles"])
            s.set_ydata(Data.loc[(Data['Elapsed Cycles'] > int(val[0])) & (Data['Elapsed Cycles'] < int(val[1]))]["Stress Amplitude (MPa)"])

            #u.set_xdata(Data.loc[(Data['Elapsed Cycles'] < int(val[0])) & (Data['Elapsed Cycles'] > int(val[1]))]["Elapsed Cycles"])
            #u.set_ydata(Data.loc[(Data['Elapsed Cycles'] < int(val[0])) & (Data['Elapsed Cycles'] > int(val[1]))]["Stress Amplitude (MPa)"])

            #u.set_xdata(Data.loc[Data['Stable'] == 'Unstable']["Elapsed Cycles"])
            #u.set_ydata(Data.loc[Data['Stable'] == 'Unstable']["Stress Amplitude (MPa)"])


            # ax.scatter(x=Data.loc[Data['Stable'] == 'Stable']["Elapsed Cycles"],
            #            y=Data.loc[Data['Stable'] == 'Stable']['Stress Amplitude (MPa)'], color='b')
            # ax.scatter(x=Data.loc[Data['Stable'] == 'Unstable']["Elapsed Cycles"],
            #            y=Data.loc[Data['Stable'] == 'Unstable']['Stress Amplitude (MPa)'], color='r')

            #plt.pause(0.5)
            #fig.canvas.draw()
            #fig.canvas.draw_idle()
            #fig.canvas.flush_events()
            # fig.canvas.draw_idle()

        def finished(event):
            filename = os.path.splitext(os.path.basename(file))[0]
            Data.to_excel(savedirectory + '/' + filename + '_evaluated.xlsx')
            plt.close(fig)


        slider.on_changed(update)
        button.on_clicked(finished)
        plt.show()


def filecleaner_jupyter(filepath: str, savepath: str):
    """Reads excel file produced by FatigueTestFileReader and interacts with the user to clean up the data

    Keyword arguments:
        filepath            -- path to excel
        savepath            -- path where to save the file"""

    import numpy as np
    from ipywidgets import Layout, IntSlider, interact_manual
    import matplotlib.pyplot as plt
    import seaborn as sns

    Data = pd.read_excel(filepath, engine='openpyxl')  # , index_col=0)

    high = Data["Elapsed Cycles"].max()

    def create_lineplot(high=high):
        with plt.style.context("ggplot"):
            plt.close()
            plt.figure(figsize=(16, 8))

            Data["Stable"] = np.where(Data["Elapsed Cycles"] <= high, "Stable", "Unstable")

            # sns.scatterplot(data=Data.loc[Data["Elapsed Cycles"]<=high], x="Elapsed Cycles", y ='Stress Amplitude (MPa)', hue="Stable" )
            sns.scatterplot(data=Data, x="Elapsed Cycles", y='Stress Amplitude (MPa)', hue="Stable")
            plt.xlim(0, Data["Elapsed Cycles"].max() * 1.05)
            plt.ylim(0, Data['Stress Amplitude (MPa)'].max() * 1.05)
            plt.title(f"Stable part. Last Cycle: {high}")
            # fig.canvas.draw()

            plt.show()

            Data.to_excel(savepath)

    interact_manual(create_lineplot,
                    high=IntSlider(value=Data["Elapsed Cycles"].max(), min=1, max=Data["Elapsed Cycles"].max(), step=1,
                                   layout=Layout(width='1000px')))


def filecleaner_extern(filepath: str, savepath: str):
    """Reads excel file produced by FatigueTestFileReader and interacts with the user to clean up the data

    Keyword arguments:
        filepath            -- path to excel
        savepath            -- path where to save the file"""

    import plotly.express as px
    import jupyter_dash

    Data = pd.read_excel(filepath, engine='openpyxl')  # , index_col=0)

    high = Data["Elapsed Cycles"].max()
