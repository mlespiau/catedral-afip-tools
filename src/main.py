from flask import Flask, request, render_template, Response
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from detalle import Detalle
from cabecera import CabeceraTipoUno, CabeceraTipoDos
import io
import csv


ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
            ventasCsv = csv.reader(stream, delimiter=',', quotechar='"')
            next(ventasCsv, None)
            detalle = ''
            cabecera = ''
            isLastRound = False
            cDos = CabeceraTipoDos()
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
            return Response(cabecera + cDos.toAfip() + "\r\n" + "\r\n\r\n\r\n\r\n\r\n---\r\n\r\n\r\n" + detalle, mimetype='text/text')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)

# http://www.afip.gov.ar/afip/resol136102_Anexo_II.html
