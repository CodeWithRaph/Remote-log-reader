# Installation

## Installation et mise en place de la BDD

### Créer le fichier "installation.sql"

```sql 
create database if not exists applogs DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

use applogs

create table if not exists privileges(
       id TinyInt not null unique,
       p_name varchar(50) not null,
       primary key (id)
) engine=InnoDB default charset=utf8; 

insert into privileges values
       (1, "Viewing logs"),
       (2, "Servers management"),
       (4, "Users management");
       
create table if not exists roles(
       id TinyInt not null auto_increment,
       r_name varchar(50) not null,
       privileges TinyInt not null unique,
       primary key (id)
) engine=InnoDB default charset=utf8; 

insert into roles (r_name, privileges) values
       ("User", 1),
       ("Manager", 3),
       ("Administrator", 7);

create table if not exists machines(
       id Int not null auto_increment,
       hostname varchar(50) not null unique,
       ip varchar(15) not null unique,
       primary key (id)
) engine=InnoDB default charset=utf8; 

insert into machines (hostname, ip) values
       ("srv1", "94.56.133.12"),
       ("srv2", "94.56.133.15"),
       ("srv3", "94.56.132.110"),
       ("srv4", "94.56.132.124"),
       ("srv5", "94.56.134.2");

create table if not exists users(
       id Int not null auto_increment,
       username varchar(50) not null,
       passwd varchar(255) not null,
       rights Int not null,
       primary key (id)
) engine=InnoDB default charset=utf8;

insert into users (username, passwd, rights) values
       ("admin", SHA2("admin", 256), 7),
       ("manager", SHA2("manager", 256), 3),
       ("user", SHA2("user", 256), 3);

create table if not exists logs (
       id Int not null auto_increment,
       file_path varchar(255) not null unique,
       primary key (id)
) engine=InnoDB default charset=utf8;

insert into logs (file_path) values
    ('/var/log/syslog');
```

### Installation du paquet et éxécution du script

```bash
    sudo apt install mariadb-server
    mysql -u <username> -p
```

Puis l'éxécuter avec :

```sql
       source installation.sql;
```


## Installation des dépendances de l'application

Il faut d'abord créer l'environnement python

```bash
    pip install Flask
    pip install -U Flask-SQLAlchemy
    pip install mariadb
    pip3 install fabric
```

## Setup d'une machine cliente

```bash
       sudo useradd <user>
       sudo passwd <mdp>
       sudo groupadd <logs-readers>
       sudo usermod -aG <logs-readers> user

       sudo apt install acl
       sudo setfacl -m g:<logs-readers>:r /chemin/vers/le/fichier.log
```

- Récupérer la clé RSA publique du serveur central
```bash
       sudo mkdir ~/.ssh
       cat rsa_public_serveur >> ~/.ssh/authorized_keys
```

## Setup du serveur

définir les paramètres dans le script python
```python
       # path of the rsa key on the central server
       private_key_path = os.path.expanduser("~/.ssh/id_rsa")
       # user used on remotes machines
       username = "qamu" 
```