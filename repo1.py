import requests
import time

def main():
    access_token = input("Enter your GitHub access token: ")
    session_duration = 30 * 60  # 30 minutes
    session_start = time.time()

    while time.time() - session_start < session_duration:
        print("1. List repositories")
        print("2. Delete a repository")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            repositories = list_repositories(access_token)
            if repositories:
                print_repositories(repositories)
        elif choice == "2":
            delete_repository(access_token)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Session expired. You have been logged out.")

def list_repositories(access_token):
    response = requests.get("https://api.github.com/user/repos", headers={"Authorization": f"token {access_token}"})
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve repositories.")
        return None

def print_repositories(repositories):
    for index, repo in enumerate(repositories, start=1):
        print(f"{index}. {repo['name']}")

def delete_repository(access_token):
    repositories = list_repositories(access_token)
    if repositories:
        print_repositories(repositories)
        repo_number = input("Enter the number of the repository to delete: ")

        if repo_number.isdigit() and int(repo_number) <= len(repositories):
            confirmation = input(f"Are you sure you want to delete the repository '{repositories[int(repo_number) - 1]['name']}'? (y/n): ")

            if confirmation.lower() == "y":
                response = requests.delete(f"https://api.github.com/repos/{repositories[int(repo_number) - 1]['full_name']}", headers={"Authorization": f"token {access_token}"})

                if response.status_code == 204:
                    print("Repository deleted successfully.")
                else:
                    print(f"Failed to delete the repository '{repositories[int(repo_number) - 1]['name']}'.")
            else:
                print("Operation cancelled.")
        else:
            print("Invalid repository number.")
    else:
        print("No repositories to delete.")

if __name__ == "__main__":
    main()
