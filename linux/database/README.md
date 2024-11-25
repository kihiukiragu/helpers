# PostgreSQL

## Install PostgreSQL
> [!NOTE]
> Versions mentioned in this document might not be current if this document has not been updated in a while

There are 2 ways to install PostgreSQL. Either you install the version that ships with Debian (easiest and recommended for stability) OR you install the current release from PostgreSQL( newer but not as stable):
- Stable: PostgreSQL 15 (Current Stable version for Debian repositories) - if on Debian 12.X, simply run the following:
 ```
 sudo apt install postgresql postgresql-contrib
 ```
- PostgreSQL 16 or 17 (if you want latest PostgreSQL features):
   1. Add PostgreSQL repo key:
      ```
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /usr/share/keyrings/postgresql.gpg
      ```
   2. Add PostgreSQL repo to your Debian installation repo lists folder:
      ```
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | sudo tee  /etc/apt/sources.list.d/pgdg.list
      ```
   3. Install psql server and client: `apt -y install postgresql-17`
   4. Change user to the `postgres` user and start creating databases, tables and running SQL queries:
      - Change user:
      ```
      sudo su - postgres
      ```
      OR
      ```
      sudo -u postgres zsh #if using oh-my-zsh
      ```
      - Access the postgres terminal based front end `psql`:
      `psql`
      - Create roles/user, databases and queries in here.
      - To exit or quit from `psql` type: `\q`
   4. (Recommended) Secure user postgres - TBD
   5. (Recommended) Improve postgres performance - TBD

## Upgrading/Migrating Databases
If you have version 15 and 17 installed on the same server, it is possible to upgrade the databases running on the 15 cluster to 17:
- Check/confirm what clusters are running:
  ```
  sudo pg_lsclusters
  ```
  Should yield something like:
  ```
  Ver Cluster Port Status Owner    Data directory              Log file
  15  main    5432 online postgres /var/lib/postgresql/15/main /var/log/postgresql/postgresql-15-main.log
  17  main    5433 online postgres /var/lib/postgresql/17/main /var/log/postgresql/postgresql-17-main.log
  ```
- Stop the 17 cluster to prepare for upgrade:
  ```
  sudo pg_dropcluster 17 main --stop
  ```
- Upgrade databases on cluster 15 (this will upgrade 15 to any newer version eg 17):
  ```
  sudo pg_upgradecluster 15 main
  ```
- If upgrade is successful with no errors, confirm that your databases still exist
- Drop the 15 cluster:
  ```
  sudo pg_dropcluster 15 main --stop
  ```

## Uninstall PostgreSQL:
> [!WARNING]
> If not done right, this will delete all your databases running on the version you delete. Be careful with this!

After installing a newer version e.g. you install postgresql-17 **AND** successfully upgrading to a new cluster, you might want to remove and purge older version postgresql-15:
```
apt remove --purge postgresql-15 postgresql-client-15
```

## Access a Remove Database via SSH Tunneling
### Using Terminal

Create an ssh tunnel:
```
ssh -f -o ExitOnForwardFailure=yes -L 63333:localhost:5432 username@remote.postgresql.server.com sleep 10
```

Access the database:
```
psql -d database_name -h localhost -p 63333
```

### Using pgAdmin4
The safer way to access a remote database is to use [SSH Tunneling](https://en.wikipedia.org/wiki/Tunneling_protocol#Secure_Shell_tunneling). This ensures:
- Password brute force attacks cannot be carried out as there's no direct way to connect to the database.
- Database port (typically port #5432) can thus be locked down to internal server use only.

Steps:
- Ensure postgres is installed on the ssh tunnel host (ie the PC you're currently using)
- Install pgAdmin4
  ```
  curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
  sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
  sudo apt install pgadmin4
  ```
- Start pgAdmin4 (If using a menu based Desktop Environment eg xfce or Cinnamon, it will likely be in the Applications menu under 'Development')
- Create a new Server
  - General tab: Give the connection a name of your choice eg `customer-db-ssh-tunnel`
  - Connection tab:
    - Host name/address (host is the PC you are using): `localhost`
    - Port (default port on your local PC): `5432`
    - Maintanance database (enter the database that you have been granted access to remotely): `customer`
    - Username (your username on the local PC): `pomollo`
  - SSH Tunnel tab:
    - Tunnel host (remote server where the db resides): `server.remote.example.com`
    - Tunnel port (usually 22 unless it has been configured otherwise): `22`
    - Username (your username on remote server): `pomollo`
    - Identity file (your private ssh key on your local PC): `/home/pomollo/.ssh/id_rsa`
  - Click on `Save`
- Connect to the server. You will be prompted to enter 2 passwords:
  - SSH Identity file password - if your ssh key contains a passphrase/password, enter it here
  - Connection password - the postgres password associated with your username on the remote server. Obtain this from the DBA.
