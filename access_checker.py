from future.moves import configparser

def check_user_access(user_id):
    config = configparser.ConfigParser()
    config.read('config.ini')
    admin_id = config.get("USER", "ids")
    admin_id = admin_id.strip('"[]')
    admin_id_list = list(map(int, admin_id.split(',')))
    if user_id in admin_id_list:
        return True
    else:
        return False