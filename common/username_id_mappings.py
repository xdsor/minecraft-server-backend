user_id_name_mapping = {}
# For my little cosy server I decided to fill it manually
user_name_id_mapping = {
    "Andatra120": "87b57afb-1e42-46ad-8ad8-1ba55a6a44df",
    "DeletiV": "f751b491-352e-4142-892d-6ceb0cbfb97b",
    "corvore": "5e797d22-2e0b-4b43-af2d-f8f37334f840",
    "xdsor": "4519e23c-5d5c-4c0a-b2f4-fa7e1bca7f1e"
}

if len(user_id_name_mapping.items()) == 0:
    user_id_name_mapping = {value: key for key, value in user_name_id_mapping.items()}