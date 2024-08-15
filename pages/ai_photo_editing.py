import os
import streamlit as st
from PIL import Image
import requests
import replicate
from io import BytesIO
from navigation import make_sidebar

# Set Streamlit page configuration
st.set_page_config(page_title="AI Photo Editing - MicroSaaS", page_icon="📷", layout="centered", initial_sidebar_state="auto", menu_items=None)
print('Loading AI Photo Editing Page...')

make_sidebar()

os.environ["REPLICATE_API_TOKEN"] = os.environ.get("REPLICATE_API_TOKEN")

st.title('Edit Your Photos with AI 📷')
html_text = f"""
<p>Upload your photo and let our AI transform it for you. Our AI model uses the latest in Generative AI technology to generate stunning visual effects and edits to your photos.</p>
<p>Supported file formats include JPG, JPEG, and PNG.</p>
"""

st.html(html_text)

uploaded_files = st.file_uploader("Select a photo",  type = (["jpg", "jpeg", "png", "JPEG"]), accept_multiple_files=True)

# The rest of your code remains unchanged.

prompts = {'winter': {'prompt': 'change the season of weather to winter, add snow, snowing, dead plants', 
                      'negative': 'summer, spring, autumn, fall, colorful plants'},
           'summer': {'prompt': 'change the season of weather to summer',
                      'negative': 'winter, spring, autumn, fall, snow, snowing, dead plants'}}

season = st.selectbox("Select a season to change to", options=list(prompts.keys()))

if st.button('Transform') and uploaded_files:
    c1, c2 = st.columns(2)
    
    with c1:
        for file in uploaded_files:
            image = Image.open(file)
            st.image(image, caption='Original')
            st.download_button(
                label="Download Original",
                data=file,
                file_name="original_image.png",
                mime="image/png"
            )

    with c2:
        for file in uploaded_files:
            inputs = {
                'image': file,
                'prompt': prompts[season]['prompt'],
                'negative_prompt': prompts[season]['negative'],
                'num_outputs': 1,
                'num_inference_steps': 150,
                'guidance_scale': 10,
                'image_guidance_scale': 1.3,
                'scheduler': "K_EULER_ANCESTRAL",
            }

            output_url = replicate.run("timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                                        input=inputs)[0]
            transformed_image = Image.open(BytesIO(requests.get(output_url).content))
            st.image(transformed_image, caption='Transformed')

            # Convert the PIL Image to bytes
            transformed_image_bytes = BytesIO()
            transformed_image.save(transformed_image_bytes, format='PNG')

            st.download_button(
                label="Download Transformed",
                data=transformed_image_bytes.getvalue(),
                file_name="transformed_image.png",
                mime="image/png"
            )