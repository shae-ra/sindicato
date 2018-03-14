import unittest
import modelos
from modelos import modelo_proveedores
from datetime import date

class FixturesTest(unittest.TestCase):

    def setUp(self):
        self.fixture = {
        'id': 3142213,
        'nombre': 'Juan Armando',
        'servicios': 'venta de repisas',
        'calle': 'Portana',
        'altura': 2146,
        'localidad': 'Merlo',
        'telefono': '(0220) 466-5253',
        'celular': '(011) 15 56492815',
        'email': 'porta@hotmail.com',
        'cuit': '18453254681',
        'razon_social': 'Repisas Fructiferas',
        'cbu': 4251587943351548796453,
        'banco': 'Provincia',
        'cuenta': 4831354675621509,
        'comision': '450156',
        'responsable': 'Martin Garcia',
        'forma_pago': 'Bono',
        'notas': 'Esto es un coso que no me importa la longitud que tenga. Es más debería sacar la restricción de maxlength teniendo en cuenta que estoy usando text en la base de datos y no ese no tiene límites :/'
        }

        self.model = modelo_proveedores.ModeloProveedores()

    def tearDown(self):
        del self.fixture
        del self.model

    def test_guardar_proveedor(self):
        self.assertTrue(self.model.guardarProveedor(self.fixture))

if __name__ == '__main__':
    unittest.main()
