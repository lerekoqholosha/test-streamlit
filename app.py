import streamlit as st
import sqlite3
import pandas as pd

# Create a connection to the SQLite database
# (if the file doesn't exist, it will be created)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a table to store user data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        school TEXT,
        age INTEGER
    )
''')
conn.commit()

# Function to fetch data from the SQLite database
def fetch_data():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=["id", "username", "school", "age"])

# Function to add a new user to the SQLite database
def add_user(username, school, age):
    cursor.execute("INSERT INTO users (username, school, age) VALUES (?, ?, ?)", (username, school, age))
    conn.commit()

# Function to update the SQLite database (not used here, but can be implemented if needed)
def update_user(id, username, school, age):
    cursor.execute("UPDATE users SET username = ?, school = ?, age = ? WHERE id = ?", (username, school, age, id))
    conn.commit()

# Function to delete a user (not used here, but can be implemented if needed)
def delete_user(id):
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()

# Streamlit app
def app():
    st.title("SQLite User Database")

    # Load existing data from SQLite
    df = fetch_data()

    # Show current data
    st.write("Current data:")
    st.write(df)

    # Input form for new data
    username = st.text_input("Enter username")
    school = st.text_input("Enter school name")
    age = st.number_input("Enter age", min_value=1, max_value=100)

    if st.button("Add Row"):
        # Add new user to the database
        add_user(username, school, age)

        # Reload the data
        df = fetch_data()
        st.write("New row added:")
        st.write(df)

    # Optional: Save the data to a CSV file
    if st.button("Download CSV"):
        df.to_csv("users_data.csv", index=False)
        st.success("CSV file saved!")

if __name__ == "__main__":
    app()
