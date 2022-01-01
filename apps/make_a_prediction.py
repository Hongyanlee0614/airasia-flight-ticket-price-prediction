import streamlit as st
import pickle
import pandas as pd 
import numpy as np
import datetime
import shap
import matplotlib
import lightgbm
from matplotlib import rcParams

# make sure the feature names in shap summary plot are displayed properly 
rcParams.update({'figure.autolayout': True})
# to display shap plot in the web app

shap.initjs()

airport_list = ['Alor Setar (AOR)','Kota Kinabalu (BKI)','Bintulu (BTU)', 'Ipoh (IPH)', 'Johor Bahru (JHB)', 'Kota Bahru (KBR)', 'Kuching (KCH)', 'Kuala Lumpur (KUL)', 'Labuan (LBU)', 'Langkawi (LGK)', 'Miri (MYY)', 'Penang (PEN)', 'Sandakan (SDK)', 'Sibu (SBW)', 'Kuala Terengganu (TGG)', 'Tawau (TWU)']
source_list = ['North', 'South', 'Middle', 'Labuan', 'Sabah', 'Sarawak']
destination_list = ['North', 'South', 'Middle', 'Labuan', 'Sabah', 'Sarawak']
source_one_hot = [0,0,0,0,0,0]
destination_one_hot = [0,0,0,0,0,0]
weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

