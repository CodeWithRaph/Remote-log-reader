from flask import request
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, SmallInteger, Integer
from sqlalchemy import desc
from app import db


class Privilege(db.Model):
    """ORM model for 'privileges' table"""
    __tablename__ = 'privileges'
    
    id: Mapped[SmallInteger] = mapped_column(SmallInteger, primary_key=True, autoincrement=False, unique=True)
    p_name: Mapped[str] = mapped_column(String(50), nullable=False)

    



class Role(db.Model):
    """ORM model for 'roles' table"""
    __tablename__ = 'roles'
    
    id: Mapped[SmallInteger] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    r_name: Mapped[str] = mapped_column(String(50), nullable=False)
    privileges: Mapped[SmallInteger] = mapped_column(SmallInteger, nullable=False, unique=True)





class User(db.Model):
    """ORM model for 'users' table"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    passwd: Mapped[str] = mapped_column(String(255), nullable=False)
    rights: Mapped[int] = mapped_column(Integer, nullable=False)
    
    @staticmethod
    def add_user(username, passwd, passwd2, rights):
        """Add a new user in the right table of the db"""

        from app.utils import string_hash

        username = username.strip()
        if passwd == passwd2:
            passwd = string_hash(passwd)

            test_username = User.query.filter_by(username=username).first()

            if username != "" and test_username == None:
                u = User(username=username, passwd=passwd, rights=rights)
                db.session.add(u)
                db.session.commit()
                return (True, "")
            else:
                return (False, "Le nom d'utilisateur est déjà utilisé ou invalide.")
        else:
            return (False, "Les mots de passe ne correspondent pas.")

    @staticmethod
    def remove_user(id):
        """Remove the concerned user from the right table of the db"""
        u = User.query.get(id)
        
        if u != None:
            db.session.delete(u)
            db.session.commit()
            return True
        return False

    @staticmethod
    def edit_user(id, username, rights):
        """Update the concerned user in the right table of the db"""
        u = User.query.get(id)

        if u != None:
            username = username.strip()
            
            if username != "":
                test_username = User.query.filter_by(username=username).first()
                # check if username is unchanged or unique
                if username == u.username or test_username == None:
                    u.username = username
                    u.rights = rights
                    db.session.commit()
                    return (True, "")
                else:
                    return (False, "Le nom d'utilisateur est déjà utilisé.")
            else:
                return (False, "Le nom d'utilisateur est invalide.")
        else:
            return (False, "L'utilisateur demandé n'existe pas.")





class Machine(db.Model):
    """ORM model for 'machines' table"""
    __tablename__ = 'machines'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hostname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    ip: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)

    @staticmethod
    def add_machine(host, ip):
        """Add a new machine in the right table of the db"""

        from app.utils import ip_valide

        host = host.strip()
        test_host = Machine.query.filter_by(hostname=host).first()
        if host != "" and test_host == None:
            if ip_valide(ip):
                test_ip = Machine.query.filter_by(ip=ip).first()
                if test_ip == None:
                    m = Machine(hostname=host, ip=ip)
                    db.session.add(m)
                    db.session.commit()
                    return (True, "")
                else:
                    return (False, "L'adresse IP est déjà utilisée.")
            else:
                return (False, "L'adresse IP n'est pas valide.")
        else:
            return (False, "Le nom d'hôte est déjà utilisé ou invalide.")

    @staticmethod
    def remove_machine(id):
        """Remove the concerned machine from the right table of the db"""
        m = Machine.query.get(id)
        
        if m != None:
            db.session.delete(m)
            db.session.commit()
            return True
        return False

    @staticmethod
    def edit_machine(id, host, ip):
        """Update the concerned machine in the right table of the db"""

        from app.utils import ip_valide

        m = Machine.query.get(id)

        if m != None:
            host = host.strip()
                
            if host != "" and ip != "":
                test_host = Machine.query.filter_by(hostname=host).first()
                # check if hostname is unchanged or unique
                if host == m.hostname or test_host == None:
                    if ip_valide(ip):
                        test_ip = Machine.query.filter_by(ip=ip).first()
                        # check if ip is unchanged or unique
                        if ip == m.ip or test_ip == None:
                            m.hostname = host
                            m.ip = ip
                            db.session.commit()
                            return (True, "")
                        else:
                            return (False, "L'adresse IP est déjà utilisée.")
                    else:
                        return (False, "L'adresse IP n'est pas valide.")
                else:
                    return (False, "Le nom d'hôte est déjà utilisé.")
            else:
                return (False, "Le nom d'hôte ou l'adresse IP est invalide.")
        return (False, "La machine demandée n'existe pas.")





class Log(db.Model):
    """ORM model for 'logs' table"""
    __tablename__ = 'logs'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    @staticmethod
    def add_log(path):
        """Add a new log file in the in the right table of the db"""
        path = path.strip()
        if path == "":
            return False

        test = Log.query.filter_by(file_path=path).first()
        if test is None:
            l = Log(file_path=path)
            db.session.add(l)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_log(path):
        """Deletes a log file"""
        if not path:
            return False
        l = Log.query.filter_by(file_path=path).first()
        if l is not None:
            db.session.delete(l)
            db.session.commit()
            return True
        return False