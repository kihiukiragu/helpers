# Install Apache Tomcat

## Install JDK
```
sudo apt install default-jdk -y
```

## Create User
```
sudo useradd -m -d /opt/tomcat -U -s /bin/false tomcat
```

## Install Tomcat
```
cd /opt
wget https://downloads.apache.org/tomcat/tomcat-11/v11.0.8/bin/apache-tomcat-11.0.8.tar.gz
tar -xzvf apache-tomcat-11.0.8.tar.gz -C /opt/tomcat --strip-components=1
```

## Create systemd Service

```
echo "[Unit]
Description="Tomcat Service"
After=network.target
[Service]
Type=forking
User=tomcat
Group=tomcat
Environment="JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64"
Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom"
Environment="CATALINA_BASE=/opt/tomcat"
Environment="CATALINA_HOME=/opt/tomcat"
Environment="CATALINA_PID=/opt/tomcat/temp/tomcat.pid"
Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"
ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/tomcat.service
```

## Install Apache

Follow this [link](https://www.rosehosting.com/blog/how-to-install-apache-tomcat-on-debian-11/)

## Apache Conf

```
<VirtualHost *:443>
    ServerName cyber.pontypriddholdings.com
    DocumentRoot /opt/tomcat

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/cyber.pontypriddholdings.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/cyber.pontypriddholdings.com/privkey.pem

    # Configure proxy connection timeout
    ProxyTimeout 300

    ProxyPass / http://localhost:8080/
    ProxyPassReverse / http://localhost:8080/

</VirtualHost>

<VirtualHost *:80>
    ServerName cyber.pontypriddholdings.com
    Redirect permanent / https://cyber.pontypriddholdings.com
</VirtualHost>
```

## Enable an Admin user

Note: The roles and password have to be set for it to work.
```shell
  <role rolename="manager-gui"/>
  <role rolename="manager-script"/>
  <role rolename="manager-jmx"/>
  <role rolename="manager-status"/>
  <role rolename="admin-gui"/>
  <role rolename="admin-script"/>
  <user username="admin" password="<must-be-changed>" roles="manager-gui,manager-script,manager-jmx,manager-status,admin-gui,admin-script"/>
```

