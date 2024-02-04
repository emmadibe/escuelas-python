
import sqlite3

import pandas as pd #Imprto la librería pandas. Esta es una librería muy usada para trabajar con el análisis de datos. Me permite, entre otras cosas, crear tablas. La estudié mucho en el curso de Aprendizaje automático brindado por la Universidad Nacional de Hurlingham.

import pygame #Librería para pasar música.

##Por consola, ya cree la base de datos con los comandos sqlite3 proyecto.db. Luego, también la puyse en modo tabla con el comando .mode table. Ahora, me conecto a mi base de datos ya creada por consola con el siguiente comando:
conexion = sqlite3.connect("proyecto.db")

##Ahora, voy a crear un objeto de cursor utilizando el método cursor()de conexión. El cursor me permitirá poner en ejecución consultas SQL en la base de datos:
cursor = conexion.cursor()

def comprobarUsuarioLargo(nombreUsuario):
    #Voy a comprobar que tenga 5 caracteres como mínimo: 
    cantidadChar = 0
    for char in nombreUsuario:
        cantidadChar = cantidadChar +  1

    if cantidadChar >= 5:

        return 0
    
    else:

        return 1

def comprobarUsuarioNoExista (nombreUsuario): ##Quiero comprobar que ya no exista el nombre de usuario.
        
    try: ##Debo hacer el try porque si todavía no se creó la tabla llamada docentes, el programa se romperá.

        traer = "SELECT nombre FROM docentes;"
        cursor.execute(traer)
        registros = cursor.fetchall()

        existe = 0

        for n in registros: #En  cada bucle, la variable n almacenará una tupla de la lista registros.

            if nombreUsuario in n: #Si el valor dela variable nombreUsuario coincide con el valor de la tupla que en este momento de bucle almacena n, entonces el nombre ya existe. Cambio el valor de la variable existe a 1. Es para identificar que se encontró una coincidencia. 

                existe = 1 

        if existe == 0:

            return 0
        
        else:

            return 1
        
    except:

        return 0
    
def comprobarContraseniaLargo(contrasenia):

    contador = 0

    for char in contrasenia:

        contador = contador + 1

    if contador >= 7:

        return 0
    
    else:

        return 1
    
def comprobarContraseniaNumero(contrasenia): #Quiero comprobar si en el valor ingresado por el usuario hay, al menos, dos int.

    hayNumero = 0

    for n in contrasenia:

        if n.isdigit(): #El método isdigit() retorna true si el valor al cual lo invoco es un int.

            hayNumero = hayNumero + 1

    if hayNumero >= 2:

        return 0
    
    else:

        return 1
    
def comprobarContraseniaIguales(contrasenia, contrasenia2):

    if contrasenia == contrasenia2:

        return 0
    
    else:

        return 1
    
def existeConsultaSql(consulta, id_docente, curso_id=0):#Si le asigno un valor a la variable-parámetro un valor predeterminado, esa variable es opcional. Es decir, puedo, si quiero no pasarle ese parámetro. Lo hago porque no en todas las consultas necesito de la variable curso_id
    existe_consulta_sql = False

    try:#El bloque try-except, intentará ejecutar la consulta sql. Si puede, o sea, si no es None(vacío), el valor de la variable registros_existen será True; sino, False.

        if curso_id == 0:

            cursor.execute(consulta, (str(id_docente),))

        else:

            cursor.execute(consulta, (str(id_docente), curso_id))

        result = cursor.fetchall() #La función fetchall retorna una lista de tuplas.

        if len(result) > 0: #La función len() me retorna un int que indica la cantidad de elementos que hay en un contenedor, sea este un string, una lista, una tupla, un set o un diccionario. Si la lista de tuplas que está almacenada en result tiene un contenido al menos, significa que hay registros. 

            existe_consulta_sql = True
            
    except sqlite3.Error as error:

        print("Error: ", error)

    return existe_consulta_sql

def sacarCorchetes(var): #Quiero sacar los corchetes.

    for char in var: #En cada bucle, la variable llamada char almacenará un caracter  del valor de la variable llamada var. Si ese valor no es ni [ ni ], se almacena en la variable llamada nombreBien 

        if char != "[" and char != "]":

            nombreBien = char

    return nombreBien

