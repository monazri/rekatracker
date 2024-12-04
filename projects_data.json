import streamlit as st
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
import plotly.graph_objects as go

# Configure the page
st.set_page_config(
    page_title="Project Management Dashboard",
    page_icon="🏗️",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing data
if 'projects' not in st.session_state:
    st.session_state.projects = {}

def save_project_data(project_name):
    """Save project data to JSON file"""
    if not project_name:
        st.error("Please enter a project name")
        return

    project_data = {
        'development_data': {
            'gdv': gdv,
            'gdc': gdc,
            'status': status,
            'land_owner': land_owner,
            'developer': developer,
            'location': location,
            'land_size': land_size,
            'plot_ratio': plot_ratio,
            'land_title': land_title,
            'dev_type': dev_type,
            'dev_requirement': dev_requirement,
            'gfa': gfa,
            'nfa': nfa,
            'parking': parking,
            'consultants': consultants
        },
        'development_progress': {
            'status': status,
            'design_progress': design_progress if status == 'Pre-Development' else None,
            'submission_status': submission_status if status == 'Pre-Development' else None,
            'contractor_name': contractor_name if status == 'Construction' else None,
            'contract_period': contract_period if status == 'Construction' else None,
            'contract_amount': contract_amount if status == 'Construction' else None,
            'paid_amount': paid_amount if status == 'Construction' else None
        },
        'sales_progress': {
            'total_units': total_units,
            'units_sold': units_sold,
            'spa_date': str(spa_date),
            'handover_date': str(handover_date)
        },
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    st.session_state.projects[project_name] = project_data

    with open('projects_data.json', 'w') as f:
        json.dump(st.session_state.projects, f)
    st.success(f'Project "{project_name}" saved successfully!')

def load_projects_data():
    """Load projects data from JSON file"""
    try:
        with open('projects_data.json', 'r') as f:
            st.session_state.projects = json.load(f)
    except FileNotFoundError:
        st.session_state.projects = {}

# Load existing projects data
load_projects_data()

# Main app layout
st.title('Project Management Dashboard')

# Create tabs
tab_home, tab1, tab2, tab3 = st.tabs(['Home Dashboard', 'Development Data', 'Development Progress', 'Sales Progress'])

with tab_home:
    st.header('Projects Overview Dashboard')

    # Calculate overall metrics
    total_gdv = sum(project['development_data']['gdv'] for project in st.session_state.projects.values())
    total_gdc = sum(project['development_data']['gdc'] for project in st.session_state.projects.values())
    total_gpm = total_gdv - total_gdc
    total_gpm_percentage = (total_gpm / total_gdv * 100) if total_gdv > 0 else 0

    # Project status counts
    status_counts = {
        'Pre-Development': 0,
        'Construction': 0,
        'Post-Contract': 0
    }
    for project in st.session_state.projects.values():
        status = project['development_data']['status']
        status_counts[status] = status_counts.get(status, 0) + 1

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Projects", len(st.session_state.projects))
    with col2:
        st.metric("Total GDV", f"RM {total_gdv:,.2f}")
    with col3:
        st.metric("Total GDC", f"RM {total_gdc:,.2f}")
    with col4:
        st.metric("Overall GPM", f"{total_gpm_percentage:.2f}%")

    # Create two columns for charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Project Status Distribution
        fig_status = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Project Status Distribution"
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with chart_col2:
        # GDV by Project
        gdv_by_project = {name: data['development_data']['gdv'] 
                         for name, data in st.session_state.projects.items()}
        fig_gdv = px.bar(
            x=list(gdv_by_project.keys()),
            y=list(gdv_by_project.values()),
            title="GDV by Project"
        )
        fig_gdv.update_layout(
            xaxis_title="Project Name",
            yaxis_title="GDV (RM)"
        )
        st.plotly_chart(fig_gdv, use_container_width=True)

    # Projects Table
    st.subheader("Projects List")
    if st.session_state.projects:
        projects_df = pd.DataFrame([
            {
                'Project Name': name,
                'Status': data['development_data']['status'],
                'GDV (RM)': data['development_data']['gdv'],
                'GDC (RM)': data['development_data']['gdc'],
                'GPM (%)': ((data['development_data']['gdv'] - data['development_data']['gdc']) / 
                           data['development_data']['gdv'] * 100) if data['development_data']['gdv'] > 0 else 0,
                'Last Updated': data['timestamp']
            }
            for name, data in st.session_state.projects.items()
        ])
        st.dataframe(projects_df, use_container_width=True)
    else:
        st.info("No projects saved yet. Add a new project using the Development Data tab.")

# [Previous tab1, tab2, tab3 code remains the same...]

# Modified save button section
with st.sidebar:
    st.header("Save Project")
    project_name = st.text_input("Project Name")
    if st.button('Save Project Data'):
        save_project_data(project_name)
