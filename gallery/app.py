import streamlit as st
from PIL import Image
import requests
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Image Uploader & Recommender",
    page_icon=':frame_with_picture:',
    layout="wide",
    initial_sidebar_state="expanded",
)

# API URL
url = 'https://gallery-5jwtgfgjta-ew.a.run.app'

# Custom CSS for enhanced visuals
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .main {
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
            margin-bottom: 0.5em;
        }
        .markdown-text {
            font-size: 1.5em;
            text-align: center;
            margin-bottom: 2em;
        }
        .footer {
            text-align: center;
            font-size: 1em;
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
        .white-text {
            color: #FFFFFF;
            background-color: #B0E3E8;
            border-radius: 10px;
            padding: 1.5em;
            margin: 1em 0;
            text-align: center;
            font-size: 1.2em;
        }
        .prediction-text {
            text-align: center;
            font-size: 1.8em;
            margin-top: 1em;
            margin-bottom: 1em;
            color: #FF4B4B;
            background-color: #FFF4F4;
            padding: 1em;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<div class="header-text1">GALLERY GENIE</div>', unsafe_allow_html=True)
st.markdown('<div class="header-text">Image Uploader & Recommender &#128247;</div>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="markdown-text">Let\'s do a simple painting recognition and get recommendations &#128071;</div>', unsafe_allow_html=True)

# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
img_file_buffer = st.file_uploader('', type=['png', 'jpg', 'jpeg'])
st.markdown('</div>', unsafe_allow_html=True)

if img_file_buffer is not None:
    st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded 👆")

    with st.spinner("Wait for it..."):
        # Get bytes from the file buffer
        img_bytes = img_file_buffer.getvalue()

        # Make request to API
        try:
            res = requests.post(url + "/upload_image", files={'img': img_bytes})

            if res.status_code == 200:
                prediction = res.json()
                st.markdown(f'<div class="prediction-text">The style of this image is {prediction["pred_label"]}!</div>', unsafe_allow_html=True)

                but = st.button('Press me to get predictions!')

                if but:
                    # Mock recommendation function
                    def get_recommendations(image):
                        return [
                            "Recommendation 1: Similar item 1",
                            "Recommendation 2: Similar item 2",
                            "Recommendation 3: Similar item 3",
                            "Recommendation 4: Similar item 4"
                        ]

                    recommendations = get_recommendations(img_bytes)
                    st.markdown('<div class="header-text">Recommended Items Based on Your Image:</div>', unsafe_allow_html=True)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.image(prediction["most_similar"][0]['url'], use_column_width=True)
                        button1 = st.button(prediction["most_similar"][0]['painting_name'])
                        st.image(prediction["most_similar"][1]['url'], use_column_width=True)
                        button2 = st.button(prediction["most_similar"][1]['painting_name'])
                        st.image(prediction["most_similar"][4]['url'], use_column_width=True)
                        button3 = st.button(prediction["most_similar"][4]['painting_name'])
                    with col2:
                        st.image(prediction["most_similar"][2]['url'], use_column_width=True)
                        button4 = st.button(prediction["most_similar"][2]['painting_name'])
                        st.image(prediction["most_similar"][3]['url'], use_column_width=True)
                        button5 = st.button(prediction["most_similar"][3]['painting_name'])
                        st.image(prediction["most_similar"][5]['url'], use_column_width=True)
                        button6 = st.button(prediction["most_similar"][5]['painting_name'])

                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    index_ = 6
                    if button1:
                        index_ = 0
                    elif button2:
                        index_ = 1
                    elif button3:
                        index_ = 2
                    elif button4:
                        index_ = 3
                    elif button5:
                        index_ = 4
                    elif button6:
                        index_ = 5

                    def get_details(name, author_name):
                        prompt = f"Give a short, 4 line description about the picture {name} from {author_name} and focus on history and meaning. Explain a bit about the author's style and provide a location if you know."
                        stream = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                            stream=True,
                        )
                        response_text = ""
                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                response_text += chunk.choices[0].delta.content
                        return response_text.strip()

                    details = get_details(prediction["most_similar"][index_]['painting_name'], prediction["most_similar"][index_]['author_name'])
                    st.write(details)

            else:
                st.error("**Oops**, something went wrong :sweat: Please try again.")
                st.write(f"Error {res.status_code}: {res.content.decode('utf-8')}")
        except requests.exceptions.RequestException as e:
            st.error("**Oops**, something went wrong :sweat: Please try again.")
            st.write(f"RequestException: {e}")
else:
    st.markdown('<div class="white-text">Please upload an image to get started.</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="footer">Developed with :heart: using Streamlit, FastAPI, and Docker.</div>', unsafe_allow_html=True)
