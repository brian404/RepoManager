import requests
import time
from termcolor import colored

SESSION_DURATION = 30 * 60  # 30 minutes in seconds
MAX_AUTH_ATTEMPTS = 3

def delete_repository(username, token, repo_name):
    delete_url = f'https://api.github.com/repos/{username}/{repo_name}'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        print(f"The repository '{repo_name}' has been deleted successfully!")
    else:
        print(f"Failed to delete the repository '{repo_name}'.")

def list_repositories(username, token):
    url = f'https://api.github.com/users/{username}/repos'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()

        print("Available Repositories:")
        for i, repo in enumerate(repos, start=1):
            print(f"{i}. {repo['name']}")
    else:
        print("Failed to retrieve repositories. Incorrect authentication. Please check your username and access token.")

def main():
    print(colored("╔════════════════════════╗", "green"))
    print(colored("║ Repo Manager Tool      ║", "green"))
    print(colored("╚════════════════════════╝", "green"))
    print()

    auth_attempts = 0
    while auth_attempts < MAX_AUTH_ATTEMPTS:
        username = input("Enter your GitHub username: ")
        token = input("Enter your GitHub Access Token: ")

        url = f'https://api.github.com/users/{username}'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print(colored("Successfully logged in!", "green"))
            break
        else:
            print(colored("Failed to authenticate. Please try again.", "red"))
            auth_attempts += 1

    if auth_attempts == MAX_AUTH_ATTEMPTS:
        print(colored("Authorization revoked. Exiting...", "red"))
        return

    session_start_time = time.time()

    while True:
        print("\nMenu Options:")
        print("1. List Repositories")
        print("2. Delete Repositories")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_repositories(username, token)
        elif choice == "2":
            repo_numbers = input("Enter the number(s) of the repository to delete (separated by commas): ")
            repo_numbers = [int(num.strip()) for num in repo_numbers.split(',') if num.strip().isdigit()]
            if not repo_numbers:
                print(colored("Invalid input. Please enter valid repository number(s).", "red"))
                continue

            repositories = list_repositories(username, token)
            selected_repos = [repositories[num - 1]['name'] for num in repo_numbers if 0 < num <= len(repositories)]

            if not selected_repos:
                print(colored("Invalid repository number(s). No repositories selected for deletion.", "red"))
                continue

            print(f"Are you sure you want to delete the following repositories? (y/n):")
            for repo in selected_repos:
                print(repo)

            confirm = input()
            if confirm.lower() == 'y':
                for repo_name in selected_repos:
                    delete_repository(username, token, repo_name)
            else:
                print("Deletion cancelled by user.")
        elif choice == "3":
            print(colored("Exiting...", "red"))
            break
        else:
            print(colored("Invalid choice. Please enter a valid menu option.", "red"))

        current_time = time.time()
        if current_time - session_start_time > SESSION_DURATION:
            print(colored("Session expired. Please log in again.", "red"))
            break

if __name__ == '__main__':
    main()
