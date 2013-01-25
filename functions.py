from subprocess import call
import commands
import sys
from random import choice
import os
import hashlib
from base64 import urlsafe_b64encode as encode
import ldap
import ldap.modlist as modlist
import MySQLdb as mysql

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

def createdir(username,lastuid):
    call(["mkdir","-p","/srv/hosting/" + username])
    call(["cp","src/index.html","/srv/hosting/" + username])
    call(["chmod","-R","755","/srv/hosting/" + username])
    call(["chgrp","-R","2002","/srv/hosting/" + username])
    call(["chown","-R",lastuid,"/srv/hosting/" + username])

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

def lastuid():
	
	l = ldap.initialize("ldap://hosting.example.com")
    
	base_dn = 'ou=People,dc=example,dc=com' 
	filtro = '(uidNumber=*)' 
	attrs = ['uidNumber'] 
	
	result = l.search_s( base_dn, ldap.SCOPE_SUBTREE, filtro, attrs )
	
	list = []

	for i in result:
		
		list.append(i[1]['uidNumber'][0])
	
	uidnumber = max(list)
	uidnumber = int(uidnumber)
	uidnumber = uidnumber+1
	uidnumber = str(uidnumber)
	
	return uidnumber
	
def adduserldap(username,domainname,passencrypt,uidnumber):

    l = ldap.initialize("ldap://hosting.example.com")
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
    
def addusermysql(username,domainname,userpass):
	
    db=mysql.connect(host='localhost',user='root',passwd='usuarioq')
    cursor=db.cursor()
    sql='create database db_%s;' %domainname
    cursor.execute(sql)
    sql="GRANT ALL PRIVILEGES ON db_%s.* TO 'my%s'@'localhost' IDENTIFIED BY %s;" %(domainname,username,userpass)
    cursor.execute(sql)
    cursor.close()
    
