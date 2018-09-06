from cabecera import formatearImporte, CabeceraTipoDos
from main import crearReporte
import os

class TestMain(object):
    CUIT_EMERY = "20276886542"

    def test_formatear_importe_integer_ten(self):
        assert formatearImporte("10", 13, 2) == "000000000001000"

    def test_formatear_importe_float_ten(self):
        assert formatearImporte("10.0", 13, 2) == "000000000001000"

    def test_formatear_importe_float_ten_ten(self):
        assert formatearImporte("10.10", 13, 2) == "000000000001010"

    def test_formatear_importe_float_ten_rounding(self):
        assert formatearImporte("10.199", 13, 2) == "000000000001019"

    def test_formatear_importe_float_rounding(self):
        assert formatearImporte("271770.0099999999", 13, 3) == "0000000271770009"
        
    def test_formatear_importe_float_rounding_v2(self):
        assert formatearImporte("41133.18999999999", 13, 3) == "0000000041133189"

    def test_formatear_importe_float_rounding_sin_decimales(self):
        assert formatearImporte("47865.0", 13, 3) == "0000000047865000"
    
    def test_formatear_importe_float_rounding_v3(self):
        assert formatearImporte("310373.07999999996", 13, 3) == "0000000310373079"

    def test_cabecera_dos(self):
        csv_file = open("./test-data/iva-ventas-jun18.csv", "r")
        cDos = CabeceraTipoDos(self.CUIT_EMERY)
        actual_result = crearReporte(cDos, csv_file.read())
        actual_result = actual_result.replace('\r\n', os.linesep)
        csv_file.close()
        # "2201801             00000302                 20276886542                    00000031037307900000000000000000000002717700090000000041133189000000000000000000000000000000000000000000000000000000000000000000000000000"
        # +\
        assert "2" == cDos.getTipoRegistro()
        #    self.getPeriodo() +\
        assert "201801" == cDos.getPeriodo()
        #    self.getRelleno(13) +\
        assert "             " == cDos.getRelleno(13)
        #    self.getCandidadRegistrosDeTipoUno() +\
        assert "00000302" == cDos.getCandidadRegistrosDeTipoUno()
        #    self.getRelleno(17) +\
        assert "                 " == cDos.getRelleno(17)
        #    self.getCuitDelInformante() +\
        assert "20276886542" == cDos.getCuitDelInformante()
        #    self.getRelleno(20) +\
        assert "                    " == cDos.getRelleno(20)
        #    formatearImporte(self.getImporteTotal(), 12, 3) +\
        assert "000000310373079" == formatearImporte(cDos.getImporteTotal(), 12, 3)
        #    formatearImporte(self.getTotalConceptosQueNoIntegranElPrecioGravado(), 13, 2) +\
        assert "000000000000000" == formatearImporte(cDos.getTotalConceptosQueNoIntegranElPrecioGravado(), 13, 2)
        #    formatearImporte(self.getImporteNetoGravado(), 13, 2) +\
        assert "0000000271770009" == formatearImporte(cDos.getImporteNetoGravado(), 13, 3)
        #assert 271770.0099999999 == cDos.getImporteNetoGravado()
        #assert "111" == cDos.getImpuestoLiquidado()
        #    formatearImporte(self.getImpuestoLiquidado(), 13, 3) +\
        assert "0000000041133189" == formatearImporte(cDos.getImpuestoLiquidado(), 13, 3)
        assert "000000000000000" == formatearImporte(cDos.getImpuestoOperacionesExcentas(), 13, 2)
        assert "000000000000000" == formatearImporte(cDos.getImpuestosNacionales(), 13, 2)
        assert "2201801             00000302                 20276886542                    00000031037307900000000000000000000002717700090000000041133189000000000000000000000000000000" == cDos.getTipoRegistro() +\
            cDos.getPeriodo() +\
            cDos.getRelleno(13) +\
            cDos.getCandidadRegistrosDeTipoUno() +\
            cDos.getRelleno(17) +\
            cDos.getCuitDelInformante() +\
            cDos.getRelleno(20) +\
            formatearImporte(cDos.getImporteTotal(), 12, 3) +\
            formatearImporte(cDos.getTotalConceptosQueNoIntegranElPrecioGravado(), 13, 2) +\
            formatearImporte(cDos.getImporteNetoGravado(), 13, 3) +\
            formatearImporte(cDos.getImpuestoLiquidado(), 13, 3) +\
            formatearImporte(cDos.getImpuestoOperacionesExcentas(), 13, 2)  +\
            formatearImporte(cDos.getImpuestosNacionales(), 13, 2) # +\
            #formatearImporte(self.getImpuestosIngresosBrutos(), 13, 2) +\
            #formatearImporte(self.getImpuestosMunicipales(), 13, 0) +\
            #formatearImporte(self.getImpuestosInternos(), 14, 0)
        #    formatearImporte(self.getImpuestoOperacionesExcentas(), 13, 2) +\
        #    formatearImporte(self.getImpuestosNacionales(), 13, 2) +\
        #    formatearImporte(self.getImpuestosIngresosBrutos(), 13, 2) +\
        #    formatearImporte(self.getImpuestosMunicipales(), 13, 0) +\
        #    formatearImporte(self.getImpuestosInternos(), 14, 0)
        