import json
try:
    import streamlit
    import cloudinary
    import cloudinary.uploader
    from imagekitio import ImageKit
    print("Imports successful")
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)

# Test logic
data = {
    "name": "Test User",
    "skills": ["Python", "AI"],
    "projects": [{
        "title": "P1", 
        "description": "Test Project",
        "tech_stack": ["Python"],
        "github_link": "http://github.com",
        "live_link": "http://example.com",
        "thumbnail": "http://example.com/img.png"
    }],
    "publications": [{
        "title": "My Paper",
        "journal": "Nature",
        "year": "2023",
        "link": "http://arxiv.org"
    }]
}
json_output = json.dumps(data, indent=4)
print("JSON generation successful")
