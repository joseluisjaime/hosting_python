import functions as fun
import sys

username = raw_input("enter your username: ")
existeuser = fun.checkusername(username)

if existeuser == 'y':
	print "el usuario ya existe"
	sys.exit()


domainname = raw_input("enter your domain name, only .com :")
domainname = domainname[:-4]
existedomain = fun.checkdomainname(domainname)

if existedomain == 'y':
	print "el dominio ya existe"
	sys.exit()

lastuid = fun.lastuid()

fun.createdir(username,lastuid)

fun.createvh(username,domainname)

passldap = fun.aleatorypassword()

enpassldap = fun.encryptpassword(passldap)

fun.adduserldap(username,domainname,enpassldap,lastuid)

passmysql = fun.aleatorypassword()
fun.addusermysql(username,domainname,passmysql)

fun.createzone(domainname)

print "---------------------------------------------"
print """
Hosting creado correctamente

"""
print "tu usuario para entrar en ftp es: " + username+"\n"
print "Tu nombre de dominio es: " +domainname + ".com\n"
print "tu password ftp es: " + passldap+"\n"
print "Nombre de la base de datos: db_"+domainname+"\n"
print "Nombre usuario para entrar a la base de datos: my"+username+"\n"
print "Password para entrar a phpmyadmin: "+passmysql+"\n"
