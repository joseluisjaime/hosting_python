f = open ('hola','r')
lista = f.readlines()
f.close()

f = open ('hecho','w')

elemento = 'zone "pepe.com"\n'


temp = 'asd'
for i in range(0,len(lista)):
	if (lista[i] == elemento):
		temp = i	

for i in 4:
	temp = temp
    print lista[temp]

