from config import mongo

class Contact:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def save(self):
        contact = mongo.db.contacts

        if contact.find_one({'email': self.email}):
            raise ValueError('Email already exists')
        
        contact.insert_one({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        })

    @staticmethod
    def find_all():
        contacts = mongo.db.contact
        return list(contacts.find())
    