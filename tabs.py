import streamlit as st  # Importing the Streamlit library
from streamlit_option_menu import option_menu  # Importing a custom module for creating an option menu
import pandas as pd
import plotly.express as px

standard_values = {
    'Road': 0.000163, 'Road_supp': 0.000163,
    'Rail': 0.000046, 'Rail_supp': 0.000046,
    'Air': 0.000185, 'Air_supp': 0.000185,
    'Standard_Laptop': 0.009618, 'Standard_Laptop_supp': 0.009618,
    'HP_Laptop': 0.0133308, 'HP_Laptop_supp': 0.0133308,
    'Monitor': 0.013398, 'Monitor_supp': 0.013398,
    'Desktop': 0.073017, 'Desktop_supp': 0.073017,
    'Smartphone': 0.0015, 'Smartphone_supp': 0.0015,
    'Router': 0.053, 'Router_supp': 0.053,
    'Hotel': 0.02262, 'Hotel_supp': 0.02262,
    'Building': 0.056028, 'Building_supp': 0.056028,
    'Video_Conference': 0.00000193, 'Video_Conference_supp': 0.00000193,
    'Data_Transmission': 0.001, 'Data_Transmission_supp': 0.001,
    'Email': 0.000017, 'Email_supp': 0.000017,
    'Data_Storage': 0.221, 'Data_Storage_supp': 0.221,

    'Price_CO2_Certificate': 30, 'Price_CO2_Filtering': 696
    }


def home():
    st.header("Hi! We should work together & take care of Mother Earth")
    #st.image("earth.png")


def add_attribute_data(input_1, input_2, input_3, view_name):
    if view_name in ["Road", "Road_supp", "Rail", "Rail_supp", "Air", "Air_supp"]:
        data = {
            "distance": 2*input_1,
            "people": input_2,
            "meetings": input_3,
        }
    elif view_name in ["Standard_Laptop", "Standard_Laptop_supp",
                       "HP_Laptop", "HP_Laptop_supp",
                       "Monitor", "Monitor_supp",
                       "Desktop", "Desktop_supp",
                       "Smartphone", "Smartphone_supp"
                       ]:
        data = {
            "people": input_2,
            "number_of_devices": input_3,
        }
    elif view_name in ["Router", "Router_supp"]:
        data = {
            "number_of_devices": input_3,
        }
    elif view_name in ["Hotel", "Hotel_supp"]:
        data = {
            "people": input_2,
            "nights": input_3,
        }
    elif view_name in ["Building", "Building_supp"]:
        data = {
            "area": input_1,
            "people": input_2,
            "year": input_3,
        }
    elif view_name in ["Video_Conference", "Video_Conference_supp"]:
        data = {
            "hours": input_1,
            "people": input_2,
            "number": input_3,
        }
    elif view_name in ["Data_Transmission", "Data_Transmission_supp"]:
        data = {
            "people": input_2,
        }
    elif view_name in ["Email", "Email"]:
        data = {
            "emails": input_1,
            "people": input_2,
            "number": input_3,
        }
    elif view_name in ["Data_Storage", "Data_Storage_supp"]:
        data = {
            "size": input_2,
        }

    if 'views' not in st.session_state:
        st.session_state.views = []

    if any(not value for value in data.values()):
        st.error("All fields are required. Please complete the form.")

    else:
        for view in st.session_state['views']:
            if view['view_name'] == view_name:
                st.write("Updated Entry")
                if 'properties' not in view:
                    view['properties'] = [data]  # Initialize with the new data if empty
                else:
                    # Replace the properties entirely or update a specific property
                    view['properties'] = [data]  # Replace all properties with new data
                break
        else:
            st.write("New Entry")
            view = {
                "view_name": view_name,
                "properties": [data]
            }
            st.session_state['views'].append(view)
        st.write(st.session_state['views'])


