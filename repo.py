import requests
import time

SESSION_DURATION = 30 * 60  # 30 minutes in seconds

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
    print("╔════════════════════════╗")
    print("║   Repo Manager Tool     ║")
    print("╚════════════════════════╝")

    username = input("Enter your GitHub username: ")
    token = input("Enter your GitHub Access Token: ")

    session_start = time.time()
    session_end = session_start + SESSION_DURATION

    while time.time() < session_end:
        print("\nMenu Options:")
        print("1. List Repositories")
        print("2. Delete Repositories")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            list_repositories(username, token)
        elif choice == '2':
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

                repo_numbers = input("Enter the number(s) of the repository to delete (separated by commas): ")
                repo_numbers = [int(num.strip()) for num in repo_numbers.split(',') if num.strip()]

                for repo_number in repo_numbers:
                    if repo_number < 1 or repo_number > len(repos):
                        print(f"Invalid repository number '{repo_number}'. Skipping...")
                        continue

                    selected_repo = repos[repo_number - 1]

                    confirm = input(f"Are you sure you want to delete the repository '{selected_repo['name']}'? (y/n): ")
                    if confirm.lower() == 'y':
                        delete_repository(username, token, selected_repo['name'])
                    else:
                        print(f"Deletion cancelled for repository '{selected_repo['name']}'.")

            else:
                print("Failed to retrieve repositories. Incorrect authentication. Please check your username and access token.")
                break

        elif choice == '3':
            print("Exiting...")
            break

    print("Session has expired. Exiting...")

if __name__ == "__main__":
    main()
