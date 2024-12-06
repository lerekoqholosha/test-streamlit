import streamlit as st
import pandas as pd
import requests
import base64
import json
import datetime

# GitHub credentials and repository details
GITHUB_TOKEN = "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"  # Replace with your GitHub token
REPO_OWNER = "lerekoqholosha"  # Replace with your GitHub username
REPO_NAME = "test-streamlit"  # Replace with your GitHub repo name
FILE_PATH = "users.csv"  # Path to the file in the repo
BRANCH_NAME = "main"  # Branch you want to commit to
COMMIT_MESSAGE = "Automated update " + str(datetime.datetime.now())

# Function to get the file content from GitHub
def get_file_from_github():
    url = 'https://raw.githubusercontent.com/lerekoqholosha/test-streamlit/refs/heads/main/users.csv'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(response.text)
    else:
        st.error(f"Failed to fetch the file from GitHub: {response.status_code}")
        return pd.DataFrame(columns=["username", "school", "age"])

# Function to push the updated file back to GitHub
def push_to_github(file_path, content, sha):
    update_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    data = {
        "path": file_path,
        "branch": BRANCH_NAME,
        "message": COMMIT_MESSAGE,
        "content": base64.b64encode(content.encode()).decode()
    }

    if sha:
        data["sha"] = sha

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.put(update_url, json=data, headers=headers)
    
    if response.status_code == 200:
        st.success("CSV file updated successfully on GitHub!")
    else:
        st.error(f"Failed to update the file: {response.status_code} - {response.text}")

# Function to get the sha of the file on GitHub
def get_sha_from_github():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH_NAME}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['sha']
    else:
        st.error(f"Failed to fetch file details: {response.status_code} - {response.text}")
        return None

# Streamlit app
def app():
    st.title("CSV Updater (GitHub)")

    # Load existing CSV data from GitHub
    df = get_file_from_github()

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

        # Get the sha of the existing file on GitHub
        sha = get_sha_from_github()

        # Convert the updated DataFrame to CSV format
        updated_csv = updated_df.to_csv(index=False)

        # Push the updated file back to GitHub
        push_to_github(FILE_PATH, updated_csv, sha)

if __name__ == "__main__":
    app()
