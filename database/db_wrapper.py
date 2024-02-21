from pymongo import MongoClient
import objects
import logging
from config import CONNECTION_STRING


class Database:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Database init")
        self.db = MongoClient(CONNECTION_STRING)
        self.db = self.db["LoveandCareDB"]

    def get_user_language(self, user_id):
        user = self.db["user"].find_one({"id": user_id})
        if user:
            return user["lang"]
        else:
            self.db["user"].insert_one(vars(objects.User(user_id)))
            return "en"

    def set_user_language(self, user_id, lang):
        self.db["user"].update_one({"id": user_id}, {"$set": {"lang": lang}})

    def get_user(self, user_id):
        user = self.db["user"].find_one({"id": user_id})
        if not user:
            return False
        return user

    def create_adopter(self, adopter: objects.Adopter):
        new_parent = self.db["adopter"].insert_one(
            vars(adopter))
        return new_parent

    def get_adopter(self, user_id):
        adopter = self.db["adopter"].find_one({"id": user_id})
        if not adopter:
            return False
        return adopter

    def create_volunteer(self, volunteer: objects.Volunteer):
        new_blood = self.db["volunteer"].insert_one(
            vars(volunteer))
        return new_blood

    def get_volunteer(self, user_id: int, name: str, phone: str):
        volunteer = self.db["volunteer"].find_one({"id": user_id})
        if not volunteer:
            return False
        return volunteer
    def get_all_volunteer(self):
        volunteers = self.db["volunteer"].find() 
        return volunteers 


database = Database()
