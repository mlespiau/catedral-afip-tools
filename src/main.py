from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import datetime
import io
import csv

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class VentaCatedral:
    def __init__(self, data):
        self.data = data
        self.tipoComprobante = data[2]
        self.fechaComprobante = data[1]
        if self.isEmpty() == False:
            puntoDeVentaAndNumeroDeComprobante = data[3].split("-")
            self.puntoDeVenta = puntoDeVentaAndNumeroDeComprobante[0]
            self.numeroDeComprobante = puntoDeVentaAndNumeroDeComprobante[1]

    def getTipoComprobante(self):
        tipoComprobantes = { 'FA': '01', 'FB': '06', 'N/C B': '08', 'N/C A': '03' }
        tipo = tipoComprobantes.get(self.tipoComprobante);
        if tipo == None:
            raise ValueError('El tipo de comprobante es desconocido: ' + self.tipoComprobante)
        else:
            return tipo

    def getControladorFiscal(self):
        return 'C'

    def getFechaComprobante(self):
        return datetime.datetime.strptime(self.fechaComprobante, "%m/%d/%y").strftime("%Y%m%d")

    def getPuntoDeVenta(self):
        return self.puntoDeVenta

    def getNumeroDeComprobante(self):
        return self.numeroDeComprobante

    def getNumeroDeComprobanteRegistrado(self):
        return 'NOSEQUEVAACA'

    def isEmpty(self):
        return self.tipoComprobante == ''

    def toAfip(self):
        return self.getTipoComprobante() + \
            self.getControladorFiscal() + \
            self.getFechaComprobante() + \
            self.getPuntoDeVenta() + \
            self.getNumeroDeComprobante() + \
            self.getNumeroDeComprobanteRegistrado() + \
            "a"

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
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            ventasCsv = csv.reader(stream, delimiter=',', quotechar='|')
            next(ventasCsv, None)
            result = ''
            isLastRound = False
            for row in ventasCsv:
                print(row)
                c = VentaCatedral(row)
                if c.isEmpty():
                    isLastRound = True
                    print('isLastRound is true')
                else:
                    if isLastRound == True:
                        # calculate last line
                        doNothing = None
                    else:
                        result += c.toAfip() + "\n"
            return result
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)

# Contralodor fiscal es siempre C en nuestro caso? de donde lo saco?
# http://www.afip.gov.ar/afip/resol136102_Anexo_II.html
