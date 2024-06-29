import subprocess

#------------------------------------------------------------#
def es_root():
  """
  Verifica si el usuario actual tiene permisos de root.
  """
  # Ejecuta el comando "whoami" y captura la salida
  proceso = subprocess.run(["whoami"], stdout=subprocess.PIPE)

  # Obtiene la salida del proceso como un string
  salida = proceso.stdout.decode().strip()

  # Compara la salida con "root"
  return salida == "root"    
#------------------------------------------------------------#


#------------------------------------------------------------#
def crear_usuario():
  """
  Crea un usuario en Debian, lo agrega al grupo SU y le asigna una contraseña.
  """
  if not es_root():
    print("Error: Este comando requiere permisos de root.")
    return

  nombre_usuario = input("Nombre de usuario: ")

  while True:
    contraseña = input("Contraseña: ")
    confirmar_contraseña = input("Confirmar contraseña: ")

    if contraseña != confirmar_contraseña:
      print("Las contraseñas no coinciden. Inténtalo de nuevo.")
    else:
      break

  subprocess.run(["adduser", "-m", "-p", f"{contraseña}s", nombre_usuario])
  subprocess.run(["usermod", "-aG", "sudo", nombre_usuario])
  
  # Actualiza y muestra la lista de usuarios
  subprocess.run(["users"])    
  print(f"Usuario {nombre_usuario} creado correctamente.")
  #print("Usuario creado y listado correctamente.")
#------------------------------------------------------------#


#------------------------------------------------------------#
def listar_usuarios():
  """
  Lista los usuarios existentes en el sistema.
  """
  if not es_root():
    print("Error: Este comando requiere permisos de root.")
    return

  subprocess.run(["users"])
#------------------------------------------------------------#


#------------------------------------------------------------#
def eliminar_usuario():
  """
  Elimina un usuario del sistema.
  """
  if not es_root():
    print("Error: Este comando requiere permisos de root.")
    return

  nombre_usuario = input("Nombre de usuario a eliminar: ")

  while True:
    confirmar = input(f"¿Estás seguro de eliminar al usuario {nombre_usuario}? (s/n): ")

    if confirmar.lower() == "s":
      # Intenta eliminar el usuario
      proceso = subprocess.run(["userdel", nombre_usuario], stderr=subprocess.PIPE)

      # Verifica si la eliminación fue exitosa
      if proceso.returncode == 0:
        print(f"Usuario {nombre_usuario} eliminado correctamente.")
        break
      else:
        # La eliminación falló, muestra el error
        error = proceso.stderr.decode().strip()
        print(f"Error al eliminar el usuario: {error}")
        break
    elif confirmar.lower() == "n":
      print("Eliminación cancelada.")
      break
    else:
      print("Opción no válida. Ingresa 's' o 'n'.")
#------------------------------------------------------------#


#------------------------------------------------------------#
def actualizar_sistema():
  """
  Actualiza el sistema Debian.
  """
  if not es_root():
    print("Error: Este comando requiere permisos de root.")
    return   

  subprocess.run(["sudo", "apt", "update"])
  subprocess.run(["sudo", "apt", "upgrade"])
  print("Sistema actualizado correctamente...")
#------------------------------------------------------------#


#------------------------------------------------------------#
def modificar_hostname():
  """
  Muestra el hostname actual, permite modificarlo y actualiza los archivos /etc/hostname y /etc/hosts.
  """
  if not es_root():
    print("Error: Este comando requiere permisos de root.")
    return

  # Obtiene el hostname actual
  # hostname_actual = subprocess.run(["hostname"], stdout=subprocess.PIPE).decode().strip()
  hostname_actual = subprocess.run(["hostname"], stdout=subprocess.PIPE)
  hostname_actual = hostname_actual.stdout.decode().strip()

  # Muestra el hostname actual y pregunta si desea modificarlo
  print(f"Hostname actual: {hostname_actual}")
  modificar = input("¿Desea modificar el hostname? (s/n): ")

  if modificar.lower() == "s":
    # Solicita el nuevo hostname
    nuevo_hostname = input("Nuevo hostname: ")

    # Edita el archivo /etc/hostname
    with open("/etc/hostname", "w") as archivo:
      archivo.write(nuevo_hostname + "\n")

    # Actualiza la entrada del hostname en /etc/hosts
    subprocess.run(["sed", "-i", f"s/{hostname_actual}/{nuevo_hostname}/", "/etc/hosts"])

    # Busca la IP del hostname actual
    ip_actual = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE)
    ip_actual = ip_actual.stdout.decode().strip()
    ip_actual = ip_actual.split()[0]

    # Edita la entrada del hostname actual en /etc/hosts
    subprocess.run(["sed", "-i", f"s/{hostname_actual} {ip_actual}/{nuevo_hostname} 127.0.0.1/", "/etc/hosts"])

    # Reinicia el servicio hostname para aplicar los cambios
    # subprocess.run(["systemctl", "restart", "hostname"])
    subprocess.run(["systemctl", "restart", "hostname"])

    print(f"Hostname modificado a: {nuevo_hostname}")
  else:
    print("Hostname no modificado.")
#------------------------------------------------------------#


#------------------------------------------------------------#
def menu_principal():
  """
  Muestra el menú principal y permite al usuario seleccionar una opción.
  """
  while True:
    print("\nMenú Principal:")
    print("1. Agregar usuario perteneciente al grupo SU")
    print("2. Listar usuarios existentes")
    print("3. Eliminar algún usuario")
    print("4. Actualizar el sistema")
    print("5. Actualizar hostname")
    print("0. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
      crear_usuario()
    elif opcion == "2":
      listar_usuarios()
    elif opcion == "3":
      eliminar_usuario()
    elif opcion == "4":
      actualizar_sistema()
    elif opcion == "5":
      modificar_hostname()      
    elif opcion == "0":
      print("Saliendo del menú...")
      break
    else:
      print("Opción no válida.")

if __name__ == "__main__":
  menu_principal()
