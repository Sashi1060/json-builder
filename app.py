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

**Last updated: March 2026**

---

### 1. About This Tool

This is a **free, publicly accessible web tool** that helps you build the `portfolio.json` file
required by the Portfolio Template. You can fill in your details here in the browser, optionally
upload images to your own cloud storage, preview the generated JSON, and download it — without
installing anything.

> *"This particular JSON creator you are seeing can be used as long as you know how to use it
> on desktop. We have also included the Documentation in the Zip file of the Portfolio
> Template you download."*

This tool is available in **two ways**:

| Mode | How to access |
|---|---|
| **Online (this page)** | Use it directly in your browser — no setup required |
| **Local copy** | A copy of this app is included inside the Portfolio Template ZIP file. Run it on your own machine using Python + Streamlit if you prefer to work offline or want full control over your environment. Refer to the Documentation in the ZIP for setup instructions. |

The **portfolio website** built from this JSON is designed and optimised for **desktop viewing**.
By continuing to use this tool (in either mode), you agree to these Terms & Conditions and the
Privacy Policy below.

---

### 2. Bring Your Own Key (BYOK) Model

This application operates on a **strict Bring Your Own Key (BYOK)** model.

- This tool has **no built-in API keys** and no pre-configured cloud storage of any kind.
- Image uploading functionality is **entirely optional**. If you choose not to use it, you can
  still paste direct image URLs into the URL fields and the tool works completely without any
  credentials.
- If you **do** want to upload images through this tool, you must supply your **own** API keys
  from either Cloudinary or ImageKit — services you have independently registered for.
- At no point does the developer of this tool provide, share, or subsidise API access for users.
- You are solely responsible for obtaining, safeguarding, and managing your own API credentials.

This model exists to ensure complete transparency: **your images go to your account, under your
control, using your keys — this tool is only the bridge.**

---

### 3. Who Can Use This Tool

This tool is intended for individuals building their own personal portfolio websites using the
accompanying Portfolio Template. It is provided free of charge as a convenience for those users.

You must not use this tool to:
- Generate content on behalf of another person without their explicit knowledge and consent.
- Submit false, misleading, or harmful information.
- Attempt to probe, reverse-engineer, stress-test, or interfere with the hosting infrastructure.
- Use another person's API credentials without their authorisation.

---

### 4. Third-Party Services — Cloudinary & ImageKit

If you choose to use the optional image upload feature:

- You are connecting this tool to **your own** Cloudinary or ImageKit account, governed
  entirely by your agreement with those platforms.
- You must comply with the Terms of Service of
  [Cloudinary](https://cloudinary.com/tos) and [ImageKit](https://imagekit.io/terms).
- You are solely responsible for all API usage, storage consumption, bandwidth charges, and
  any activity on your account that results from uploads made through this tool.
- This tool and its developer are **not affiliated with, endorsed by, sponsored by, or
  responsible for** Cloudinary or ImageKit in any capacity.

---

### 5. Your Content

- All content you enter (name, bio, links, images, etc.) belongs entirely to you.
- You confirm that you own or have the right to use any images or materials you submit.
- The developer of this tool takes no ownership of and bears no responsibility for the
  content you generate or download.

---

### 6. Security & Clearing Your Fields *(Important)*

This tool processes your form data and any API credentials you enter on the server hosting
this application (see Privacy Policy §2 for technical details). To protect your credentials:

| Safeguard | When it applies |
|---|---|
| **Auto-clear** — all fields and keys wiped from server memory | Immediately after **Download JSON** is clicked |
| **Manual clear** — "🗑️ Clear All Fields" button | Any time you choose |
| **Session end** — all session data discarded by the server | When you close the tab or the session times out |

> ⚠️ **Always click "Clear All Fields" or close this tab after downloading your JSON —
> especially on a shared or public computer.** The auto-clear on download is a safety net,
> not a substitute for mindful use of your own credentials.

---

### 7. No Warranty

This tool is provided **as-is** and **free of charge**, with no guarantees of uptime,
correctness, or fitness for any particular purpose. The developer reserves the right to modify,
update, or discontinue the tool at any time without prior notice.

---
---

## Privacy Policy

**Last updated: March 2026**

---

### 1. How This App Works (Technical Context)

This is a **server-rendered web application** built with Streamlit. Unlike a static website,
your inputs are processed by a Python server — this is how all Streamlit apps function.
Understanding this is important context for the sections below.

If you are using the **local copy** from the Portfolio Template ZIP, the "server" is your own
machine — nothing leaves your computer unless you trigger an image upload to Cloudinary or
ImageKit.

---

### 2. What Data Is Processed

When you use this tool, the following data temporarily exists in **server-side session memory**:

| Data | Purpose | Persisted to disk or database? |
|---|---|---|
| Name, bio, email, location, links, skills, etc. | Building your JSON | **No** — session only |
| Project & publication details | Building your JSON | **No** — session only |
| Cloudinary / ImageKit API keys *(if provided)* | Authenticating image uploads (BYOK) | **No** — session only |
| Uploaded image files *(if provided)* | Forwarding to your own cloud account | **No** — not stored |

"Session only" means the data lives in server memory **only while your session is active**. It
is never written to a database, log file, or any form of persistent storage by this tool.

---

### 3. API Keys & Credentials (BYOK)

This tool follows a strict BYOK model — it has no keys of its own.

- If you provide Cloudinary or ImageKit credentials, they are stored in **server-side session
  memory** solely to authenticate upload requests to those services on your behalf.
- Credentials are **never** logged, written to disk, sent to any analytics service, or
  shared with any party other than the specific cloud service you selected.
- Credentials are permanently erased from server memory the moment you click **Download JSON**
  (auto-clear) or **Clear All Fields**.

---

### 4. Image Uploads

- Uploaded images are temporarily held in session memory and then forwarded directly to
  **your own** Cloudinary or ImageKit account using the credentials you provided.
- The developer of this tool has no access to your cloud storage and cannot view, modify,
  or delete content within your account.

---

### 5. No Tracking, No Cookies, No Analytics

- This tool does **not** use cookies, tracking pixels, or third-party analytics scripts.
- No personal data is transmitted to any advertising or analytics platform.
- No user accounts or profiles are created at any point.

---

### 6. Data Retention

All session data — including any API keys you entered — is discarded:
- Automatically, the moment you click **Download JSON**.
- When you click **Clear All Fields**.
- When your session ends (tab closed or session timeout).

There is no data to delete or request on your behalf because nothing is ever stored beyond
your active session.

---

### 7. Children's Privacy

This tool is not directed at children under the age of 13 and does not knowingly process
personal data from minors.

---

### 8. Changes to This Policy

If these Terms or this Privacy Policy are updated, the "Last updated" date above will reflect
that change. Continued use of the tool after any update constitutes acceptance of the revised
terms.

---

### 9. Questions & Support

For guidance on using this tool or the Portfolio Template, refer to the **Documentation**
included in the Portfolio Template ZIP file.

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
