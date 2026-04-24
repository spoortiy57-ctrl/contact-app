import streamlit as st
import pandas as pd
import os

FILE = "contacts.csv"

st.title("Contact Management System")

# Create CSV if not exists
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["First Name","Last Name","Address","Email","Phone"])
    df.to_csv(FILE, index=False)

# Load contacts
df = pd.read_csv(FILE)

# ---------------- VIEW CONTACTS ----------------
st.header("View Contacts")
st.dataframe(df)

# ---------------- ADD CONTACT ----------------
st.header("Add Contact")

first = st.text_input("First Name")
last = st.text_input("Last Name")
address = st.text_input("Address")
email = st.text_input("Email")
phone = st.text_input("Phone")

if st.button("Add Contact"):
    new_contact = {
        "First Name": first,
        "Last Name": last,
        "Address": address,
        "Email": email,
        "Phone": phone
    }

    df = pd.concat([df, pd.DataFrame([new_contact])], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("Contact added successfully")

# ---------------- UPDATE CONTACT ----------------
st.header("Update Contact")

update_name = st.text_input("Enter First Name to Update")
new_address = st.text_input("New Address")
new_phone = st.text_input("New Phone")

if st.button("Update Contact"):

    rows = df[df["First Name"] == update_name]

    if len(rows) > 0:

        index = rows.index[0]

        if new_address != "":
            df.loc[index, "Address"] = new_address

        if new_phone != "":
            df.loc[index, "Phone"] = new_phone

        df.to_csv(FILE, index=False)

        st.success("Contact updated")

    else:
        st.error("Contact not found")

# ---------------- DELETE CONTACT ----------------
st.header("Delete Contact")

delete_name = st.text_input("Enter First Name to Delete")

if st.button("Delete Contact"):

    rows = df[df["First Name"] == delete_name]

    if len(rows) > 0:

        df = df[df["First Name"] != delete_name]
        df.to_csv(FILE, index=False)

        st.success("Contact deleted")

    else:
        st.error("Contact not found")