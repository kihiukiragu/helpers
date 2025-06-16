# Lime Survey Installation


## Pre-requisites
```
sudo apt install php php-fpm php-pdo php-pgsql php-mbstring php-ldap php-intl php-zip php-gd php-imap php-xml
```

## Download Lime Survey

```
wget -c https://download.limesurvey.org/latest-master/limesurvey6.10.2+250127.zip
```

## Create limesurvey web folder
```
unzip limesurvey6.10.2+250127.zip 
```

## Create PostgreSQL User for LimeSurvey

```
CREATE DATABASE limesurv;
CREATE USER limesurv WITH ENCRYPTED PASSWORD 'the-password-goes-here';
GRANT ALL PRIVILEGES ON DATABASE limesurv TO limesurv;
```

## File Permissions
```
chmod -R 755 limesurvey/
chmod -R 777 limesurvey/application/config
chmod -R 777 limesurvey/tmp
chmod -R 777 limesurvey/upload
```

## Install Limesurvey
```
http://local.kihiu.kiragu/index.php?r=surveyAdministration/view&surveyid=516226
```
## Admin Login
```
http://local.kihiu.kiragu/index.php?r=admin/authentication/sa/login
```