# Installing & Configuring OpenOlat

## Install JDK or JRE
```shell
sudo apt install openjdk-17-jdk
```

## Create user

```shell
sudo useradd -m -s /bin/bash openolat
```

## Install OpenOLAT on Apache Tomcat

### Download OpenOLAT

```shell
cd downloads
wget -c https://www.openolat.com/releases/openolat_2004.war
cd
unzip -d openolat-2004 downloads/openolat_2004.war
ln -s openolat-2004 webapp
```

### Setup Tomcat in user openolat home

```shell
cd ~/; mkdir bin conf lib run logs
```

### web.xml and catalina.sh
```shell
cd ~/conf; ln -s ../tomcat/conf/web.xml web.xml
cd ~/bin; ln -s ../tomcat/bin/catalina.sh catalina.sh
```

### Start & Stop - Tomcat

```shell
cd
ln -s tomcat/bin/startup.sh start
ln -s tomcat/bin/shutdown.sh stop
```

### Create setevn.sh

```
echo "CATALINA_HOME=~/tomcat
CATALINA_BASE=~
JRE_HOME=/usr/lib/jvm/java-17-openjdk-amd64
CATALINA_PID=~/run/openolat.pid
CATALINA_TMPDIR=/tmp/openolat
mkdir -p $CATALINA_TMPDIR

CATALINA_OPTS=" \
-Xmx1024m -Xms512m -XX:MaxMetaspaceSize=512m \
-Duser.name=openolat \
-Duser.timezone=Europe/Zurich \
-Dspring.profiles.active=myprofile \
-Djava.awt.headless=true \
-Djava.net.preferIPv4Stack=true \
-Djava.security.egd=file:/dev/urandom \
-XX:+HeapDumpOnOutOfMemoryError \
-XX:HeapDumpPath=. \
" > ~/bin/setenv.sh
```

### server.xml

```
cat << 'EOF' > ~/conf/server.xml
<?xml version='1.0' encoding='utf-8'?>
<Server port="8085" shutdown="SHUTDOWN">
  <Service name="Catalina">
    <Connector port="8088" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443"
               URIEncoding="UTF-8"
               scheme="https"
               proxyName="training.pontypriddholdings.com"
               proxyPort="443"
               relaxedPathChars="[]|{}^&#x5c;"
               relaxedQueryChars="[]|{}^&#x5c;" />
    <Engine name="Catalina" defaultHost="localhost">
        <Host name="localhost"  appBase="webapps"
              unpackWARs="true" autoDeploy="true">

            <Valve className="org.apache.catalina.valves.RemoteIpValve"
                internalProxies="127\.0\.0\.1"
                remoteIpHeader="x-forwarded-for"
                proxiesHeader="x-forwarded-by"
                protocolHeader="x-forwarded-proto"
                protocolHeaderHttpsValue="https"
                portHeader="x-forwarded-port"/>
        </Host>
    </Engine>
  </Service>
</Server>
EOF
```

### Set ENV variables

Backup:
```shell
if [ ! -d ~/backup ]; then
 mkdir ~/backup
fi
timestamp=d$(date +"%Y%m%d").t$(date +"%H%M%S")
cp ~/.zshrc ~/backup/.zshrc.$timestamp.bak
```

```shell
echo "export CATALINA_BASE=~
export CATALINA_HOME=~/tomcat
export JRE_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> ~/.zshrc

cd; . .zshrc
```

### Test Start & Stop
```shell
./start
```

Should show:
```
Using CATALINA_BASE:   /home/openolat
Using CATALINA_HOME:   /home/openolat/tomcat
Using CATALINA_TMPDIR: /tmp/openolat
Using JRE_HOME:        /usr/lib/jvm/java-17-openjdk-amd64
Using CLASSPATH:       /home/openolat/tomcat/bin/bootstrap.jar:/home/openolat/tomcat/bin/tomcat-juli.jar
Using CATALINA_OPTS:    -Xmx1024m -Xms512m -XX:MaxMetaspaceSize=512m -Duser.name=openolat -Duser.timezone=Europe/Zurich -Dspring.profiles.active=myprofile -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Djava.security.egd=file:/dev/urandom -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=.
Using CATALINA_PID:    /home/openolat/run/openolat.pid
Tomcat started.
```

```shell
./stop
```

Shows:
```
Using CATALINA_BASE:   /home/openolat
Using CATALINA_HOME:   /home/openolat/tomcat
Using CATALINA_TMPDIR: /tmp/openolat
Using JRE_HOME:        /usr/lib/jvm/java-17-openjdk-amd64
Using CLASSPATH:       /home/openolat/tomcat/bin/bootstrap.jar:/home/openolat/tomcat/bin/tomcat-juli.jar
Using CATALINA_OPTS:    -Xmx1024m -Xms512m -XX:MaxMetaspaceSize=512m -Duser.name=openolat -Duser.timezone=Europe/Zurich -Dspring.profiles.active=myprofile -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Djava.security.egd=file:/dev/urandom -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=.
Using CATALINA_PID:    /home/openolat/run/openolat.pid
PID file found but either no matching process was found or the current user does not have permission to stop the process. Stop aborted.
```

