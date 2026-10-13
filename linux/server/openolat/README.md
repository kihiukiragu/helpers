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
wget -c https://www.openolat.com/releases/openolat_2105.war
cd
unzip -q -d openolat-2105 downloads/openolat_2105.war
ln -s openolat-2105 webapp
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

Note: `maxPartCount="-1"` and `maxParameterCount="-1"` are required for Tomcat 10.1.42 and later (including the 11.0.8 used here); the defaults break OpenOlat.

```
cat << 'EOF' > ~/conf/server.xml
<?xml version='1.0' encoding='utf-8'?>
<Server port="8085" shutdown="SHUTDOWN">
  <Service name="Catalina">
    <Connector port="8088" protocol="HTTP/1.1"
               maxPartCount="-1"
               maxParameterCount="-1"
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
CREATE user oodbu WITH password '<db-password>';
CREATE DATABASE oodb WITH OWNER oodbu;
```

### Test
```
psql oodb -U oodbu -h localhost
```

### Rotate the DB password

The password lives in three places: PostgreSQL, `~/conf/Catalina/localhost/ROOT.xml` (the `password` attribute of the `jdbc/openolatDS` resource) and `~/.pgpass`. Never commit it to this repo.

```shell
NEWPW=$(openssl rand -base64 24 | tr -d '/+=\n')
sudo -u postgres psql -c "ALTER USER oodbu WITH PASSWORD '$NEWPW';"

export CATALINA_BASE=~ CATALINA_HOME=~/tomcat JRE_HOME=/usr/lib/jvm/java-17-openjdk-amd64
~/stop
cp ~/conf/Catalina/localhost/ROOT.xml ~/backup/ROOT.xml.bak
sed -i "s|password=\"[^\"]*\"|password=\"$NEWPW\"|" ~/conf/Catalina/localhost/ROOT.xml
sed -i "s|^\(localhost:5432:oodb:oodbu:\).*|\1$NEWPW|" ~/.pgpass
~/start

psql oodb -U oodbu -h localhost -c 'SELECT 1'
```

If the password contains `&`, `<` or `>` it must be XML-escaped in `ROOT.xml`; the generated one above avoids this. Check `~/logs/olat.log` and `https://training.pontypriddholdings.com/` after the restart.

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
         username="oodbu" password="<db-password>"
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

## Upgrading OpenOlat

Upgrades can skip versions (from 15.3 onwards). Done so far: 2004 (20.0.4) -> 20310 (20.3.10) -> 2105 (21.0.5), both on 2026-10-12. Check https://www.openolat.com/releases/ for newer WARs and https://docs.openolat.org/manual_admin/installation/updateGuide/ for version-specific steps.

The app is served at the root path (`Context path=""` in `ROOT.xml`), so REST is at `https://training.pontypriddholdings.com/restapi/`, not under `/openolat/`.

### 1. Download and extract (site can stay up)

```shell
cd ~/downloads
wget -c https://www.openolat.com/releases/openolat_NNNNN.war
cd
unzip -q -d openolat-NNNNN downloads/openolat_NNNNN.war
```

### 2. Stop Tomcat

Over a non-interactive `ssh host 'cmd'` the env from `.zshrc` is not loaded, so `./stop` talks to the default port 8005 instead of 8085 and fails. Export the vars first:

```shell
export CATALINA_BASE=~ CATALINA_HOME=~/tomcat JRE_HOME=/usr/lib/jvm/java-17-openjdk-amd64
~/stop
```

Wait until the process in `~/run/openolat.pid` is gone before backing up.

### 3. Backup (with Tomcat stopped)

```shell
ts=d$(date +%Y%m%d).t$(date +%H%M%S)
pg_dump -h localhost -U oodbu oodb | gzip > ~/backup/oodb.$ts.sql.gz
tar czf ~/backup/olatdata.$ts.tgz -C ~ olatdata
cp ~/conf/server.xml ~/backup/server.xml.$ts.bak
gzip -t ~/backup/oodb.$ts.sql.gz && tar tzf ~/backup/olatdata.$ts.tgz > /dev/null && echo verified
```

### 4. Switch and start

```shell
rm ~/webapp && ln -s ~/openolat-NNNNN ~/webapp
~/start
```

The first start runs DB migrations and can take a while (21.0.5 took about 40 seconds here); do not stop Tomcat until it finishes. Watch with:

```shell
tail -f ~/logs/olat.log | grep -i upgrade
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8088/dmz/    # 200 when up
```

