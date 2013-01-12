import functions as fun

username = raw_input("enter your username: ")
fun.checkusername(username)
domainname = raw_input("enter your domain name, without www and .com :")
fun.checkdomainname(domainname)

fun.createdir(username)
fun.createvh(username,domainname)
