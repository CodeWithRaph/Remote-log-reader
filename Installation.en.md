# Installation & Configuration

This project uses Docker containers.<br>
One to set up the database and another to run the Flask application.

## Table of contents
- [Install the Flask app and the DB](#install-the-flask-app-and-the-db)
  - [Configuration before starting containers](#configuration-before-starting-containers)
- [Prepare a client machine](#prepare-a-client-machine)
  - [Granting log read permissions](#granting-log-read-permissions)
- [Switching the server to production](#switching-the-server-to-production)


## Install the Flask app and the DB

Clone the repository.
```bash
git clone https://github.com/CodeWithRaph/Remote-log-reader.git
cd Remote-log-reader
```

### Configuration before starting the containers

1. Edit the file `.env.example` and fill the required values.

> ## Help:
> ### Required parameters
>- **DB_PASSWD:** password for the database user.
>- **SECRET_KEY:** the secret used by Flask to secure sessions/cookies/forms. Replace with a randomly generated value in production.
>- **SSH_USER:** the user used to read logs on client machines.
>- **SSH_PASSPHRASE:** passphrase for the server SSH private key. Leave empty if your key has no passphrase.
> ---
> ### Optional parameters
>- DB_HOST: host for MariaDB. If you run the DB in the provided container you typically leave the default.
>- SSH_KEY_PATH: path to the SSH private key (default path can be used).

2. Rename the example env file to `.env`
```bash
cp .env.example .env
```

3. Start the containers
```bash
docker compose up -d
```

4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) (development server)
*(If you run on a remote machine, replace 127.0.0.1 with the host IP.)*

Default accounts included for testing:

| Login | Password |
|:-----:|:--------:|
| admin | admin |
| manager | manager |
| user | user |


## Prepare a client machine

First, ensure the client machine can reach the server.

### Granting log read permissions

There are **2 options**:
- Give a group (e.g. `log-readers`) read access to an entire directory (simpler).
- Give that group read access to a specific list of files (more secure).

---
#### Option 1 — allow reading a whole directory

1. Create the user that will be used to establish the SSH connection.

> ## Help:
>`<user>`: replace with the user that will read logs on the client.<br>
>`<password>`: user password.<br>
>`adm`: Debian/Ubuntu group that already has read access to some system logs.

```bash
sudo useradd <user>
sudo passwd <password>
sudo groupadd adm
sudo usermod -aG adm <user>
```

2. Copy the central server's public RSA key to the client's authorized keys (via scp).

```bash
su <user>
mkdir -p ~/.ssh
cat server_public_key >> ~/.ssh/authorized_keys
```

---
#### Option 2 — allow reading a specific list of files

1. Create the user for SSH access and a dedicated group for log readers.

> ## Help:
>`<user>`: replace with the user used to read logs.<br>
>`<password>`: user password.<br>
>`<logs-readers>`: replace with the name of the group that will get read rights.

```bash
sudo useradd <user>
sudo passwd <password>
sudo groupadd <logs-readers>
sudo usermod -aG <logs-readers> <user>
```

2. Copy the central server's public RSA key to the client's authorized keys (via scp).

```bash
su <user>
sudo mkdir ~/.ssh
```

```bash
sudo apt install acl
```

You will need to update the script below to reflect the files you authorize.<br>
Example script to set ACL read permission for the group on specific log files.

> ## Aide:
>`<logs-readers>`: Replace by the name of the group that will read the logs.

```bash
#!/usr/bin/bash
group="logs-readers"
files_path=("/var/log/syslog" "/var/log/auth.log" "/var/log/kern.log")

for path in "${files_path[@]}"; do
  sudo setfacl -m g:$group:r $path
  echo "Set read permission for group '$group' on file '$path'"
done
```

## Switch the server to production

To prepare production assets you can swap the compose and Dockerfile variants (example approach used in this project):

```bash
mv compose.yaml compose.dev.yaml
mv compose.prod.yaml compose.yaml
mv Dockerfile Dockerfile.dev
mv Dockerfile.prod Dockerfile
```

> ## Warning !
> **In production**, use a securely **generated random** `SECRET_KEY`.
> Update the `.env` file you created earlier with this random key.
> [Voir aide](#configuration-before-starting-containers)

```bash
docker compose up --build
```

*(Remove test users created by the database seeding before running in production.)*<br>

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) (Production server)

*(If you run on a remote machine, replace 127.0.0.1 with the host IP.)*