### Rollback

Stop Tomcat, drop and recreate `oodb`, restore the dump with `gunzip -c ~/backup/oodb.<ts>.sql.gz | psql oodb -U oodbu -h localhost`, restore `olatdata` from the tarball, and repoint `~/webapp` at the previous `openolat-NNNN` directory (old directories are kept).

## REST API access

The API key is created by an admin in the portal: Administration -> User management -> (user) -> Authentications -> Add API-Key. On 20.3 the UI shows a "Client ID" and "Client secret"; use them as the Basic Auth username and password (not as Bearer or OAuth):

```shell
curl -u "$CLIENT_ID:$CLIENT_SECRET" https://training.pontypriddholdings.com/restapi/users/me
```

The key only sees what its user can see. Give the user the `olatAdmin` and `author` roles (User management -> Roles) to list all tests via `/restapi/repo/entries`. Never pass the secret as the username in a test: failed logins write the username to `olat.log`.

REST cannot read or edit test questions (export returns 403, no question-bank list), so bulk quiz edits are done on disk, below.

## Editing quiz questions on disk

Tests are QTI 2.1 packages under `~/olatdata/bcroot/repository/<olatResourceId>/_unzipped_/`. `<olatResourceId>` is the `olatResourceId` field from `/restapi/repo/entries`. Each question is a folder containing an `<type><hash>.xml` file (`mc`, `sc`, `fib`), and the test's `test<uuid>.xml` lists them in `assessmentItemRef` elements. Some folders contain more than one item file, so identify items by file or `identifier`, not folder name.

Fill-in-the-blank (`fib*.xml`) answers live in `<responseDeclaration>`: one `<correctResponse><value>` (shown as the correct answer) and one `<mapEntry mapKey="..." mappedValue="10.0" caseSensitive="false"/>` per accepted answer. Add an entry per alternative; set `caseSensitive="true"` where case matters (regex `\d` vs `\D`, vi keys). Escape quotes with an attribute delimiter that does not clash (`'"x"'`).

Procedure:

1. Check nobody is mid-test:
   ```shell
   psql -h localhost -U oodbu oodb -At -c "select count(*) from o_qti_assessmenttest_session where q_finish_time is null and q_termination_time is null and lastmodified > now() - interval '3 hours'"
   ```
2. Stop Tomcat (see Upgrading, step 2), then back up the DB and the repository folders being edited:
   ```shell
   ts=d$(date +%Y%m%d).t$(date +%H%M%S)
   pg_dump -h localhost -U oodbu oodb | gzip > ~/backup/oodb.$ts.sql.gz
   (cd ~/olatdata/bcroot/repository && tar czf ~/backup/repo-quizzes.$ts.tgz <id1> <id2>)
   ```
3. Copy the folders off the server, edit, check every changed file parses (`xml.etree.ElementTree.parse`), and copy only the changed files back into the same paths.
4. Start Tomcat, check `http://localhost:8088/dmz/` returns 200 and `olat.log` has no errors, then answer one edited question in the UI.

Past results keep their stored scores. Adding accepted answers or fixing an answer is safe. Removing questions from a test (below) can leave old attempts that answered them showing incomplete detail, so only do it when old results are no longer needed. Rollback: stop Tomcat and extract the tarball over `repository/`.

Only stop Tomcat when no student attempt is running; author-mode previews (`q_author_mode = true`) do not count:

```shell
psql -h localhost -U oodbu oodb -At -c "select count(*) from o_qti_assessmenttest_session where q_finish_time is null and q_termination_time is null and q_author_mode = false and lastmodified > now() - interval '3 hours'"
```

### Removing duplicate questions

A test lists its questions as self-closing `<assessmentItemRef identifier="..." href="<folder>/<file>.xml"/>` elements. To remove duplicates, delete the extra `assessmentItemRef` tags and leave the question files on disk.

- Compare the question text and the correct answers exactly (lowercase and collapse whitespace only). Do not strip punctuation: answers made only of symbols (`?????`, `*.txt`) all look identical once stripped, and a wrong copy gets kept.
- For choice questions compare the text of the correct choice, not its identifier, which is random per copy. For fill-in questions compare the accepted answers.
- If two copies disagree on the correct answer, keep the one that is right and remove the other.
- The test also stores a fixed `MAXSCORE` (the sum of all question points). Lower it by the points of the removed questions, in the `<outcomeDeclaration identifier="MAXSCORE">` default value of the test file. The per-attempt pick count (`<selection select="N"/>`) is unchanged.
- Afterwards re-run the duplicate check and confirm it finds none.

