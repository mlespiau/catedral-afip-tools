import io, csv, datetime

def normalizarTipo(tipo):
    if tipo == "B":
        return "FB"
    else:
        return tipo

def normalizarTasa(tasa):
    return "{0:0.2f}".format(float(tasa.replace(',', '.')))

def normalizarFloat(valor):
    return valor.replace('.', '').replace(',', '.')

result = []
with open('../test-data/SUR-utf8.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    i = 0
    for row in reader:
        newRow = []
        if i == 0:
            newRow.append('')
            newRow.append('Fecha')
            newRow.append('Tipo')
            newRow.append('PV-Comprobante')
            newRow.append('Razon social')
            newRow.append('CUIT')
            newRow.append('Tasa')
            newRow.append('IVA - RI')
            newRow.append('Neto - RI')
            newRow.append('IVA - CF')
            newRow.append('Neto - CF')
            newRow.append('IVA - MON')
            newRow.append('Neto - MON')
            newRow.append('IVA - EX')
            newRow.append('Neto - EX')
            newRow.append('IVA - NC')
            newRow.append('Neto - NC')
            newRow.append('Percepciones')
            newRow.append('Perc. IVA')
            newRow.append('Imp. Internos')
            newRow.append('Total')
        elif row[8].strip() == '':
            continue
        elif row[8].strip() != '' and row[2].strip() == '':
            newRow.append('')
            newRow.append('')
            newRow.append('')
            newRow.append('')
            newRow.append('')
            newRow.append('')
            newRow.append('')
            newRow.append(normalizarFloat(row[7]))
            newRow.append(normalizarFloat(row[8]))
            newRow.append(normalizarFloat(row[9]))
            newRow.append(normalizarFloat(row[10]))
            newRow.append(normalizarFloat(row[11]))
            newRow.append(normalizarFloat(row[12]))
            newRow.append(normalizarFloat(row[13]))
            newRow.append(normalizarFloat(row[14]))
            newRow.append(normalizarFloat(row[15]))
            newRow.append(normalizarFloat(row[16]))
            newRow.append(normalizarFloat(row[17]))
            newRow.append(normalizarFloat(row[18]))
            newRow.append(normalizarFloat(row[19]))
            newRow.append(normalizarFloat(row[20]))
        else:
            newRow.append('')
            newRow.append(datetime.datetime.strptime(row[1], "%d/%m/%Y").strftime("%d/%m/%y"))
            newRow.append(normalizarTipo(row[2]))
            newRow.append(row[3])
            newRow.append(row[4])
            newRow.append(row[5])
            newRow.append(normalizarTasa(row[6]))
            newRow.append(normalizarFloat(row[7]))
            newRow.append(normalizarFloat(row[8]))
            newRow.append(normalizarFloat(row[9]))
            newRow.append(normalizarFloat(row[10]))
            newRow.append(normalizarFloat(row[11]))
            newRow.append(normalizarFloat(row[12]))
            newRow.append(normalizarFloat(row[13]))
            newRow.append(normalizarFloat(row[14]))
            newRow.append(normalizarFloat(row[15]))
            newRow.append(normalizarFloat(row[16]))
            newRow.append(normalizarFloat(row[17]))
            newRow.append(normalizarFloat(row[18]))
            newRow.append(normalizarFloat(row[19]))
            newRow.append(normalizarFloat(row[20]))
        result.append(newRow)
        i += 1

with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(result)
