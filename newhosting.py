import functions as fun

username = raw_input("enter your username: ")
domainname = raw_input("enter your domain name, without www and .com :")

fun.createdir(username)
fun.createvh(username,domainname)
