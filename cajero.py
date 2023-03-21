import json


class Cajero():
    archivo_datos = 'datos.json'
    quejas_bajas = 'quejas.json'
    saldos_usuarios = 'saldos.json'

    def prender(self):
        flag1 = True
        while flag1 != False:
            crear_user = input(
                'Desea crear un nuevo usuario?Escriba "si" si quiere hacerlo: ')
            if crear_user.lower() == 'si':
                self.usuario_nuevo()
            else:
                flag1 = False
        flag2 = True
        while flag2 != False:
            flag2 = self.iniciar_sesion()
        print('Cuenta cerrada, hasta pronto!!')


    def usuario_nuevo(self):
        try:
            with open(cajero.archivo_datos, 'r') as file:
                datos = json.load(file)
        except:
            datos = {}

        try:
            with open(cajero.saldos_usuarios, 'r') as file:
                saldo = json.load(file)
        except:
            saldo = {}

        while True:
            nro_tarjeta = input('Ingrese su nro de tarjeta: ')
            password = input('Ingrese su clave, debe contener minimo 8 digitos: ')
            if len(password) < 8:
                print('La clave debe contener minimo 8 digitos')
                continue
            else:
                if nro_tarjeta in datos:
                    print('Este nro de tarjeta ya tiene una cuenta creada')
                    continue
                elif password in datos.values():
                    print('Ya existe un usario con esa clave, porfavor creese otra')
                    continue
                else:
                    datos[nro_tarjeta] = password
                    saldo_inicial = 0
                    saldo[nro_tarjeta] = saldo_inicial

                    print('Se creo el usuario correctamete.')
                    break
            
        with open(cajero.saldos_usuarios, 'w') as file:
                    json.dump(saldo, file, indent=4)
                    
        with open(cajero.archivo_datos, 'w') as file:
            json.dump(datos, file, indent=4)


    def iniciar_sesion(self):

        while True:
            print("""
    BIENVENIDO A BANCO SANTANDER
    
          INGRESE AL MENU
        ====================
        1- INICIAR SESION
        2- SALIR
        ====================
    
    QUE OPCION DESEA REAELIZAR(1-3)
              """)
            entrar = input('Que desea hacer?(1-2): ')
            if entrar == '1':
                nro_tarjeta = input('Ingrese su nro de tarjeta: ')
                password = input('Ingrese su clave: ')
                if self.autenticar_usuario(nro_tarjeta, password):
                    self.menu(nro_tarjeta,password)
                else:
                    print(
                        'No se encontro el usuario,intente nuevamente o salga del programa')
            elif entrar == '2':
                print('Saliendo del programa...')
                break
            else:
                print('La opcion que escribio es incorrecta')
        return False


    def autenticar_usuario(self, nro_tarjeta, password):
        with open(Cajero.archivo_datos, 'r') as f:
            datos = json.load(f)

        for nro_tarjeta_almacenado, password_almacenada in datos.items():
            if nro_tarjeta == nro_tarjeta_almacenado and password == password_almacenada:
                return True


    def cambiar_contrasenia(self):
        with open(cajero.archivo_datos, 'r') as file:
                datos = json.load(file)
        while True:
                nro_tarjeta = input('Ingrese su numero de tarjeta: ')
                if nro_tarjeta in datos:
                    password_valida = False
                    while not password_valida:
                        nueva_password = input('Ingrese su nueva contraseña (minimo 8 digitos): ')
                        if len(nueva_password) >= 8:
                            datos[nro_tarjeta] = nueva_password
                            password_valida = True
                            print('Se registraron los cambios con exito!!')
                            
                        else:
                            print('Debe contener minimo 8 digitos')
                            
                    with open(cajero.archivo_datos, 'w') as file:
                        json.dump(datos, file, indent=4)
                    break
                else:
                    print('No se encontro el numero de tarjeta. Verifiquelo e intente nuevamente')


    def darse_de_baja(self):
        with open(cajero.archivo_datos, 'r') as file:
            datos = json.load(file)
                
        with open(cajero.saldos_usuarios, 'r') as file:
            saldo = json.load(file)

            
        while True:
                nro_tarjeta = input('Ingrese su numero de tarjeta para confirmar: ')
                password = input('Ingrese su contraseña para confirmar: ')
                if nro_tarjeta in datos:
                   if datos[nro_tarjeta] == password:
                       quejas = input('Podrias explicarnos los motivos por el cual quiere darse de baja?, si no lo desea escriba "no": ')
                       if quejas.lower() == 'no':
                           datos.pop(nro_tarjeta,password)
                           for key,value in saldo:
                                if key == nro_tarjeta:
                                    saldo.pop(key,value)
                           print('Eliminando cuenta...')
                           break
                       else:
                            try:
                                with open(cajero.quejas_bajas, 'r') as file:
                                    quejas_bajas = json.load(file)
                            except:
                                    quejas_bajas = {}
                                       
                            quejas_bajas[nro_tarjeta] = quejas
                            datos.pop(nro_tarjeta,password)
                            
                            with open(cajero.quejas_bajas, 'w') as file:
                                json.dump(quejas_bajas, file, indent=4)
                                
                            print('Eliminando cuenta... gracias por darnos su opinion')
                            break
        with open(cajero.archivo_datos, 'w') as file:
            json.dump(datos, file, indent=4)
            
        with open(cajero.saldos_usuarios, 'w') as file:
            json.dump(saldo, file, indent=4)


    def retirar_efectivo(self,nro_tarjeta,password):
        
        with open(cajero.saldos_usuarios, 'r') as file:
            saldo = json.load(file)
        
        while True:
            saldo_a_retirar = int(input('Escriba el monto a retirar: '))

            if saldo_a_retirar < saldo[nro_tarjeta]:
                print('Operacion fallida, fondos insuficientes')
                continue
            else:
                saldo[nro_tarjeta] -= saldo_a_retirar
                print(f'Efectivo retirado, le queda en la cuenta un total de ${saldo[nro_tarjeta]}')
        
                with open(cajero.saldos_usuarios, 'w') as file:
                    json.dump(saldo, file, indent=4)
                    break


    def depositar_efectivo(self,nro_tarjeta,password):
        
        with open(cajero.saldos_usuarios, 'r') as file:
            saldo = json.load(file)

        
        while True:
            saldo_a_depositar = int(input('Escriba el monto a depositar: '))
            saldo[nro_tarjeta] += saldo_a_depositar
            print(f'Efectivo depositado, ahora su cuenta tiene un total de ${saldo[nro_tarjeta]}')
        
            with open(cajero.saldos_usuarios, 'w') as file:
                json.dump(saldo, file, indent=4)
                break


    def ver_saldo(self, nro_tarjeta,password):
        with open(cajero.saldos_usuarios, 'r') as file:
            saldo = json.load(file)
        
        print(f'Su saldo es ${saldo[nro_tarjeta]}')
        
        with open(cajero.archivo_datos, 'w') as file:
                    json.dump(saldo, file, indent=4)


    def transferir_dinero(self,nro_tarjeta,password):
        with open(cajero.saldos_usuarios, 'r') as file:
            saldo = json.load(file)
            
        while True:
            usuario_a_depositar = input('Ingrese el numero de tarjeta del usuario al que le quiere transferir: ')
            if saldo[usuario_a_depositar] not in saldo:
                print('No se encontro la cuenta, intente nuevamemnte')
                continue
            else:
                monto_a_transferir = int(input('Indique el monto a transferir: '))
                if monto_a_transferir < saldo[nro_tarjeta]:
                    print('No tiene los fondos suficientes para transferir ese monto')
                    break
                else:
                    saldo[usuario_a_depositar] += monto_a_transferir
                    saldo[nro_tarjeta] -= monto_a_transferir
                    print(f'Transferido con exito, le queda en su cuenta un total de ${saldo[nro_tarjeta]}')
                    with open(cajero.archivo_datos, 'w') as file:
                        json.dump(saldo, file, indent=4)
                        break


    def menu(self,nro_tarjeta,password):
        while True:
            print("""
    BIENVENIDO A BANCO SANTANDER
    
               MENU
        ====================
        
        1- OPERACIONES
        2- CONFIGURACION DE CUENTA
        3- SALIR DEL MENU
        
        ====================
    
    QUE OPCION DESEA REAELIZAR(1-3)
              """)
            try:
                opcion = int(input('Ingrese el numero aqui: '))
            except ValueError:
                print('Debe ingresar un numero (1-3)')

            if opcion == 1:
                self.operaciones(nro_tarjeta,password)
            elif opcion == 2:
                if self.configuracion_de_cuenta() != True:
                    break
            elif opcion == 3:
                print('Hasta pronto!!!')
                break
            else:
                print('La opcion que elijio no es valida, intente nuevamente')


    def operaciones(self,nro_tarjeta,password):
        while True:
            print("""
        BIENVENIDO A BANCO SANTANDER
    
            OPERACIONES
        ====================
        
        1- DEPOSITAR EFECTIVO
        2- RETIRAR EFECTIVO
        3- VER SALDO
        4- TRANSFERIR DINERO
        5- SALIR
        
        ====================
    
    QUE OPCION DESEA REALIZAR(1-5)
              """)
            try:
                opcion = int(input('Ingrese el número aquí: '))
            except ValueError:
                print('Debe ingresar un número (1-5)')

            if opcion == 1:
                self.depositar_efectivo(nro_tarjeta,password)
            elif opcion == 2:
                self.retirar_efectivo(nro_tarjeta,password)
            elif opcion == 3:
                self.ver_saldo(nro_tarjeta,password)
            elif opcion == 4:
                self.transferir_dinero(nro_tarjeta,password)
            elif opcion == 5:
                print('Hasta pronto!!!')
                break
            else:
                print('La opción que eligió no es válida, intente nuevamente.')


    def configuracion_de_cuenta(self):
        while True:
            print("""
    BIENVENIDO A BANCO SANTANDER
    
            CONFIGURACION
        ====================
        
        1- CAMBIAR CONTRASEÑA
        2- DARSE DE BAJA
        3- SALIR
        
        ====================
    
    QUE OPCION DESEA REALIZAR(1-3)
              """)
            try:
                opcion = int(input('Ingrese el número aquí: '))
            except ValueError:
                print('Debe ingresar un número (1-3)')

            if opcion == 1:
                self.cambiar_contrasenia()
                return True
            elif opcion == 2:
                if self.darse_de_baja() != True:
                    break
            elif opcion == 3:
                print('Saliendo de la sección...')
                break
            else:
                print('La opción que eligió no es válida, intente nuevamente.')

cajero = Cajero()
cajero.prender()