# app.py

import streamlit as st
import pandas as pd
from datetime import datetime
import json

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
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing data
if 'project_data' not in st.session_state:
    st.session_state.project_data = {}

def save_project_data():
    """Save project data to JSON file"""
    with open('project_data.json', 'w') as f:
        json.dump(st.session_state.project_data, f)
    st.success('Data saved successfully!')

def load_project_data():
    """Load project data from JSON file"""
    try:
        with open('project_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Main app layout
st.title('Project Management Dashboard')

# Create tabs
tab1, tab2, tab3 = st.tabs(['Development Data', 'Development Progress', 'Sales Progress'])

with tab1:
    st.header('Development Data')

    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        # Financial Information
        gdv = st.number_input('Total Gross Development Value (RM)', 
                            min_value=0.0, 
                            format='%f')
        gdc = st.number_input('Total Gross Development Cost (RM)', 
                            min_value=0.0, 
                            format='%f')

        if gdv > 0:
            gpm = gdv - gdc
            gpm_percentage = (gpm / gdv) * 100
            st.info(f'Gross Profit Margin: RM {gpm:,.2f} ({gpm_percentage:.2f}%)')

        status = st.selectbox('Development Status',
                            ['Pre-Development', 'Construction', 'Post-Contract'])

        land_owner = st.text_input('Land Owner')
        developer = st.text_input('Developer')
        location = st.text_area('Location')

    with col2:
        # Land Information
        land_size = st.number_input('Land Size (acres)', 
                                  min_value=0.0,
                                  format='%f')
        st.info(f'Land Size (sqft): {land_size * 43560:,.2f}')

        plot_ratio = st.number_input('Plot Ratio / Density',
                                   min_value=0.0,
                                   format='%f')

        land_title = st.selectbox('Land Title',
                                ['Freehold Residential',
                                 'Freehold Commercial',
                                 'Leasehold Residential',
                                 'Leasehold Commercial',
                                 'Malay Reserve Land',
                                 'Malaysia Agricultural Settlement (MAS)'])

        dev_type = st.selectbox('Development Type',
                              ['Master Planning',
                               'Landed Residential',
                               'High-rise Residential',
                               'Commercial / Retail'])

        dev_requirement = st.selectbox('Development Requirement',
                                     ['Open',
                                      'RUMAWIP',
                                      'RSKU',
                                      'PRIMA',
                                      'PPAM'])

    # Building Details
    st.subheader('Building Details')
    col3, col4 = st.columns(2)

    with col3:
        gfa = st.number_input('Total Gross Floor Area (sqft)',
                            min_value=0.0,
                            format='%f')
        nfa = st.number_input('Total Nett Floor Area (sqft)',
                            min_value=0.0,
                            format='%f')

    with col4:
        parking = st.number_input('Total Parking Allocation (no.)',
                                min_value=0,
                                step=1)

    # Consultants Section
    st.subheader('Consultants')
    consultants = {}
    consultant_types = [
        'Project Management Consultant',
        'Master Planner',
        'Architect',
        'Civil & Structural Engineer',
        'Mechanical & Electrical Engineer',
        'Quantity Surveyor',
        'Land Surveyor',
        'Landscape Architect',
        'Geotechnical Engineer',
        'Retail/Market Consultant',
        'Interior Design'
    ]

    for consultant in consultant_types:
        consultants[consultant] = st.text_input(consultant)

with tab2:
    st.header('Development Progress')

    if status == 'Pre-Development':
        design_progress = st.slider('Design Progress (%)',
                                  0, 100, 0)
        submission_status = st.selectbox('Submission Status',
                                       ['Not Submitted',
                                        'Submitted',
                                        'Approved',
                                        'Rejected'])

    elif status == 'Construction':
        st.subheader('Contract Details')

        contractor_name = st.text_input('Contractor Name')
        contract_period = st.number_input('Contract Period (months)',
                                        min_value=0,
                                        step=1)

        col5, col6 = st.columns(2)

        with col5:
            site_possession = st.date_input('Site Possession Date')
            completion_date = st.date_input('Completion Date')

        with col6:
            contract_amount = st.number_input('Contract Amount (RM)',
                                            min_value=0.0,
                                            format='%f')
            paid_amount = st.number_input('Paid Amount (RM)',
                                        min_value=0.0,
                                        format='%f')

with tab3:
    st.header('Sales Progress')

    total_units = st.number_input('Total Units Available',
                                min_value=0,
                                step=1)
    units_sold = st.number_input('Total Units Sold',
                               min_value=0,
                               max_value=total_units if total_units > 0 else 0,
                               step=1)

    if total_units > 0:
        sales_percentage = (units_sold / total_units) * 100
        st.info(f'Sales Progress: {sales_percentage:.2f}%')

    spa_date = st.date_input('First Sales & Purchase Agreement Signed')
    handover_date = st.date_input('Hand Over / Vacant Possession Date')

# Save Button
if st.button('Save Project Data'):
    st.session_state.project_data = {
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
        }
    }
    save_project_data()
