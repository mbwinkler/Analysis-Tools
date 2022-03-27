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
            #fig.canvas.draw()

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




