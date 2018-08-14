from flask import Flask, request, render_template, Response
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from detalle import Detalle
from cabecera import CabeceraTipoUno, CabeceraTipoDos
import io
import csv
import datetime

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def normalizarTipo(tipo):
    if tipo == "CF":
        return "FB"
    elif tipo == "RI":
        return "FA"
    else:
        return tipo

def normalizarTasa(tasa):
    return "{0:0.2f}".format(float(tasa.replace(',', '.')))

def normalizarFloat(valor):
    return valor.replace(',', '')

def crearReporte(cuit, ventasCsvText):
    stream = io.StringIO(ventasCsvText, newline=None)
    ventasCsv = csv.reader(stream, delimiter=',', quotechar='"')
    next(ventasCsv, None)
    detalle = ''
    cabecera = ''
    isLastRound = False
    cDos = CabeceraTipoDos(cuit)
    for row in ventasCsv:
        print(row)
        cUno = CabeceraTipoUno(row)
        d = Detalle(row)
        if cUno.isEmpty():
            isLastRound = True
            print('isLastRound is true')
        else:
            cDos.addRow(row, cUno)
            print('cUno' + row[0])
            if isLastRound == True:
                # calculate last line
                doNothing = None
            else:
                detalle += d.toAfip() + "\r\n"
                cabecera += cUno.toAfip() + "\r\n"
    return cabecera + cDos.toAfip() + "\r\n" + getSeparador() + detalle

def getSeparador():
    return "\r\n\r\n\r\n\r\n\r\n---\r\n\r\n\r\n"

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            return Response(crearReporte(request.form['cuit'], file.stream.read().decode("UTF8")), mimetype='text/text')
    return render_template('index.html')

@app.route("/csv/", methods=['GET', 'POST'])
def csv_parser():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            result = []
            reader = csv.reader(stream, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                print(i)
                print(row)
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
                    result.append(newRow)
                elif i < 8:
                    # do nothing
                    pepe = 0
                elif row[7].strip() == '':
                    # do nothing
                    pepe = 0
                else:
                    print(row[0])
                    newRow.append('')
                    try:
                        newRow.append(datetime.datetime.strptime(row[0].strip(), "%d/%m/%Y  %H:%M:%S").strftime("%m/%d/%y"))
                    except ValueError:
                        newRow.append(row[0])
                    newRow.append(normalizarTipo(row[9]))
                    newRow.append('{0:04d}'.format(int(row[11])) + '-' + '{0:08d}'.format(int(row[13])))
                    newRow.append(row[2])
                    newRow.append(row[4])
                    ivaRI = '0.0'
                    netoRI = '0.0'
                    ivaCF = '0.0'
                    netoCF = '0.0'
                    if row[9] == 'CF':
                        tasa = '21.00'
                        ivaCF = row[16]
                        netoCF = row[29]
                    elif row[9] == 'RI':
                        tasa = '21.00'
                        ivaRI = row[16]
                        netoRI = row[29]
                    else:
                        tasa = '21.00'
                    newRow.append(normalizarFloat(tasa))
                    newRow.append(normalizarFloat(ivaRI))
                    newRow.append(normalizarFloat(netoRI))
                    newRow.append(normalizarFloat(ivaCF))
                    if netoCF == '':
                        netoCF = '0.0'    
                    newRow.append(normalizarFloat(netoCF))
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append('0.0')
                    newRow.append(normalizarFloat(row[22]))
                    result.append(newRow)
                i = i + 1
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(result)
        csvText = output.getvalue()
        print(csvText)
        return Response(crearReporte(request.form['cuit'], csvText), mimetype='text/text')
    return render_template('csv.html')

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=8080, debug=True)

# http://www.afip.gov.ar/afip/resol136102_Anexo_II.html
