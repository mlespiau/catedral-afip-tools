from main import crearReporte 
from main import getSeparador
from cabecera import formatearImporte, CabeceraTipoDos
import os

class TestMain(object):
    CUIT_EMERY = "20276886542"
    
    def test_crear_reporte_emery_jun_2018(self):
        csv_file = open("./test-data/iva-ventas-jun18.csv", "r")
        f_cabecera = open("./test-data/cabecera_emery_jun_2018.txt", "r")
        f_detalle = open("./test-data/detalle_emery_jun_2018.txt", "r")
        expected_result = f_cabecera.read() + getSeparador() + f_detalle.read()
        expected_result = expected_result.replace('\r\n', os.linesep)
        f_cabecera.close()
        f_detalle.close()
        actual_result = crearReporte(CabeceraTipoDos(self.CUIT_EMERY), csv_file.read())
        actual_result = actual_result.replace('\r\n', os.linesep)
        csv_file.close()
        test_file = open("./test-data/test-expected.txt", "w")
        test_file.write(expected_result)
        test_file = open("./test-data/test-actual.txt", "w")
        test_file.write(actual_result)
        assert actual_result == expected_result

    def test_crear_reporte_emery_jul_2018_sin_decimales(self):
        csv_file = open("./test-data/iva-ventas-jul18-sin-decimales.csv", "r")
        f_cabecera = open("./test-data/cabecera_emery_jul_2018.txt", "r")
        f_detalle = open("./test-data/detalle_emery_jul_2018.txt", "r")
        expected_result = f_cabecera.read() + getSeparador() + f_detalle.read()
        expected_result = expected_result.replace('\r\n', os.linesep)
        f_cabecera.close()
        f_detalle.close()
        actual_result = crearReporte(CabeceraTipoDos(self.CUIT_EMERY), csv_file.read())
        actual_result = actual_result.replace('\r\n', os.linesep)
        csv_file.close()
        test_file = open("./test-data/test-emery-jul-2018-expected.txt", "w")
        test_file.write(expected_result)
        test_file = open("./test-data/test-emery-jul-2018-actual.txt", "w")
        test_file.write(actual_result)
        assert actual_result == expected_result
