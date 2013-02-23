import sys
import functions as fun
sys.argv

if len(sys.argv) != 2:
	print "Para eliminar un dominio necesitas pasar el como parametro el nombre de este"
	sys.exit()
	
domainname = sys.argv[1]
domainname = domainname[:-4]

existe = fun.checkdomainname(domainname)
if existe != 'y':
	print "el dominio que intenta eliminar no existe"
	sys.exit()

username = fun.getusername(domainname)

fun.delzone(domainname)

fun.delmysql(username,domainname)

fun.deluserldap(username)

fun.delvh(domainname)

fun.deldir(username)

print "El dominio %s junto con el usuario %s ha sido eliminado correctamente" % (domainname,username)
