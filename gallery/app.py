import streamlit as st
from PIL import Image
import requests
st.set_page_config(
    page_title="Image Uploader & Recommender",
    page_icon=':frame_with_picture:',
    layout="wide",
    initial_sidebar_state="expanded",
)
url = 'https://gallery-5jwtgfgjta-ew.a.run.app'
# load_dotenv()
# url = os.getenv('API_URL')
# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #F0F2F6;
        }
        .main {
            background-color: #FFFFFF;
            padding: 2rem;
            color: #333333;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stSpinner {
            color: #FF4B4B;
        }
        .header-text1 {
            background-color: #FF4B4B;
            text-align: center;
            color: #FFFFFF;
            font-size: 3em;
            padding: 0.5em;
            border-radius: 10px;
            margin-bottom: 1em;
        }
        .header-text {
            text-align: center;
            color: #FF4B4B;
            font-size: 2em;
            margin-top: 1em;
            margin-bottom: 0.5em; /* Adjusted margin bottom */
        }
        .markdown-text {
            font-size: 1.1em;
            text-align: center;
            margin-bottom: 2em;
        }
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #888888;
            margin-top: 2rem;
        }
        .upload-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 2em;
        }
        .recommendations {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .recommendation-item {
            background-color: #F9F9F9;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 1em;
            margin: 0.5em;
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        /* CSS for white text */
    .white-text {
        color: #FFFFFF;
        background-color: #B0E3E8; /* Light blue background */
        border-radius: 10px;
        padding: 1.5em; /* Increased padding */
        margin: 1em 0; /* Increased margin */
        text-align: center; /* Center align text */
    """, unsafe_allow_html=True)
# App title and description
st.markdown('<div class="header-text1">GALLERY GENIE</div>', unsafe_allow_html=True)
st.markdown('<div class="header-text">Image Uploader & Recommender :camera:</div>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)  # Add space between lines
st.markdown('<div class="markdown-text">Let\'s do a simple painting recognition and get recommendations :point_down:</div>', unsafe_allow_html=True)
# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
img_file_buffer = st.file_uploader('', type=['png', 'jpg', 'jpeg'])
st.markdown('</div>', unsafe_allow_html=True)
if img_file_buffer is not None:
    col1, col2 = st.columns(2)
    with col1:
        # Display the image user uploaded
        st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded :point_up:", use_column_width=True)
    with col2:
        with st.spinner("Wait for it..."):
            # Get bytes from the file buffer
            img_bytes = img_file_buffer.getvalue()
            # Make request to API (stream=True to stream response as bytes)
            try:
                res = requests.post(url + "/upload_image", files={'img': img_bytes})

                if res.status_code == 200:
                    # Display the image returned by the API
                    prediction = res.json()
                    #st.write(prediction)
                    st.write(f'The style of this image is {prediction["pred_label"]}')
                    # Mock recommendation function (replace this with actual API call or local function)
                    def get_recommendations(image):
                        # Dummy data for example purposes
                        return [
                            "Recommendation 1: Similar item 1",
                            "Recommendation 2: Similar item 2",
                            "Recommendation 3: Similar item 3"
                        ]
                    recommendations = get_recommendations(img_bytes)
                    st.markdown('<div class="header-text">Recommended Items Based on Your Image:</div>', unsafe_allow_html=True)
                    st.markdown('<div class="recommendations">', unsafe_allow_html=True)
                    for recommendation in recommendations:
                        st.markdown(f'<div class="recommendation-item">{recommendation}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("**Oops**, something went wrong :sweat: Please try again.")
                    st.write(f"Error {res.status_code}: {res.content.decode('utf-8')}")
            except requests.exceptions.RequestException as e:
                st.error("**Oops**, something went wrong :sweat: Please try again.")
                st.write(f"RequestException: {e}")
else:
    # Change text color to white for info message
    st.markdown('<div class="white-text">Please upload an image to get started.</div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown('<div class="footer">Developed with :heart: using Streamlit, FastAPI, and Docker.</div>', unsafe_allow_html=True)
