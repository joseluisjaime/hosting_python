from subprocess import call
import commands
import sys

def checkusername(username):
    listuser = commands.getoutput("ls /srv/hosting/")
    listuser = listuser.split("\n")
    if username in listuser:
        print "Username in use"
        sys.exit()

def checkdomainname(domainname):
    listdomain = commands.getoutput("ls /etc/apache2/sites-available/")
    listdomain = listdomain.split("\n")
    if domainname in listdomain:
        print "domain in use"
        sys.exit()

def createdir(username):
    call(["mkdir","-p","/srv/hosting/" + username])
    call(["chmod","777","/srv/hosting/" + username])
    call(["cp","src/index.html","/srv/hosting/" + username])


def createvh(username,domainname):
    f = open("src/default", "r")
    texto = f.read()
    texto = texto.replace("cambiarname",domainname)
    texto = texto.replace("cambiarruta",username)
    f.close()

    nuevo = open("/etc/apache2/sites-available/"+domainname,"w")
    nuevo.write(texto)
    nuevo.close() 

    call(["a2ensite",domainname])
    call(["service","apache2","reload"])
