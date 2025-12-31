drop DATABASE IF EXISTS applogs;

CREATE DATABASE IF NOT EXISTS applogs DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE applogs;

CREATE TABLE IF NOT EXISTS privileges(
       id TINYINT NOT NULL,
       p_name VARCHAR(50) NOT NULL,
       PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO privileges (id, p_name) VALUES
       (1, 'Consultation de journaux.'),
       (2, 'Gestion de serveurs.'),
       (4, 'Gestion des utilisateurs.');

CREATE TABLE IF NOT EXISTS roles(
       id TINYINT NOT NULL AUTO_INCREMENT,
       r_name VARCHAR(50) NOT NULL,
       privileges TINYINT NOT NULL,
       PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO roles (r_name, privileges) VALUES
       ('Utilisateur', 1),
       ('Gestionnaire', 3),
       ('Administrateur', 7);

CREATE TABLE IF NOT EXISTS machines(
       id INT NOT NULL AUTO_INCREMENT,
       hostname VARCHAR(50) NOT NULL UNIQUE,
       ip VARCHAR(15) NOT NULL UNIQUE,
       PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO machines (hostname, ip) VALUES
       ('srv1', '94.56.133.12'),
       ('srv2', '94.56.133.15'),
       ('srv3', '94.56.132.110'),
       ('srv4', '94.56.132.124'),
       ('srv5', '94.56.134.2');

CREATE TABLE IF NOT EXISTS users(
       id INT NOT NULL AUTO_INCREMENT,
       username VARCHAR(50) NOT NULL,
       passwd VARCHAR(255) NOT NULL,
       rights INT NOT NULL,
       PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO users (username, passwd, rights) VALUES
       ('admin', SHA2('admin', 256), 7),
       ('manager', SHA2('manager', 256), 3),
       ('user', SHA2('user', 256), 1);

CREATE TABLE IF NOT EXISTS logs (
       id INT NOT NULL AUTO_INCREMENT,
       file_path VARCHAR(255) NOT NULL UNIQUE,
       PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO logs (file_path) VALUES
    ('/var/log/syslog');