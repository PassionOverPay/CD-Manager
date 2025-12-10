import streamlit as st
from typing import List, Optional
import pandas as pd
from CD import CD
from CDRepository import CDRepository
from CDService import CDService

DATA_FILE = "cd_library.json"

def init_state():
    """Initialize the Service and Repository in Streamlit Session State"""
    if 'service' not in st.session_state:
        repo = CDRepository()
        # Auto-load on startup
        repo.loadData("F:/repo/MSIC_CD-Tracker/cd_library.json")
        st.session_state.service = CDService(repo)

def display_cds(cd_list: List[CD]):
    """Helper to display a list of CDs as a nice DataFrame"""
    if not cd_list:
        st.info("No CDs found matching criteria.")
        return

    # Convert objects to pandas DataFrame for pretty display
    data = [cd.to_dict() for cd in cd_list]
    df = pd.DataFrame(data)
    
    # Rename columns for display
    df.rename(columns={
        "id": "ID", "name": "Name", "size": "Total Size (MB)", 
        "encryption_speed": "Speed (x)", "occupied_space": "Occupied (MB)",
        "free_space": "Free (MB)", "session_count": "Sessions", 
        "session_type": "Type", "is_open": "Writable"
    }, inplace=True)
    
    st.dataframe(df, use_container_width=True, hide_index=True)

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
            display_cds(results)
        else:
            # Show All
            st.subheader("All Discs")
            display_cds(service.get_all_cds())

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
        st.title("📊 Reports & Analytics")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sort Name", "Sort Size", "Sort Speed", "Free Space", "Open Sessions"])
        
        with tab1:
            st.caption("Sorted Alphabetically")
            display_cds(service.sortByName())
            
        with tab2:
            st.caption("Sorted by Total Size (Descending)")
            display_cds(service.sortBySize())
            
        with tab3:
            st.caption("Sorted by Write Speed (Descending)")
            display_cds(service.sortBySpeed())
            
        with tab4:
            st.caption("Filter by available storage")
            min_mb = st.slider("Minimum Free Space (MB)", 0, 1000, 100)
            display_cds(service.filterByFreeSpace(min_mb))
            
        with tab5:
            st.caption("Discs that are not finalized")
    # --- Page: Settings (Save/Load) ---
    elif page == "Settings":
        st.title("Settings")
        st.write(f"Data is saved to `{DATA_FILE}`.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save to File", use_container_width=True):
                if service.save(DATA_FILE):
                    st.success("Library saved successfully!")
                else:
                    st.error("Could not save file.")
                    
        with col2:
            if st.button("📂 Reload from File", use_container_width=True):
                if service.load(DATA_FILE):
                    st.success("Library reloaded!")
                    st.rerun() # Refresh app
                else:
                    st.error("Could not load file.")
                
if __name__ == "__main__":
    main()