import xlrd
import csv

def csv_from_excel(fileName):
    wb = xlrd.open_workbook('./inputs/' + fileName + '.xlsx')
    sh = wb.sheet_by_index(0)
    your_csv_file = open('./outputs/' + fileName + '.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()
# runs the csv_from_excel function:
csv_from_excel('iva-ventas-ago18')