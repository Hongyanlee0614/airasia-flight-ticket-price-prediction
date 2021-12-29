from datetime import time
import streamlit as st

def app():
    st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
    )
    query_params = st.experimental_get_query_params()
    tabs = ["About", "User Guide", "Contact"]
    if "tab" in query_params:
        active_tab = query_params["tab"][0]
    else:
        active_tab = "About"

    if active_tab not in tabs:
        active_tab = "About"

    li_items = "".join(
        f"""
        <li class="nav-item">
            <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
        </li>
        """
        for t in tabs
    )
    tabs_html = f"""
        <ul class="nav nav-tabs">
        {li_items}
        </ul>
    """

    st.markdown(tabs_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if active_tab == "About":
        st.write("Travelaysia is an AirAsia flight price prediction and comparison website that serves as a platform for the target users (All Malaysians or people) to plan for their future flights.")
        st.write("As most of us have known, flight ticket prices fluctuate quite frequently. It would be better if we can develop some sort of understanding about the current flight ticket price to see if it is extremely more expensive than the normal price. By comparing the current price in real AirAsia flight booking website, for example [this link](https://www.airasia.com/select/en/gb/JHB/PEN/2022-02-19/N/1/0/0/O/N/MYR/ST) to the price predicted in the website, the users can see whether the current price for the flight is considered expensive or not. It can help them plan for the time of the flight and decide which flight to take.")
        st.write("This website is developed fully using Python. You can find the developer information in the Contact tab in case you have any suggestion on how to improve the website or if you have any enquiry. Please click on the User Guide tab to understand how to use each section of this website.")
        st.write("This website was last updated on 31 December 2021. Please note that this website is served as a reference only. The developer is not responsible for any money waste during flight bookings.")
        if st.sidebar.button("Click for Surprise!"):
            st.balloons()
            st.sidebar.audio('AirAsia boarding announcement.mp3')

    elif active_tab == "User Guide":
        st.subheader("Home Page")
        st.write("At About tab, you can understand the motivation behind the development of this website and the first step that you should take for the first time entering this website.")
        st.write("At User Guide tab (you are currently here), you can have a rough understanding on what each page means and what to be clicked on.")
        st.write("At Contact tab, you can view the developer's information such as GitHub and LinkedIn.")
        
        st.subheader("Visualization Page")
        st.write("You can tick the checkbox \"Display Raw Data\" to display all raw flight information in table form. You can further interact with the table displayed by clicking the hamburger icon (three horizontal lines) to filter the data shown. You can download the data later on.")
        
        st.write("You can also select any chart type from the list on the sidebar to view some visualizations related to the data.")
        
        st.subheader("Analysis Page")
        st.write("This page shows some statistical analysis results related to the data based on questions such as \"Is the number of stops causing a significant difference in ticket price?\". So, unless you are a math geek or statistic geek, you will less likely to find this page useful.")
        
        st.subheader("Make a Prediction Page")
        st.write("This page is the core page for the entire website. Here is where you can input the departure date, departure hour, departure minute, departure location, destination location and number of stops to predict the ticket price. A interpretation plot will also be generated so that the user will understand what feature causes the price and by how much is the effect.")
    elif active_tab == "Contact":
        st.write("""    """)
        st.write(''' ***Built by LEE HONG YAN***  ''')
        st.write(''' ***Email*** : mailto:hongyanlee0614@gmail.com ''')
        st.write(''' ***Linkedin*** : https://www.linkedin.com/in/leehongyan ''')
        st.write(''' ***Github*** : https://github.com/Hongyanlee0614 ''')
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("2021 © All Rights Reserved")
    else:
        st.error("Something has gone terribly wrong.")