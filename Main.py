import importlib
import Library.src.Analysis.FatigueTest
importlib.reload(Library.src.Analysis.FatigueTest)
from Library.src.Analysis.FatigueTest import filereader, filecleaner_jupyter, filecleaner_extern, fileevaluator


import pandas as pd





#filecleaner('Output/RawData.xlsx','Output/StableAnalysisData.xlsx')
# for file in ['Input/Test1.csv','Input/Test2.csv']:
#     filereader(filepath=file,savepath=f'Output/{file[6:11]}_analysed.xlsx', cols=[0,3,8,10])

#
# for file in ['Output/Test1_analysed.xlsx','Output/Test2_analysed.xlsx']:
#     filecleaner_jupyter(filepath=file,savepath=f"{file[:-5]}_evaluated.xlsx")

fileevaluator()


# data = pd.read_excel('Output/Test1_analysed.xlsx', engine='openpyxl')
#
# print(data.dtypes)