def results():
    if st.button("Calculate", use_container_width=1):
        st.header("Calculated Results")

        try:
            # Initialize domain-wise cumulative emissions
            domain_totals = {
                "Transport": 0,
                "Electronic Devices": 0,
                "Hotel": 0,
                "ICT": 0,
                "Building": 0
            }
            cumulative_sum = 0  # Total CO₂ emissions across all domains

            # Categorize view_names into domains
            transport_views = ["Road", "Road_supp", "Rail", "Rail_supp", "Air", "Air_supp"]
            e_devices_views = ["Standard_Laptop", "Standard_Laptop_supp", "HP_Laptop", "HP_Laptop_supp",
                               "Monitor", "Monitor_supp", "Desktop", "Desktop_supp",
                               "Smartphone", "Smartphone_supp", "Router", "Router_supp"]
            hotel_views = ["Hotel", "Hotel_supp"]
            ict_views = ["Video_Conference", "Video_Conference_supp", "Data_Transmission", "Data_Transmission_supp",
                         "Email", "Email_supp", "Data_Storage", "Data_Storage_supp"]
            building_views = ["Building", "Building_supp"]

            # Loop through views and calculate CO₂ emissions
            for view in st.session_state['views']:
                view_name = view['view_name']
                cumulative_product = 1

                # Calculate emissions for the current view
                for prop in view['properties']:
                    for key, value in prop.items():
                        cumulative_product *= int(value)
                cumulative_product *= standard_values[view_name]
                cumulative_sum += cumulative_product

                # Classify and add to the respective domain
                if view_name in transport_views:
                    domain_totals["Transport"] += cumulative_product
                elif view_name in e_devices_views:
                    domain_totals["Electronic Devices"] += cumulative_product
                elif view_name in hotel_views:
                    domain_totals["Hotel"] += cumulative_product
                elif view_name in ict_views:
                    domain_totals["ICT"] += cumulative_product
                elif view_name in building_views:
                    domain_totals["Building"] += cumulative_product

            # Display total emissions for each domain
            st.subheader("CO₂ Emissions by Domain:")
            for domain, total in domain_totals.items():
                st.write(f"**{domain}:** {total:.4f} t CO₂")

            # Display overall totals
            st.write("### Total CO₂ Emissions:")
            st.write(f"The total mass of CO₂ emitted = {cumulative_sum:.4f} t CO₂")

            # Calculate cost
            price = standard_values["Price_CO2_Certificate"] + standard_values["Price_CO2_Filtering"]
            cost = cumulative_sum * price
            st.write(f"The total cost incurred for CO₂ emissions = € {cost:.2f}")

            display_graphs(domain_totals)
            display_data()

        except KeyError as e:
            st.error(f"Invalid Input - Key error: {e}")
        except ValueError as e:
            st.error(f"Invalid Input - Value error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred. Please Start Again: {e}")


