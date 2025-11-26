import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Feedback & Comments", layout="centered")

st.title("💬 Feedback & Comments")
st.write("Your feedback helps improve the Innovation Mentor Platform. Public comments are visible to all, while private comments are only visible to the platform owner.")

# ---------------------------------------------
# Files
# ---------------------------------------------
PUBLIC_FILE = "data/public_comments.csv"
PRIVATE_FILE = "data/private_comments.csv"

os.makedirs("data", exist_ok=True)

def load_or_init(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=["timestamp", "name", "comment"])
        df.to_csv(path, index=False)
        return df

public_df = load_or_init(PUBLIC_FILE)
private_df = load_or_init(PRIVATE_FILE)

# ---------------------------------------------
# Submit comment
# ---------------------------------------------
st.subheader("Submit Feedback")

name = st.text_input("Your name (optional)")
comment = st.text_area("Your comment")

visibility = st.radio(
    "Comment visibility:",
    ["Public", "Private"],
    help="Public comments appear in the list below. Private comments are only visible to the platform owner."
)

if st.button("Submit"):
    if comment.strip() == "":
        st.error("Please enter a comment before submitting.")
    else:
        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name if name.strip() else "Anonymous",
            "comment": comment.strip()
        }

        if visibility == "Public":
            public_df = pd.concat([public_df, pd.DataFrame([new_entry])], ignore_index=True)
            public_df.to_csv(PUBLIC_FILE, index=False)
        else:
            private_df = pd.concat([private_df, pd.DataFrame([new_entry])], ignore_index=True)
            private_df.to_csv(PRIVATE_FILE, index=False)

        st.success("Thank you! Your feedback has been submitted.")

# ---------------------------------------------
# Public comments section
# ---------------------------------------------
st.markdown("---")
st.subheader("Public Comments")

if len(public_df) == 0:
    st.info("No public comments yet.")
else:
    df_display = public_df.sort_values("timestamp", ascending=False)

    search = st.text_input("Search public comments")

    if search.strip():
        df_display = df_display[df_display["comment"].str.contains(search, case=False)]

    # Render
    for _, row in df_display.iterrows():
        st.markdown(f"""
        **{row['name']}** — *{row['timestamp']}*  
        {row['comment']}
        ---
        """)

# ---------------------------------------------
# Disclaimer
# ---------------------------------------------
st.markdown("""
<br>
<div style='font-size: 0.80em; color: grey; text-align: center;'>
Public comments are visible to all users.  
Private comments are stored securely and visible only to the platform owner.  
For legal and privacy terms, please refer to the Legal/Disclaimer section.
</div>
""", unsafe_allow_html=True)