def concepto(alumno_id):

    # Obtener las notas existentes del alumno de la base de datos
    cursor.execute("SELECT notas FROM alumnos WHERE alumno_id = ?", (alumno_id,))
    notas_existente = cursor.fetchone()[0]

    # Convertir las notas existentes a una lista
    notas = eval(notas_existente) if notas_existente else [] #Con el método eval(), trato al valor de notas_existente como una lista. Pero eso depende, si notas_existente es True (o sea, tiene contenido), se evalluará como un eval (lista con contenido); sino, se evaluarác omo una lista vacía.

    ######################SACO PROMEDIO DE NOTAS:
    #TOTAL DE NOTAS:
    contador = 0

    for n in notas:

        contador = contador + 1
    #
        
    #SUMO NOTAS:
        
    suma = 0

    for n in notas:

        suma = suma + n
    #############################################

    #PROMEDIO:

    promedio = suma / contador

    #############GUARDO EL VALOR EN EL CAMPO PROMEDIO:

    cursor.execute("UPDATE alumnos SET promedio = ? WHERE alumno_id = ?", (promedio, str(alumno_id)))
    conexion.commit()

    conceptual = "TEA"

    if promedio >= 7:

        conceptual = "TEA"

    elif promedio >= 4 and promedio <7:

        conceptual = "TEP"

    else:

        conceptual = "TED"

    #

    # Actualizar la lista completa de notas en la base de datos
    cursor.execute("UPDATE alumnos SET concepto = ? WHERE alumno_id = ?", (conceptual, str(alumno_id)))
    conexion.commit()

def main():

    ####################VAMOS A PASAR MUSICA:

    pygame.init() #Inicializamos la libreria pygame.

    pygame.mixer.music.load("LOTR.mp3") #Cargamos la musica desde el archivo

    while True:

        pygame.mixer.music.play(-1)


        print("Bienvenido\n")

        opcion = 22
            
        while opcion > 3 or opcion < 1 :

            try:

                opcion = int(input("Marque 1, para crear un nuevo usuario\n 2, para iniciar sesión\n o 3, para salir "))
                

            except ValueError:

                print("Debe ingresar un número\n")

        if opcion == 1:

            validoNombreUsario = 2

            while validoNombreUsario == 2:

                nombre = input("Seleccionar un nombre de usuario. Debe tener, por lo menos, cinco caracteres:\n ")

                ################### COMPROBACIONES DEL NOMBRE DE USUARIO ELEGIDO ###########################

                #### Que el nombre de usuario no exista ####

                comprobeishonExiste = comprobarUsuarioNoExista(nombre)

                if comprobeishonExiste == 1:

                    print("EL NOMBRE DE USUARIO YA EXISTE\n ")

                ########

                ### QUE EL NOMBRE TENGA, AL MENOS, CINCO CARACTERES #####

                comprobeishhonLargo = comprobarUsuarioLargo(nombre)

                if comprobeishhonLargo == 1:

                    print("EL NOMBRE DE USUARIO DEBE CONTENER, AL MENOS, CINCO CARACTERES\n ")

                if comprobeishonExiste == 0 and comprobeishhonLargo == 0:

                    validoNombreUsario = 0

            ########

            validezContrasenia = 2

            while validezContrasenia == 2:

                contrasenia = input("Seleccionar una contraseña. Debe tener, al menos, 7 caracteres. Dos de ellos deben ser enteros\n ")

                repetirContrasenia = input("Repetir contraseña:\n ")

                ############### COMPROBAR VALIDEZ DE LA CONTRASENIA ELEGIDA ############

                ##COMPROBAR QUE SEAN IGUALES

                comprobeishonContraseniaIguales = comprobarContraseniaIguales(contrasenia, repetirContrasenia)

                if comprobeishonContraseniaIguales == 1:

                    print("LAS CONTRASEÑAS NO COINCIDEN\n")

                ##COMPROBAR LARGO 

                comprobeishonContrasenialargo = comprobarContraseniaLargo(contrasenia)

                if comprobeishonContrasenialargo == 1:

                    print("LA CONTRASENIA DEBE TENER, AL MENOS, SIETE CARACTERES\n ")

                comprobeishonContraseniaNum = comprobarContraseniaNumero(contrasenia)

                if comprobeishonContraseniaNum == 1:

                    print("LA CONTRASENIA DEBE TENER, AL MENOS, DOS NÚMEROS ENTEROS\n ")

                if comprobeishonContraseniaIguales == 0 and comprobeishonContrasenialargo == 0 and comprobeishonContraseniaNum == 0:

                    validezContrasenia = 0
