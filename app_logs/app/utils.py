from werkzeug.datastructures import ImmutableMultiDict
import hashlib, hmac

def ip_valide(ip):
    """Says if a string is an ip address or not"""
    ip = ip.split(".")
    if len(ip) == 4:
        for byte in ip:
            byte = int(byte)
            if not(byte >= 0 and byte <= 255):
                return False
    else:
        return False
    return True

def get_rights(role):
    """Gives rights that are linked with a role name"""
    # local import to avoid circular import issues
    from app.models.applogs import Role

    r = Role.query.filter_by(r_name=role).first()
    
    if r != None:
        return r.privileges
    return None

def get_role(rights):
    """Gives role linked with a 'rights' code"""
    # local import to avoid circular import issues
    from app.models.applogs import Role

    r = Role.query.filter_by(privileges=rights).first()
    if r != None:
        return r.r_name
    return None

def get_privileges(table_role):
    """
    Gives a list of tuples that contains
    role table data and associated privileges.
    """
    # local imports to avoid circular import issues
    from app.models.applogs import Privilege
    from sqlalchemy import desc

    tuple_list = []
    privileges = Privilege.query.order_by(desc(Privilege.id)).all()
    for row in table_role:
        privilege_list = []
        rights = row.privileges
        while rights > 0:
            for privilege in privileges:
                if rights - privilege.id >= 0:
                    rights -= privilege.id
                    privilege_list.append(privilege.p_name)
        tuple_list.append((row, privilege_list))
    return tuple_list

def string_hash(string):
    """Gives the hash fingerprint for a string input"""
    hash_elem = hashlib.sha256(string.encode('utf-8'))
    return hash_elem.hexdigest()

def registered(username, passwd):
    """Says True if the user exist and the password match with the db"""
    # local import to avoid circular import issues
    from app.models.applogs import User

    user = User.query.filter_by(username=username).first()
    passwd = string_hash(passwd)
    if user != None:
        if hmac.compare_digest(user.passwd, passwd):
            return (True, "")
    return (False, "Login ou mot de passe incorrect.")