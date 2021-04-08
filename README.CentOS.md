Shibbolet-SP SPID - Just a simple howto
=======================================

Questo piccolo howto vi guiderà nella configurazione di Shibboleth-SP su Centos7.

Installazione di Apache
-----------------------
```
sudo yum clean all
sudo yum -y update
sudo yum -y install httpd
```

Configurare Shibd come servizio:
```
sudo systemctl start httpd.service
sudo systemctl enable httpd.service
```

Creazione del virtualhost:
```
sudo mkdir -p /var/www/<hostname-sp>/main
sudo chown -R $USER:$USER /var/www/<hostname-sp>/main/
sudo chmod -R 755 /var/www
sudo vi /var/www/<hostname-sp>/main/index.html
```

Se non sono stati creati altri virtual host creare:
```
sudo mkdir /etc/httpd/sites-available
sudo mkdir /etc/httpd/sites-enabled
```

Modificare httpd.conf:
```
sudo vi /etc/httpd/conf/httpd.conf
```

Alla fine del file aggiungere:
```
IncludeOptional sites-enabled/*.conf
```

Configurare il virtual host:
```
sudo vi /etc/httpd/sites-available/<hostname-sp>.conf
```

```
<VirtualHost *:80>
  ServerName <hostname-sp>
  DocumentRoot /var/www/<hostname-sp>/web
  ErrorLog /var/www/<hostname-sp>/logs/error.log
  CustomLog /var/www/<hostname-sp>/logs/requests.log combined
</VirtualHost>
```

Creare il link su sites-enabled:
```
sudo ln -s /etc/httpd/sites-available/<hostname-sp>.conf /etc/httpd/sites-enabled/<hostname-sp>.conf
```

Aprire le porte 80 e 443
```
sudo firewall-cmd --add-service=http
sudo firewall-cmd --add-service=https
sudo firewall-cmd --runtime-to-permanent
sudo firewall-cmd --reload
sudo systemctl restart httpd
```

Installare un certificato let's encrypt:
```
sudo yum install epel-release
sudo yum install httpd mod_ssl python-certbot-apache
sudo certbot --apache -d <hostname-sp>
sudo systemctl restart httpd
```

Impostare il rinnovo del certificato
```
sudo certbot renew
sudo crontab -e
30 2 * * * /usr/bin/certbot renew >> /var/log/le-renew.log
```

Le installazioni seguenti sono opzionali:

Installare php
```
sudo yum install php
sudo systemctl restart httpd
```

Creare la cartella protetta
```
sudo mkdir -p /var/www/<hostname-sp>-protected/main/
sudo chown -R $USER:$USER /var/www/<hostname-sp>-protected/main/
sudo chmod -R 755 /var/www
sudo vi /var/www/<hostname-sp>-protected/main/index.php
```

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
   <head>
      <title>SP test</title>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   </head>
   <body>
Dati:<br>
<?php
      foreach ($_SERVER as $key => $value){
         print $key." = ".$value."<br>";
      }
      foreach ($_ENV as $key => $value){
         print $key." = ".$value."<br>";
      }
      foreach ($_COOKIE as $key => $value){
         print $key." = ".$value."<br>";
      }
?>
   </body>
</html>
```

Configurare il virtual host:
```
sudo vi /etc/httpd/sites-available/<hostname-sp>-protected.conf
```

```
<IfModule mod_alias.c>
  Alias /secure /var/www/<hostname-sp>-protected/
  <Directory //var/www/<hostname-sp>-protected>
    Options Indexes MultiViews FollowSymLinks
    Require all granted
  </Directory>
  <Location /protected>
    AuthType shibboleth
    ShibRequestSetting requireSession 1
    Require valid-user
  </Location>
</IfModule>
```

Creare il link su sites-enabled:
```
sudo ln -s /etc/httpd/sites-available/<hostname-sp>-protected.conf /etc/httpd/sites-enabled/<hostname-sp>-protected.conf
```

Installazione di Shibboleth
---------------------------

```
sudo yum install wget
sudo wget http://download.opensuse.org/repositories/security://shibboleth/CentOS_7/security:shibboleth.repo -O /etc/yum.repos.d/shibboleth.repo
yum install shibboleth.x86_64
```

Installare ntp:
```
sudo yum install ntp
```

Configurare Shibd come servizio:
```
sudo systemctl start shibd.service
sudo systemctl enable shibd.service
```

Copiare i file xml di configurazione di Shibbolet e configurare shibboleth2.xml
[SPID SP Shibboleth](https://github.com/italia/spid-sp-shibboleth)

Sul file shibboleth2.xml allegato è riportata la configurazione dell'IDP di test, per aggiungere gli IDP di produzione di SPID, scaricare i metadata attraverso l'invocazione dell'api del Registro SPID
```
curl -H "Accept:application/json" https://registry.spid.gov.it/api/identity-providers
```
copiarli in /etc/shibboleth/metadata/ (creare la cartella) e aggiungerli come fatto per l'ambiente di test.

Creare il certificato di signing che andrà copiato nella cartella /etc/shibboleth/certs/ (creare la cartella):
```
openssl req -x509 -nodes -sha256 -days 365 -newkey rsa:2048 -keyout sp-cert.key -out sp-cert.crt
```

Uno dei primi rilasci di SPID sulla community developers è stato il [playbook Ansible di shibboleth-sp](https://github.com/italia/spid-sp-playbook).
