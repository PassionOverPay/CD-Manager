import streamlit as st
from typing import List, Optional
import pandas as pd
from CD import CD
from CDRepository import CDRepository
from CDService import CDService

def init_state():
    """Initialize the Service and Repository in Streamlit Session State"""
    if 'service' not in st.session_state:
        repo = CDRepository()
        # Auto-load on startup
        repo.loadData("cd_library.json")
        st.session_state.service = CDService(repo)

def display_interactive_cds(cd_list, key_suffix="default"):
    """
    Displays CDs in an editable table with a 'Finalized' toggle.
    Updates the backend service automatically on change.
    
    Args:
        cd_list: List of CD objects
        key_suffix: Unique string to prevent duplicate widget ID errors
    """
    if not cd_list:
        st.info("No CDs found matching criteria.")
        return

    service = st.session_state.service

    # Prepare data for display
    data = []
    for cd in cd_list:
        d = cd.to_dict()
        # Create a logical 'Finalized' field based on 'is_open'
        d['Finalized'] = not d['is_open'] 
        data.append(d)
    
    df = pd.DataFrame(data)

    # Rename columns for friendly display
    # We map 'Finalized' to the editable checkbox
    column_config = {
        "Finalized": st.column_config.CheckboxColumn(
            "Finalized?",
            help="Check to finalize this CD",
            default=False,
        ),
        "id": "ID", "name": "Name", "size": "Total Size (MB)", 
        "encryption_speed": "Speed (x)", "occupied_space": "Occupied (MB)",
        "free_space": "Free (MB)", "session_count": "Sessions", 
        "session_type": "Type"
    }

    # Display the editor
    # We disable editing for all columns EXCEPT 'Finalized'
    # We use f-string for the key to ensure uniqueness across tabs
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        disabled=["id", "name", "size", "encryption_speed", "occupied_space", "free_space", "session_count", "session_type"],
        hide_index=True,
        use_container_width=True,
        key=f"cd_editor_{key_suffix}" # Unique key fix
    )

    # --- Sync Changes Logic ---
    # We iterate through the edited dataframe to sync changes back to the service
    # This is a simple sync: it updates the objects based on the checkbox state
    if not edited_df.empty:
        for index, row in edited_df.iterrows():
            cd_id = int(row['id'])
            is_finalized = bool(row['Finalized'])
            
            # Call service to update the actual object
            service.update_status(cd_id, is_finalized)


