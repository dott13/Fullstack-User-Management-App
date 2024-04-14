from flask import request, jsonify
from config import app, mongo
from models import Contact

@app.route("/contacts", methods = ["GET"])
def get_contacts():
    contacts = Contact.find_all()
    return jsonify(contacts), 200

if __name__ == "__main__":
    app.run(debug=True)
