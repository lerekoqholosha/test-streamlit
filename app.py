import streamlit as st
import pandas as pd
import requests
from base64 import b64decode

# GitHub API details
GITHUB_TOKEN = "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"  # Replace with your GitHub token
GITHUB_USERNAME = "lerekoqholoshat"  # Replace with your GitHub username
REPO_NAME = "test-streamlit"  # Replace with your GitHub repo name
FILE_PATH = "users.csv"  # Path to the file in the repo (no raw URL here)
BRANCH_NAME = "main"  # Branch you want to commit to

# GitHub API URL for accessing the file
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

# Function to get the CSV file from GitHub
def get_csv_from_github():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        # Decode the base64 content
        content = b64decode(file_data['content']).decode('utf-8')
        return pd.read_csv(pd.compat.StringIO(content))
    else:
        st.error("Failed to fetch the CSV file from GitHub.")
        return pd.DataFrame(columns=["username", "school", "age"])

# Function to update the CSV file on GitHub
def update_csv_on_github(updated_df):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data['sha']  # Get the SHA of the file

        # Encode the new CSV content in base64
        new_content = updated_df.to_csv(index=False)
        encoded_content = b64encode(new_content.encode()).decode()

        data = {
            "message": "Updated CSV file via Streamlit",
            "sha": sha,
            "content": encoded_content,
            "branch": BRANCH_NAME
        }

        update_response = requests.put(API_URL, headers=headers, json=data)
        if update_response.status_code == 200:
            st.success("CSV file updated successfully!")
        else:
            st.error("Failed to update the file on GitHub.")
    else:
        st.error("Failed to fetch file details from GitHub.")

# Streamlit app
def app():
    st.title("CSV Updater (GitHub)")

    # Load existing CSV data from GitHub
    df = get_csv_from_github()

    # Show current data
    st.write("Current data:")
    st.write(df)

    # Input form for new data
    username = st.text_input("Enter username")
    school = st.text_input("Enter school name")
    age = st.number_input("Enter age", min_value=1, max_value=100)

    if st.button("Add Row"):
        # Add new row
        new_row = pd.DataFrame({"username": [username], "school": [school], "age": [age]})
        updated_df = pd.concat([df, new_row], ignore_index=True)
        st.write("New row added:")
        st.write(updated_df)

        # Update the CSV on GitHub
        update_csv_on_github(updated_df)

if __name__ == "__main__":
    app()