def main():
    st.set_page_config(page_title="My CD Library", page_icon="💿", layout="wide")
    init_state()
    service = st.session_state.service

    # --- Sidebar Navigation ---
    st.sidebar.title("💿 CD Manager")
    page = st.sidebar.radio("Navigate", ["Library", "Add CD", "Reports", "Settings"])

    # --- Page: Library (Home) ---
    if page == "Library":
        st.title("My CD Collection")
        
        # Search Bar
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search by ID or Name", placeholder="Enter ID (e.g., 1) or Name...")
        
        # Logic to decide what to show
        if search_query:
            if search_query.isdigit():
                # Search by ID
                result = service.find_by_id(int(search_query))
                results = [result] if result else []
            else:
                # Search by Name (simple contains)
                results = [cd for cd in service.get_all_cds() if search_query.lower() in cd.name.lower()]
            
            st.subheader(f"Search Results ({len(results)})")
            display_interactive_cds(results, key_suffix="search")
        else:
            # Show All
            st.subheader("All Discs")
            display_interactive_cds(service.get_all_cds(), key_suffix="library")

        # Quick Delete Action
        st.divider()
        with st.expander("Delete a CD"):
            del_id = st.number_input("Enter ID to delete", min_value=1, step=1)
            if st.button("Delete CD", type="primary"):
                if service.delete_cd(del_id):
                    st.success(f"CD {del_id} deleted!")
                    st.rerun() # Refresh to show changes
                else:
                    st.error("ID not found.")

    # --- Page: Add CD ---
    elif page == "Add CD":
        st.title("Add New CD")
        
        with st.form("add_cd_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("CD Name")
                size = st.number_input("Total Size (MB)", min_value=0.0, value=700.0)
                speed = st.number_input("Write Speed (x)", min_value=1, value=52)
            with col2:
                occupied = st.number_input("Occupied Space (MB)", min_value=0.0, value=0.0)
                sessions = st.number_input("Session Count", min_value=1, value=1)
                sType = st.selectbox("Session Type", ["Data", "Audio", "Mixed", "Finalized"])

            submitted = st.form_submit_button("Add to Library")
            
            if submitted:
                if not name:
                    st.error("Name is required.")
                elif occupied > size:
                    st.error("Occupied space cannot exceed total size.")
                else:
                    success = service.add(name, size, speed, occupied, sessions, sType)
                    if success:
                        st.success(f"'{name}' added successfully!")
                    else:
                        st.error("Failed to add CD.")

    # --- Page: Reports ---
    elif page == "Reports":
        st.title("📊 Dashboard")
        
        all_cds = service.get_all_cds()
        
        if not all_cds:
            st.info("No data available for dashboard.")
        else:
            # --- KPIs ---
            total_cds = len(all_cds)
            total_storage_mb = sum(cd.size for cd in all_cds)
            total_occupied_mb = sum(cd.occupied_space for cd in all_cds)
            efficiency_pct = (total_occupied_mb / total_storage_mb * 100) if total_storage_mb > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total CDs", total_cds)
            col2.metric("Total Storage", f"{total_storage_mb/1024:.2f} GB")
            col3.metric("Storage Efficiency", f"{efficiency_pct:.1f}%")

            st.divider()

            # --- Charts ---
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("💾 Space Utilization")
                # Create a DataFrame for the chart
                chart_data = pd.DataFrame([
                    {"Name": cd.name, "Occupied": cd.occupied_space, "Free": cd.getFreeSpace}
                    for cd in all_cds
                ])
                # We want a stacked bar chart-like view? 
                # Let's simple show Top 5 Fullest CDs
                top_5_full = sorted(all_cds, key=lambda x: x.occupied_space, reverse=True)[:5]
                top_5_data = pd.DataFrame([
                    {"CD Name": cd.name, "Occupied (MB)": cd.occupied_space} 
                    for cd in top_5_full
                ])
                st.bar_chart(top_5_data.set_index("CD Name"))
                st.caption("Top 5 CDs by Usage")

            with col_chart2:
                st.subheader("💿 Session Types")
                # Fix: Explicitly format data for bar_chart to avoid Index errors
                types = [cd.session_type for cd in all_cds]
                if types:
                    # Create a simple DataFrame mapping Type -> Count
                    counts = pd.Series(types).value_counts().reset_index()
                    counts.columns = ["Type", "Count"]
                    st.bar_chart(counts.set_index("Type"))
                else:
                    st.text("No data")
                st.caption("Distribution of Session Types")

            st.divider()
            
            # --- Detailed Views (Existing Tabs) ---
            st.expander("Detailed Reports", expanded=False).write("Expand to see detailed lists.")
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sort Name", "Sort Size", "Sort Speed", "Free Space", "Open Sessions"])
            
            with tab1:
                st.caption("Sorted Alphabetically")
                display_interactive_cds(service.sortByName(), key_suffix="sort_name")
                
            with tab2:
                st.caption("Sorted by Total Size (Descending)")
                display_interactive_cds(service.sortBySize(), key_suffix="sort_size")
                
            with tab3:
                st.caption("Sorted by Write Speed (Descending)")
                display_interactive_cds(service.sortBySpeed(), key_suffix="sort_speed")
                
            with tab4:
                st.caption("Filter by available storage")
                min_mb = st.slider("Minimum Free Space (MB)", 0, 1000, 100)
                display_interactive_cds(service.filterByFreeSpace(min_mb), key_suffix="filter_space")
                
            with tab5:
                st.caption("Discs that are not finalized")
                display_interactive_cds(service.get_open_sessions(), key_suffix="open_sessions")

    # --- Page: Settings (Save/Load) ---
    elif page == "Settings":
        st.title("Settings")
        st.write("Data is saved to `cd_library.json`.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save to File", use_container_width=True):
                if service.save("cd_library.json"):
                    st.success("Library saved successfully!")
                else:
                    st.error("Could not save file.")
                    
        with col2:
            if st.button("📂 Reload from File", use_container_width=True):
                if service.load("cd_library.json"):
                    st.success("Library reloaded!")
                    st.rerun() # Refresh app
                else:
                    st.error("Could not load file.")

if __name__ == "__main__":
    main()