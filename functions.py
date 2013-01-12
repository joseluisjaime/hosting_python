from subprocess import call


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
