import sqlite3
import random
import pandas as pd
def create_db():
    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    # Create the 'users' table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')

    # Create the 'issues' table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS issues (
                    issue_code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    issue_status TEXT,
                    principal_risk_type TEXT,
                    subrisk_type TEXT,
                    business_unit TEXT,
                    bu_rating TEXT,
                    agl_rating TEXT,
                    assurance_provider TEXT,
                    due_date TEXT,
                    financially_implicated TEXT,
                    review_name TEXT,
                    issue_number_and_title TEXT,
                    date_submitted_to_risk_assurance TEXT,
                    ra_reviewers TEXT,
                    closure_email_or_feedback_date TEXT,
                    issuer_name TEXT,
                    issuer_surname TEXT,
                    issuer_email TEXT,
                    username TEXT,
                    FOREIGN KEY (username) REFERENCES users (username))''')

    conn.commit()
    conn.close()

create_db()  # Create the database and tables
# Function to check if the username already exists in the database
def username_exists(username):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    conn.close()
    return user is not None
# Function to insert a new user into the database
def signup(username, password):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    # Hash the password before saving it
    hashed_password = hash_password(password)

    try:
        # Insert the new user into the 'users' table
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return "Signup successful!"
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    # Hash the entered password
    hashed_password = hash_password(password)
    
    # Find the user and compare the hashed password
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()

    if stored_password and stored_password[0] == hashed_password:
        return True
    return False
def log_issue(issue_code, name, description, issue_status, principal_risk_type, subrisk_type, business_unit,
              bu_rating, agl_rating, assurance_provider, due_date, financially_implicated, review_name,
              issue_number_and_title, date_submitted_to_risk_assurance, ra_reviewers, closure_email_or_feedback_date,
              issuer_name, issuer_surname, issuer_email, username):

    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    try:
        # Insert new issue into the 'issues' table
        c.execute('''INSERT INTO issues (
                        issue_code, name, description, issue_status, principal_risk_type, subrisk_type, 
                        business_unit, bu_rating, agl_rating, assurance_provider, due_date, 
                        financially_implicated, review_name, issue_number_and_title, 
                        date_submitted_to_risk_assurance, ra_reviewers, closure_email_or_feedback_date, 
                        issuer_name, issuer_surname, issuer_email, username)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (issue_code, name, description, issue_status, principal_risk_type, subrisk_type,
                     business_unit, bu_rating, agl_rating, assurance_provider, due_date,
                     financially_implicated, review_name, issue_number_and_title,
                     date_submitted_to_risk_assurance, ra_reviewers, closure_email_or_feedback_date,
                     issuer_name, issuer_surname, issuer_email, username))

        conn.commit()
        return "Issue logged successfully!"
    except Exception as e:
        return f"Error logging issue: {e}"
    finally:
        conn.close()
def view_all_issues():
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    c.execute("SELECT * FROM issues")
    issues = c.fetchall()
    
    conn.close()
    return issues
def update_issue_status(issue_code, new_status, new_description):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    c.execute('''UPDATE issues SET issue_status = ?, description = ? WHERE issue_code = ?''',
              (new_status, new_description, issue_code))

    conn.commit()
    conn.close()
    return "Issue status updated successfully!"
import streamlit as st
import sqlite3
from hashlib import sha256

# Helper function to hash password
def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()
# Streamlit Signup UI
def signup_page():
    st.title("Signup - Register")

    # User input fields
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Validate user inputs and handle signup
    if st.button("Sign Up"):
        if not username or not password:
            st.error("Please fill in both fields.")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        elif username_exists(username):
            st.error("Username already exists. Please choose another one.")
        else:
            # If all checks pass, proceed to signup
            result = signup(username, password)
            if result == "Signup successful!":
                st.success(result)
            else:
                st.error(result)


# Function to generate a unique issue code
def generate_unique_code():
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    
    while True:
        # Generate a random four-digit code
        code = str(random.randint(1000, 9999))
        
        # Check if the code already exists in the 'issues' table
        c.execute("SELECT * FROM issues WHERE issue_code = ?", (code,))
        existing_code = c.fetchone()
        
        if existing_code is None:  # Code is unique
            conn.close()
            return code
# Function to fetch data from SQL dynamically
def fetch_data_from_sql():
    # Connect to the SQLite database
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    # Execute your SQL query (change this to your actual query)
    query = "SELECT * FROM issues"  # Example query
    c.execute(query)

    # Fetch the column names dynamically from the query
    columns = [description[0] for description in c.description]

    # Fetch the data
    data = c.fetchall()

    # Convert to DataFrame and close the connection
    df = pd.DataFrame(data, columns=columns)

    conn.close()
    
    return df
# Streamlit UI
def main():
    st.title("Issue Tracker App")

    page = st.sidebar.radio("Navigation", ["Login", "View Current Issues", "Log Issue", "Signup","Update Issue"])

    if page == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")

    elif page == "Log Issue":
        st.header("Log Issue")
        if 'username' in st.session_state:
            issue_code = generate_unique_code()
            st.text(f"Generated Issue Code: {issue_code}")

            name = st.text_input("Issue Name")
            description = st.text_area("Description")
            issue_status = st.selectbox("Status", ["Open", "Closed","Risk Accepted", "Overdue"])
            principal_risk_type.st.text_input("Risk Type")
            subrisk_type =st.text_input("subrisk_type")
            business_unit= st.text_input(" business_unit")
            bu_rating=st.text_input("bu_rating")
            agl_rating=st.text_input("agl_rating")
            assurance_provider=st.text_input("assurance_provider")
            due_date=st.date_input("due_date")
            financially_implicated=st.selectbox(" financially_implicated",["Yes","NO"])
            review_name=st.text_input("review_name")
            issue_number_and_title=st.text_input("issue_number_and_title")
            date_submitted_to_risk_assurance=st.text_inpu("date_submitted_to_risk_assurance")
            ra_reviewers=st.text_input("ra_reviewers")
            closure_email_or_feedback_date=st.date_input("closure_email_or_feedback_date")
            issuer_name=st.text_input("issuer_name")
            issuer_surname=st.text_input("issuer_surname")
            issuer_email=st.text_input("issuer_email")

            if st.button("Log Issue"):
                result = log_issue(issue_code, name, description, issue_status, principal_risk_type,subrisk_type, business_unit,   bu_rating,  agl_rating, assurance_provider, due_date,  financially_implicated, review_name, issue_number_and_title, , date_submitted_to_risk_assurance, date_submitted_to_risk_assurance, ra_reviewers, closure_email_or_feedback_date, issuer_name, issuer_email, st.session_state.username)
                st.success(result)
        else:
            st.warning("Please login to log an issue.")
    
    elif page == "Signup":
        signup_page()
    elif page == "View Current Issues":
        st.header("View Issues")
        issues= view_all_issues()
        # Fetch data from SQL
        df = fetch_data_from_sql()
    
        # Display the data
        st.write("Issues in the Database:")
        st.write(df)
        for issue in issues:
            st.write(issue)

    elif page == "Update Issue":
        st.header("Update Issue")
        issue_code = st.text_input("Enter Issue Code to Update")
        new_status = st.selectbox("New Status", ["Open", "Closed"])
        new_description = st.text_area("New Description")

        if st.button("Update Issue"):
            result = update_issue_status(issue_code, new_status, new_description)
            st.success(result)

if __name__ == "__main__":
    main()
