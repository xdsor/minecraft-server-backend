import requests

def get_user_name_by_id(user_id):
    return requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + user_id).json()['name']

def get_user_id_by_name(user_name):
    return requests.get("https://api.mojang.com/users/profiles/minecraft/" + user_name).json()['id']