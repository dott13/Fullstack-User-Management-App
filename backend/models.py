from config import mongo

class Contact():
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_json(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }
    
    def save(self):
        contacts = mongo.db.contacts
        
        contacts.insert_one({
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email
        })
    
    @staticmethod
    def find_all():
        contacts = mongo.db.contacts
        return list(contacts.find())
        

    