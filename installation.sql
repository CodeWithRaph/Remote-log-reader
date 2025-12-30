drop database if exists applogs;

create database if not exists applogs DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

use applogs

create table if not exists privileges(
       id TinyInt not null unique,
       p_name varchar(50) not null,
       primary key (id)
) engine=InnoDB default charset=utf8; 

insert into privileges values
       (1, "Consultation de journaux."),
       (2, "Gestion de serveurs."),
       (4, "Gestion des utilisateurs.");
       
create table if not exists roles(
       id TinyInt not null auto_increment,
       r_name varchar(50) not null,
       privileges TinyInt not null unique,
       primary key (id)
) engine=InnoDB default charset=utf8; 

insert into roles (r_name, privileges) values
       ("Utilisateur", 1),
       ("Gestionnaire", 3),
       ("Administrateur", 7);

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
       ("user", SHA2("user", 256), 1);

create table if not exists logs (
       id Int not null auto_increment,
       file_path varchar(255) not null unique,
       primary key (id)
) engine=InnoDB default charset=utf8;

insert into logs (file_path) values
    ('/var/log/syslog');