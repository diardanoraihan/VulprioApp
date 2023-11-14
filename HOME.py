import streamlit as st

st.set_page_config(page_title="Home",
                   layout="wide",
                   page_icon='./images/home.png')

st.sidebar.image("./images/TSDN_logo.png", use_column_width=True)

# Content
st.markdown(
"""
# Vulprio 1.0 - *Vulnerability Detection and Prioritization App*
Aplikasi web untuk mendeteksi kerentanan situs dan memprioritaskan temuan yang perlu segera diatasi. [Klik di sini untuk menjalankan App](/Vulprio_App/)

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
