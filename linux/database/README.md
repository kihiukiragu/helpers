# PostgreSQL

## Install PostgreSQL
> [!NOTE]
> Versions mentioned in this document might not be current if this document has not been updated in a while

There are 2 ways to install PostgreSQL. Either you install the version that ships with Debian (easiest and recommended for stability) OR you install the current release from PostgreSQL( newer but not as stable):

### Install Debian's Default PostgreSQL Version
The simplest PostgreSQL install( this will install whatever the current stable PostgreSQL that ships with your Debian OS):
```
sudo apt install postgresql postgresql-client
```

### Install PostgreSQL via PostgreSQL Apt Repository
You might want flexibility to be able to pick whatever a certain PostgreSQL version. For that follow the following steps:
1. Add PostgreSQL repo key:
   ```
   sudo apt install -y postgresql-common
   sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
   ```
2. Install psql server and client (this can be adjusted to install 15,16, or even 18 etc.): 
   ```
   sudo apt -y install postgresql postgresql-client`
   ```
   OR
   ```
   sudo apt -y install postgresql-17 postgresql-client17`
   ```
3. Installing postgres in Linux results in a user `postgres` being created. Change to this user i.e. `postgres` and you can then start creating databases, tables and running SQL queries:
   - Change user:
     ```
     sudo su - postgres
     ```
     OR
     ```
     sudo -u postgres zsh #if using oh-my-zsh
     ```
   - Access the postgres terminal based application `psql`:
     ```
     psql
     ```
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
- Upgrade databases on cluster 15 (this will upgrade 15 to any newer version e.g. 17):
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
For zsh users (asterisk must be enclosed in quotes):
```
sudo apt remove --purge postgresql-'*'
```
For bash users:
```
sudo apt remove --purge postgresql-*
```

## Installing and Using pgAdmin
pgAdmin is a helpful tool to easily run queries on the fly similar to psql but can come in handy if you:
- Don't have command-line access.
- Would like to run queries from a file, save them in a certain order.
- You simply prefer a UI client to run SQL and not the psql client.
- To install pgAdmin4
  ```
  curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
  sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
  sudo apt install pgadmin4
  ```
- You might need to edit your local `pg_hba.conf` file e.g. `vi /etc/postgresql/17/main/pg_hba.conf` and add the following line (below `# IPv4 local connections:` line):
  ```
  host        all                 127.0.0.1/32                trust
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
- Start pgAdmin4 (If using a menu based Desktop Environment e.g. xfce or Cinnamon, it will likely be in the Applications menu under 'Development')
- Create a new Server
  - General tab: Give the connection a name of your choice eg `customer-db-ssh-tunnel`
  - Connection tab:
    - Host name/address (host is the PC you are using): `localhost`
    - Port (default port on your local PC): `5432`
    - Maintenance database (enter the database that you have been granted access to remotely): `customer`
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
