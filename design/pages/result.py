import streamlit as st
import streamlit.components.v1 as components
import base64

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def App1page():
    st.write("hello world")
 

img = get_img_as_base64("vin-page-2.jpeg")
logo = get_img_as_base64("logo.png")

page_bg_img = f"""
<style>
 [data-testid="stSidebarNav"] {{
                background-image: url("data:image/png;base64,{logo}");
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 10px 10px;
                background-size: 200px 200px;
            }}

[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-position: left;
background-repeat: no-repeat;
background-attachment: local;
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.write(

    f'''
<div style='margin-left: 40%; margin-top: 10%;'> 
            <div style='color: #db545a; font-size: 25px; font-weight: 700;letter-spacing: 1px; text-align: right; '>NOTRE SÉLECTION POUR VOUS</div>
            
</div>

            ''', unsafe_allow_html=True,
)

   

# st.write("You have entered", st.session_state["my_input"])