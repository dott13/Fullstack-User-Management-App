import React from "react";

const ContactList = ({ contacts, updateContact, updateCallback }) => {
  const onDelete = async (email) => {
    try {
      const options = {
        method: "DELETE",
      };
      const response = await fetch(
        `http://127.0.0.1:5000/delete_contact/${email}`,
        options
      );
      if (response.status === 200) {
        updateCallback();
      } else {
        console.error("Failed to delete contact");
      }
    } catch (error) {
      alert(error);
    }
  };

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
};

export default ContactList;
