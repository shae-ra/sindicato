# Referencia de la librería querier.py

La presente es una lista de las funciones y las variables miembro de la clase Querier.
Querier es una clase que funciona como libreria intermedia para el conector a una base de datos hecha en MySQL, el objeto es un singleton que debe usarse como objeto global entre todos los archivos de la aplicación.

## Miembros de la clase Querier:

- tablas
- usuario
- password
- host
- database

## Funciones de la clase Querier

### Querier(usuario, password, host, database)

Constructor del objeto Querier, éste crea una instancia única que al ser llamado.

Parámetros:

| Variable  | Tipo      | Valor por Defecto |   
| ----------|---------- | ------------------|
| usuario   | string    | root              |
| password  | string    | toor              |
| host      | string    | 127.0.0.1         |
| database  | string    | database          |

### insertarElemento(tabla, elemento)

Primero se asegura que exista la tabla mediante el método existeTabla(), de ser verdadero intentará hacer una consulta. Si la consulta es exitosa devuelve **True** *(verdadero)*, de lo contrario devuelve el error producido por MySQL.

El error retornado está para ser implementado en el programa, ya sea en un log, debugger o incluso puede modificarse para que se muestre en pantalla.

#### Parámetros:

| Variable  | Tipo      | Valor por Defecto |   
| ----------|---------- | ------------------|
| tabla     | string    | Ninguno           |
| elemento  | dict      | Ninguno           |

##### Elemento:

El elemento a insertar debe ser un diccionario en el que la clave *(key)* corresponda con el nombre de la columna en la base de datos y el valor *(value)* del diccionario corresponda con el valor que tendrá en la base de datos dicha columna.

#### Retornos:

| Tipo      | Motivo            |
|---------- | ----------------- |
| Bool      | Ingreso exitoso   |
| Object    | Error             |

#### Ejemplo:

```python
usuario = { 'username' : 'RStallman',
  'nombre' : 'Richard',
  'apellido' : 'Stallman' }

querier.insertarElemento("usuarios", usuario)
  ```
### traerElemento(tabla, elemento)
### traerElementos(campos, condiciones, limite, uniones, orden)

#### Parámetros

| Parámetro   | Tipo                | Valor por Defecto |
| ------------|---------------------|-------------------|
| campos      | [string, ]          | Ninguno           |
| condiciones | [(str, str, str), ] | Obligatorio       |
| limite      | string              | Obligatorio       |
| uniones     | string              | Obligatorio       |
| orden       | (string, string)    | Ninguno           |

##### Campos
##### Condiciones
##### Limite
##### Uniones
##### Orden

#### Retorno

#### Ejemplo

### actualizarElemento(elemento, condiciones)
### unirTabla()

## Métodos privados
### __agregarFiltros(elemento)
### __conectar()
### __consultar(elemento)
### __encampar(elemento)
### __probarConexion()
### __unirTabla()