### Fill-in-the-blank layout

Fill-in questions are `fib*.xml` items. The question body is one paragraph with a single `<textEntryInteraction responseIdentifier="RESPONSE_1"/>`. To get an inline box instead of a typed `___`:

- Replace the `___` in the text with the `<textEntryInteraction .../>` element and delete the copy at the end of the paragraph.
- Convert backtick pairs to `<code>...</code>` (the renderer shows it as monospace). The box can sit inside `<code>`.
- Questions with two `___` but one input need a second interaction and `RESPONSE_2` declaration with its own mapping; leave them for manual editing. The simpler fix is to reword to a single blank and replace the `<correctResponse>` and `<mapping>` (done for the ssh-keygen question, now "generate an SSH ___ of public and private keys", answer `pair`). A single box that accepts either word of a two-word answer lets students pass by typing only one of them.

Do not set `expectedLength` on the box: it hints at the length of the answer.

### Regex and other backslash content

The original import ran question text through Markdown, which swallowed backslashes (`\d` became `d`), `*...*` pairs and `_`. Check any new import for this. In the RegEx test, 40 item files were repaired on 2026-10-12: write the backslash literally in `<p>`/`<simpleChoice>` text, wrap regex in stems in `<code>`, and set `caseSensitive="true"` on fill-in answers (`\d` vs `\D`). Do not add bare-letter alternatives (`d` for `\d`); they teach the wrong thing.

### Content review (2026-10-12)

All seven quizzes were reviewed and corrected on disk with the procedure above (RegEx, PostgreSQL, Bash, Git, Linux Admin, Kenya DPA, Cyber-Security). Things to keep in mind for future edits:

- Questions removed from a test (wrong or duplicate): Git "git reset soft HEAD", PostgreSQL `DROP DATABASE ... CASCADE` and the `SET` role attribute, DPA Data Protection Tribunal. The question files stay on disk; `MAXSCORE` was lowered by 10 each.
- Some folders hold two item files for the same question (a duplicate that was dropped from the test). Edit every file in the folder so they stay identical.
- Kenya DPA questions were checked against the Act and the Data Protection (General) Regulations, 2021, not against GDPR. Points that differ from GDPR: DPO designation is optional ("may", s.24), breach notification to data subjects needs a "real risk of harm" and to the Commissioner is within 72 hours (s.43), no Tribunal (appeals go to the High Court, s.64), administrative fines are KES 5 million or 1% of turnover whichever is lower (s.63), general penalty is KES 3 million or 10 years (s.73), access requests are due in 7 days and rectification/erasure in 14 days (Regulations), portability in 30 days (s.38).
- Verify PostgreSQL claims against the running version (18.x here): `VIRTUAL` generated columns exist only from 18; `TRUNCATE` resets sequences only with `RESTART IDENTITY`.
- Markdown stripped backslashes from the original RegEx import (`\d`, `\b`, `\.`); they were restored, and bare-letter answers such as `d` for `\d` were removed so students learn the real syntax.
- Structure check after editing: every `responseIdentifier`/choice reference resolves, correct answers point at existing choice ids, and `MAXSCORE` equals the sum of item points. This caught RegEx "grep whole words" (one choice only, now `-w`/`--word-regexp` plus three distractors) and Bash `ssh-keygen` (blank answer scored; now `-N`/`N`, case-sensitive).
- Not changed, for a later decision: DPA transfer questions that mention "standard contractual clauses" (Kenyan law says "legal instrument" and binding corporate rules).

### Notes for 21.x

- The guide documents Tomcat 10.1, Java 17 and PostgreSQL 18. This server runs Tomcat 11.0.8 with Java 17 and works on 21.0.5.
- 21.0 and later recommend delivering user-provided content (HTML pages, CPs, SCORM) from a second domain via `server.content.domainname=<other-domain>` in `olat.local.properties`, with a matching reverse-proxy vhost. It must not be a subdomain of `server.domainname`. Not configured here.
- Hibernate prints thousands of `deprecated annotation [jakarta.persistence.Temporal]` warnings at startup; they are harmless.
- Tomcat's `catalina.out` shows `Invalid character found in method name` exceptions when scanners send TLS to the plain HTTP port 8088; also harmless.
