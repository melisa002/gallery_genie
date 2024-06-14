import streamlit as st
from PIL import Image
import requests
import os


st.set_page_config(
    page_title="Image Uploader & Recommender",
    page_icon=':frame_with_picture:',
    layout="wide",
    initial_sidebar_state="expanded",
)
# Example local Docker container URL
url = 'http://api:8000'
# Example localhost development URL
url = 'http://localhost:8000'
# load_dotenv()
# url = os.getenv('API_URL')
# Custom CSS

st.markdown("""
    <style>
        body {
            background-color: #FFFFFF;
        }
        .main {
            background-color: #FFFFFF;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stSpinner {
            color: #FFFFFF;
        }
        .header-text1 {
            background-color: #FF4B4B;
            text-align: center;
            color: #FFFFFF;
            font-size: 4em;
            margin-top: 1em;
        }
        .header-text {
            text-align: center;
            color: #FF4B4B;
            font-size: 2em;
            margin-top: 1em;
        }
        .markdown-text {
            font-size: 1.1em;
        }
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #888;
            margin-top: 2rem;
        }
        .upload-section {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
    </style>
    """, unsafe_allow_html=True)
# App title and description
st.markdown('<h1 class="header-text1">GALLERY GENIE </h1>', unsafe_allow_html=True)
### Create a native Streamlit file upload input
st.markdown("### Let's do a simple painting recognition and get recommendations :point_down:", unsafe_allow_html=True)
# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
img_file_buffer = st.file_uploader('', type=['png', 'jpg', 'jpeg'])
st.markdown('</div>', unsafe_allow_html=True)
if img_file_buffer is not None:
    col1, col2 = st.columns(2)
    with col1:
        ### Display the image user uploaded
        st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded :point_up:", use_column_width=True)
    with col2:
        with st.spinner("Wait for it..."):
            ### Get bytes from the file buffer
            img_bytes = img_file_buffer.getvalue()
            ### Make request to API (stream=True to stream response as bytes)
            try:
                res = requests.post(url + "/upload_image", files={'img': img_bytes})
                if res.status_code == 200:
                    ### Display the image returned by the API
                    prediction = res.json()
                    st.write(prediction)
                    # st.image(res.content, caption="Image returned from API :point_up:", use_column_width=True)
                    # Mock recommendation function (replace this with actual API call or local function)
                    def get_recommendations(image):
                        # Dummy data for example purposes
                        return [
                            "Recommendation 1: Similar item 1",
                            "Recommendation 2: Similar item 2",
                            "Recommendation 3: Similar item 3"
                        ]
                    recommendations = get_recommendations(img_bytes)
                    st.markdown("### Recommended Items Based on Your Image:", unsafe_allow_html=True)
                    for recommendation in recommendations:
                        st.write(recommendation)
                else:
                    st.error("**Oops**, something went wrong :sweat: Please try again.")
                    st.write(f"Error {res.status_code}: {res.content.decode('utf-8')}")
            except requests.exceptions.RequestException as e:
                st.error("**Oops**, something went wrong :sweat: Please try again.")
                st.write(f"RequestException: {e}")
else:
    st.info("Please upload an image to get started.")
st.markdown("---")
st.markdown('<div class="footer">Developed with :heart: using Streamlit, FastAPI, and Docker.</div>', unsafe_allow_html=True)
