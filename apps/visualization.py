import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid
import time
from datetime import datetime

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

def app():
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.checkbox('Display Raw Data'):
        # raw data
        st.subheader("Raw Data")
        st.write("Airasia flight information dataset from 24 October to XXX")
        
        with st.spinner('Loading flights data...'):
            df_raw = pd.read_csv('Airasia Domestic Flight Tickets.csv')
            time.sleep(3)
            st.success('Done!')
        
        # st.dataframe(df_raw) 
        AgGrid(df_raw)
            
        # download box
        csv = convert_df(df_raw)
        st.download_button(label="Download", data=csv, file_name='AirAsia Flights.csv', mime='text/csv')
      
    
    # dataframe for EDA
    df = pd.read_csv('Airasia Domestic Flight Tickets Cleaned (for EDA).csv')
        
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    st.sidebar.subheader("Please Select a Chart Type:")
    st.sidebar.caption("You will be seeing some example visualizations of the chart type you have chosen.")
    graph_type = st.sidebar.selectbox(" " , ['Bar', 'Box', 'Line', 'Highlight Table', 'Histogram'])
    
    # dashboard
    st.write("*If you wish to interact with the visualizations, please visit this [link](https://public.tableau.com/app/profile/lee.hong.yan/viz/visualization_16406974784720/AirAsiaFlightAnalysis).*")
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.subheader("Reference:")
    st.sidebar.caption("AOR - Sultan Abdul Halim Airport, Alor Setar, Kedah")
    st.sidebar.caption("BKI - Kota Kinabalu International Airport, Sabah")
    st.sidebar.caption("BTU - Bintulu Airport, Sarawak")
    st.sidebar.caption("IPH - Sultan Azlan Shah Airport, Ipoh, Perak")
    st.sidebar.caption("JHB - Senai International Airport, Johor Bahru, Johor")
    st.sidebar.caption("KBR - Sultan Ismail Petra Airport, Kota Bharu, Kelantan")
    st.sidebar.caption("KCH - Kuching International Airport, Sarawak")
    st.sidebar.caption("KUL - Kuala Lumpur International Airport, Sepang, Selangor")
    st.sidebar.caption("LBU - Labuan Airport")
    st.sidebar.caption("LGK - Langkawi International Airport, Kedah")
    st.sidebar.caption("MYY - Miri International Airport, Sarawak")
    st.sidebar.caption("PEN - Penang International Airport")
    st.sidebar.caption("SBW - Sibu Airport, Sarawak")
    st.sidebar.caption("SDK - Sandakan Airport, Sabah")
    st.sidebar.caption("TGG - Sultan Mahmud Airport, Kuala Terengganu, Terengganu")
    st.sidebar.caption("TWU - Tawau Airport, Sabah")
    
    if graph_type == "Box":
        # stop vs price
        with st.spinner('Loading graph 1...'):
            fig_stop_price = plt.figure(figsize=(15,8))
            sns.boxplot(x='Stop',y='Price (RM)', data=df)
            st.markdown("### Graph of number of stops against ticket price")
            plt.xlabel('Number of stops', size=20)
            plt.ylabel('Price (RM)', size=20)
            st.pyplot(fig_stop_price)
            st.write('We can clearly see that ticket price for flights with 1 stop in between is higher than those direct flights.')
    
        # break
        st.markdown("<br>", unsafe_allow_html=True)

        # departure location vs price
        with st.spinner('Loading graph 2...'):
            fig_dep_price = plt.figure(figsize=(15,5))
            sns.boxplot(x='Departure Location',y='Price (RM)',data=df)
            st.markdown("#### Graph of departure location against ticket price")
            plt.xlabel('Departure Location', size=20)
            plt.ylabel('Price (RM)', size=20)
            st.pyplot(fig_dep_price)
            st.write('We can see how distributed the price is for each departure location. The large box probably refers to the location having a wider range of destination location (East and Peninsular Malaysia). We can also see that the box for Kuala Lumpur is small, indicating it has flights to all the destinations therefore there are no stops which is more likely to burst up the price.')
           
        # break
        st.markdown("<br>", unsafe_allow_html=True)
         
        # destination location vs price
        with st.spinner('Loading graph 3...'):
            fig_dest_price = plt.figure(figsize=(15,5))
            sns.boxplot(x='Destination Location',y='Price (RM)',data=df)
            st.markdown("#### Graph of destination location against ticket price")
            plt.xlabel('Destination Location', size=20)
            plt.ylabel('Price (RM)', size=20)
            st.pyplot(fig_dest_price)
            st.write('We can see how distributed the price is for each departure location.')
    elif graph_type == 'Line':
        with st.spinner('Loading graph...'):
            st.markdown("### Graph of number of direct and 1 stop flights for each departure day")
            st.image('1.png')
            st.write('There is a slight increase of number of flights with time. This signals that there are more and more demand for flights due to the movement control that loosens as a result of vaccination progress.')
    elif graph_type == 'Bar':
        with st.spinner('Loading graph 1...'):
            st.markdown("### Graph of Number of Flights for Each Airport per Month")
            st.image('2.png')
            st.write('Langkawi Airport (as denoted by LGK) recorded the most flights for three consecutive months. This may be due to the fact that Langkawi is among the earliest tourist spots that allow for travellers. Note that there are less records for October because the data was collected starting from 24 October.')
        with st.spinner('Loading graph 2...'):
            st.markdown("### Graph of Average Price of Flights Departed at Each Hour")
            st.image('3.png')
            st.write('In average, flights departed at 9am and 4pm are more expensive.')
    elif graph_type == 'Highlight Table':
        with st.spinner('Loading graph 1...'):
            st.markdown("### Graph of Average Ticket Price (RM) for Each Route")
            st.image('4.png')
            st.write('The average most expensive flight is from Langkawi International Airport to Miri International Airport. The average least expensive flight is from Penang International Airport to Sultan Ismail Petra Airport in Kota Bharu, Kelantan .')
        with st.spinner('Loading graph 2...'):
            st.markdown("### Graph of Average Duration (Hour) for Each Route")
            st.image('5.png')
            st.write('The average longest flight duration is from Miri International Airport to Sultan Mahmud Airport in Terengganu. The average shortest flight duration is from Penang International Airport to Langkawi International Airport.')
    elif graph_type == 'Histogram':
        with st.spinner('Loading graph 1...'):
            st.markdown("### Flight Ticket Price Distribution")
            st.image('6.png')
            st.write('The distribution of flight ticket price is right-skewed. This indicates that there are price outliers in the dataset. We can also roughly see that direct flights are cheaper than flight with an intermediary stop.')
        with st.spinner('Loading graph 2...'):
            st.markdown("### Flight Duration Distribution")
            st.image('7.png')
            st.write('There is no clear shape of distribution for flight duration. However, using number of stop as the dimension we see that almost none of the direct domestic flights exceed three hours.')