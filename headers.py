import pandas as pd
import xlrd
import glob
import os


cur_path = os.getcwd()  # gets the path where the python file is located
path = cur_path + r'\excel'
files = [f for f in glob.glob(path + '**/*.xlsx', recursive=True)]  # gets the paths for all the excel files stored in 'excel' folder
filename = []
lenpath = len(path) + 1
dest_path = os.getcwd() + '\\'
dest_path = dest_path + 'template\\'
dest_path = dest_path + 'template' + '.txt'  # destination file for markdown
dest = open(dest_path, "w")

for f in files:
    filename.append(f[lenpath:len(f) - 5])  # gets the filenames of all the files in the 'excel' folder

for i in range(len(filename)):
    spreadsheet = pd.ExcelFile(files[i])  # opens all the excel files one by one
    spreadsheet_sheets = spreadsheet.sheet_names  # gets the list of names of all the sheets in an excel file
    if len(spreadsheet_sheets) <= 2:
        dest.write('t,' + filename[i] + ',' + spreadsheet_sheets[1] + ',')
        for j in range(len(spreadsheet_sheets)):
            sheet = pd.read_excel(spreadsheet, spreadsheet_sheets[j])  # opens all the sheets in an excel file sequentially
            sheetname = spreadsheet_sheets[j]
            dim = sheet.shape
            col_name = sheet.columns
            for k in range(dim[1]):
                if col_name[k][0] != '_':
                    l = len(col_name[k]) - 1
                    while col_name[k][l] != '>' and l > 0:
                        l = l-1
                    if len(col_name[k]) - l<=40:
                        if not l:
                            dest.write(col_name[k] + ',')
                        else:
                            dest.write(col_name[k][l+1:] + ',')
        dest.write("\n")
    else:
        sheets = []
        for j in range(len(spreadsheet_sheets)):
            sheets.append(pd.read_excel(spreadsheet, spreadsheet_sheets[j]))
        for j in range(len(sheets)):
            sheets[j].rename(columns={'_submission__uuid':'_uuid'}, inplace=True)
        temp = pd.merge(sheets[0], sheets[1], on = '_uuid')
        combined_sheet = []
        for j in range(len(spreadsheet_sheets)-2):
            combined_sheet.append(pd.merge(temp, sheets[j+2], on = '_uuid'))
        for j in range(len(combined_sheet)):
            dest.write('t,' + filename[i] +',' +spreadsheet_sheets[j+2]+ ',')
            dim = combined_sheet[j].shape
            col_name = combined_sheet[j].columns
            for k in range(dim[1]):
                if col_name[k][0] != '_':
                    l = len(col_name[k]) - 1
                    while col_name[k][l] != '>' and l > 0:
                        l = l-1
                    if len(col_name[k]) - l<=40:
                        if not l:
                            dest.write(col_name[k] + ',')
                        else:
                            dest.write(col_name[k][l+1:] + ',')
            dest.write('\n')
