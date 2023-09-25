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

#------------------------------------------------------------------------------------------
            #se crea el menu central del programa
            def menu():
                while True:
                    print("==================================")
                    print("\nSistema de Control de Parqueo")
                    print("1. Registrar Entrada")
                    print("2. Registrar Salida")
                    print("3. Ver Historial")
                    print("4. Salir")

                    opcion = input("Seleccione una opción: ")
                    print()

                    if opcion == "1":
                        registrar_entrada()
                    elif opcion == "2":
                        registrar_salida()
                    elif opcion == "3":
                        ver_historial()
                    elif opcion == "4":
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