## Setup Database

```sql
CREATE user oodbu WITH password 'V2*/>O\~dd44';
CREATE DATABASE oodb WITH OWNER oodbu;
```

### Test
```
psql oodb -U oodbu -h localhost
```

### Create Schema

Note: Obtain postgreSQL setup file from GitHub repo (`src/main/resources/database/postgresql/setupDatabase.sql`)

```
psql oodb -U oodbu -h localhost -f /tmp/setupDatabase.sql
```

## OpenOlat Config
```
cat << 'EOF' > ~/lib/olat.local.properties
db.source=jndi
db.jndi=java:comp/env/jdbc/openolatDS
db.vendor=postgresql
installation.dir=/home/openolat
log.dir=/home/openolat/logs
server.contextpath=/openolat
server.domainname=training.pontypriddholdings.com
server.port=443
server.port.ssl=443
smtp.host=disabled
tomcat.id=1
userdata.dir=/home/openolat/olatdata
EOF
```

## Application context descriptor

```shell
mkdir -p ~/conf/Catalina/localhost/

cat << 'EOF' > ~/conf/Catalina/localhost/ROOT.xml
<?xml version="1.0" encoding="UTF-8" ?>
<Context path="" docBase="/home/openolat/webapp" debug="0" reloadable="false" allowLinking="true">
     <Resource name="jdbc/openolatDS" auth="Container" type="javax.sql.DataSource"
         maxTotal="16" maxIdle="4" maxWaitMillis="60000"
         username="oodbu" password="oodbpasswd"
         driverClassName="org.postgresql.Driver"
         validationQuery="SELECT 1"
         validationQueryTimeout="-1"
         testOnBorrow="true"
         testOnReturn="false"
         url="jdbc:postgresql://localhost:5432/oodb"/>
</Context>
EOF
```

## log4j2
```shell
cat << 'EOF' > ~/lib/log4j2.xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
   <Appenders>
       <RollingFile name="RollingFile" fileName="/home/openolat/logs/olat.log"
           filePattern="/home/openolat/logs/olat.log.%d{yyyy-MM-dd}">
           <PatternLayout
                   pattern="%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %marker %c{1} ^%%^ I%X{ref}-J%sn ^%%^ %logger{36} ^%%^ %X{identityKey} ^%%^ %X{ip} ^%%^ %X{referer} ^%%^ %X{userAgent} ^%%^ %msg%ex{full,separator( )}%n" />
           <Policies>
               <TimeBasedTriggeringPolicy interval="1" />
           </Policies>
       </RollingFile>
   </Appenders>
   <Loggers>
       <Logger name="org.apache.commons.httpclient" additivity="false" level="warn">
           <AppenderRef ref="RollingFile" />
       </Logger>
       <Logger name="org.apache.pdfbox" additivity="false" level="fatal">
           <AppenderRef ref="RollingFile" />
       </Logger>
       <Logger name="org.apache.fontbox" additivity="false" level="fatal">
           <AppenderRef ref="RollingFile" />
       </Logger>
       <Logger name="org.hibernate.engine.internal.StatisticalLoggingSessionEventListener" additivity="false" level="fatal">
           <AppenderRef ref="RollingFile" />
       </Logger>
       <Logger name="org.hibernate.SQL" additivity="false" level="fatal">
           <AppenderRef ref="RollingFile" />
       </Logger>
        <Logger name="org.hibernate.type.descriptor.sql.BasicBinder" additivity="false" level="fatal">
            <AppenderRef ref="RollingFile" />
        </Logger>
        <Logger name="org.apache.activemq.audit" additivity="false" level="warn">
           <AppenderRef ref="RollingFile" />
        </Logger>
        <Root level="info">
            <AppenderRef ref="RollingFile" />
        </Root>
   </Loggers>
</Configuration>
EOF
```

## Generate SSL Certs & Nginx Configuration

```shell
sudo apt install python3-certbot-nginx
sudo certbot --nginx certonly -d training.pontypriddholdings.com
```

Nginx `location /` block configuration should look like:
```
...
    location / {
        proxy_pass http://localhost:8088/; # Replace 8080 with OpenOlat's Tomcat port if different
        # Add this for debugging:
        add_header X-Debug-Host $host;
        add_header X-Debug-Proto $scheme;
        add_header X-Debug-For $proxy_add_x_forwarded_for;
    }
...
```