import streamlit as st

st.set_page_config(page_title="Home",
                   layout="wide",
                   page_icon='./images/home.png')
st.sidebar.header('')
st.sidebar.image("./images/TSDN_logo.png", use_column_width=True)

# Content
st.markdown(
"""
# 🔍 Vulprio 1.0
### *Risk Based Vulnerability Prioritization App using Machine Learning Model*
Aplikasi web untuk memprioritaskan temuan kerentanan CVE berbasis risiko. [Klik di sini untuk menjalankan App](/Vulprio_App/)

---
### Latar Belakang

. . . . .

### Fitur


App ini dapat mendeteksi kerentanan pada suatu situs web sekaligus memberikan rekomendasi daftar kerentanan utama yang perlu diprioritaskan. 


### Panduan Pengguna
Cara menggunakan app ini adalah sebagai berikut:
- xxx
- xxx
- xxx

""")


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)