import streamlit as st
import pandas as pd
from github import Github
import requests
from io import StringIO

# GitHub credentials and repository details
GITHUB_TOKEN = "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"  # Replace with your GitHub token
REPO_OWNER = "lerekoqholosha"  # Replace with your GitHub username
REPO_NAME = "test-streamlit"  # Replace with your GitHub repo name
FILE_PATH = "users.csv"  # Path to the file in the repo
BRANCH_NAME = "main"  # Branch you want to commit to
COMMIT_MESSAGE = "Updated CSV file via Streamlit"

# Initialize PyGithub with the token
github = Github(GITHUB_TOKEN)
repo = github.get_user(REPO_OWNER).get_repo(REPO_NAME)

# Function to read the CSV file from GitHub
def get_csv_from_github():
    url = f'https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH_NAME}/{FILE_PATH}'
    response = requests.get(url)
    
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        return df
    else:
        st.error("Failed to fetch the CSV file from GitHub.")
        return pd.DataFrame(columns=["username", "school", "age"])

# Function to update the CSV file on GitHub
def update_csv_on_github(updated_df):
    # Get the current content of the file from the repository
    content = repo.get_contents(FILE_PATH)
    
    # Convert the DataFrame to CSV format
    new_content = updated_df.to_csv(index=False)
    
    # Update the file on GitHub
    repo.update_file(FILE_PATH, COMMIT_MESSAGE, new_content, content.sha)
    st.success("CSV file updated successfully on GitHub!")

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
