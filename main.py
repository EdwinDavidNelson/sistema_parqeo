from datetime import datetime
import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = '1234'
port_id = 5432

try:
    with psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id,
        conn = None) as conn:
   
        with conn.cursor(cursor_factory= psycopg2.extras.DictCursor) as cur:


            cur.execute('DROP TABLE IF EXISTS vehiculo')
            cur.execute('DROP TABLE IF EXISTS registro')

            create_script_vehiculo = '''
                CREATE TABLE IF NOT EXISTS vehiculo (
                    placa int PRIMARY KEY,
                    marca varchar(40) NOT NULL,
                    color varchar(40) NOT NULL,
                    conductor varchar(30) NOT NULL,
                    hora varchar(30) NOT NULL
                )
                '''
            
            cur.execute(create_script_vehiculo)
            
            create_script_registro = '''CREATE TABLE IF NOT EXISTS registro (
                                    placa int,
                                    marca varchar(40) NOT NULL,
                                    estado varchar(40) NOT NULL,
                                    hora varchar(30) NOT NULL) '''

            cur.execute(create_script_registro)

            #posible manera de jugar dentro de la base de datos
            '''cur.execute('SELECT * FROM employee')
            for record in cur.fetchall():
                print(record['name'], record['salary'])'''

#------------------------------------------------------------------------------------------
            #se definen funciones del programa
            def registrar_entrada():
                placa = int(input('Ingrese el numero de placa: '))
                marca = input('Ingrese el marca del vehiculo: ')
                color = input('Ingrese el color del vehiculo: ')
                conductor = input('Ingrese el nombre del propietario: ')
                estado = "Entrada"
                hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Insertar datos en las tablas
                insert_script = f"INSERT INTO vehiculo (placa, marca, color, conductor, hora) VALUES ('{placa}', '{marca}','{color}', '{conductor}', '{hora}')"
                cur.execute(insert_script)
                conn.commit()

                insert_script = f"INSERT INTO registro (placa, marca, estado, hora) VALUES ('{placa}', '{marca}','{estado}', '{hora}')"
                cur.execute(insert_script)
                conn.commit()

                print("\n------REGISTRO DE AUTOS------")
                cur.execute('SELECT * FROM vehiculo')
                for record in cur.fetchall():
                    print(record)
            
            #funcion para la salida de los vehiculos
            def registrar_salida():
                estado = "Salida"
                placa = int(input('Ingrese el numero de placa: '))
                marca = input('Ingrese la marca del vehiculo: ')
                delete_script = f"DELETE FROM vehiculo WHERE placa = '{placa}' AND marca = '{marca}'"
                cur.execute(delete_script)
                conn.commit()

                hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                insert_script = f"INSERT INTO registro (placa, marca, estado, hora) VALUES ('{placa}', '{marca}', '{estado}', '{hora}')"
                cur.execute(insert_script)
                conn.commit()
            
                print("\n------REGISTRO DE AUTOS------")
                cur.execute('SELECT * FROM vehiculo')
                for record in cur.fetchall():
                    print(record)

            def ver_historial():
                print("------Historial de entradas y salidas------")
                cur.execute('SELECT * FROM registro')
                for record in cur.fetchall():
                    print(record)
            
            #submenu para registro (MODIFICACION)
            def registro():
                print("==================================")
                print("\nMenu de Reportes")
                print("1. Generar Reporte Ganancias")
                print("2. Generar Reporte de Vehiculos")
                opcion = int(input("Ingrese numero de opcion: "))
                if opcion == 1:
                    print("\n\tReporte de Ganancias")
                    generar_reporte_ganancias()
                    
                elif opcion == 2:
                    print("\n\tReporte de Vehiculos")
                    generar_reporte_vehiculos()
                else:
                    print("Opción no válida.\n")
            
            def calcular_ganancias():
                cur.execute("SELECT COUNT(*) FROM registro WHERE hora IS NOT NULL")
                total_registros = cur.fetchone()[0]
                ganancias = total_registros * 5
                return ganancias

            def generar_reporte_ganancias():
                ganancias = calcular_ganancias()
                print(f"Total de Ganancias al Día de Hoy: ${ganancias:.2f}".format(ganancias))

            def generar_reporte_vehiculos():
                cur.execute("SELECT marca, COUNT (*) FROM registro GROUP BY marca")
                for record in cur.fetchall():
                    marca = record[0]
                    cantidad = record[1]
                    print("{}: {}".format(marca, cantidad)) 
#------------------------------------------------------------------------------------------
            #se crea el menu central del programa
            def menu():
                while True:
                    print("==================================")
                    print("\nSistema de Control de Parqueo")
                    print("1. Registrar Entrada")
                    print("2. Registrar Salida")
                    print("3. Ver Historial")
                    print("4. Reportes")
                    print("5. Salir")

                    opcion = input("Seleccione una opción: ")
                    print()

                    if opcion == "1":
                        registrar_entrada()
                    elif opcion == "2":
                        registrar_salida()
                    elif opcion == "3":
                        ver_historial()
                    elif opcion == "4":
                        #aqui va la actualizacion
                        registro()
                    elif opcion == "5":
                        print("Cerrando Programa")
                        break
                    else:
                        print("Opción no válida. Por favor, seleccione una opción válida.")
            menu()

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
