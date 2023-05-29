import requests

username = input("Enter your GitHub username: ")
token = input("Enter your GitHub personal access token with repo scope: ")

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

    repo_number = int(input("Enter the number of the repository to delete: "))

    if repo_number < 1 or repo_number > len(repos):
        print("Invalid repository number. Exiting...")
    else:
        selected_repo = repos[repo_number - 1]

        confirm = input(f"Are you sure you want to delete the repository '{selected_repo['name']}'? (y/n): ")
        if confirm.lower() == 'y':
            delete_url = f'https://api.github.com/repos/{username}/{selected_repo["name"]}'

            response = requests.delete(delete_url, headers=headers)

            if response.status_code == 204:
                print(f"The repository '{selected_repo['name']}' has been deleted successfully!")
            else:
                print(f"Failed to delete the repository '{selected_repo['name']}'.")
        else:
            print("Deletion cancelled by user.")
else:
    print("Failed to retrieve repositories. Incorrect authentication. Please check your username and access token.")
