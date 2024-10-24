# PostgreSQL

## Install PostgreSQL
> [!NOTE]
> The versions might be outdated if this document is not up to date.

There are 2 ways to install PostgreSQL. Either you install the version that ships with Debian (easiest and recommended for stability) OR you install the current release from PostgreSQL( newer but not as stable):
- Stable: PostgreSQL 15 (Current Stable version for Debian repositories) - if on Debian 12.X, simply run the following:
 ```
 sudo apt install postgresql postgresql-contrib
 ```
- PostgreSQL 16 or 17 (if you want latest PostgreSQL features):
   1. Add PostgreSQL repo key:
      ```
      wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
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
- If upgrade is successful with no errors, confirm databases exist
- Drop the 15 cluster:
  ```
  pg_dropcluster 15 main
  ```

## Uninstall PostgreSQL:
> [!WARNING]
> If not done right, this will delete all your databases running on the version you delete. Be careful with this!

After installing a newer version e.g. you install postgresql-16 **AND** successfully upgrading to a new cluster, you might want to remove and purge older version postgresql-15:
```
apt remove --purge postgresql-15
```
