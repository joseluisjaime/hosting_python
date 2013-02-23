import sys
import functions as fun
from getpass import getpass
sys.argv


if len(sys.argv) != 3:
	print "Para cambiar la password se deben pasar dos parametros -ftp o -sql y el usuario"
	sys.exit()
	
accion = sys.argv[1]
username = sys.argv[2]

existe = fun.checkusername(username)
if existe != 'y':
	print "el usuario no existe"
	sys.exit()



if accion == '-sql':
	
    password = getpass("Introduce la nueva password: ") 
    rpassword = getpass("vuelva a escribir la password: ")

    if password != rpassword: 
        print "Las pasword no coinciden"
        sys.exit()
    fun.changepassmysql(username,password)

elif accion == '-ftp':
	
    password = getpass("Introduce la nueva password: ") 
    rpassword = getpass("vuelva a escribir la password: ")

    if password != rpassword: 
        print "Las pasword no coinciden"
        sys.exit()
	
else:
	
	print "El primer argumento debe ser -sql para mysql o -ftp para ftp"



