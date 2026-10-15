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
archive.apache.org keeps every release (downloads.apache.org only hosts the current ones). Verify the checksum before extracting:
```
cd /opt
sudo wget https://archive.apache.org/dist/tomcat/tomcat-11/v11.0.8/bin/apache-tomcat-11.0.8.tar.gz
sudo wget https://archive.apache.org/dist/tomcat/tomcat-11/v11.0.8/bin/apache-tomcat-11.0.8.tar.gz.sha512
sha512sum -c apache-tomcat-11.0.8.tar.gz.sha512
sudo tar -xzvf apache-tomcat-11.0.8.tar.gz -C /opt/tomcat --strip-components=1
sudo chown -R tomcat:tomcat /opt/tomcat
```

## Create systemd Service

A quoted heredoc keeps the quotes (systemd needs them around values containing spaces) and `tee` runs with sudo:
```
sudo tee /etc/systemd/system/tomcat.service << 'EOF'
[Unit]
Description=Tomcat Service
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
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now tomcat
```

## Install Apache

Install Apache and enable the modules the vhost below needs (the [Debian 11 guide](https://www.rosehosting.com/blog/how-to-install-apache-tomcat-on-debian-11/) is only a reference):
```
sudo apt install apache2
sudo a2enmod ssl proxy proxy_http
```

## Apache Conf

```
<VirtualHost *:443>
    ServerName tomcat.example.com
    DocumentRoot /opt/tomcat

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/tomcat.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/tomcat.example.com/privkey.pem

    # Configure proxy connection timeout
    ProxyTimeout 300

    ProxyPass / http://localhost:8080/
    ProxyPassReverse / http://localhost:8080/

</VirtualHost>

<VirtualHost *:80>
    ServerName tomcat.example.com
    Redirect permanent / https://tomcat.example.com
</VirtualHost>
```

## Enable an Admin user

Note: The roles and password have to be set for it to work. Grant only the roles needed (`manager-gui` for the web UI); add `manager-script`, `manager-jmx`, `manager-status` or the `admin-*` roles only if a tool needs them.
```shell
  <role rolename="manager-gui"/>
  <user username="admin" password="<must-be-changed>" roles="manager-gui"/>
```

