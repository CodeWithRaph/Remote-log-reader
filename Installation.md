# Installation & Configuration

Ce projet utilise des conteneurs Docker.<br>
Un qui permet la mise en place de la DB. Et l'autre permet la mise en place de l'application Flask.

## Sommaire
- [Installation de l'application Flask et de la DB](#installation-de-lapplication-flask-et-de-la-db)
  - [Configuration avant lancement des conteneurs](#configuration-avant-lancement-des-conteneurs)
- [Installation d'une machine cliente](#installation-dune-machine-cliente)
  - [Autorisation de lecture des logs](#autorisation-de-lecture-des-logs)


## Installation de l'application Flask et de la DB

Cloner le repositorie GitHub
```bash
git clone https://github.com/CodeWithRaph/Remote-log-reader.git
cd Remote-log-reader
```

### Configuration avant lancement des conteneurs

1. Modifiez le contenu du fichier `.env.example` :

> ## Aide:
> ### Paramètres (obligatoire)
>- **DB_PASSWD:** Mot de passe de l'utilisateur DB.
>- **SECRET_KEY:** La clé qui permet l'encryption de l'application Flask côté serveur.
>- **SSH_USER:** L'utilisateur qui sera utilisé pour lire les logs sur les machines clientes.
>---
> ### Paramètres (Facultatifs)
>- DB_HOST: *Identifie la machine qui host le serveur MariaDb. Sauf si vous décidez de mettre le conteneur sur une autre machine il est inutile de changer cette variable.*
>- SSH_KEY_PATH : *préréglé sur le chemin relatif par défaut.*

2. Renommer le fichier `.env.example` par `.env`
```bash
cp .env.example .env
```

3. Lancer les conteneurs Docker
```bash
docker compose up -d
```

4. Now open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Installation d'une machine cliente

### Autorisation de lecture des logs

Il y a **2 options** possibles:
- Autoriser le groupe <log-readers> à lire tout les fichiers d'un répertoire (plus simple).
- Autoriser le groupe <log-readers> à lire une liste précise de fichiers (plus sécurisé).

---
#### 1ère option: Autoriser un répertoire entier

1. Création de l'utilisateur qui servira à établir la connexion SSH.
> ## Aide:
>`<user>`: Remplacer par l'utilisateur qui sera utilisé pour lire les logs sur la machine.<br>
>`<mdp>`: Mot de passe utilisateur.<br>
>`adm`: Groupe prédéfini sur Debian/Ubuntu qui possède les droits de lecture sur certains journaux système sensibles.

```bash
sudo useradd <user>
sudo passwd <mdp>
sudo groupadd adm
sudo usermod -aG adm <user>
```

2. Récupérer la clé RSA publique du serveur central (via scp) puis la glisser dans la liste de clé autorisées.
```bash
su <user>
sudo mkdir ~/.ssh
cat rsa_publique_serveur >> ~/.ssh/authorized_keys
```

---
#### 2ème option: Autoriser une liste précise de fichiers

1. Création de l'utilisateur qui servira à établir la connexion SSH.
> ## Aide:
>`<user>`: Remplacer par l'utilisateur qui sera utilisé pour lire les logs sur la machine.<br>
>`<mdp>`: Mot de passe utilisateur.<br>
>`<logs-readers>`: Remplacer par le nom du groupe qui aura les droits de lecture.

```bash
sudo useradd <user>
sudo passwd <mdp>
sudo groupadd <logs-readers>
sudo usermod -aG <logs-readers> <user>
```

2. Récupérer la clé RSA publique du serveur central (via scp) puis la glisser dans la liste de clé autorisées.
```bash
su <user>
sudo mkdir ~/.ssh

```bash
sudo apt install acl
```

Pour cette méthode il faudra mettre à jour manuellement le script pour changer la liste de fichiers.<br>
Dans ce contexte on ne fait pas entièrement confiance aux supposées autorisations de lecture de fichiers, données dans l'application Flask.

> ## Aide:
>`<logs-readers>`: Remplacer par le nom du groupe qui aura les droits de lecture.

```bash
#!/usr/bin/bash
group="logs-readers"
files_path=("/var/log/syslog" "/var/log/auth.log" "/var/log/kern.log")

for path in "${files_path[@]}"; do
  sudo setfacl -m g:$group:r $path
  echo "Set read permission for group '$group' on file '$path'"
done
```
