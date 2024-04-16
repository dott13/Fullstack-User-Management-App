# Fullstack User Management Web Application

## Introduction

In this project I developed a simple <b>Full-Stack CRUD application</b> using such technologies as for frontend I used the Python library <i>Flask</i> with database in MongoDB, for frontend I used React with the Vite template.

This application was solely made to learn Full-Stack development, because in the past I was a Back-end developer, right now I am focused on expanding my professional skills as a <b>Full-Stack Software Engineer</b>. As a second grade quest I wanted to learn how to work with a NoSQL database such as <i>MongoDB</i>.

## Backend

For backend I created a Flask application using the easy aproach to just `pip install flask`. First I created the main parts of a Flask app: [config.py](/backend/config.py), [main.py](/backend/main.py) and [models.py](/backend/models.py). Later in the project I understood that with a <b>NoSQL</b> aproach to my database I dont need the <i>models.py</i> file as that <b>MongoDB</b> is working with directories and documents that are jsonified, so we don't need for actual models.

### Database

To implement our database without creating ourselfes any documents or schemas in python there are a lot of libraries that do it for you when you interact with your backend. Such libraries are: `MongoDB-Alchemy, PyMongo, MongoEngine`. These libraries are very alike, so I just went with the easiest approach and chose <i>PyMongo</i>, implementing in my config files like that:

```python
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/UserDb"

mongo = PyMongo(app)
```

After that in our <i>main</i> directory we can just import the `mongo` variable from <i>config</i> and work with it to create the directories and documents needed for our database to work.

### Implementation

As our database definition is ready we can now create our first API routes. First I made the <i>Read</i> part of our <i>CRUD</i> in the `main.py` file. In flask to create an API to a route we use something called a <b>Decorator</b> in which we say that our app will get the route on the following http request, with the following method, like this:

```python
@app.route("/contacts", methods = ["GET"])
```

As we can see we create the route to <i>"/contacts"</i> and the method of use being <b>GET</b>. After that we just want to get the list of contacts that we have in our database. Basically we call our database on the variable that we imported and search through the directory that we want it to search in, the directory being <b>contacts</b>. We use the method that is already in <i>PyMongo</i> by default, called `find()`and then we just return it with jsonify to make it into a json file and return a 200 code, which stands for successful.

```python
def get_contacts():
    try:
        contacts = list(mongo.db.contacts.find({}, {"_id": 0}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"contacts" : contacts}), 200
```

We do the same thing for all other routes, byt we just change the route on which every call stays and the methods we use. In the <b>UPDATE</b> and <b>DELETE</B> we also use variables in the route to check what contact we delete or update by users <i>email</i>. Adding this variable to the method we use. Very basic stuff!

```python
@app.route("/update_contact/<email>", methods=["PATCH"])
def update_contact(email):
    contact = mongo.db.contacts.find_one({'email': email})
```

This is basically all we need for a stable backend, we just run `python main.py` in our terminal and we are all set up.

### P.S

To test my API connection and all the routes I set up, I've used `Postman`. I didn't write any of my own tests becuase I didn't see it necessary in a small project like this.

## Frontend

As we want to create a web application to do so I've used the most popular JavaScript Library there is on the Internet <b>React</b>. I've used it because it is the most demanding right now on the Frontend part of the job search and also because I want to learn more about <i>Frontend Software Engineering</i> in general, and where can we start other than the most niche part of it!

### Setup

There are many ways of creating a <i>React Application</i>. The most popular and the worst one in my opinion is by using [React App](https://create-react-app.dev/). I consider it bad because it makes a lot of unnecessary additions to React projects. That's why I chose the one with the easiest and smallest layout the <b>Vite + React</b> approach. <i>Vite</i> is a JavaScript framework made for best design possible for your Web Application. So to create a <i>React</i> application with a <I>Vite</i> layout we need to first install `nodejs` and second to write in our terminal in the frontend directory the following line:

`npm create vite@latest frontend -- --template react`

Then our layout and the app is created, to verify it we write in the terminal `npm run dev` and we're done with the setup.

### Implementation

To implement our Frontend and for it to interact with the Backend we first fetch the data from our API endpoints in our [App.jsx](/frontend/src/App.jsx).

```JSX
  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    const response = await fetch("http://127.0.0.1:5000/contacts");
    const data = await response.json();
    setContacts(data.contacts);
  };
```

Then we build an easy table to see all the information that we have in the database. This table design we make in a separate file that we named [ContactList.jsx](/frontend/src/ContactsList.jsx) and then import it in our `App.jsx`.

```JSX
return (
    <div>
      <h2>Contacts</h2>
      <table>
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map((contact) => (
            <tr key={contact.email}>
              <td>{contact.firstName}</td>
              <td>{contact.lastName}</td>
              <td>{contact.email}</td>
              <td>
                <button onClick={() => updateContact(contact)}>Update</button>
                <button onClick={() => onDelete(contact.email)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
```

As you can see we also have two buttons there that are made for updating and deleting the contacts, we do it by fetching our other API endpoints and getting the methods correctly.

To update or create a new <b>Contact</b> we will have a form for which I made the design and a new file: [ContactForm.jsx](/frontend/src/ContactForm.jsx). This form will be displayed to the user dynamically via a button that we made in `App.jsx`. It will get the API request from our backend for our respective PATCH and POST routes dynamically and after pressing the button will work with the result adding or changing data into the <i>database</i> and displaying it to the user.

```JSX
const url =
      "http://127.0.0.1:5000/" +
      (updating ? `update_contact/${existingContact.email}` : "create_contact");
    const options = {
      method: updating ? "PATCH" : "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    const response = await fetch(url, options);
```

And the final product is exported to our `App.jsx`, changed with some <i>css</i> to look accordingly and we are done.

```JSX
<button onClick={openCreateModal}>Create New Contact</button>
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>
              &times;
            </span>
            <ContactForm
              existingContact={currentContact}
              updateCallback={onUpdate}
            />
          </div>
        </div>
```

That is it for our <i>Frontend</i>, therefore for our <b>Web Application in general!</b>

## Conclusion

In conclusion I want to say that this <i>Project</i> was very easy and not demanding at all, but it helped me evaluate my <i>Frontend</i> skills and work for the first time in my life with MongoDB.

While connecting the endpoints from both places I understood that both parties have to be done correctly and with as least as hustle as possible. For a better understanding of the code and workflow a <i>FullStack Engineer</i> would be prefferable, as well as the leading a project. But from a maintenance perspective a Backend and another Frontend developer would be better.

In this project I learned the hardships of being <i>FullStack Developer</i> as well as the fun part of it.
