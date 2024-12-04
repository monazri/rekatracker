import os
import json
from datetime import datetime

def load_projects_data():
    """Load projects data from JSON file"""
    try:
        with open('projects_data.json', 'r') as f:
            content = f.read()
            if content.strip():  # Check if file is not empty
                st.session_state.projects = json.load(f)
            else:
                st.session_state.projects = {}
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.projects = {}

def save_project_data(project_name):
    """Save project data to JSON file"""
    if not project_name:
        st.error("Please enter a project name")
        return

    try:
        # First try to load existing data
        if os.path.exists('projects_data.json'):
            with open('projects_data.json', 'r') as f:
                content = f.read()
                if content.strip():
                    existing_data = json.load(f)
                else:
                    existing_data = {}
        else:
            existing_data = {}

        # Update with new project data
        existing_data[project_name] = {
            'development_data': {
                'gdv': gdv,
                'gdc': gdc,
                'status': status,
                # ... rest of your project data ...
            },
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save updated data
        with open('projects_data.json', 'w') as f:
            json.dump(existing_data, f)
        st.success(f'Project "{project_name}" saved successfully!')
    except Exception as e:
        st.error(f"Error saving project data: {str(e)}")
