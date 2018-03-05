import unittest
import modelos
from modelos import modelo_afiliado
from datetime import date

class FixturesTest(unittest.TestCase):

    def setUp(self):
        print(date(1993, 1, 28))
        self.fixture = {
        'legajo' : 84625731,
        'dni' : 12949573,
        'tipo_afiliado' : 'activo',
        'cuil' : 84621584637,
        'apellido' : 'Ramirez',
        'nombre' : 'Mario',
        'fecha_nacimiento' : date(1993, 1, 28),
        'edad' : 28,
        'estado_civil' : 'soltero',
        'nacionalidad' : 'argentino',
        'calle' : 'Azcuenaga',
        'altura' : 425,
        'piso' : '3ro',
        'depto' : '4 D',
        'cod_postal' : '1523',
        'barrio' : 'Torcuato',
        'localidad' : 'Torcuato',
        'telefono_particular' : '(0220) 462-4542',
        'telefono_laboral' : '(0237) 462-4492',
        'celular' : '(011) 15529392',
        'email' : 'ramed90@hotmail.com.ar',
        'lugar_trabajo' : 'Castelar',
        'jerarquia' : 'Peon',
        'fecha_ingreso' : date(2012, 5, 22),
        'antiguedad' : 4,
        'nivel_estudios' : 'Secundario'
        }

        self.model = modelo_afiliado.ModeloAfiliado()

    def tearDown(self):
        del self.fixture

    def test_guardar_afiliado(self):
        self.assertTrue(self.model.guardarAfiliado(self.fixture))
        self.model.borrarAfiliado('afiliados', self.fixture['legajo'])

if __name__ == '__main__':
    unittest.main()
