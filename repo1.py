import requests

BANNER = r'''
╔════════════════════════╗
║    Repo Manager Tool    ║
╚════════════════════════╝
'''

def main():
    layout = [
        [sg.Text(BANNER)],
        [sg.Text("GitHub Username"), sg.Input(key="-USERNAME-")],
        [sg.Text("GitHub Token"), sg.Input(key="-TOKEN-", password_char="*")],
        [sg.Button("Authenticate"), sg.Button("Exit")]
    ]

    window = sg.Window("RepoManager", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Authenticate":
            username = values["-USERNAME-"]
            token = values["-TOKEN-"]
            authenticated = authenticate(username, token)

            if authenticated:
                sg.popup("Authentication Successful!")
                repositories = list_repositories(username, token)
                delete_repositories(repositories)
            else:
                sg.popup("Authentication Failed!")

    window.close()

def authenticate(username, token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get(f"https://api.github.com/user", headers=headers)

    if response.status_code == 200 and response.json().get("login") == username:
        return True

    return False

def list_repositories(username, token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get(f"https://api.github.com/users/{username}/repos", headers=headers)

    if response.status_code == 200:
        repositories = response.json()
        return repositories

    return []

def delete_repositories(repositories):
    repo_names = [repo["name"] for repo in repositories]

    layout = [
        [sg.Text("Enter repository numbers to delete (e.g., 1,3,7,8):")],
        [sg.Input(key="-REPOS-")],
        [sg.Button("Delete"), sg.Button("Cancel")]
    ]

    window = sg.Window("RepoManager - Delete Repositories", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break
        elif event == "Delete":
            repo_numbers = values["-REPOS-"].replace(" ", "").split(",")
            valid_repo_numbers = [int(num) for num in repo_numbers if num.isdigit() and 1 <= int(num) <= len(repo_names)]
            repos_to_delete = [repo_names[num - 1] for num in valid_repo_numbers]

            confirm_layout = [
                [sg.Text(f"Are you sure you want to delete the following repositories?")],
                [sg.Listbox(values=repos_to_delete, size=(50, 6))],
                [sg.Button("Confirm"), sg.Button("Cancel")]
            ]

            confirm_window = sg.Window("RepoManager - Confirm Deletion", confirm_layout)

            while True:
                confirm_event, confirm_values = confirm_window.read()

                if confirm_event == sg.WINDOW_CLOSED or confirm_event == "Cancel":
                    break
                elif confirm_event == "Confirm":
                    delete_selected_repos(repos_to_delete)
                    break

            confirm_window.close()

    window.close()

def delete_selected_repos(repos_to_delete):
    for repo in repos_to_delete:
        response = requests.delete(f"https://api.github.com/repos/{username}/{repo}", headers=headers)

        if response.status_code == 204:
            print(f"Successfully deleted repository: {repo}")
        else:
            print(f"Failed to delete repository: {repo}")

if __name__ == "__main__":
    main()
