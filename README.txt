El objetivo de este proyecto es implementar mediante el uso de scripts una infraestructura de
hosting web, en el que se podrá dar de alta un usuario y que este tenga un dominio propio, pueda
acceder a su espacio mediante ftp y tenga una base de datos a la que podrá acceder mediante
phpmyadmin.

También tendrá la funcionalidad de poder cambiar las contraseñas a los usuarios, tanto para mysql
como para ldap que sera el sistema de cuentas centralizada donde esta la información de los
usuarios para poder acceder por ftp.

Por ultimo, se podrá dar de baja un dominio junto con el usuario, donde se borrara toda la
información del usuario y dominio de los servicios.

Los servicios implementados son:

-Apache como servidor web
-MySQL como servidor de Base de datos
-OpenLDAP como servidor de cuentas centralizadas
-Proftpd como servidor ftp.
-bind9 como servidor de resolución de nombres DNS
-phpmyadmin como gestor web de base de datos
