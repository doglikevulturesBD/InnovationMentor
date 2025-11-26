import streamlit as st
import pandas as pd
import requests
import base64
import json
from io import StringIO
from datetime import datetime


# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Feedback & Comments", layout="centered")
st.title("💬 Feedback & Comments")
st.write("You can submit public or private comments. Private comments are stored securely and only visible to the platform owner.")


# ---------------------------
# LOAD STREAMLIT SECRETS
# ---------------------------
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = st.secrets["GITHUB_REPO"]
BRANCH = st.secrets["GITHUB_BRANCH"]


# ---------------------------
# GITHUB HELPER FUNCTIONS
# ---------------------------
def github_get_file(path):
    """Load file contents + sha from GitHub private repo."""
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    content = r.json()

    file_data = base64.b64decode(content["content"]).decode("utf-8")
    sha = content["sha"]

    return file_data, sha


def github_update_file(path, new_content, sha):
    """Commit updated file back to GitHub."""
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    commit_message = f"Update {path} — {datetime.now().isoformat()}"

    data = {
        "message": commit_message,
        "content": base64.b64encode(new_content.encode()).decode(),
        "sha": sha,
        "branch": BRANCH
    }

    r = requests.put(url, headers=headers, data=json.dumps(data))
    r.raise_for_status()


def append_comment_to_github(path, name, comment):
    """Append a row to the CSV file stored in GitHub."""
    old_content, sha = github_get_file(path)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Replace commas to preserve CSV structure
    safe_name = name.replace(",", " ")
    safe_comment = comment.replace(",", " ")

    new_row = f"{ts},{safe_name},{safe_comment}\n"
    new_content = old_content + new_row

    github_update_file(path, new_content, sha)


# ---------------------------
# COMMENT SUBMISSION FORM
# ---------------------------
st.subheader("Submit Feedback")

name = st.text_input("Your name (optional)")
comment = st.text_area("Your comment")

visibility = st.radio(
    "Comment visibility:",
    ["Public", "Private"],
    help="Public comments appear below. Private comments go only to the platform owner."
)

if st.button("Submit"):
    if comment.strip() == "":
        st.error("Please write a comment before submitting.")
    else:
        file_path = (
            "data/public_comments.csv"
            if visibility == "Public"
            else "data/private_comments.csv"
        )

        append_comment_to_github(
            file_path,
            name if name.strip() else "Anonymous",
            comment.strip()
        )

        st.success("Your feedback has been securely submitted!")


# ---------------------------
# DISPLAY PUBLIC COMMENTS
# ---------------------------
st.markdown("---")
st.subheader("Public Comments")

try:
    public_raw, _ = github_get_file("data/public_comments.csv")
    public_df = pd.read_csv(StringIO(public_raw))
except Exception:
    public_df = pd.DataFrame(columns=["timestamp", "name", "comment"])

if public_df.empty:
    st.info("No public comments yet.")
else:
    public_df = public_df.sort_values("timestamp", ascending=False)

    search = st.text_input("Search public comments")

    if search.strip():
        public_df = public_df[public_df["comment"].str.contains(search, case=False)]

    for _, row in public_df.iterrows():
        st.markdown(f"""
        **{row['name']}** — *{row['timestamp']}*  
        {row['comment']}
        ---
        """)


# ---------------------------
# DISCLAIMER
# ---------------------------
st.markdown("""
<br>
<div style='font-size: 0.85em; color: grey; text-align: center;'>
Public comments are visible to all app users.  
Private comments are stored securely in a private GitHub repository.  
For privacy and legal terms, please refer to the Legal & Disclaimer section.
</div>
""", unsafe_allow_html=True)
