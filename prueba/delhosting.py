f = open ('hola','r')
lista = f.readlines()
f.close()

f = open ('hola','w')

elemento = 'zone "pepepalote.com"\n'


temp = 'asd'
for i in range(0,len(lista)):
	if (lista[i] == elemento):
		temp = i	


for i in range(0,6):
	
    del lista[temp]
    

for i in range(0,len(lista)):
	f.write(lista[i])


f.close()
