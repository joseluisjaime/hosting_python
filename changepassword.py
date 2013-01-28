import sys
from getpass import getpass

sys.argv

nombre=sys.argv[1]

print nombre

common_pass = getpass("password comun para todos los usuarios: ") 
rcommon_pass = getpass("vuelva a escribir la password: ")

if common_pass != rcommon_pass: 
    print "Las pasword no coinciden"
    sys.exit()
