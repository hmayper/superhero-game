import requests
import base64
import json
from datetime import datetime

class DirectGitHubUpdater:
    def __init__(self, repo_owner, repo_name, access_token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.access_token = access_token
        self.api_base = "https://api.github.com"
        
    def update_file(self, file_path, content, commit_message, branch="main"):
        """Update a file directly via GitHub API"""
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Get current file info (if exists)
        try:
            url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
            response = requests.get(url, headers=headers)
            sha = response.json().get("sha") if response.status_code == 200 else None
        except Exception as e:
            print(f"Error checking existing file: {e}")
            sha = None
        
        # Prepare file content
        content_encoded = base64.b64encode(content.encode()).decode()
        
        # Create/update file
        data = {
            "message": commit_message,
            "content": content_encoded,
            "branch": branch
        }
        
        if sha:
            data["sha"] = sha
            
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            print(f"✅ Successfully updated {file_path}")
            return response.json()
        else:
            print(f"❌ Failed to update {file_path}: {response.text}")
            return None
    
    def get_file_content(self, file_path, branch="main"):
        """Get current content of a file"""
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}?ref={branch}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            content_data = response.json()
            return base64.b64decode(content_data['content']).decode('utf-8')
        else:
            print(f"❌ Failed to get {file_path}: {response.text}")
            return None

def create_updater():
    """Create updater with your credentials"""
    return DirectGitHubUpdater(
        repo_owner="hmayper",
        repo_name="superhero-game",
        access_token="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"
    )

# Example usage functions
def update_main_py(content, commit_message):
    """Update main.py with new content"""
    updater = create_updater()
    return updater.update_file("main.py", content, commit_message)

def update_story_file(content, commit_message):
    """Update story file with new content"""
    updater = create_updater()
    return updater.update_file("story/enhanced_superhero.ink", content, commit_message)

def get_current_main_py():
    """Get current content of main.py"""
    updater = create_updater()
    return updater.get_file_content("main.py")

# Command line interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python direct_updater.py file_path> <commit_message> [content]")
        print("Examples:")
        print("  python direct_updater.py main.py 'Update main file'")
        print("  python direct_updater.py main.py 'Fix bug' 'new code content here'")
        sys.exit(1)
    
    file_path = sys.argv[1]
    commit_message = sys.argv[2]
    content = sys.argv[3] if len(sys.argv) > 3 else None
    
    updater = create_updater()
    
    if content:
        # Update with provided content
        result = updater.update_file(file_path, content, commit_message)
    else:
        # Get current content (for reading)
        content = updater.get_file_content(file_path)
        if content:
            print(f"Current content of {file_path}:")
            print(content)
