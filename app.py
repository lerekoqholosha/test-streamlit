import streamlit as st
import pandas as pd
import requests
from base64 import b64encode, b64decode

# GitHub API details
GITHUB_TOKEN = "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"  # Replace with your GitHub token
GITHUB_USERNAME = "lerekoqholosha"  # Replace with your GitHub username
REPO_NAME = "test-streamlit"  # Replace with your GitHub repo name
FILE_PATH = "users.csv"  # Path to the file in the repo
BRANCH_NAME = "main"  # Branch you want to commit to

# GitHub API URL for accessing the file (correct URL)
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

# Function to get the CSV file from the raw GitHub URL
def get_csv_from_github():
    try:
        # Use pandas to read the CSV directly from the raw GitHub URL
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH_NAME}/{FILE_PATH}"
        df = pd.read_csv(raw_url)
        return df
    except Exception as e:
        st.error(f"Failed to fetch the CSV file from GitHub. Error: {e}")
        return pd.DataFrame(columns=["username", "school", "age"])

# Function to update the CSV file on GitHub
def update_csv_on_github(updated_df):
    # Fetch the current file details to get the SHA (required for updating)
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data['sha']  # Get the SHA of the file

        # Encode the new CSV content in base64
        new_content = updated_df.to_csv(index=False)
        encoded_content = b64encode(new_content.encode()).decode()

        # Prepare the data for the API request
        data = {
            "message": "Updated CSV file via Streamlit",
            "sha": sha,
            "content": encoded_content,
            "branch": BRANCH_NAME
        }

        # Send PUT request to update the file on GitHub
        update_response = requests.put(API_URL, headers=headers, json=data)
        
        if update_response.status_code == 200:
            st.success("CSV file updated successfully!")
        else:
            st.error(f"Failed to update the file on GitHub. Status code: {update_response.status_code}")
            st.error(f"Response content: {update_response.text}")
    else:
        st.error(f"Failed to fetch file details from GitHub. Status code: {response.status_code}")
        st.error(f"Response content: {response.text}")

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
