import json
import pyrebase


class DBhandler:
    def __init__(self):
        with open("./authentication/firebase_auth.json") as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # ---------- products ----------
    def insert_item(self, name, data, img_path):
        item_info = {
            "seller": data["seller_id"],
            "price": data["price"],
            "addr": data["address"],
            "status": data["status"],
            "email": data["email"],
            "img_path": img_path,
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True

    # ---------- users ----------
    def insert_user(self, data, pw):
        user_info = {
            "id": data["id"],
            "pw": pw,
            "nickname": data["nickname"],
        }
        if self.user_duplicate_check(str(data["id"])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        if str(users.val()) == "None":   # no users yet
            return True
        for res in users.each():
            value = res.val()
            if value["id"] == id_string:
                return False             # ID already taken
        return True

    def find_user(self, id_string, pw_hash):
        users = self.db.child("user").get()
        if str(users.val()) == "None":
            return None
        for res in users.each():
            value = res.val()
            if value["id"] == id_string and value["pw"] == pw_hash:
                return value
        return None