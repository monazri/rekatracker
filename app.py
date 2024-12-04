import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Initialize session state
if 'projects' not in st.session_state:
    st.session_state.projects = {}

def calculate_metrics(projects):
    total_gdv = sum(project['development_data'].get('gdv', 0) for project in projects.values())
    total_gdc = sum(project['development_data'].get('gdc', 0) for project in projects.values())
    total_gpm = total_gdv - total_gdc
    gpm_percentage = (total_gpm / total_gdv * 100) if total_gdv > 0 else 0

    status_counts = {}
    for project in projects.values():
        status = project['development_data'].get('status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        'total_gdv': total_gdv,
        'total_gdc': total_gdc,
        'total_gpm': total_gpm,
        'gpm_percentage': gpm_percentage,
        'status_counts': status_counts
    }

def save_project(project_name, project_data):
    st.session_state.projects[project_name] = {
        'development_data': project_data,
        'timestamp': datetime.now().isoformat()
    }

def main():
    st.title("Project Management Dashboard")

    # Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Home", "Development", "Progress", "Sales"])

    metrics = calculate_metrics(st.session_state.projects)

    with tab1:
        st.header("Dashboard Overview")

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total GDV", f"RM{metrics['total_gdv']:,.2f}")
        with col2:
            st.metric("Total GDC", f"RM{metrics['total_gdc']:,.2f}")
        with col3:
            st.metric("Gross Profit", f"RM{metrics['total_gpm']:,.2f}")
        with col4:
            st.metric("GPM %", f"{metrics['gpm_percentage']:.1f}%")

        # Status Overview
        st.subheader("Project Status Overview")
        if metrics['status_counts']:
            fig = px.pie(
                values=list(metrics['status_counts'].values()),
                names=list(metrics['status_counts'].keys()),
                title="Project Status Distribution"
            )
            st.plotly_chart(fig)
        else:
            st.info("No projects added yet")

    with tab2:
        st.header("Add New Project")

        with st.form("new_project_form"):
            project_name = st.text_input("Project Name")
            col1, col2 = st.columns(2)
            with col1:
                gdv = st.number_input("GDV (RM)", min_value=0.0)
            with col2:
                gdc = st.number_input("GDC (RM)", min_value=0.0)

            status = st.selectbox("Status", ["Planning", "In Progress", "Completed"])

            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
            with col2:
                completion_date = st.date_input("Completion Date")

            if st.form_submit_button("Add Project"):
                if project_name:
                    project_data = {
                        'gdv': gdv,
                        'gdc': gdc,
                        'status': status,
                        'start_date': start_date.isoformat(),
                        'completion_date': completion_date.isoformat()
                    }
                    save_project(project_name, project_data)
                    st.success("Project added successfully!")
                else:
                    st.error("Please enter a project name")

    with tab3:
        st.header("Project Progress")

        if st.session_state.projects:
            for name, project in st.session_state.projects.items():
                with st.expander(f"Project: {name}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Status: {project['development_data']['status']}")
                        st.write(f"Start Date: {project['development_data']['start_date']}")
                        st.write(f"Completion Date: {project['development_data']['completion_date']}")
                    with col2:
                        st.write(f"GDV: RM{project['development_data']['gdv']:,.2f}")
                        st.write(f"GDC: RM{project['development_data']['gdc']:,.2f}")
                        gpm = project['development_data']['gdv'] - project['development_data']['gdc']
                        st.write(f"GPM: RM{gpm:,.2f}")
        else:
            st.info("No projects to display")

    with tab4:
        st.header("Sales Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Financial Summary")
            st.write(f"Total GDV: RM{metrics['total_gdv']:,.2f}")
            st.write(f"Total GDC: RM{metrics['total_gdc']:,.2f}")
            st.write(f"Total GPM: RM{metrics['total_gpm']:,.2f}")
            st.write(f"GPM %: {metrics['gpm_percentage']:.1f}%")

        with col2:
            st.subheader("Project Status Distribution")
            if metrics['status_counts']:
                for status, count in metrics['status_counts'].items():
                    st.write(f"{status}: {count}")
            else:
                st.info("No projects added yet")

        # Financial Trends
        if st.session_state.projects:
            st.subheader("Financial Trends")
            df = pd.DataFrame([
                {
                    'Project': name,
                    'GDV': project['development_data']['gdv'],
                    'GDC': project['development_data']['gdc'],
                    'GPM': project['development_data']['gdv'] - project['development_data']['gdc']
                }
                for name, project in st.session_state.projects.items()
            ])

            fig = go.Figure()
            fig.add_trace(go.Bar(name='GDV', x=df['Project'], y=df['GDV']))
            fig.add_trace(go.Bar(name='GDC', x=df['Project'], y=df['GDC']))
            fig.add_trace(go.Bar(name='GPM', x=df['Project'], y=df['GPM']))
            fig.update_layout(barmode='group', title='Project Financial Comparison')
            st.plotly_chart(fig)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Project Management Dashboard",
        page_icon="📊",
        layout="wide"
    )
    main()
