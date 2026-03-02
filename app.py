import streamlit as st
import json
import cloudinary
import cloudinary.uploader
from imagekitio import ImageKit

st.set_page_config(page_title="JSON Generator", layout="wide")

# ──────────────────────────────────────────────────────────────
# Auto-clear: triggered immediately after JSON download
# ──────────────────────────────────────────────────────────────
if st.session_state.get("pending_clear"):
    new_fk = st.session_state.get("form_key", 0) + 1
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state["form_key"] = new_fk

# ──────────────────────────────────────────────────────────────
# Form key — incrementing this resets all widget values
# ──────────────────────────────────────────────────────────────
if "form_key" not in st.session_state:
    st.session_state["form_key"] = 0
fk = st.session_state["form_key"]

# ──────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────
def clear_all_fields():
    """Manual clear — user clicked 'Clear All Fields'."""
    new_fk = st.session_state.get("form_key", 0) + 1
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state["form_key"] = new_fk

def trigger_download_clear():
    """Set flag so the very next rerun auto-clears all fields."""
    st.session_state["pending_clear"] = True

# ──────────────────────────────────────────────────────────────
# Title
# ──────────────────────────────────────────────────────────────
st.title("Portfolio JSON Generator")

# ──────────────────────────────────────────────────────────────
# Terms & Conditions / Privacy Policy
# ──────────────────────────────────────────────────────────────
with st.expander("📋  Terms & Conditions & Privacy Policy — Please Read Before Use", expanded=False):
    st.markdown("""
---
## Terms & Conditions

### 1. Intended Use
This tool is designed exclusively for building portfolio JSON files in a **desktop environment**.

> *"This particular JSON creator you are seeing can be used as long as you know how to use it on
> desktop. We have also included the Documentation in the Zip file of the Portfolio Template
> you download."*

By using this application you acknowledge that it is a local utility bundled with a portfolio
template, and agree to these terms.

---

### 2. Third-Party Services — Cloudinary & ImageKit
- This app offers **optional** integration with **Cloudinary** and **ImageKit** for image hosting.
- By entering your API credentials you agree to the respective Terms of Service of those platforms:
  **Cloudinary** (cloudinary.com/tos) and **ImageKit** (imagekit.io/terms).
- You are solely responsible for all usage, charges, storage quotas, and activity on your
  Cloudinary and ImageKit accounts arising from uploads made through this tool.
- The developers of this tool are not affiliated with, endorsed by, or responsible for
  Cloudinary or ImageKit.

---

### 3. Your Content & Data Responsibility
- The generated JSON file contains only the information you have voluntarily entered.
- You are responsible for the accuracy, copyright ownership, and appropriateness of all content
  you submit, including images, links, and personal information.
- Do not enter credentials or personal information belonging to others.

---

### 4. Security — Clearing Your Fields *(Important)*
Protecting your API keys is **your responsibility**. This application takes the following steps
to help:

| Action | When it happens |
|---|---|
| **Auto-clear all fields** (including API keys) | Immediately after you click **Download JSON** |
| **Manual clear** via "🗑️ Clear All Fields" button | Any time you choose |
| **Session expiry** | When the browser tab is closed or the page is refreshed |

> ⚠️ **Please always click "Clear All Fields" or close the browser tab after downloading your
> JSON — especially on shared or public computers.** Even though auto-clear runs after download,
> taking this extra step ensures your credentials are never left on screen.

---

### 5. No Warranty
This tool is provided **as-is**, without warranty of any kind, express or implied, including but
not limited to warranties of merchantability, fitness for a particular purpose, or
non-infringement. The developers make no guarantees regarding uptime, accuracy, or correctness
of the generated output.

---
---

## Privacy Policy

### 1. No Data Collection
This application does **not** collect, store, transmit, or log any personal data, API credentials,
form inputs, or uploaded images to any server operated by this tool's developers.
All data processing happens **locally in your browser session only**.

---

### 2. API Keys & Credentials
- Your Cloudinary and ImageKit API keys are held **only** in your browser's session memory
  for the duration you are actively using the tool.
- Keys are used **exclusively** to authenticate upload requests sent directly from your browser
  to Cloudinary's or ImageKit's own API endpoints.
- Keys are **never** forwarded to, stored by, or visible to any server other than the
  respective cloud service you have chosen.
- Keys are automatically erased from session memory the moment you download your JSON
  (auto-clear) or click "Clear All Fields".

---

### 3. Image Uploads
- Images you choose to upload are transmitted directly to **your own** Cloudinary or ImageKit
  account using your credentials.
- This tool has no visibility into, and exercises no control over, your cloud storage, its
  contents, or the URLs generated.

---

### 4. Session Data & Persistence
- All form data — name, about, projects, publications, social links, etc. — lives **only** in
  your browser's active session memory.
- No cookies, local storage, databases, or any form of persistent storage are used.
- All data is permanently lost when you close the tab or refresh the page.

---

### 5. Questions & Support
For further guidance, refer to the **Documentation** included in the Portfolio Template ZIP file.

---
    """)

