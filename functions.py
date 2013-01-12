from subprocess import call

def createdir(nameuser):
    call(["mkdir","-p","/srv/hosting/" + nameuser])
    call(["chmod","777","/srv/hosting/" + nameuser])
    call(["cp","src/index.html","/srv/hosting/" + nameuser])


createdir("jose")
