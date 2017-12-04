
Comportamiento de las ventanas:


-- login/ingreso_sistema
	
	pushbutton_Ingresar --> Principal/menu_principal.ui (stackedWidget con los archivos .ui)
		
		pushButton_afiliados  --> lista_afiliados.ui
			click(nombre_del_afiliado) --> detalle_afiliados.ui
				pushbutton_guardar --> Guarda la modificacion
				pushbutton_ingresarDebito --> carga_debito.ui
				pushbutton_imprimir_planilla --> ARCHIVO .PDF

		pushbutton_proveedores --> lista_proveedores.ui
			click(nombre_del_proveedor) --> detalle_proveedores.ui
		
		pushbutton_liquidacion --> liquidador.ui

		

		