# ──────────────────────────────────────────────────────────────
# Sidebar — Image Hosting + Security Notice + Clear Button
# ──────────────────────────────────────────────────────────────
st.sidebar.header("Image Hosting Configuration")

st.sidebar.warning(
    "🔐 **Security Notice**\n\n"
    "Your API keys are stored only for this session and are cleared automatically "
    "after you download your JSON.\n\n"
    "**Always clear all fields after downloading, especially on shared devices.**"
)

image_service = st.sidebar.selectbox(
    "Choose Image Service",
    ["None", "Cloudinary", "ImageKit"],
    key=f"image_service_{fk}"
)

api_keys = {}
if image_service == "Cloudinary":
    api_keys["cloud_name"] = st.sidebar.text_input("Cloud Name", key=f"cloud_name_{fk}")
    api_keys["api_key"] = st.sidebar.text_input("API Key", key=f"api_key_{fk}")
    api_keys["api_secret"] = st.sidebar.text_input("API Secret", type="password", key=f"api_secret_{fk}")
elif image_service == "ImageKit":
    api_keys["public_key"] = st.sidebar.text_input("Public Key", key=f"ik_public_{fk}")
    api_keys["private_key"] = st.sidebar.text_input("Private Key", type="password", key=f"ik_private_{fk}")

st.sidebar.divider()
st.sidebar.button(
    "🗑️  Clear All Fields",
    on_click=clear_all_fields,
    use_container_width=True,
    help="Clears all form fields and API keys from this session."
)

# ──────────────────────────────────────────────────────────────
# Upload helper
# ──────────────────────────────────────────────────────────────
def upload_image(file, service, keys):
    if not file:
        return None
    try:
        if service == "Cloudinary":
            cloudinary.config(
                cloud_name=keys["cloud_name"],
                api_key=keys["api_key"],
                api_secret=keys["api_secret"]
            )
            response = cloudinary.uploader.upload(file)
            return response.get("secure_url")
        elif service == "ImageKit":
            imagekit = ImageKit(
                private_key=keys["private_key"]
            )
            upload = imagekit.files.upload(
                file=file,
                file_name=file.name,
                public_key=keys["public_key"]
            )
            return upload.url
    except Exception as e:
        st.error(f"Error uploading image: {e}")
        return None

# ──────────────────────────────────────────────────────────────
# Form Data Collection
# ──────────────────────────────────────────────────────────────
data = {}

# Profile Section
st.header("Profile")
col1, col2 = st.columns(2)
with col1:
    data["name"] = st.text_input("Name", key=f"name_{fk}")
    data["headline"] = st.text_input("Headline", key=f"headline_{fk}")

    profile_pic_option = st.radio("Profile Picture Source", ["URL", "Upload"], key=f"pp_radio_{fk}")
    if profile_pic_option == "URL":
        data["profile_pic"] = st.text_input("Profile Picture URL", key=f"pp_url_{fk}")
    else:
        uploaded_file = st.file_uploader(
            "Upload Profile Picture", type=["jpg", "png", "jpeg"], key=f"pp_upload_{fk}"
        )
        if uploaded_file and image_service != "None":
            if st.button("Upload Profile Pic", key=f"pp_btn_{fk}"):
                url = upload_image(uploaded_file, image_service, api_keys)
                if url:
                    st.success("Uploaded!")
                    data["profile_pic"] = url
                    st.session_state[f"profile_pic_url_{fk}"] = url
        if f"profile_pic_url_{fk}" in st.session_state:
            data["profile_pic"] = st.session_state[f"profile_pic_url_{fk}"]
            st.image(data["profile_pic"], width=100)

with col2:
    data["about"] = st.text_area("About (Description)", height=150, key=f"about_{fk}")
    data["email"] = st.text_input("Email", key=f"email_{fk}")
    data["location"] = st.text_input("Location", key=f"location_{fk}")

# Skills Section
st.header("Skills")
skills_input = st.text_area(
    "Enter skills (comma separated)",
    "Python, Streamlit, React, Cloudinary",
    key=f"skills_{fk}"
)
data["skills"] = [s.strip() for s in skills_input.split(",") if s.strip()]

# Projects Section
st.header("Projects")
if "projects" not in st.session_state:
    st.session_state.projects = []

