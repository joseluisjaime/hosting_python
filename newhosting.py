import functions as fun

username = raw_input("enter your username: ")
fun.checkusername(username)
domainname = raw_input("enter your domain name, without www and .com :")
fun.checkdomainname(domainname)

lastuid = fun.lastuid()

fun.createdir(username,lastuid)

fun.createvh(username,domainname)

passldap = fun.aleatorypassword()

enpassldap = fun.encryptpassword(passldap)

fun.adduserldap(username,domainname,enpassldap,lastuid)

passmysql = fun.aleatorypassword()
fun.addusermysql(username,domainname,passmysql)

print "---------------------------------------------"
print """
Hosting creado correctamente

"""
print "tu usuario para entrar en ftp es: " + username+"\n"
print "Tu nombre de dominio es: www." +domainname + ".com\n"
print "tu password ftp es: " + passldap+"\n"
print "Nombre de la base de datos: db_"+domainname+"\n"
print "Password para entrar a phpmyadmin: "+passmysql
