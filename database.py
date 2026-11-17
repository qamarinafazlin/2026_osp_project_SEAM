import json
import pyrebase


class DBhandler:
    def __init__(self):
        with open("./authentication/firebase_auth.json") as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # ————— products —————
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

    # ————— get items —————
    def get_items(self):
        items = self.db.child("item").get()
        products = []

        if items.val() is None:
            return products

        for item in items.each():
            name = item.key()
            data = item.val()

            if not isinstance(data, dict):
                continue

            products.append({
                "id": name,
                "name": name,
                "country": data.get("country", "Unknown"),
                "status": data.get("status", "On sale"),
                "price": int(data.get("price", 0)),
                "seller": data.get("seller", ""),
                "pickup": data.get("addr", ""),
                "email": data.get("email", ""),
                "image_url": (
                    "/static/images/" + data["img_path"]
                    if data.get("img_path") else ""
                )
            })

        return products

    def get_item_byname(self, name):
        return self.db.child("item").child(name).get().val()


    # ————— likes —————
    # stored as  heart / <user_id> / <product_name> : {"liked": true/false}
    def get_heart(self, user_id, name):
        heart = self.db.child("heart").child(user_id).child(name).get().val()
        if heart is None:
            return False
        return heart.get("liked", False)

    def set_heart(self, user_id, name, liked):
        self.db.child("heart").child(user_id).child(name).set({"liked": bool(liked)})
        return bool(liked)
    
    # ————— reviews —————
    def insert_review(self, data, img_path, author):
        review_info = {
            "title": data["title"],
            "product_name": data["product_name"],
            "body": data["body"],
            "rating": data["rating"],
            "img_path": img_path,
            "author": author,
        }
        self.db.child("review").push(review_info)
        print(review_info)
        return True

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        if reviews is None:
            return {}
        return reviews

    def get_review_by_id(self, review_id):
        return self.db.child("review").child(review_id).get().val()

    # ————— users —————
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