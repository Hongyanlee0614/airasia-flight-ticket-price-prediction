import streamlit as st
from multiapp import MultiApp
from apps import home, visualization, analysis, make_a_prediction # import your app modules here
from PIL import Image

# set title and favicon at the tab
st.set_page_config(page_title="Travelaysia", page_icon='logo500.png')

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Visualization", visualization.app)
app.add_app("Analysis", analysis.app)
app.add_app("Make a Prediction", make_a_prediction.app)

# sidebar logo
image = Image.open('logo.png')
st.sidebar.image(image, width=270, use_column_width='never')

# The main app
app.run()