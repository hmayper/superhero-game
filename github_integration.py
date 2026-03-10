import os
import subprocess
import tempfile
import shutil
from datetime import datetime

class GitHubDirectIntegration:
    def __init__(self, repo_url, access_token):
        self.repo_url = repo_url
        self.access_token = access_token
        self.temp_dir = None
        
    def clone_repository(self):
        """Clone repository to temporary directory"""
        self.temp_dir = tempfile.mkdtemp()
        print(f"Cloning repository to {self.temp_dir}")
        
        # Use HTTPS with token
        auth_url = f"https://{self.access_token}@github.com/{self.repo_url}.git"
        
        try:
            subprocess.run([
                "git", "clone", auth_url, self.temp_dir
            ], check=True, capture_output=True)
            print("✅ Repository cloned successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone repository: {e}")
            return False
    
    def update_file(self, file_path, content, commit_message):
        """Update a file in the repository"""
        if not self.temp_dir:
            if not self.clone_repository():
                return False
        
        file_full_path = os.path.join(self.temp_dir, file_path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        
        # Write content
        with open(file_full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Stage the file
        subprocess.run([
            "git", "add", file_path
        ], cwd=self.temp_dir, check=True)
        
        # Commit
        try:
            subprocess.run([
                "git", "commit", "-m", commit_message
            ], cwd=self.temp_dir, check=True, capture_output=True)
            
            print(f"✅ File committed: {file_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Commit failed: {e}")
            return False
    
    def push_changes(self):
        """Push changes to remote"""
        if not self.temp_dir:
            return False
        
        try:
            subprocess.run([
                "git", "push", "origin", "main"
            ], cwd=self.temp_dir, check=True, capture_output=True)
            
            print("✅ Changes pushed to GitHub")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Push failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("🧹 Temporary directory cleaned up")

# Example usage
if __name__ == "__main__":
    # Configuration
    REPO_URL = "your-username/superhero-game"
    ACCESS_TOKEN = "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"
    
    # Initialize integration
    integrator = GitHubDirectIntegration(REPO_URL, ACCESS_TOKEN)
    
    try:
        # Update a file
        test_content = "# Test file\nprint('Hello from Thaura!')\n"
        integrator.update_file("test.py", test_content, "Add test file via Thaura")
        
        # Push changes
        integrator.push_changes()
    finally:
        integrator.cleanup()
