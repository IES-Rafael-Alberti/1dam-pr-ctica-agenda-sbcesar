"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute()

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1,2,3,4,5,6,7,8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def cargar_contactos(contactos: list):
    """
    Carga los contactos iniciales de la agenda desde un fichero

    Args:
        contactos (list): Lista con los contactos
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...
    try:
        with open(RUTA_FICHERO, 'r') as fichero:
            for linea in fichero:

                if linea == "\n":
                    continue

                datos = linea.strip().split(";")

                nombre = datos[0]

                if len(datos) > 1:
                    apellido = datos[1]
                else:
                    apellido = ""
                
                if len(datos) > 2:
                    correo = datos[2]
                else:
                    correo = ""

                if len(datos) > 3:
                    telefonos = datos[3:]
                else:
                    telefonos = []

                contactos.append({
                    "nombre":nombre,
                    "apellido":apellido,
                    "email":correo,
                    "telefonos":telefonos
                })

    except FileNotFoundError:
        print(f"No se encontró el archivo {NOMBRE_FICHERO}")

def buscar_contacto(contactos: list, email: str):
    """
    recupera la posicion de un contacto con un email determinado

    Args:
        contactos (list): Lista con los contactos
        email (str): Email de cada usuario

        return (int | None): Devuelve None si el email no está o su posicion si se encuentra
    """

    cont = None
    for i in range(len(contactos)):
        if contactos[i]["email"] == email:
            cont = i
            break
    
    return cont

def eliminar_contacto(contactos: list, email):
    """
    Elimina un contacto de la agenda

    Args:
        contactos (list): Lista con los contactos
        email (str): Email de cada usuario
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        pos = buscar_contacto(contactos, email)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")

def pedir_opcion():
    """
    Esta función pide que itroduzcas un número concorde a las opciones que hay

    Returns:
        int: Si es válida devuelve el entero y -1 si no lo es
    """

    try:
        opcion = int(input("Elige una acción (1-8): "))
        return opcion
    except ValueError:
        print("*** ERROR *** - Por favor, ingrese una opción válida.")
        return -1

def mostrar_menu():
    """Muestra el menú en la terminal"""

    print("AGENDA")
    print(" 1. Nuevo contacto")
    print(" 2. Modificar contacto")
    print(" 3. Eliminar contacto")
    print(" 4. Vaciar agenda")
    print(" 5. Cargar agenda inicial")
    print(" 6. Mostrar contactos por criterio")
    print(" 7. Mostrar la agenda completa")
    print(" 8. Salir")

def agregar_contacto(contactos: list):
    """
    Agrega contactos a la agenda

    Args:
        contactos (list): Lista vacia de los contactos de la agenda
    """

    nombre = input("Introduce el nombre: ")
    apellido = input("Introduce el apellido: ")
    email = pedir_email(contactos)

    telefonos = []

    while True:
        telefono = pedir_telefono()
        if telefono == "":
            break

        telefonos.append(telefono)
    
    nuevo_contacto = {"nombre": nombre, "apellido": apellido, "email": email, "telefonos": telefonos}
    contactos.append(nuevo_contacto)

def pedir_email(contactos: list) -> str:
    email =  input("Introduce tu correo electrónico (correo@gmail.com): ")

    if email == "":
        raise ValueError("el email no puede ser una cadena vacía")
    
    if "@" not in email:
        raise ValueError("el email no es un correo válido")
    
    for i in range(len(contactos)):
        if contactos[i]["email"].lower() == email.lower():
            raise ValueError("El email ya existe en la agenda")
        
    return email

def validar_email(contactos: list, email):
    
    if email == "":
        raise ValueError("el email no puede ser una cadena vacía")
    
    if "@" not in email:
        raise ValueError("el email no es un correo válido")
    
    for i in range(len(contactos)):
        if contactos[i]["email"].lower() == email.lower():
            raise ValueError("El email ya existe en la agenda")

def pedir_telefono() -> str:
    telefono = input("Introduce tu telefono (prefijo opcional): ")
    validar_telefono(telefono)
    return telefono

