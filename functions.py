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
        control = "y"
	return control
       
def checkdomainname(domainname):
    listdomain = commands.getoutput("ls /etc/apache2/sites-available/")
    listdomain = listdomain.split("\n")
    if domainname in listdomain:
        control = "y"  
	return control

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

    call(["a2ensite",domainname], stdout=open(os.devnull, 'wb'))
    call(["service","apache2","reload"], stdout=open(os.devnull, 'wb'))

def aleatorypassword():
	
	length = 4
	string = "1234567890abcdefghijklmnopqrstuvwxyz"
	password = ""
	password = password.join([choice(string) for i in range(length)])
	return password
	
def encryptpassword(password):
	
	enpassword = commands.getoutput("slappasswd -h {SSHA} -s "+password)
	return enpassword

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
    sql="GRANT ALL PRIVILEGES ON db_%s.* TO 'my%s'@'localhost' IDENTIFIED BY '%s';" %(domainname,username,userpass)
    cursor.execute(sql)
    cursor.close()
    
def createzone(domainname):
	
	f = open("src/db.changename","r")
	texto = f.read()
	texto = texto.replace("changename",domainname)
	f.close()
	
	nuevo = open("/var/cache/bind/db."+domainname,"w")
	nuevo.write(texto)
	nuevo.close()
	
	f = open("/etc/bind/named.conf.local","a")
	newzone = """
zone "%s.com"
{
	type master;
	file "db.%s";
};
""" %(domainname,domainname)
	f.write(newzone)
	f.close()
	
	call(["service","bind9","restart"], stdout=open(os.devnull, 'wb'))
	
def changepassmysql(username,password):	
    
	db=mysql.connect('localhost','root','usuarioq','mysql')
	sql = "set password for my%s@'localhost' = password('%s');" % (username,password)
	cursor=db.cursor()
	cursor.execute(sql)
	cursor.close()
	
def changepassftp(username,password):
	
    l = ldap.initialize("ldap://hosting.example.com")
    l.simple_bind_s("cn=admin,dc=example,dc=com","usuarioq")    
    dn="uid=%s,ou=People,dc=example,dc=com" %username
    l.passwd_s(dn,None,password)

def getusername(domainname):
	
	l = ldap.initialize("ldap://hosting.example.com")
	base_dn = 'ou=People,dc=example,dc=com' 
	filtro = '(description=%s)' % domainname 
	attrs = ['cn'] 
	
	result = l.search_s( base_dn, ldap.SCOPE_SUBTREE, filtro, attrs )
	username = result[0][1]['cn'][0]
	return username
	
def deldir(username):
	
	call(["rm","-r","/srv/hosting/" + username])

def delvh(domainname):
	
    call(["a2dissite",domainname], stdout=open(os.devnull, 'wb'))
    call(["service","apache2","reload"] , stdout=open(os.devnull, 'wb'))
    call(["rm","/etc/apache2/sites-available/"+domainname])

def deluserldap(username):
	
	    l = ldap.initialize("ldap://hosting.example.com")
	    l.simple_bind_s("cn=admin,dc=example,dc=com","usuarioq")
	    dn="uid=%s,ou=People,dc=example,dc=com" %username
	    l.delete_s(dn)

def delmysql(username,domainname):
	
    db=mysql.connect(host='localhost',user='root',passwd='usuarioq')
    cursor=db.cursor()
    sql='drop database db_%s;' %domainname
    cursor.execute(sql)
    sql="drop user 'my%s'@'localhost';" % username
    cursor.execute(sql)
    cursor.close()
	
def delzone(domainname):

    f = open ('/etc/bind/named.conf.local','r')
    contenido = f.readlines()
    f.close()
    
    elemento = 'zone "%s.com"\n' % domainname
    temp = 1
    for i in range(0,len(contenido)):
		
        if (contenido[i] == elemento):
            temp = i
	

    for i in range(0,5):
        del contenido[temp]
    
    f = open ('/etc/bind/named.conf.local','w')

    for i in range(0,len(contenido)):		
        f.write(contenido[i])
	
    f.close()
    
    call(["rm","/var/cache/bind/db."+domainname])	
    call(["service","bind9","restart"], stdout=open(os.devnull, 'wb'))
	
	
		