####################################################################

            email = input("ingrese su email: ")

            crearTabla = "CREATE TABLE IF NOT EXISTS docentes(docente_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nombre VARCHAR NOT NULL, contrasenia VARCHAR NOT NULL, email VARCHAR NOT NULL);"     
            #crarTabla es una variable que almacena un string. Ese string es la consulta sql. O sea, crearTabla almacena el string "CREATE TABLE IF...". NO EJECUTA NADA. Eso se hace con el método excecute del o  bjeto cursor.

            guardarDocente = "INSERT INTO docentes(nombre, contrasenia, email) VALUES (?, ?, ?);"

            cursor.execute(crearTabla) #Ejecuto la consulta almacenada en el objeto crearTabla. O sea, el método execute() ejecuta la consulta sql que le paso como parámetro.

            try:

                cursor.execute(guardarDocente, (nombre, contrasenia, email)) #Ejecuto la consulta sql almacenada en el objeto guardarDocente

                conexion.commit()  # Guardar los cambios en la base de datos de las consultas anteriormente ejecutadas dentro del método execute() del objeto cursor.

                print("Usuario creado con éxito.\n")

            except ValueError:

                print("ERROR. NO SE PUDO CREAR EL USUARIO.\n")

        elif opcion == 2:

            nombre = input("Ingrese su nombre ")

            contrasenia = input("Ingrese su contraseña ")

            id = "SELECT docente_id FROM docentes WHERE nombre = ? AND contrasenia = ?;" #Utilizo placeholder(?) para evitar inyecciones de sql.
            #Almaceno la consulta "SELECT" en la variable id.
            cursor.execute(id, (nombre, contrasenia)) #Ejecuto la consulta sql almacenada en la variable id.

            idEjecutada = cursor.fetchone() #COn el método fetchone() del objeto Cursor obtengo una tupla con los valores de los campos del primer registro que me retorna la consulta ejecutada con el método execute().
            if idEjecutada == None : #Aquí compruebo si la fila de reusltados, buscada con el método fetchone() del objeto Cursor, existe. Si es None, no existe. 

                print("Nombre o contraseña incorrectos.")

            else:

                print("Bienvenido al menú principal ")

                id_docente = idEjecutada[0] #Es que el método fetchone() retorna una tupla. EL primer valor de la tupla es el que pedí: campo docente_id. Me traigo ahora el valor de esta variable así la puedo usar siempre

                opcion_curso = 9

                while opcion_curso != 0:   #Mientras que el valor ingresado por el usuario almacenado en la variable opcion_curso sea diferente a cero, volverá a aparecer el siguiente menú principal:

                    try:
                            
                        opcion_curso = int(input("Seleccione una opción:\n 1, para ver todos los cursos\n 2, para crear un nuevo curso\n 3, para ingresar a un curso\n 4, para eliminar un curso\n 5, para modificar un curso\n 0, para salir\n "))

                    except ValueError:

                        print("Debe ingresar un número\n")

                    if opcion_curso == 0:

                        return 0

                    elif opcion_curso == 1:

                        registros_cursos = "SELECT * FROM cursos WHERE docente_id = ?;" #Almaceno la consulta "SELECT" dentro de la variable registros_cursos.

                        #### AHORA VAMOS A COMPROBAR SI EXISTEn REGISTROS EN LA TABLA CURSOS EN DONDE EL VALOR DEL CAMPO docente_id SEA EL DEL PRESENTE USUARIO #####
                        
                        #Vamos a comprobar si existen registros utilizando el bloque try-except. Dicho bloque intenta ejecutar un código. Si no se puede, ejecuta otro código. Esto lo hago para que no le tire un error feo al usuario si no existen registros y se corte el programa.
                    

                        registros_cursos_existen = existeConsultaSql(registros_cursos, id_docente)
            
                        if registros_cursos_existen: # Ejecutar el código solo si exiten registros; o sea, si la variable registros_cursos_existen almacena el valor True.

                            cursor.execute(registros_cursos, (str(id_docente),))
                            
                            registros_cursos_mostrar = cursor.fetchall() #Los resultados, los registros que devuelve la consulta SQL, los guardo en la lista de tuplas registros_cursos_mostrar. Acordate que el método fetchall del objeto cursor retorna una lista de tuplas. Con el método fetchall, a diferencia de con fetchone(), obtengo TODOS (all) los registros que me retorna la consulta ejecutada con el método execute(), no solo el primero.
                            # El método fetchall() retorna una LISTA de TUPLAS. Cada tupla es un registro. Entonces, cada tupla contendrá los valores de cada campo de cada registro. En otras palabras, el método fetchal nos retorna una lista de registros.
                            #También existe el método fetchmany(), del objeto cursor, en donde obtengo tantos registros como yo le indique por parámetro.

                            #Ahora, lo que quiero es representar todos los registros (con los valores que corresponden a cada campo) en una tabla. Para ello, utilizaré el método DataFrame, que está en la librería pandas. A ese método le paso como parámetro aquella variable que contenga los datos que deseo representar en forma de tabla. En este caso, le paso mi LISTA de TUPLAS registros_cursos_mostrar.


                            tablaCursos = pd.DataFrame(registros_cursos_mostrar)

                            #Por defecto, DataFrame llama a mis columna con un número iniciando en 0. Para cambiar el nombre de mis columnas, debo utilizar el método columns:

                            tablaCursos.columns = ['curso_id', 'cantidad de notas', 'curso', 'escuela', 'docente_id']

                            print(tablaCursos) #Muestra la tabla en pantalla.

                        else:

                            print("No tenés cursos creados todavía")

                            print(registros_cursos_existen)

                    elif opcion_curso == 2:
                            
                        while True:

                            try:

                                cant_notas = int(input("Seleccione la cantidad de notas "))

                                break  

                            except ValueError:

                                print("Debe ingresar un número\n")

                        nombre_curso = input("Ingrese el nombre del curso ")

                        nombre_colegio = input("Ingrese el nombre del colegio ")

                        crearTablaCurso = "CREATE TABLE IF NOT EXISTS cursos(curso_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, cant_notas INTEGER NOT NULL, nombre_curso VARCHAR NOT NULL, escuela VARCHAR NOT NULL,  docente_id INTEGER NOT NULL);"          

                        guardarCurso = "INSERT INTO cursos(cant_notas, nombre_curso, escuela, docente_id) VALUES (?, ?, ?, ?);"      
                
                        cursor.execute(crearTablaCurso)

                        try:

                            cursor.execute(guardarCurso, (cant_notas, nombre_curso, nombre_colegio, id_docente))

                            conexion.commit()

                            print("Curso creado con éxito.\n")

                        except ValueError:

                            print("ERROR. NO SE PUDO CREAR EL CURSO.\n")

                    elif opcion_curso == 3:

                        choose_curso = input("Ingrese el id del curso al que desea ingresar: ")

                        registro_curso_seleccionado = "SELECT * FROM cursos WHERE docente_id = ? AND curso_id = ?;" #Yo me quiero traer todos los registros con todos los campos en donde el campo docente_id y curso_id sean los solicitados.

                        ## COMPROBEMOS QUE HAY REGISTROS:

                        existe_curso_registro = existeConsultaSql(registro_curso_seleccionado, id_docente, choose_curso)

                        if existe_curso_registro:

                            choose_dentro_del_curso = 0

                            while choose_dentro_del_curso < 1 or choose_dentro_del_curso > 7:

                                while True:

                                    try:

                                        choose_dentro_del_curso = int(input("Apriete\n 1, para ver todos los alumnos\n 2, para agregar un alumno\n 3, para eliminar un alumno\n 4, para modificar un alumno\n 5, para agregar una nota\n 6, para modificar una nota\n 7, para ver las notas de un alumno específico\n 8, para volver al menú principal"))
                                        break
                                    
                                    except ValueError:

                                        print("Error: debe ingrese un número")

                            if choose_dentro_del_curso == 1:

                                registros_alumnos = "SELECT * FROM alumnos WHERE docente_id = ? AND curso_id = ?;"

                                registros_alumnos_existen = existeConsultaSql(registros_alumnos, id_docente, choose_curso)

                                if registros_alumnos_existen:

                                    cursor.execute(registros_alumnos, (str(id_docente), choose_curso))
                                    registros_alumnos_mostrar = cursor.fetchall() 
                                    tablaAlumnos = pd.DataFrame(registros_alumnos_mostrar) ##Acá tengo un data frame de todos los registros de la tabla alumnos con todos sus campos para ese curso_id y ese docente_id.

                                    ######

                                    #OBTENGO NOMBRE DEL COLEGIO:
                                    cursor.execute(registro_curso_seleccionado, (str(id_docente), choose_curso))
                                    todosLosCampos = cursor.fetchall()
                                    tablaCursos_tabla = pd.DataFrame(todosLosCampos)
                                    #Por defecto, DataFrame llama a mis columna con un número iniciando en 0. Para cambiar el nombre de mis columnas, debo utilizar el método columns:
                                    tablaCursos_tabla.columns = ['curso_id', 'cantidad de notas', 'curso', 'escuela', 'docente_id']
                                    nombreDelColegio = tablaCursos_tabla['escuela'].tolist() #Con el método tolist() recupero el valor de la columna, quitándome información adicional que me tiraba.
                                    nombreDelColegioMayuscula = sacarCorchetes(nombreDelColegio).upper() #La función upper()convierte a mayúscula el string al que va unido.

                                    ########

                                    tablaAlumnos.columns = ['alumno_id', 'nombre del alumno', 'notas', 'promedio', 'concepto', 'docente_id', 'curso_id']

                                    print("INSTITUCIÓN: {0}".format(nombreDelColegioMayuscula)) #Imprimo el nombre del colegio sin corchetes.

                                    print(tablaAlumnos) 

                                else:

                                    print("Todavía no agregaste ningún alumno al curso\n")

                            elif choose_dentro_del_curso == 2:

                                nombre = input("Seleccionar el nombre del alumno: ")

                                crearTablaAlumnos = "CREATE TABLE IF NOT EXISTS alumnos(alumno_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nombre VARCHAR NOT NULL, notas VARCHAR NULL, promedio INTEGER NULL, concepto VARCHAR NULL, docente_id INTEGER NOT NULL, curso_id INTEGER NOT NULL);"
                                #En el campo notas escribí NULL para que acepte valores nullos. Es que, cuando ingreso a un alumno no le pongo ninguna nota.
                                guardarAlumno = "INSERT INTO alumnos(nombre, docente_id, curso_id) VALUES (?, ?, ?);"

                                cursor.execute(crearTablaAlumnos)

                                try:

                                    cursor.execute(guardarAlumno, (nombre, id_docente , choose_curso))

                                    conexion.commit()

                                    print("Alumno guardado con éxito.\n")

                                except ValueError:

                                    print("ERROR. NO SE PUDO GUARDAR EL ALUMNO.\n")

                            elif choose_dentro_del_curso == 3:
                                    
                                while True:

                                    try:

                                        alumnoAEliminar = int(input("Escribir el id del alumno a eliminar: "))
                                        break

                                    except ValueError:

                                        print("Debe ingresar un número\n")

                                eliminarAlumno = "DELETE FROM alumnos WHERE alumno_id = ?;"
                                cursor.execute(eliminarAlumno, (str(alumnoAEliminar)))
                                conexion.commit()

                            elif choose_dentro_del_curso == 4:
                                    
                                while True:

                                    try:

                                        alumnoAEditar = int(input("Escribir el id del alumno a editar: "))

                                        break

                                    except ValueError:

                                        print("Debe ingresar un número\n")

                                nuevoNombreAlumno = input("Escribir el nuevo nombre")

                                editarAlumno = "UPDATE alumnos SET nombre = ? WHERE alumno_id = ?"

                                try:

                                    cursor.execute(editarAlumno, (nuevoNombreAlumno, str(alumnoAEditar)))
                                    conexion.commit()
                                    print("Alumno editado con éxito.\n")

                                except ValueError:
                                    print("ERROR AL EDITAR EL ALUMNO.\n")

                            elif choose_dentro_del_curso == 5:
                                    
                                while True:

                                    try:          
                                                            
                                        alumnoAEvaluar = int(input("Escribir el id del alumno al cual le deseas agregar una nota: "))
                                        break

                                    except ValueError:

                                        print("Debe ingresar un número")

                                while True:

                                    try:

                                        notaNueva = int(input("Nota: "))
                                        break

                                    except ValueError:

                                        print("Debe ingresar un número\n")

                                ####COMPRUEBO QUE EXISTA ESE ALUMNO_ID:
                                existe_alumnoId = existeConsultaSql("SELECT * FROM alumnos WHERE alumno_id = ? AND docente_id = ?;", alumnoAEvaluar, id_docente)
                                #####

                                if existe_alumnoId:

                                    # Obtener las notas existentes del alumno de la base de datos
                                    cursor.execute("SELECT notas FROM alumnos WHERE alumno_id = ?", (alumnoAEvaluar,))
                                    notas_existente = cursor.fetchone()[0]

                                    # Convertir las notas existentes a una lista
                                    notas = eval(notas_existente) if notas_existente else [] #Con el método eval(), trato al valor de notas_existente como una lista. Pero eso depende, si notas_existente es True (o sea, tiene contenido), se evalluará como un eval (lista con contenido); sino, se evaluarác omo una lista vacía.

                                    # Agregar la nueva nota a la lista
                                    notas.append(notaNueva)

                                    try:

                                        # Actualizar la lista completa de notas en la base de datos
                                        cursor.execute("UPDATE alumnos SET notas = ? WHERE alumno_id = ?", (str(notas), str(alumnoAEvaluar)))
                                        conexion.commit()

                                        #Actualizo el campo concepto

                                        concepto(alumnoAEvaluar)

                                        print("NOTA GUARDADA CORRECTAMENTE\n")

                                    except ValueError:

                                        print("ERROR AL GUARDAR LA NOTA\n")

                                else:
                                    
                                    print("No tienen un alumno con ese id")

                            elif choose_dentro_del_curso == 6:

                                try:

                                    alumnoAEditarNota = int(input("Escribir el id del alumno al cual le deseas editar la nota\n"))
                                    

                                except ValueError:

                                    print("Debe ingresar un número\n")

                                existeAlumnoId = existeConsultaSql("SELECT * FROM alumnos WHERE alumno_id = ? AND docente_id = ?;", alumnoAEditarNota, id_docente)

                                if existeAlumnoId:
                                    
                                    try:

                                        numNota = int(input("Número de nota que desea editar: \n"))
                                        

                                    except ValueError:

                                        print("Debe ingresar un número\n")

                                    try:

                                        nuevaNota = int(input("Ingrese el nuevo valor de la nota: \n"))

                                    except ValueError:

                                        print("Debe ingresar un número\n")

                                    cursor.execute("SELECT notas FROM alumnos WHERE alumno_id = ? AND docente_id = ?", (alumnoAEditarNota, id_docente))
                                    notas_existente = cursor.fetchone()[0]

                                    notas = eval(notas_existente) if notas_existente else []

                                    notas[numNota - 1] = nuevaNota

                                    # Actualizar la lista completa de notas en la base de datos
                                    cursor.execute("UPDATE alumnos SET notas = ? WHERE alumno_id = ?", (str(notas), str(alumnoAEditarNota)))
                                    conexion.commit()

                                    #Actualizo el campo concepto

                                    concepto(alumnoAEditarNota)

                                else:

                                    print("No tienes un alumno con ese id.\n")

                            elif choose_dentro_del_curso == 7:
                                    
                                while True:

                                    try:

                                        idAlumnoEspecifico = int(input("Escribir el id del alumno específico del cual deseas saber la nota:\n"))

                                        ######### COMPROBEMOS QUE EXISTE EL ALUMNO_ID PARA ESE DOCENTE_ID:

                                        alumnoExiste = existeConsultaSql("SELECT * FROM alumnos WHERE alumno_id = ? AND docente_id = ?;", idAlumnoEspecifico, id_docente)

                                        ######################################

                                        if alumnoExiste:

                                            cursor.execute("SELECT notas FROM alumnos WHERE alumno_id = ? AND docente_id = ?", (idAlumnoEspecifico, id_docente))

                                            notas_existente = cursor.fetchone()

                                            if notas_existente[0] != None: #Comprueba que haya algo en notas_existente. 

                                                notas = eval(notas_existente[0])

                                                ############ RECUPERO EL NOMBRE, EL PROMEDIO y EL CONCEPTO:

                                                cursor.execute("SELECT nombre FROM alumnos WHERE alumno_id = ?", (idAlumnoEspecifico,))
                                                nombreEspecifico = cursor.fetchone()

                                                cursor.execute("SELECT concepto FROM alumnos WHERE alumno_id = ?", (idAlumnoEspecifico,))
                                                conceptoEspecifico = cursor.fetchone()

                                                cursor.execute("SELECT promedio FROM alumnos WHERE alumno_id = ?", (idAlumnoEspecifico,))
                                                promedioEspecifico = cursor.fetchone()
                                                #########################3 

                                                contador = 1

                                                print("Nombre: {0}".format(sacarCorchetes(nombreEspecifico)))

                                                print("Concepto: {0}".format(sacarCorchetes(conceptoEspecifico)))

                                                print("Promedio: {0}".format(sacarCorchetes(promedioEspecifico)))

                                                for nota in notas:

                                                    print("Nota Nº{0}: {1} \n".format(contador, nota))

                                                    contador = contador + 1

                                            else:

                                                print("El alumno todavía no posee notas\n")

                                        else:

                                            print("No tienes un alumno con ese id\n")

                                        break

                                    except ValueError:

                                        print("ERROR: Debe ingresar un número\n")

                        else: 

                            print("No tenés un curso con ese id.\n")

                    elif opcion_curso == 4:

                        while True:       

                            try:

                                cursoAEliminar = int(input("Ingrese el id del curso que desea eliminar: "))
                                
                                break

                            except ValueError:

                                print("Debe ingresar un número\n")

                        eliminarCurso = "DELETE FROM cursos WHERE docente_id = ? AND curso_id = ?;"

                        ###VAMOS A COMPROBAR QUE EXISTAN REGISTROS:
                        existe_curso_eliminar = existeConsultaSql("SELECT * FROM cursos WHERE docente_id = ? AND curso_id = ?;", id_docente, cursoAEliminar)
                        ####
                        if existe_curso_eliminar:

                                cursor.execute(eliminarCurso, (str(id_docente), str(cursoAEliminar)))
                                conexion.commit()

                                #Pero, también debo eliminar a todos los registros de la tabla alumno cuyo valor de curso_id sea el del curso_id que acabo de eliminar:
                                eliminar_alumnos_del_curso = "DELETE FROM alumnos WHERE curso_id = ?;"

                                try:

                                    cursor.execute(eliminar_alumnos_del_curso, (str(cursoAEliminar),))
                                    conexion.commit()
                                    print("Curso eliminado correctamente.\n")

                                except ValueError:

                                    print("ERROR. NO SE PUDO ELIMINAR EL CURSO.\n")

                        else:

                            print("No tenés un curso con ese número de id.\n")

                    elif opcion_curso == 5:
                        
                        try:

                            cursoAEditar = int(input("Ingrese el id del curso a editar "))                            

                        except ValueError:

                            print("Debe ingresar un número\n")

                        ####VAMOS  COMPROBAR QUE EXISTAN REGISTROS :

                        existe_curso_editar = existeConsultaSql("SELECT * FROM cursos WHERE docente_id = ? AND curso_id = ?;", id_docente, cursoAEditar)

                        if existe_curso_editar:

                            nuevoNombreCurso = input("Nuevo nombre: ")

                            nuevoColegioCurso = input("Colegio: ")

                            try:
                                
                                nuevaCantNotas = int(input("Cantidad de notas: "))

                            except ValueError:

                                print("Debe ingresar un número\n")

                            editarCurso = "UPDATE cursos SET cant_notas = ?, nombre_curso = ?, escuela = ? WHERE curso_id = ?;"

                            try: 

                                cursor.execute(editarCurso, (str(nuevaCantNotas), nuevoNombreCurso, nuevoColegioCurso, str(cursoAEditar)))
                                conexion.commit()
                                print("Curso editado correctamente.\n")

                            except ValueError:

                                print("ERROR. NO SE PUDO EDITAR EL CURSO.\n")

                        else:

                            print("No tenés un curso con ese número de id.\n")

        else:

            return 0

main()