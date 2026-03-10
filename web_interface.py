from flask import Flask, request, jsonify, render_template_string
import direct_updater

app = Flask(__name__)

@app.route('/')
def index():
    """Simple web interface"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Updater</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .form-group { margin-bottom: 15px; }
        textarea { width: 100%; height: 200px; font-family: monospace; }
        button { background: #0366d6; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
        .result { margin-top: 20px; padding: 10px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>GitHub Repository Updater</h1>
    
    <div class="form-group">
        <label>File Path:</label>
        <input type="text" id="filePath" placeholder="e.g., main.py" style="width: 300px;">
    </div>
    
    <div class="form-group">
        <label>Commit Message:</label>
        <input type="text" id="commitMessage" placeholder="e.g., Fix button issue" style="width: 400px;">
    </div>
    
    <div class="form-group">
        <label>Content:</label>
        <textarea id="content" placeholder="Paste your code here..."></textarea>
    </div>
    
    <button onclick="updateFile()">Update File</button>
    
    <div id="result"></div>
    
    <script>
        function updateFile() {
            const filePath = document.getElementById('filePath').value;
            const commitMessage = document.getElementById('commitMessage').value;
            const content = document.getElementById('content').value;
            
            if (!filePath || !commitMessage || !content) {
                alert('Please fill in all fields');
                return;
            }
            
            fetch('/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    file_path: filePath,
                    commit_message: commitMessage,
                    content: content
                })
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('result');
                if (data.success) {
                    resultDiv.innerHTML = '<div class="result success">✅ File updated successfully!</div>';
                } else {
                    resultDiv.innerHTML = '<div class="result error">❌ Error: ' + data.error + '</div>';
                }
            })
            .catch(error => {
                document.getElementById('result').innerHTML = '<div class="result error">❌ Network error: ' + error + '</div>';
            });
        }
    </script>
</body>
</html>
    ''')

@app.route('/update', methods=['POST'])
def update_file():
    """Web endpoint to update GitHub files"""
    data = request.json
    
    try:
        updater = direct_updater.create_updater()
        result = updater.update_file(
            file_path=data['file_path'],
            content=data['content'],
            commit_message=data['commit_message']
        )
        
        if result:
            return jsonify({"success": True, "result": result})
        else:
            return jsonify({"success": False, "error": "Update failed"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
