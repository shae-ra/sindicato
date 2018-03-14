# validador_proveedor.py

esquemaProveedor = {
    'id' : { 'type' : 'integer', 'max' : 99999999 },
    'nombre' : { 'type': 'string', 'maxlength' : 50 },
    'servicios' : { 'type': 'string', 'maxlength' : 100 },
    'calle' : { 'type': 'string', 'maxlength' : 80 },
    'altura' : { 'type': 'integer', 'max' : 99999999 },
    'localidad' : { 'type': 'string', 'maxlength' : 50 },
    'telefono' : { 'type': 'string', 'maxlength' : 20 },
    'celular' : { 'type': 'string', 'maxlength' : 20 },
    'email' : { 'type': 'string', 'maxlength' : 80 },
    'cuit' : { 'type' : 'string', 'maxlength' : 11 },
    'razon_social' : { 'type': 'string', 'maxlength' : 60 },
    'cbu' : { 'type': 'integer', 'max' : 9999999999999999999999 },
    'banco' : { 'type': 'string', 'maxlength' : 60 },
    'cuenta' : { 'type': 'integer', 'max' : 9999999999999999 },
    'comision' : { 'type': 'string', 'maxlength' : 40 },
    'responsable' : { 'type': 'string', 'maxlength' : 40 },
    'forma_pago' : { 'type': 'string', 'maxlength' : 40 },
    'notas' : { 'type': 'string'},
}
