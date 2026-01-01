from fabric import Connection
import subprocess
import paramiko
import os
import getpass

# path of the rsa key on the central server
private_key_path = "/root/.ssh/id_rsa"
# user used on remotes machines
username = os.environ.get("SSH_USER")

def findLogs(hosts, logs):
    """
    Display sorted logs from a log file list for each remote machine in the hosts list.
    Returns a single concatenated content that contains the logs for each machine.
    """

    if len(hosts) == 0 and len(logs) == 0:
        return "", "Erreur: les listes des hôtes et des fichiers journaux sont vides."
    elif len(hosts) == 0:
        return "", "Erreur: la liste des hôtes est vide."
    elif len(logs) == 0:
        return "", "Erreur: la liste des fichiers journaux est vide."

    all_logs = []
    errors = []
    for host in hosts:
        try:
            c = Connection(
                host=host,
                user=username,
                port=22,
                connect_kwargs={
                    "key_filename": private_key_path
                }
            )
        except Exception as e:
            errors.append(f"Erreur [{host}]: connexion SSH échouée: {e}")
            continue

        files = ""
        for path in logs:
            files += f"{path} "

        try:
            result = c.run(f"cat {files} | sort -k1 -r", hide=True, warn=True)
        except Exception as e:
            errors.append(f"Erreur [{host}]: erreur lors de l'exécution distante: {e}")
            continue

    
        for line in result.stdout.splitlines():
            if line.strip():
                all_logs.append(line)

        for line in result.stderr.splitlines():
            if line.strip():
                errors.append(f"Erreur [{host}]: {line}")

    concatenated_logs = "\n".join(all_logs)

    concatenated_errors = "\n".join(errors)

    return concatenated_logs , concatenated_errors

def sort(concatenated_logs, concatenated_errors):
    """
    Sort a log concatenated_content on the local server.
    Returns the sorted content.
    """

    proc = subprocess.run(["sort", "-k1", "-r"], input=concatenated_logs, text=True, capture_output=True)
    return proc.stdout, concatenated_errors

def read(hosts, logs):
    arg1 , arg2 = findLogs(hosts, logs)
    return sort(arg1, arg2)

def main():
    hosts = ["192.168.122.103", "192.168.122.101"]
    logs = ["/var/log/cron.log", "/var/log/syslog"]
    
    print(read(hosts, logs))

if __name__ == '__main__':
    main()