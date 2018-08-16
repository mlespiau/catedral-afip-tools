from detalle import Detalle
import pytest

class TestDetalle(object):
    CODE_FA = '01'
    CODE_FB = '06'
    CODE_NCB = '08'
    CODE_NCA = '03'
    
    def test_getTipoComprobante_FA(self):
        d = Detalle([0, 1, "FA", "3-3", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        assert d.getTipoComprobante() == self.CODE_FA

    def test_getTipoComprobante_FB(self):
        d = Detalle([0, 1, "FB", "3-3", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        assert d.getTipoComprobante() == self.CODE_FB

    def test_getTipoComprobante_NCB(self):
        d = Detalle([0, 1, "N/C B", "3-3", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        assert d.getTipoComprobante() == self.CODE_NCB

    def test_getTipoComprobante_NCA(self):
        d = Detalle([0, 1, "N/C A", "3-3", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        assert d.getTipoComprobante() == self.CODE_NCA

    def test_getTipoComprobante_E_returns_FA(self):
        d = Detalle([0, 1, "E", "3-3", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        assert d.getTipoComprobante() == self.CODE_FA

    def test_getTipoComprobante_UNKNOWN_raises_Error(self):
        with pytest.raises(Exception):
            d = Detalle([0, 1, "UNKNOWN", "3-3", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
            d.getTipoComprobante() == self.CODE_FA
    
