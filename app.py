import streamlit as st
import pandas as pd
import os

FILE = "contacts.csv"

# Load data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["First Name", "Last Name", "Address", "Email", "Phone"])

st.title("📇 Contact Management App")

menu = st.sidebar.selectbox("Menu", ["Add", "View", "Update", "Delete"])

# ---------------- ADD ----------------
if menu == "Add":
    st.subheader("Add Contact")

    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    address = st.text_input("Address")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    if st.button("Save"):
        if first and email and phone:
            new_data = pd.DataFrame([[first, last, address, email, phone]],
                                    columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(FILE, index=False)
            st.success("Contact Saved!")
        else:
            st.error("Please fill required fields")

# ---------------- VIEW ----------------
elif menu == "View":
    st.subheader("All Contacts")
    st.dataframe(df)

# ---------------- UPDATE ----------------
elif menu == "Update":
    st.subheader("Update Contact")

    emails = df["Email"].tolist()
    selected = st.selectbox("Select Email", emails)

    if selected:
        row = df[df["Email"] == selected].index[0]

        first = st.text_input("First Name", df.at[row, "First Name"])
        last = st.text_input("Last Name", df.at[row, "Last Name"])
        address = st.text_input("Address", df.at[row, "Address"])
        phone = st.text_input("Phone", df.at[row, "Phone"])

        if st.button("Update"):

             index = df[df["First Name"] == name].index.tolist()
             row = index[0]

             if len(index) > 0:
                df.loc[index[0], "Address"] = address
                df.loc[index[0], "Phone"] = phone

                df.to_csv("contacts.csv", index=False)
                st.success("Contact updated successfully!")
             else:
                st.error("Contact not found")
            
# ---------------- DELETE ----------------
elif menu == "Delete":
    st.subheader("Delete Contact")

    emails = df["Email"].tolist()
    selected = st.selectbox("Select Email", emails)

    if st.button("Delete"):
        df = df[df["Email"] != selected]
        df.to_csv(FILE, index=False)
        st.success("Deleted!")
