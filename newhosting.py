import functions as fun

username = raw_input("enter your username: ")
fun.checkusername(username)
domainname = raw_input("enter your domain name, without www and .com :")
fun.checkdomainname(domainname)

fun.createdir(username)
fun.createvh(username,domainname)

passldap = fun.aleatorypassword()

enpassldap = fun.encryptpassword(passldap)

lastuid = fun.lastuid()

fun.adduserldap(username,domainname,enpassldap,lastuid)

print "---------------------------------------------"
print "tu usuario para entrar en ftp es: " + username
print "Tu nombre de dominio es: www." +domainname + ".com"
print "tu password ftp es: " + passldap