def validar_telefono(telefono: str) -> bool:
    while True:
        try:
            if telefono == "":
                return False
            
            if len(telefono) > 9:
                if telefono[:3] == "+34":
                    pos1 = telefono.find("-")
                    parte_numerica = telefono[pos1+1:]

                    if not parte_numerica.isdigit():
                        raise ValueError
                    else:
                        parte_numerica = int(parte_numerica)
                    
                    if parte_numerica == 9 and type(parte_numerica) == int:
                        return True
                    else:
                        return False   
                else:
                    return False    #porque no empieza por +34
            elif len(telefono) == 9:
                if not telefono.isdigit():
                    raise ValueError
                else:
                    telefono = int(telefono)
                    return True
            else:
                return False    #porque no cumple con la longitud permitida
                
        except ValueError:
            return False


def agenda(contactos: list):
    """Ejecuta el menú de la agenda con varias opciones"""

    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...
    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 6
        
        if opcion not in OPCIONES_MENU:
            print("Por favor, introduzca una opción válida")
            continue

        match opcion:
            case 1:
                agregar_contacto(contactos)
            case 2:
                email = input("Introduce el correo del contacto que deseas modificar: ")
                modificar_contactos(contactos, email)
            case 3:
                email = input("Introduce el correo que deseas eliminar: ")
                eliminar_contacto(contactos, email)
            case 4:
                contactos.clear()
            case 5:
                #No terminado
                print()
            case 6:
                mostrar_contacto_por_criterio(contactos)
            case 7:
                mostrar_contactos(contactos)
            case 8:
                print("No fuimo, salsa y picante")

def mostrar_contacto_por_criterio(contactos: list):
    
    while True:
        
        criterio = input("Introduce el criterio de búsqueda (nombre, apellido, correo o telefono): ")

        if criterio in ["nombre", "apellido", "correo", "telefono"]:
            break
        else:
            print("Criterio no válido.")

    valor_busqueda = input(f"Introduce el valor a buscar por {criterio}: ")

    contactos_coincidentes = []

    for contacto in contactos:
        valor_contacto = contacto.get(criterio, "")

        if valor_busqueda in valor_contacto:
            contactos_coincidentes.append(contacto)

    if contactos_coincidentes:
        print("\nContactos encontrados:")
        mostrar_contactos(contactos_coincidentes)
    else:
        print("\nNo se encontraron contactos que coincidan con la búsqueda.")
    
def ordenar(contactos: list):
    return contactos['apellido'], contactos['nombre']

def mostrar_contactos(contactos: list):

    contactos_ordenados = sorted(contactos, key=ordenar)

    print(f"AGENDA ({len(contactos)})")
    print("------")

    for contacto in contactos_ordenados:
        nombre = f"{contacto['nombre']}, {contacto['apellido']}"
        email = contacto['email']
        telefonos = contacto['telefonos']

        telefonos_formateados = []

        for telefono in telefonos:

            if telefono[:3] == "+34":
                telefono_formateado = "+34-" + telefono[1:]
            else:
                telefono_formateado  = telefono

            telefonos_formateados.append(telefono_formateado)
        
        imprimir = " / ".join(telefonos_formateados)
        
        if not imprimir:
            imprimir = "ninguno"

        print(f"Nombre: {nombre} ({email})")
        print(f"Teléfonos: {imprimir}")
        print("......")

def modificar_contactos(contactos: list, email: str):
    pos = buscar_contacto(contactos, email)

    if pos is not None:
        contacto = contactos[pos]

        print("Contacto encontrado:")
        mostrar_contactos(contactos)

        print("\nSeleccione el campo que desea modificar:")
        print("1. Nombre")
        print("2. Apellido")
        print("3. Email")
        print("4. Teléfonos")

        opcion = pedir_opcion()

        if opcion == 1:
            nuevo_nombre = input("Nuevo nombre: ")
            contacto["nombre"] = nuevo_nombre
        elif opcion == 2:
            nuevo_apellido = input("Nuevo apellido: ")
            contacto["apellido"] = nuevo_apellido
        elif opcion == 3:
            nuevo_email = pedir_email(contactos)
            contacto["email"] = nuevo_email
        elif opcion == 4:
            nuevo_telefonos = []
            while True:
                nuevo_telefono = pedir_telefono()
                if not nuevo_telefono:
                    break
                nuevo_telefonos.append(nuevo_telefono)
            contacto["telefonos"] = nuevo_telefonos

        print("Contacto modificado con éxito.")
    else:
        print("No se encontró el contacto para modificar.")

def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def main():
    """Función principal del programa"""

    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    cargar_contactos(contactos)

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    agregar_contacto(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    email = "rciruelo@gmail.com"
    eliminar_contacto(contactos, email)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos)


if __name__ == "__main__":
    main()