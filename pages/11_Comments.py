import base64
import requests
import json
from datetime import datetime

# Load secrets
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = st.secrets["GITHUB_REPO"]
BRANCH = st.secrets["GITHUB_BRANCH"]

def github_get_file(path):
    """Load file from GitHub repo."""
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    content = r.json()
    file_data = base64.b64decode(content["content"]).decode("utf-8")
    sha = content["sha"]
    return file_data, sha


def github_update_file(path, new_content, sha):
    """Update file in GitHub repo."""
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    message = f"Update {path} at {datetime.now().isoformat()}"

    data = {
        "message": message,
        "content": base64.b64encode(new_content.encode()).decode(),
        "sha": sha,
        "branch": BRANCH
    }

    r = requests.put(url, headers=headers, data=json.dumps(data))
    r.raise_for_status()
    return True


def append_comment_to_github(path, name, comment):
    """Append comment row to GitHub CSV."""
    old_content, sha = github_get_file(path)

    # Clean fields
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = name.replace(",", " ")
    comment = comment.replace(",", " ")

    new_row = f"{ts},{name},{comment}\n"
    new_content = old_content + new_row

    github_update_file(path, new_content, sha)
