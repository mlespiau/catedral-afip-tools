import datetime

def formatearImporte(importe, numerales, decimales):
    resultado = str(importe).split('.')
    parteEntera = int(resultado[0])
    parteDecimal = str(resultado[1])
    if len(parteDecimal) > 3:
        parteDecimal = parteDecimal[:3]
    return ('{0:0' + str(numerales) + 'd}').format(parteEntera) + str(parteDecimal).ljust(decimales, '0')

class CabeceraTipoUno:
    def __init__(self, data):
        self.data = data
        self.fechaComprobante = data[1]
        self.tipoComprobante = data[2]
        self.cuit = data[5]
        self.importeTotal = data[20]
        self.razonSocial = data[4]
        if self.isEmpty() == False:
            puntoDeVentaAndNumeroDeComprobante = data[3].split("-")
            self.puntoDeVenta = puntoDeVentaAndNumeroDeComprobante[0]
            self.numeroDeComprobante = puntoDeVentaAndNumeroDeComprobante[1]
            self.calculateImporteNetoGravado()

    def getTipoRegistro(self):
        return '1'

    def getFechaComprobante(self):
        return datetime.datetime.strptime(self.fechaComprobante, "%m/%d/%y").strftime("%Y%m%d")

    def getTipoComprobante(self):
        tipoComprobantes = { 'FA': '01', 'FB': '06', 'N/C B': '08', 'N/C A': '03' }
        tipo = tipoComprobantes.get(self.tipoComprobante);
        if tipo == None:
            raise ValueError('El tipo de comprobante es desconocido: ' + self.tipoComprobante)
        else:
            return tipo

    def isEmpty(self):
        return self.data[1] == ''

    def getControladorFiscal(self):
        return 'C'

    def getPuntoDeVenta(self):
        return self.puntoDeVenta

    def getNumeroDeComprobante(self):
        return self.numeroDeComprobante

    def getNumeroDeComprobanteRegistrado(self):
        return self.numeroDeComprobante

    def getCantidadDeHojas(self):
        return '{0:03d}'.format(1)

    def getCodigoDeDocumentoIdentificatorioDelComprador(self):
        if self.cuit.strip() == '0' or self.cuit.strip() == '':
            return '96'
        else:
            return '80'

    def getNumeroDeDocumentoIdentificatorioDelComprador(self):
        if self.cuit.strip() == '0' or self.cuit.strip() == '':
            return '00011111111' # para consumidor final todos 1
        else:
            return self.cuit

    def getDenominacionDeComprador(self):
        if len(self.razonSocial) > 30:
            limit = 30
        else:
            limit = len(self.razonSocial)
        return self.razonSocial[:limit].ljust(30, ' ')

    def getImporteTotal(self):
        return self.importeTotal

    def getTotalConceptosQueNoIntegranElPrecioGravado(self):
        return '0.0'

    def calculateImporteNetoGravado(self):
        netoRI = self.data[8].split('.')
        netoRIinteger, netoRIdecimal = int(netoRI[0]), netoRI[1]
        netoCF = self.data[10].split('.')
        netoCFinteger, netoCFdecimal = int(netoCF[0]), netoCF[1]
        netoMON = self.data[12].split('.')
        netoMONinteger, netoMONdecimal = int(netoMON[0]), netoMON[1]
        netoEX = self.data[14].split('.')
        netoEXinteger, netoEXdecimal = int(netoEX[0]), netoEX[1]
        netoNC = self.data[16].split('.')
        netoNCinteger, netoNCdecimal = int(netoNC[0]), netoNC[1]
        if  netoRIinteger > 0:
            self.importeNetoGravado = self.data[8]
            self.impuestoLiquidado = self.data[7]
            self.tipoResponsable = '01'
        elif netoCFinteger > 0:
            self.importeNetoGravado = self.data[10]
            self.impuestoLiquidado = self.data[9]
            self.tipoResponsable = '05'
        elif netoMONinteger > 0:
            self.importeNetoGravado = self.data[12]
            self.impuestoLiquidado = self.data[11]
            self.tipoResponsable = '06'
        elif netoEXinteger > 0:
            self.importeNetoGravado = self.data[14]
            self.impuestoLiquidado = self.data[13]
            self.tipoResponsable = '09'
        elif netoNCinteger > 0:
            self.importeNetoGravado = self.data[16]
            self.impuestoLiquidado = self.data[15]
            self.tipoResponsable = '03'
        else:
            self.importeNetoGravado = '0.0'
            self.impuestoLiquidado = '0.0'
            # que ponemos?
            self.tipoResponsable = '01'

    def getImporteNetoGravado(self):
        return self.importeNetoGravado

    # Campo 15: Impuesto liquidado.- IVA que esta en el excel
    # Revisar
    def getImpuestoLiquidado(self):
        return self.impuestoLiquidado

    def getImpuestoLiquidadoRniNoCategorizados(self):
        return '0.0'

    def getImpuestoOperacionesExcentas(self):
        return '0.0'

    def getImpuestosNacionales(self):
        return '0.0'

    def getImpuestosIngresosBrutos(self):
        return '0.0'

    def getImpuestosMunicipales(self):
        return '0.0'

    def getImpuestosInternos(self):
        return '0.0'

