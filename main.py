import streamlit as st  # Importing the Streamlit library
from streamlit_option_menu import option_menu  # Importing a custom module for creating an option menu
from tabs import (home, transport, e_devices, results, hotel, building, ict, others)
# Importing functions from a custom module for various tabs

# Initialize session state variables if not present
if __name__ == '__main__':
    st.set_page_config(layout='wide')
    st.title("Calculate Co2 Emissions in Engineering")
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"]::before {
            content: "";
            display: block;
            height: 32px;
            background-image: url('bmw.png');
            background-size: contain;
            background-repeat: no-repeat;
            margin: 0 auto 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    #st.logo("bmw.png", size="large", link='https://www.bmw.de/de/index.html', icon_image=None)

    if "tab_index" not in st.session_state:
        st.session_state['tab_index'] = 0

    # List of tabs for the Streamlit app
    tab_list = [
        "Home",
        "Transport",
        "Electronic Devices",
        "Hotel",
        "ICT",
        "Office Building",
        "Others",
        "Results"
    ]

    index = st.session_state["tab_index"]

    # Create a sidebar with an option menu for selecting the main menu
    with st.sidebar:
        selected = option_menu("Main Menu", tab_list,
                               menu_icon="cast",
                               default_index=index,
                               )

        # Handle the selected tab and call the corresponding function
    if selected == "Home":
        home()  # Function call to upload graph
    elif selected == "Transport":
        transport()  # Function call to visualize the graph
    elif selected == "Electronic Devices":
        e_devices()
    elif selected == "Hotel":
        hotel()
    elif selected == "ICT":
        ict()  # Function call to store the graph
    elif selected == "Office Building":
        building()  # Function call to visualize the graph
    elif selected == "Others":
        others()  # Function call to visualize the graph
    elif selected == "Results":
        results()  # Function call to visualize the graph
