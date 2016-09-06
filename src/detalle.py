import datetime

def formatearImporte(importe, numerales, decimales):
    resultado = str(importe).split('.')
    parteEntera = int(resultado[0])
    parteDecimal = str(resultado[1])
    if len(parteDecimal) > 3:
        parteDecimal = parteDecimal[:3]
    return ('{0:0' + str(numerales) + 'd}').format(parteEntera) + str(parteDecimal).ljust(decimales, '0')

class Detalle:
    def __init__(self, data):
        self.data = data
        self.tipoComprobante = data[2]
        self.fechaComprobante = data[1]
        if self.isEmpty() == False:
            puntoDeVentaAndNumeroDeComprobante = data[3].split("-")
            self.puntoDeVenta = puntoDeVentaAndNumeroDeComprobante[0]
            self.numeroDeComprobante = puntoDeVentaAndNumeroDeComprobante[1]
            self.calculateSubTotalPorRegistro()
            if data[6] == "21.00":
                self.alicuotaIva = "2100"
            elif data[6] == "10.50":
                self.alicuotaIva = "1050"
            else:
                self.alicuotaIva = "0000"

    def calculateSubTotalPorRegistro(self):
        netoRI = float(self.data[8])
        netoCF = float(self.data[10])
        netoMON = float(self.data[12])
        netoEX = float(self.data[14])
        netoNC = float(self.data[16])
        if  netoRI > 0:
            self.subTotalPorRegistro = netoRI
        elif netoCF > 0:
            self.subTotalPorRegistro = netoCF
        elif netoMON > 0:
            self.subTotalPorRegistro = netoMON
        elif netoEX > 0:
            self.subTotalPorRegistro = netoEX
        elif netoNC > 0:
            self.subTotalPorRegistro = netoNC
        else:
            self.subTotalPorRegistro = 0.0

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
        return self.numeroDeComprobante

    # Verificar con Lore
    def getCantidad(self):
        return '000000100000'

    # Verificar con Lore
    def getUnidadDeMedida(self):
        return '07'

    def getPrecioUnitario(self):
        return self.subTotalPorRegistro

    def getImporteBonificacion(self):
        return '0.0'

    def getSubTotalPorRegistro(self):
        # neto grabado
        # - responsable inscripto
        # - consumidor final
        # - etc.
        # usar NETO de la categoria que no sea 0
        return self.subTotalPorRegistro

    def getAlicuotaDeIvaAplicable(self):
        # entro con el IVA en la tabla del anexo y obtengo el codigo
        return self.alicuotaIva

    def getIndicacionDeExcentoOGrabado(self):
        return 'G'

    def getIndicacionDeAnulacion(self):
        return ' '

    def getLibre(self):
        return 'Texto libre'

    def isEmpty(self):
        return self.tipoComprobante == ''

    def toAfip(self):
        return self.getTipoComprobante() + \
            self.getControladorFiscal() + \
            self.getFechaComprobante() + \
            self.getPuntoDeVenta() + \
            self.getNumeroDeComprobante() + \
            self.getNumeroDeComprobanteRegistrado() + \
            self.getCantidad() + \
            self.getUnidadDeMedida() + \
            formatearImporte(self.getPrecioUnitario(), 13, 3) + \
            formatearImporte(self.getImporteBonificacion(), 13, 2) + \
            formatearImporte(self.getSubTotalPorRegistro(), 13, 2) + \
            self.getAlicuotaDeIvaAplicable() + \
            self.getIndicacionDeExcentoOGrabado() + \
            self.getIndicacionDeAnulacion() + \
            self.getLibre()
