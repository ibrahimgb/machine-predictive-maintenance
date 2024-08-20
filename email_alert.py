import streamlit as st
import json
import os

# Path to the JSON file
contact_file = 'contact.json'

# Initial data to be saved if the file doesn't exist
initial_data = {
    "Maintainers": [],
    "Administration": [],
    "Management": []
}

# Load existing data from contact.json if it exists, otherwise create it
def load_contacts():
    if os.path.exists(contact_file):
        with open(contact_file, 'r') as json_file:
            contacts = json.load(json_file)
            # Convert existing string entries to dictionaries if needed
            if isinstance(contacts.get("Maintainers", []), list):
                updated_maintainers = []
                for item in contacts["Maintainers"]:
                    if isinstance(item, str):  # Old format (just an email string)
                        updated_maintainers.append({"name": "", "phone": "", "email": item})
                    elif isinstance(item, dict):  # New format (dict with name, phone, email)
                        updated_maintainers.append(item)
                contacts["Maintainers"] = updated_maintainers
            return contacts
    else:
        # Save initial data to file if it doesn't exist
        save_contacts(initial_data)
        return initial_data

# Save data to contact.json
def save_contacts(contacts):
    with open(contact_file, 'w') as json_file:
        json.dump(contacts, json_file, indent=4)

# Initialize contacts dictionary
contacts = load_contacts()

# Title of the app
st.title("Email Address Categorization")

# Function to add a maintainer to the category
def add_maintainer(name, phone, email):
    email = email.strip()
    name = name.strip()
    phone = phone.strip()
    if email and not any(contact['email'] == email for contact in contacts["Maintainers"]):
        contacts["Maintainers"].append({"name": name, "phone": phone, "email": email})
        save_contacts(contacts)

# Function to remove a maintainer from the category
def remove_maintainer(email):
    email = email.strip()
    contacts["Maintainers"] = [contact for contact in contacts["Maintainers"] if contact['email'] != email]
    save_contacts(contacts)

# Input and buttons for Maintainers
st.header("Maintainers")

# Create columns for name, phone, and email input
col1, col2, col3 = st.columns(3)
with col1:
    maintainer_name = st.text_input("Enter maintainer's name:")
with col2:
    maintainer_phone = st.text_input("Enter maintainer's phone number:")
with col3:
    maintainer_email = st.text_input("Enter maintainer's email address:")

if st.button("Add to Maintainers"):
    add_maintainer(maintainer_name, maintainer_phone, maintainer_email)
    st.success(f"Added: {maintainer_name} ({maintainer_email})")
    st.experimental_rerun()  # Clear input after adding

# Dropdown and button to remove a maintainer
maintainer_to_remove = st.selectbox("Select a maintainer to remove:", 
                                    [f"{contact['name']} ({contact['email']})" for contact in contacts["Maintainers"] if isinstance(contact, dict)])
if st.button("Remove from Maintainers"):
    email_to_remove = maintainer_to_remove.split('(')[-1][:-1]  # Extract email from selection
    remove_maintainer(email_to_remove)
    st.success(f"Removed: {maintainer_to_remove}")
    st.experimental_rerun()

# Display the current maintainers
st.write(f"**Current Maintainers ({len(contacts['Maintainers'])}):**")
for contact in contacts["Maintainers"]:
    if isinstance(contact, dict):
        st.markdown(f"- **Name**: {contact['name']} | **Phone**: {contact['phone']} | **Email**: {contact['email']}")