def display_graphs(domain_totals):
    """Display bar chart and pie chart for domain-wise CO₂ emissions."""
    st.subheader("Visual Representation of CO₂ Emissions")

    # Convert domain totals to a Pandas DataFrame
    df = pd.DataFrame(domain_totals.items(), columns=["Domain", "CO2_Emissions"])

    # Bar Chart
    st.write("#### CO₂ Emissions - Bar Chart")
    fig_bar = px.bar(df, x="Domain", y="CO2_Emissions",
                     title="Total CO₂ Emissions by Domain",
                     labels={"CO2_Emissions": "CO₂ Emissions (t CO₂)", "Domain": "Domain"},
                     text="CO2_Emissions")
    fig_bar.update_traces(marker_color='rgba(0, 123, 255, 0.7)', textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie Chart
    st.write("#### CO₂ Emissions - Pie Chart")
    fig_pie = px.pie(df, names="Domain", values="CO2_Emissions",
                     title="Proportion of CO₂ Emissions by Domain",
                     hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)


def display_data():
    if 'views' in st.session_state and st.session_state['views']:
        # Flatten data for display
        flattened_data = []
        for view in st.session_state['views']:
            view_name = view['view_name']
            for prop in view['properties']:
                row = {'View Name': view_name}
                row.update(prop)  # Merge property data
                flattened_data.append(row)

        # Convert to Pandas DataFrame
        df = pd.DataFrame(flattened_data)

        # Display the DataFrame
        st.write("### Current Data")
        st.dataframe(df)
    else:
        st.write("No data available to display.")


def transport():
    tab_list = [
        "Road",
        "Rail",
        "Air"
    ]
    selected = option_menu("Transport Emissions", tab_list,
                           menu_icon="cast",
                           default_index=0,
                           orientation="horizontal"
                           )

    if selected == "Road":
        road()
    elif selected == "Rail":
        rail()  # Function call to update node
    elif selected == "Air":
        air()


def road():
    # Add Attribute form
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            distance = st.number_input(f"Enter the distance travelled ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            meetings = st.number_input(f"Enter number of meetings ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(distance, people, meetings, "Road")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            distance = st.number_input(f"Enter the distance travelled ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            meetings = st.number_input(f"Enter number of meetings ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(distance, people, meetings, "Road_supp")


def rail():
    st.header("Railways")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            distance = st.number_input(f"Enter the distance travelled ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            meetings = st.number_input(f"Enter number of meetings ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(distance, people, meetings, 'Rail')

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            distance = st.number_input(f"Enter the distance travelled ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            meetings = st.number_input(f"Enter number of meetings ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(distance, people, meetings, 'Rail_supp')


def air():
    st.header("Airways")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            distance = st.number_input(f"Enter the distance travelled ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            meetings = st.number_input(f"Enter number of meetings ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(distance, people, meetings, 'Air')

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            distance = st.number_input(f"Enter the distance travelled ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            meetings = st.number_input(f"Enter number of meetings ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(distance, people, meetings, 'Air_supp')


def e_devices():
    tab_list = [
        "Std_Laptop",
        "HP_Laptop",
        "Monitor",
        "Desktop",
        "Smartphone",
        "Router"
    ]
    selected = option_menu("Electronic Device Emissions", tab_list,
                           menu_icon="cast",
                           default_index=0,
                           orientation="horizontal"
                           )

    if selected == "Std_Laptop":
        laptop_std()
    elif selected == "HP_Laptop":
        laptop_hp()
    elif selected == "Monitor":
        monitor()
    elif selected == "Desktop":
        desktop()
    elif selected == "Smartphone":
        smartphone()
    elif selected == "Router":
        router()


def laptop_std():
    st.header("Standard Laptops")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of Standard Laptops used ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Standard_Laptop")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of Standard Laptops used ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Standard_Laptop_supp")


def laptop_hp():
    st.header("High Performance Laptops")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of High Performance Laptops used ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "HP_Laptop")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of Laptops used ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "HP_Laptop_supp")


def monitor():
    st.header("Monitors")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of monitors ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Monitor")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of monitors ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Monitor_supp")


def desktop():
    st.header("Desktop")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of suppliers ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Desktop")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of suppliers ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Desktop_supp")


def smartphone():
    st.header("Smart Phones")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of suppliers ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Smartphone")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            number_of_devices = st.number_input(f"Enter number of suppliers ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, number_of_devices, "Smartphone_supp")


def router():
    st.header("Routers")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            number_of_devices = st.number_input(f"Enter number of devices ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, 1, number_of_devices, "Router")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            number_of_devices = st.number_input(f"Enter number of devices ", min_value=0)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, 1, number_of_devices, "Router_supp")


def hotel():
    st.header("Hotel")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            nights = st.number_input(f"Enter number of nights stayed ", min_value=0)

            if st.form_submit_button("Submit"):
                add_attribute_data(1, people, nights, "Hotel")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            nights = st.number_input(f"Enter number of nights stayed ", min_value=0)

            if st.form_submit_button("Submit"):
                add_attribute_data(1, people, nights, "Hotel_supp")


def ict():
    tab_list = [
        "Video_conferencing",
        "Data_transmission",
        "Email",
        "Data_storage"
    ]
    selected = option_menu("ICT", tab_list,
                           menu_icon="cast",
                           default_index=0,
                           orientation="horizontal"
                           )
    if selected == "Video_conferencing":
        videoconference()
    elif selected == "Data_transmission":
        data_transmission()
    elif selected == "Email":
        email()
    elif selected == "Data_storage":
        data_storage()


def videoconference():
    st.header("Video_Conference")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            hours = st.number_input(f"Enter number of hours ", min_value=0)
            number = st.number_input(f"Enter number of videoconferences ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(hours, people, number, "Video_Conference")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            hours = st.number_input(f"Enter number of hours ", min_value=0)
            number = st.number_input(f"Enter number of videoconferences ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(hours, people, number, "Video_Conference_supp")


def data_transmission():
    st.header("Data_Transmission")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, 1, "Data_Transmission")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, people, 1, "Data_Transmission_supp")


def email():
    st.header("E-mail")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            emails = st.number_input(f"Enter number of emails ", min_value=0)
            number = st.number_input(f"Enter number of working days ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(emails, people, number, "Email")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            people = st.number_input(f"Enter number of people ", min_value=0)
            emails = st.number_input(f"Enter number of emails ", min_value=0)
            number = st.number_input(f"Enter number of working days ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(emails, people, number, "Email_supp")


def data_storage():
    st.header("Data_Storage")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            size = st.number_input(f"Enter TB of data ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, size, 1, "Data_Storage")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            size = st.number_input(f"Enter TB of data ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(1, size, 1, "Data_Storage_supp")


def building():
    st.header("Building")
    with st.expander("OEM"):
        with st.form("add_attr_form", clear_on_submit=True):
            area = st.number_input(f"Enter area occupied by people ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            year = st.number_input(f"Enter number of year ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(area, people, year, "Building")

    with st.expander("Supplier"):
        with st.form("add_attr_form_1", clear_on_submit=True):
            area = st.number_input(f"Enter area occupied by people ", min_value=0)
            people = st.number_input(f"Enter number of people ", min_value=0)
            year = st.number_input(f"Enter number of year ", min_value=0)
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_attribute_data(area, people, year, "Building_supp")


def others():
    st.header("Miscellaneous Sources")

    if 'others' not in st.session_state:
        st.session_state.others = []

    source_name = st.text_input("Enter name of the source")
    source_coff = st.number_input("Enter coefficient of the CO2 emission of source")

    add_view_button = st.button("Add Source")
    if add_view_button:
        with st.form("add_attr_form", clear_on_submit=True):
            prop_col, val_col = st.columns(2)

            with prop_col:
                property_1 = st.text_input(f"Enter Property 1 ")
                property_2 = st.text_input(f"Enter Property 2")
                property_3 = st.text_input(f"Enter Property 3 ")

            with val_col:
                val_1 = st.number_input(f"Enter value 1", min_value=1)
                val_2 = st.number_input(f"Enter value 2", min_value=1)
                val_3 = st.number_input(f"Enter value 3", min_value=1)

            # Check if the form is submitted
            if st.form_submit_button("Submit"):
                # Call the add_attribute_data function with the entered values
                add_other_attribute_data(property_1, val_1, property_2, val_2, property_3, val_3, source_coff, source_name)
    st.write(st.session_state['others'])


def add_other_attribute_data(prop_1, val_1, prop_2, val_2, prop_3, val_3, view_coff, view_name):
    data = {
        prop_1: val_1,
        prop_2: val_2,
        prop_3: val_3
    }

    if 'others' not in st.session_state:
        st.session_state.others = []

    for view in st.session_state['others']:
        if view['view_name'] == view_name:
            st.write("Updated Entry")
            if 'properties' not in view:
                view['properties'] = []
            view['properties'] = [data]
            break
    else:
        st.write("New Entry")
        view = {
            "view_name": view_name,
            "properties": [data]
        }
        st.session_state['others'].append(view)
    st.write(st.session_state['others'])
