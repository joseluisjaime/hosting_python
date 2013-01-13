from subprocess import call
import commands
import sys
from random import choice
import os
import hashlib
from base64 import urlsafe_b64encode as encode
import ldap
import ldap.modlist as modlist

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

def aleatorypassword():
	
	length = 7
	string = "1234567890abcdefghijklmnopqrstuvwxyz"
	password = ""
	password = password.join([choice(string) for i in range(length)])
	return password
	
def encryptpassword(password):
	
	salt = os.urandom(4)
	h = hashlib.sha1(password)
	h.update(salt)
	return "{SSHA}" + encode(h.digest() + salt)
	
def adduserldap(username,domainname,passencrypt,uidnumber):
	l = ldap.initialize("ldap://debian.example.com")
    l.simple_bind_s("cn=admin,dc=example,dc=com","usuarioq")
    
    dn="uid=%s,ou=People,dc=example,dc=com" %username
    
    attrs = {}
    attrs['objectClass'] = ['Top','posixAccount','account']
    attrs['cn'] =username
    attrs['uid'] =username
    attrs['uidNumber'] = uidnumber
    attrs['gidNumber'] = '2002'
    attrs['homeDirectory'] = '/srv/hosting/%s' %username
    attrs['userPassword'] = passencrypt
    attrs['loginShell'] = '/bin/false'
    attrs['description'] = domainname
    
    ldif = modlist.addModlist(attrs)
    
    l.add_s(dn,ldif)
    
    l.unbind_s
    
    
