from flask import request, jsonify
from config import app, mongo
from bson import ObjectId
from models import Contact

@app.route("/contacts", methods = ["GET"])
def get_contacts():
    try:
        contacts = list(mongo.db.contacts.find({}, {"_id": 0}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"contacts" : contacts}), 200
    

@app.route("/create_contact", methods = ["POST"])
def create_contact():
    data = request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if not first_name or not last_name or not email:
        return jsonify({'error' : 'You need to specify First Name, Last Name and Email'}), 400
    
    existing_contact = mongo.db.contacts.find_one({'email': email})
    if existing_contact:
        return jsonify({'error' : 'Email already exists'}), 400
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        new_contact.save()
    except Exception as e:
        return jsonify({'error' : str(e)}), 400
    
    return jsonify({'message' : 'Contact added successfully'}), 201

@app.route("/update_contact/<email>", methods=["PATCH"])
def update_contact(email):
    contact = mongo.db.contacts.find_one({'email': email})
    data = request.json
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    if 'first_name' in data:
        contact['first_name'] = data['first_name']
    if 'last_name' in data:
        contact['last_name'] = data['last_name']
    if 'email' in data:
        if data['email'] != email:
            duplicate_contact = mongo.db.contacts.find_one({'email': data['email']})
            if duplicate_contact:
                return jsonify({'error': 'Email already exists'}), 400
        contact['email'] = data['email']
    try:
        mongo.db.contacts.update_one({'email': email}, {'$set': contact})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Contact updated successfully'}), 200

@app.route("/delete_contact/<email>", methods=["DELETE"])
def delete_contact(email):
    contact = mongo.db.contacts.find_one({'email': email})
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    try:
        mongo.db.contacts.delete_one({"email": email})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': 'Contact deleted successfully!'})


if __name__ == "__main__":
    app.run(debug=True)