def app():
    st.title("Travelaysia")

    # Departure time
    y = pd.to_datetime("today").year
    m = pd.to_datetime("today").month
    d = pd.to_datetime("today").day
    
    st.sidebar.subheader("Departure Date")
    dep = st.sidebar.date_input("" , datetime.date(y,m,d)+ datetime.timedelta(days=3))
    if dep is not None:
        # weekday_str = dep.strftime('%A')
        # dep_weekday = weekday.index(weekday_str)
        year_d = dep.year
        mon_d = dep.month
        day_d = dep.day

        st.sidebar.subheader("Departure Hour")
        hour_d = st.sidebar.selectbox("", list(range(24)))
        st.sidebar.subheader("Departure Minute")
        minute_d = st.sidebar.selectbox("", list(range(0,60)))

    st.subheader("Departure Time :")
    x = str(year_d) + "/"  +str(mon_d) + "/" + str(day_d) + " " + str(hour_d) + ":" + str(minute_d)
    if x is not None:    
        op = pd.to_datetime([x])
        if op is not None:
            print(op.date[0] - pd.to_datetime('today').date())
            if (op.date[0] - pd.to_datetime('today').date()).days >= 3:
                st.write(op.item())
            else:
                st.error('Please choose a departure date at least 3 days later the current date.')
                st.stop()
    

    # # Arrival Time
    # st.sidebar.subheader("Select Arrival")
    # arr = st.sidebar.date_input("Arrival Date" , datetime.date(y,m,d) + datetime.timedelta(days=3))
    # if arr is not None:
    #     mon_a = arr.month
    #     day_a = arr.day

    #     hour_a = st.sidebar.selectbox("Arrival Hour", list(range(24)) ,2)
    #     minute_a = st.sidebar.selectbox("Arrival Minute", list(range(0,60)))

    # st.subheader("Arrival Time :")
    # x1 = "2021" + "/"  +str(mon_a) + "/" + str(day_a) + " " + str(hour_a) + ":" + str(minute_a)
    # if x1 is not None:
        
    #     op1 = pd.to_datetime([x1])
    #     if op1 is not None:
    #         if op1 > op:
    #             st.write(op1.item())
    #         else:
    #             st.error('Arrival Time must be larger than Departure Time')
    #             st.stop()
            

    # Departure Location
    st.sidebar.subheader("Departure Location")
    source = st.sidebar.selectbox(" " , airport_list)
    # if source == 'Labuan (LBU)':
    #     source_one_hot[0] = 1
    # elif source == 'Kuala Lumpur (KUL)':
    #     source_one_hot[1] = 1
    # elif source == 'Alor Setar (AOR)' or source == 'Ipoh (IPH)' or source == 'Langkawi (LGK)' or source == 'Penang (PEN)':
    #     source_one_hot[2] = 1
    # elif source == 'Kota Kinabalu (BKI)' or source == 'Sandakan (SDK)' or source == 'Tawau (TWU)':
    #     source_one_hot[3] = 1
    # elif source == 'Bintulu (BTU)' or source == 'Kuching (KCH)' or source == 'Miri (MYY)' or source == 'Sibu (SBW)':
    #     source_one_hot[4] = 1
    # elif source == 'Johor Bahru (JHB)':
    #     source_one_hot[5] = 1
    if source == 'Alor Setar (AOR)':
        source_code = 'AOR'
    elif source == 'Kota Kinabalu (BKI)':
        source_code = 'BKI'
    elif source == 'Bintulu (BTU)':
        source_code = 'BTU'
    elif source == 'Ipoh (IPH)':
        source_code = 'IPH'
    elif source == 'Johor Bahru (JHB)':
        source_code = 'JHB'
    elif source == 'Kota Bahru (KBR)':
        source_code = 'KBR'
    elif source == 'Kuching (KCH)':
        source_code = 'KCH'
    elif source == 'Kuala Lumpur (KUL)':
        source_code = 'KUL'
    elif source == 'Labuan (LBU)':
        source_code = 'LBU'
    elif source == 'Miri (MYY)':
        source_code = 'MYY'
    elif source == 'Penang (PEN)':
        source_code = 'PEN'
    elif source == 'Sandakan (SDK)':
        source_code = 'SDK'
    elif source == 'Sibu (SBW)':
        source_code = 'SBW'
    elif source == 'Kuala Terengganu (TGG)':
        source_code = 'TGG'
    elif source == 'Tawau (TWU)':
        source_code = 'TWU'
    st.subheader("Source:")
    st.write(source)

    # Destination Location
    st.sidebar.subheader("Destination Location")
    dest = st.sidebar.selectbox("" , filter(lambda airport: airport != source, airport_list))
    # if dest == 'Labuan (LBU)':
    #     destination_one_hot[0] = 1
    # elif dest == 'Kuala Lumpur (KUL)':
    #     destination_one_hot[1] = 1
    # elif dest == 'Alor Setar (AOR)' or dest == 'Ipoh (IPH)' or dest == 'Langkawi (LGK)' or dest == 'Penang (PEN)':
    #     destination_one_hot[2] = 1
    # elif dest == 'Kota Kinabalu (BKI)' or dest == 'Sandakan (SDK)' or dest == 'Tawau (TWU)':
    #     destination_one_hot[3] = 1
    # elif dest == 'Bintulu (BTU)' or dest == 'Kuching (KCH)' or dest == 'Miri (MYY)' or dest == 'Sibu (SBW)':
    #     destination_one_hot[4] = 1
    # elif dest == 'Johor Bahru (JHB)':
    #     destination_one_hot[5] = 1
    if dest == 'Kota Kinabalu (BKI)':
        dest_code = 'BKI'
    elif dest == 'Alor Setar (AOR)':
        dest_code = 'AOR'
    elif dest == 'Bintulu (BTU)':
        dest_code = 'BTU'
    elif dest == 'Ipoh (IPH)':
        dest_code = 'IPH'
    elif dest == 'Johor Bahru (JHB)':
        dest_code = 'JHB'
    elif dest == 'Kota Bahru (KBR)':
        dest_code = 'KBR'
    elif dest == 'Kuching (KCH)':
        dest_code = 'KCH'
    elif dest == 'Kuala Lumpur (KUL)':
        dest_code = 'KUL'
    elif dest == 'Labuan (LBU)':
        dest_code = 'LBU'
    elif dest == 'Miri (MYY)':
        dest_code = 'MYY'
    elif dest == 'Penang (PEN)':
        dest_code = 'PEN'
    elif dest == 'Sandakan (SDK)':
        dest_code = 'SDK'
    elif dest == 'Sibu (SBW)':
        dest_code = 'SBW'
    elif dest == 'Kuala Terengganu (TGG)':
        dest_code = 'TGG'
    elif dest == 'Tawau (TWU)':
        dest_code = 'TWU'
        
    st.subheader("Destination ")
    st.write(dest)

    # Number of stops
    st.sidebar.subheader("Number of Stops")
    stop = st.sidebar.selectbox("" , [0,1])
    st.subheader("Stops:")
    st.write(stop)

    # # Duration
    # st.subheader("Duration")
    # st.write((op1.item() - op.item()))
    
    # op2 = str(op1-op)
    # if op2 is not None:
    #     duration_hr = int(op2.split(']')[0][-9:-7])
    #     duration_min = int(op2.split(']')[0][-6:-4])
    #     duration = duration_hr*60 + duration_min
        
        
    # model
    rfr_model = pickle.load(open("flight_rf.pkl", "rb"))

    # prediction
    par = pd.DataFrame([[stop , source_code, dest_code, mon_d , day_d , hour_d , minute_d]], columns=['Stop', 'Source', 'Destination', 'Departure Month', 'Departure Day', 'Departure Hour', 'Departure Minute'])
    par['Source'] = par['Source'].astype('category')
    par['Destination'] = par['Destination'].astype('category')

    if st.button("PREDICT"):
        pred = rfr_model.predict(par)
        for i in pred:
            st.write("Your Fare Price is : RM" , round(i ,2)  , "")
            
            explainer = shap.TreeExplainer(rfr_model)
            shap_values = explainer.shap_values(par)
            shap.summary_plot(shap_values, par, feature_names=['Stop', 'Departure Location', 'Departure Destination', 'Departure Month', 'Departure Day', 'Departure Hour', 'Departure Minute'], max_display=7, title="Model Interpretation Plot")
            
            # disable warning
            st.subheader("Interpretation Plot")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(bbox_inches='tight')
            matplotlib.pyplot.clf()
            
            # Interpretation of the prediction model
            st.write("- This plot combines feature importance (how much weights are the variables on the prediction) with feature effects (what is the direction and strength of the variables on the prediction).")
            st.write("- All points belong to the same row of observations/instances. The vertical location shows what feature it is depicting. The horizontal location shows whether the value of the feature caused a greater or smaller prediction result.")
            st.write("- The features are ordered according to their importances from top to bottom.")
            st.write("In the summary plot, we see first indications of the relationship between the value of a feature and the impact on the prediction. All effects describe the behavior of the model and are not necessarily causal in the real world.")
            
            # Greeting message
            st.write("*Happy and Safe Journey ...*")
    st.write("""    """)
    st.write("""    """)
