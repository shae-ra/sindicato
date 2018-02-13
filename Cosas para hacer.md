# Lista de cosas para hacer

- En Ficha de afiliado -> debitos automaticos -> Orden /Cred. N° debe ser autogenerado y estar bloqueado a menos que sea un proveedor específico que provea sus propios números/órdenes.
- Proveedor -> agregar campo booleano para los que provean sus propios números/órdenes

- | Mes | Proveedor | Importe | Cuota N° | Total Cuotas | #Planilla a imprimir

- | Mes | Proveedor | Importe | Cuota | Total de Cuotas | Fecha de carga | id_usuario | #Pantalla de debitos automáticos

- | Mes | Proveedor | Importe | Cuota | Total de Cuotas | Estado | Motivo | #Pantalla de historial de descuentos
    - Estados:
        - Procesado Correctamente
        - Rechazado
    - Motivos:
        - Si está procesado correctamente no muestra nada (*En Blanco*)
        - Si está rechazado el motivo es:
            - **Falta de fondos**
            - **Cuenta cerrada**
            - **Cuenta inexistente**
            - Algo #Llenar después

- | Legajo | Apellido | Nombre | DNI | Dirección | Teléfono | #Ordenado alfabéticamente por apellido. Pantalla afiliados
    - Dirección: Calle + Altura + Piso + Depto + (Localidad)

- | Fecha | Tipo | Cantidad | Detalle | #Pantalla de Servicios solicitados

- | Id de proveedor | Nombre | CUIT | Dirección | Teléfono | #Pantalla proveedores
    - Dirección: Calle + Altura

- | Codigo | Apellido | Nombre | Legajo | Secretaria | #Pantalla usuarios

- Gestión de autenticación para usuarios
- Configuración de red:
    - Dirección de IP
    - Usuario de mysql
    - Contraseña (Encriptado)
    - Base de datos
