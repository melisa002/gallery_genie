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
        .white-text {
            color: #FFFFFF;
            background-color: #B0E3E8;
            border-radius: 10px;
            padding: 1.5em;
            margin: 1em 0;
            text-align: center;
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
                st.write(f'The style of this image is {prediction["pred_label"]}!')

                but = st.button('Press me to get predictions!')

                if but:

                    st.markdown('<div class="header-text">Recommended Items Based on Your Image:</div>', unsafe_allow_html=True)

                    col1, col2 = st.columns(2)

                    buttons = []
                    with col1:
                        st.image(prediction["most_similar"][0]['url'], use_column_width=True)
                        buttons.append(st.button(prediction["most_similar"][0]['painting_name']))
                        st.image(prediction["most_similar"][1]['url'], use_column_width=True)
                        buttons.append(st.button(prediction["most_similar"][1]['painting_name']))
                        st.image(prediction["most_similar"][4]['url'], use_column_width=True)
                        buttons.append(st.button(prediction["most_similar"][4]['painting_name']))
                    with col2:
                        st.image(prediction["most_similar"][2]['url'], use_column_width=True)
                        buttons.append(st.button(prediction["most_similar"][2]['painting_name']))
                        st.image(prediction["most_similar"][3]['url'], use_column_width=True)
                        buttons.append(st.button(prediction["most_similar"][3]['painting_name']))
                        st.image(prediction["most_similar"][5]['url'], use_column_width=True)
                        buttons.append(st.button(prediction["most_similar"][5]['painting_name']))

                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

                    def get_details(name, author_name):
                        prompt = f"Give a short, 4 line description about the picture {name} from {author_name} and focus on history and meaning. Explain a bit about the author's style and provide a location if you know."
                        response = client.Completion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                        )
                        response_text = response.choices[0].text
                        return response_text.strip()

                    for index, button in enumerate(buttons):
                        if button:
                            details = get_details(prediction["most_similar"][index]['painting_name'], prediction["most_similar"][index]['author_name'])
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
