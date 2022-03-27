import pandas as pd
import xlrd


def filereader(filepath: str, savepath: str):
    """Reads excel file, saves every tensile test found within excel to unique excel.

    Keyword arguments:
        filepath            -- path to excel/csv file
        savepath            -- path to folder where to save the files.

    Additional arguments:

        """
    sheetnames = xlrd.open_workbook(filepath).sheet_names()

    for sheet in sheetnames[1:]:
        data = pd.read_excel(filepath, sheetnames = sheet, usecols=[0, 1], engine="xlrd",
                             names=["Strain (%)", "Stress (MPa)"], skiprows=3)
        data.to_excel(f'{savepath}-{sheet}.xlsx')



    #TODO: Slider für Dehngrenze wie bei Fatigue Test => Kontrolle durch Formel Spannung(Rp0.2) = 0.002 * E
    #   Schäfer Methode weiter ausprobieren