#Campo 22: Transporte.
#Es un valor mayor o igual a cero.
#Deberá contener la sumatoria de los ítems facturados hasta la hoja que se está registrando inclusive
#(sumatoria del campo 11 del archivo de detalle).
#Sólo existirá transporte si la cantidad de hojas (campo 8) es mayor a uno.
#Este campo será cero en la última hoja del comprobante lo cual, de existir una correlatividad numérica en los comprobantes,
#se determina con la siguiente validación: Campo 7 + Campo 8 - 1= Campo 6.
    def getTransporte(self):
        return '0.0'

    def getTipoResponsable(self):
        return self.tipoResponsable

    def getCodigoMoneda(self):
        return 'PES'

    def getTipoCambio(self):
        return '{0:04d}'.format(1) + str('0').ljust(6, '0')

    def getCantidadAlicuotasIva(self):
        return '1'

    def getCodigoOperacion(self):
        return ' '

    def getCai(self):
        return ' '

    def getFechaVencimiento(self):
        return ''

    def getFechaAnulacion(self):
        return ''

    def getInformacionAdicional(self):
        return ' '

    def toAfip(self):
        return self.getTipoRegistro() +\
            self.getFechaComprobante() +\
            self.getTipoComprobante() +\
            self.getControladorFiscal() +\
            self.getPuntoDeVenta() +\
            self.getNumeroDeComprobante() +\
            self.getNumeroDeComprobanteRegistrado() +\
            self.getCantidadDeHojas() +\
            self.getCodigoDeDocumentoIdentificatorioDelComprador() +\
            self.getNumeroDeDocumentoIdentificatorioDelComprador() +\
            self.getDenominacionDeComprador() +\
            formatearImporte(self.getImporteTotal(), 13, 2) +\
            formatearImporte(self.getTotalConceptosQueNoIntegranElPrecioGravado(), 13, 2) +\
            formatearImporte(self.getImporteNetoGravado(), 13, 2) +\
            formatearImporte(self.getImpuestoLiquidado(), 13, 2) +\
            formatearImporte(self.getImpuestoLiquidadoRniNoCategorizados(), 13, 2) +\
            formatearImporte(self.getImpuestoOperacionesExcentas(), 13, 2) +\
            formatearImporte(self.getImpuestosNacionales(), 13, 2) +\
            formatearImporte(self.getImpuestosIngresosBrutos(), 13, 2) +\
            formatearImporte(self.getImpuestosMunicipales(), 13, 2) +\
            formatearImporte(self.getImpuestosInternos(), 13, 2) +\
            formatearImporte(self.getTransporte(), 13, 2) +\
            self.getTipoResponsable() +\
            self.getCodigoMoneda() +\
            self.getTipoCambio() +\
            self.getCantidadAlicuotasIva() +\
            " 6631535275180520160811"
#            self.getCodigoOperacion() +\
#            self.getCai() +\
#            self.getFechaVencimiento() +\
#            self.getFechaAnulacion() +\
#            self.getInformacionAdicional()

# Campo 27: Código de operación. - E
# Campo 28: CAI. - blanco
# Campo 29: Fecha de vencimiento.
# Campo 30: Fecha anulación del comprobante.

class CabeceraTipoDos:
    def __init__(self, cuitDelInformante):
        self.tipoRegistro = '2'
        self.periodo = 'AAAAMM'
        self.cantidadRegistrosDeTipoUno = 0
        self.importeTotal = 0
        self.importeNetoGravadoTotal = 0
        self.impuestoLiquidado = 0
        self.cuitDelInformante = cuitDelInformante

    def addRow(self, data, cabeceraTipoUno):
        self.cantidadRegistrosDeTipoUno += 1
        print(data[20])
        self.importeTotal += float(data[20])
        self.importeNetoGravadoTotal += float(cabeceraTipoUno.getImporteNetoGravado())
        self.impuestoLiquidado += float(cabeceraTipoUno.getImpuestoLiquidado())
        if self.periodo == 'AAAAMM':
            self.periodo = datetime.datetime.strptime(data[1], "%d/%m/%y").strftime("%Y%m")

    def getTipoRegistro(self):
        return self.tipoRegistro

    def getPeriodo(self):
        return self.periodo

    def getRelleno(self, espaciosEnBlanco):
        return ''.ljust(espaciosEnBlanco, ' ')

    def getCandidadRegistrosDeTipoUno(self):
        return '{0:08d}'.format(self.cantidadRegistrosDeTipoUno)

    def getCuitDelInformante(self):
        # 20276886542 emery
        return self.cuitDelInformante

    def getImporteTotal(self):
        return self.importeTotal

    def getTotalConceptosQueNoIntegranElPrecioGravado(self):
        return '0.0'

    def getImporteNetoGravado(self):
        return self.importeNetoGravadoTotal

    def getImpuestoLiquidado(self):
        return self.impuestoLiquidado

    def getImpuestoOperacionesExcentas(self):
        return '0.0'

    def getImpuestosNacionales(self):
        return '0.0'

    def getImpuestosIngresosBrutos(self):
        return '0.0'

    def getImpuestosMunicipales(self):
        return '0.0'

    def getImpuestosInternos(self):
        return '0.0'

    def toAfip(self):
        return self.getTipoRegistro() +\
            self.getPeriodo() +\
            self.getRelleno(13) +\
            self.getCandidadRegistrosDeTipoUno() +\
            self.getRelleno(17) +\
            self.getCuitDelInformante() +\
            self.getRelleno(20) +\
            formatearImporte(self.getImporteTotal(), 12, 3) +\
            formatearImporte(self.getTotalConceptosQueNoIntegranElPrecioGravado(), 13, 2) +\
            formatearImporte(self.getImporteNetoGravado(), 13, 2) +\
            formatearImporte(self.getImpuestoLiquidado(), 13, 2) +\
            formatearImporte(self.getImpuestoOperacionesExcentas(), 13, 2) +\
            formatearImporte(self.getImpuestosNacionales(), 13, 2) +\
            formatearImporte(self.getImpuestosIngresosBrutos(), 13, 2) +\
            formatearImporte(self.getImpuestosMunicipales(), 13, 2) +\
            formatearImporte(self.getImpuestosInternos(), 13, 2)
