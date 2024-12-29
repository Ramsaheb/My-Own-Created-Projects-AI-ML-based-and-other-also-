import streamlit as st
import pandas as pd
import os.path
import nltk
from Backend import recommender

# Function to download NLTK packages if not already downloaded
def download_nltk_packages():
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw")

# Check if NLTK packages are downloaded, if not, download them
nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data")
if not os.path.exists(nltk_data_path):
    download_nltk_packages()

# Setting page title and background color
st.set_page_config(page_title="AI Hotel Recommender", page_icon="🏨", layout="wide")

# Load CSV data
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

hotel_detail = load_data('Hotel_details.csv')
hotel_rooms = load_data('Hotel_Room_attributes.csv')

# Title and image
st.title('AI Hotel Recommender')
st.image('hotel1.png', caption='Image source: YourSource.com', use_column_width=True)

# User inputs
col1, col2, col3 = st.columns([1, 2, 1]) 

with col1:
    number = st.slider('Number of guests:', 1, 4)

# Get unique city names from the dataset
with col2:
    city = st.selectbox('Select city:', hotel_detail['city'].unique())

with col3:
    price = st.number_input('Budget:($)', min_value=60, max_value=100)

# Features input
features = st.text_input('Desired features (e.g., "free wifi, extra toilet, aircondition"):', placeholder='Separate features by commas') 

if st.button('Get Recommendations', key='recommendations_button'):
    try:
        # If features input is empty, set a default value to indicate no specific features desired
        features = features.strip() if features.strip() != "" else "No specific features"
        
        # AI recommendation logic
        with st.spinner("Loading recommendations..."):  # Show a loading spinner while computing recommendations
            recommendations = recommender(city, number, features, price)
        
        if recommendations.empty:
            st.warning("No recommendations found. Try adjusting your search criteria.")
        else:
            for index, recommendation in recommendations.iterrows():
                expander = st.expander(f"🏨 {recommendation['hotelname']}")
                with expander:
                    st.write(f"📍 Location: {recommendation['address']}")
                    st.write(f"ℹ️ Feature Box: {recommendation['description']}")
                    st.write(f"🔗 Booking Link: {recommendation['url']}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
