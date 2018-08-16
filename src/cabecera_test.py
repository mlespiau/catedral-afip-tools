from cabecera import formatearImporte

class TestMain(object):
    def test_formatear_importe_integer_ten(self):
        assert formatearImporte("10", 13, 2) == "000000000001000"

    def test_formatear_importe_float_ten(self):
        assert formatearImporte("10.0", 13, 2) == "000000000001000"

    def test_formatear_importe_float_ten_ten(self):
        assert formatearImporte("10.10", 13, 2) == "000000000001010"