with st.expander("Add New Project", expanded=True):
    p_title = st.text_input("Project Title", key=f"p_title_{fk}")
    p_desc = st.text_area("Project Description", key=f"p_desc_{fk}")
    p_github = st.text_input("GitHub Link", key=f"p_github_{fk}")
    p_live = st.text_input("Live Link", key=f"p_live_{fk}")
    p_tech = st.text_input("Tech Stack (comma separated)", key=f"p_tech_{fk}")

    p_thumb_option = st.radio("Thumbnail Source", ["URL", "Upload"], key=f"p_thumb_radio_{fk}")
    p_thumb_url = ""
    if p_thumb_option == "URL":
        p_thumb_url = st.text_input("Thumbnail URL", key=f"p_thumb_url_{fk}")
    else:
        p_file = st.file_uploader(
            "Upload Thumbnail", type=["jpg", "png", "jpeg"], key=f"p_uploader_{fk}"
        )
        if p_file and image_service != "None":
            if st.button("Upload Thumbnail", key=f"p_upload_btn_{fk}"):
                url = upload_image(p_file, image_service, api_keys)
                if url:
                    st.success("Thumbnail Uploaded!")
                    p_thumb_url = url
                    st.session_state[f"temp_project_thumb_{fk}"] = url
        if f"temp_project_thumb_{fk}" in st.session_state:
            p_thumb_url = st.session_state[f"temp_project_thumb_{fk}"]
            st.image(p_thumb_url, width=100)

    if st.button("Add Project", key=f"add_proj_{fk}"):
        new_project = {
            "title": p_title,
            "description": p_desc,
            "tech_stack": [t.strip() for t in p_tech.split(",") if t.strip()],
            "github_link": p_github,
            "live_link": p_live,
            "thumbnail": p_thumb_url
        }
        st.session_state.projects.append(new_project)
        st.success(f"Project '{p_title}' added!")
        if f"temp_project_thumb_{fk}" in st.session_state:
            del st.session_state[f"temp_project_thumb_{fk}"]
        st.rerun()

if st.session_state.projects:
    st.subheader("Current Projects")
    for idx, p in enumerate(st.session_state.projects):
        st.write(f"**{idx+1}. {p['title']}**")
        st.write(p["description"])
        st.write(f"GitHub: {p['github_link']} | Live: {p['live_link']}")
        if p["thumbnail"]:
            st.image(p["thumbnail"], width=100)
        if st.button(f"Remove Project {idx+1}", key=f"del_proj_{idx}_{fk}"):
            st.session_state.projects.pop(idx)
            st.rerun()
        st.divider()

data["projects"] = st.session_state.projects

# Publications Section
st.header("Publications")
if "publications" not in st.session_state:
    st.session_state.publications = []

with st.expander("Add Publication"):
    pub_title = st.text_input("Publication Title", key=f"pub_title_{fk}")
    pub_journal = st.text_input("Journal/Conference Name", key=f"pub_journal_{fk}")
    pub_year = st.text_input("Year", key=f"pub_year_{fk}")
    pub_link = st.text_input("Publication Link", key=f"pub_link_{fk}")

    if st.button("Add Publication", key=f"add_pub_{fk}"):
        new_pub = {
            "title": pub_title,
            "journal": pub_journal,
            "year": pub_year,
            "link": pub_link
        }
        st.session_state.publications.append(new_pub)
        st.success(f"Publication '{pub_title}' added!")
        st.rerun()

if st.session_state.publications:
    st.subheader("Current Publications")
    for idx, pub in enumerate(st.session_state.publications):
        st.write(f"**{idx+1}. {pub['title']}**")
        st.write(f"{pub['journal']} ({pub['year']})")
        if st.button(f"Remove Publication {idx+1}", key=f"del_pub_{idx}_{fk}"):
            st.session_state.publications.pop(idx)
            st.rerun()

data["publications"] = st.session_state.publications

# Social Media Section
st.header("Social Media")
col3, col4 = st.columns(2)
data["social_media"] = {}
with col3:
    data["social_media"]["linkedin"] = st.text_input("LinkedIn URL", key=f"linkedin_{fk}")
    data["social_media"]["github"] = st.text_input("GitHub URL", key=f"github_{fk}")
    data["social_media"]["twitter"] = st.text_input("Twitter/X URL", key=f"twitter_{fk}")
with col4:
    data["social_media"]["website"] = st.text_input("Personal Website", key=f"website_{fk}")
    other_social = st.text_input("Other (Label:URL)", key=f"other_social_{fk}")
    if other_social and ":" in other_social:
        s_label, s_url = other_social.split(":", 1)
        data["social_media"][s_label.strip()] = s_url.strip()

# ──────────────────────────────────────────────────────────────
# Generate Output
# ──────────────────────────────────────────────────────────────
st.header("Generate Output")
json_output = json.dumps(data, indent=4)
st.code(json_output, language="json")

st.info(
    "⚠️  **Before you download — please note:**\n\n"
    "All fields, including your API keys, will be **automatically cleared** the moment "
    "you click **Download JSON** below.\n\n"
    "If you need to make changes after downloading, simply re-fill the form. "
    "You can also use the **🗑️ Clear All Fields** button in the sidebar at any time."
)

col_dl, col_clear = st.columns([3, 1])
with col_dl:
    st.download_button(
        label="⬇️  Download JSON",
        data=json_output,
        file_name="portfolio.json",
        mime="application/json",
        on_click=trigger_download_clear,
        use_container_width=True,
        type="primary"
    )
with col_clear:
    st.button(
        "🗑️  Clear All Fields",
        on_click=clear_all_fields,
        use_container_width=True,
        help="Immediately clears all form fields and API keys."
    )
