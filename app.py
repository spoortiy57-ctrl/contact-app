import streamlit as st
import pandas as pd
import os
import re

def create_key(first, last, phone):
    return f"{first.strip().lower()}_{last.strip().lower()}_{phone.strip()}"

FILE = "contacts.csv"

st.set_page_config(page_title="Contact Management System", layout="wide")
st.title("Contact Management System")

# Create CSV if missing
if not os.path.exists(FILE):
      df = pd.DataFrame(columns=["First Name","Last Name","Address","Email","Phone"])
      df.to_csv(FILE, index=False)

df = pd.read_csv(FILE)
df["Phone"] = df["Phone"].astype(str)

# validation
def valid_email(email):
      pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
      return re.match(pattern, email)

def valid_phone(phone):
      return phone.isdigit() and len(phone) == 10
      

menu = st.sidebar.selectbox(
      "Choose Action",
      ["View Contacts","Add Contact","Update Contact","Delete Contact"]
)

# VIEW
if menu == "View Contacts":

      st.subheader("All Contacts")

      if df.empty:
            st.info("No contacts found")
      else:
            st.dataframe(df)

# ADD
elif menu == "Add Contact":

      st.subheader("Add Contact")

      first = st.text_input("First Name")
      last = st.text_input("Last Name")
      address = st.text_input("Address")
      email = st.text_input("Email (example@domain.com)")
      phone = st.text_input("Phone (10 digits)")

      if st.button("Add Contact"):
            
            df = pd.read_csv(FILE)
            df["Phone"] = df["Phone"].astype(str)
            
            first = first.strip()
            last = last.strip()
            phone = phone.strip()
            email = email.strip()

            if not first:
              st.error("First name required")

            elif not valid_email(email):
              st.error("Enter valid email (example@domain.com)")

            elif not valid_phone(phone):
              st.error("Phone must be 10 digits")

            else:
                # Create key for new entry
                new_key = create_key(first, last, phone)

                # Create keys for existing data
                df["key"] = df.apply(
                    lambda x: create_key(x["First Name"], x["Last Name"], str(x["Phone"])),
                    axis=1
                )

                if new_key in df["key"].values:
                    st.error("Contact already exists")
            
                else:

                    new_row = {
                        "First Name": first,
                        "Last Name": last,
                        "Address": address,
                        "Email": email,
                        "Phone": phone
                    }

                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_csv(FILE, index=False)

                    st.success("Contact added successfully")

# UPDATE
elif menu == "Update Contact":

      st.subheader("Update Contact")

      if df.empty:
            st.info("No contacts available")

      else:

            selected = st.selectbox(
                  "Select Contact",
                  df["First Name"] + " " + df["Last Name"]
            )

            index = df[(df["First Name"] + " " + df["Last Name"]) == selected].index[0]   

            new_address = st.text_input("New Address", df.loc[index,"Address"])
            new_phone = st.text_input("New Phone", str(df.loc[index,"Phone"]))

            if st.button("Update Contact"):

                  if not valid_phone(new_phone):
                        st.error("Phone must be 10 digits")

                  else:
                        df.loc[index,"Address"] = new_address
                        df.loc[index,"Phone"] = new_phone

                        df.to_csv(FILE, index=False)

                        st.success("Contact updated")

# DELETE
elif menu == "Delete Contact":

      st.subheader("Delete Contact")

      if df.empty:
            st.info("No contacts available")

      else:

            selected = st.selectbox(
                  "Select Contact to Delete",
                  df["First Name"] + " " + df["Last Name"]
            )

            if st.button("Delete Contact"):
                df = df[(df["First Name"] + " " + df["Last Name"]) != selected]
                df.to_csv(FILE, index=False)

                st.success("Contact deleted")