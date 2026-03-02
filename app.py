import streamlit as st
import json
import cloudinary
import cloudinary.uploader
from imagekitio import ImageKit

st.set_page_config(page_title="JSON Generator", layout="wide")

st.title("Portfolio JSON Generator")

# Sidebar for API Keys
st.sidebar.header("Image Hosting Configuration")
image_service = st.sidebar.selectbox("Choose Image Service", ["None", "Cloudinary", "ImageKit"])

api_keys = {}
if image_service == "Cloudinary":
    api_keys["cloud_name"] = st.sidebar.text_input("Cloud Name")
    api_keys["api_key"] = st.sidebar.text_input("API Key")
    api_keys["api_secret"] = st.sidebar.text_input("API Secret", type="password")
elif image_service == "ImageKit":
    api_keys["public_key"] = st.sidebar.text_input("Public Key")
    api_keys["private_key"] = st.sidebar.text_input("Private Key", type="password")

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
    return None

# Form Data Collection
data = {}

# Profile Section
st.header("Profile")
col1, col2 = st.columns(2)
with col1:
    data["name"] = st.text_input("Name")
    data["headline"] = st.text_input("Headline")
    
    profile_pic_option = st.radio("Profile Picture Source", ["URL", "Upload"])
    if profile_pic_option == "URL":
        data["profile_pic"] = st.text_input("Profile Picture URL")
    else:
        uploaded_file = st.file_uploader("Upload Profile Picture", type=['jpg', 'png', 'jpeg'])
        if uploaded_file and image_service != "None":
            if st.button("Upload Profile Pic"):
                url = upload_image(uploaded_file, image_service, api_keys)
                if url:
                    st.success("Uploaded!")
                    data["profile_pic"] = url
                    st.session_state["profile_pic_url"] = url
        if "profile_pic_url" in st.session_state:
             data["profile_pic"] = st.session_state["profile_pic_url"]
             st.image(data["profile_pic"], width=100)

with col2:
    data["about"] = st.text_area("About (Description)", height=150)
    data["email"] = st.text_input("Email")
    data["location"] = st.text_input("Location")

# Skills Section
st.header("Skills")
skills_input = st.text_area("Enter skills (comma separated)", "Python, Streamlit, React, Cloudinary")
data["skills"] = [s.strip() for s in skills_input.split(",") if s.strip()]

# Projects Section
st.header("Projects")
if "projects" not in st.session_state:
    st.session_state.projects = []

with st.expander("Add New Project", expanded=True):
    p_title = st.text_input("Project Title")
    p_desc = st.text_area("Project Description")
    p_github = st.text_input("GitHub Link")
    p_live = st.text_input("Live Link")
    p_tech = st.text_input("Tech Stack (comma separated)")
    
    p_thumb_option = st.radio("Thumbnail Source", ["URL", "Upload"], key="p_thumb_radio")
    p_thumb_url = ""
    if p_thumb_option == "URL":
        p_thumb_url = st.text_input("Thumbnail URL")
    else:
        p_file = st.file_uploader("Upload Thumbnail", type=['jpg', 'png', 'jpeg'], key="p_uploader")
        if p_file and image_service != "None":
             if st.button("Upload Thumbnail"):
                url = upload_image(p_file, image_service, api_keys)
                if url:
                    st.success("Thumbnail Uploaded!")
                    p_thumb_url = url
                    st.session_state["temp_project_thumb"] = url
        if "temp_project_thumb" in st.session_state:
            p_thumb_url = st.session_state["temp_project_thumb"]
            st.image(p_thumb_url, width=100)

    if st.button("Add Project"):
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
        # Clear temp state for next entry
        if "temp_project_thumb" in st.session_state:
            del st.session_state["temp_project_thumb"]
        st.rerun()

# List Projects
if st.session_state.projects:
    st.subheader("Current Projects")
    for idx, p in enumerate(st.session_state.projects):
        st.write(f"**{idx+1}. {p['title']}**")
        st.write(p['description'])
        st.write(f"GitHub: {p['github_link']} | Live: {p['live_link']}")
        if p['thumbnail']:
            st.image(p['thumbnail'], width=100)
        if st.button(f"Remove Project {idx+1}", key=f"del_proj_{idx}"):
            st.session_state.projects.pop(idx)
            st.rerun()
        st.divider()

data["projects"] = st.session_state.projects

# Publications Section
st.header("Publications")
if "publications" not in st.session_state:
    st.session_state.publications = []

with st.expander("Add Publication"):
    pub_title = st.text_input("Publication Title")
    pub_journal = st.text_input("Journal/Conference Name")
    pub_year = st.text_input("Year")
    pub_link = st.text_input("Publication Link")
    
    if st.button("Add Publication"):
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
        if st.button(f"Remove Publication {idx+1}", key=f"del_pub_{idx}"):
            st.session_state.publications.pop(idx)
            st.rerun()

data["publications"] = st.session_state.publications

# Social Media Section
st.header("Social Media")
col3, col4 = st.columns(2)
data["social_media"] = {}
with col3:
    data["social_media"]["linkedin"] = st.text_input("LinkedIn URL")
    data["social_media"]["github"] = st.text_input("GitHub URL")
    data["social_media"]["twitter"] = st.text_input("Twitter/X URL")
with col4:
    data["social_media"]["website"] = st.text_input("Personal Website")
    other_social = st.text_input("Other (Label:URL)")
    if other_social and ":" in other_social:
        label, url = other_social.split(":", 1)
        data["social_media"][label.strip()] = url.strip()

# Generate JSON
st.header("Generate Output")
json_output = json.dumps(data, indent=4)
st.code(json_output, language="json")

st.download_button(
    label="Download JSON",
    data=json_output,
    file_name="portfolio.json",
    mime="application/json"
)
