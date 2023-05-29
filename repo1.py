import PyGithub
import getpass

def delete_repository(access_token):
    g = PyGithub.Github(access_token)
    user = g.get_user()
    
    repositories = []
    for repo in user.get_repos():
        repositories.append(repo)
    
    print("Available repositories:")
    for i, repo in enumerate(repositories, start=1):
        print(f"{i}. {repo.name}")
    
    repo_number = input("Enter the number of the repository to delete: ")
    repo_index = int(repo_number) - 1
    
    if 0 <= repo_index < len(repositories):
        repo_name = repositories[repo_index].name
        confirmation = input(f"Are you sure you want to delete the repository '{repo_name}'? (y/n): ")
        
        if confirmation.lower() == "y":
            repository = user.get_repo(repositories[repo_index].name)
            repository.delete()
            print(f"The repository '{repo_name}' has been deleted successfully.")
        else:
            print("Repository deletion canceled.")
    else:
        print("Invalid repository number.")

def main():
    print("Repo Manager Tool")
    print("------------------")
    
    username = input("Enter your GitHub username: ")
    access_token = getpass.getpass("Enter your GitHub access token: ")
    
    delete_repository(access_token)

if __name__ == "__main__":
    main()
