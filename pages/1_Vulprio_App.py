import streamlit as st

st.set_page_config(page_title="Vulprio App",
                   layout="wide",
                   page_icon='./images/app.png')

st.markdown(
"""
# Vulprio 1.0 - *Vulnerability Detection and Prioritization App*
---
"""
)

st.sidebar.image("./images/TSDN_logo.png", use_column_width=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
  url = st.text_input('Link URL Situs')
  if url:
    st.write('Situs yang hendak dideteksi kerentanan: ', url)

  
with col2:
  publicAccess = st.selectbox('Akses Publik', options=['Ya', 'Tidak'], index=None)
  if publicAccess == 'Ya':
    st.success('Situs memiliki akses ke publik')
  elif publicAccess == 'Tidak':
    st.error('Situs tidak memiliki akses ke publik')

with col3: 
  pii = st.selectbox('Informasi Identifikasi Pribadi', options = ['Ya', 'Tidak'], index=None)
  if pii == 'Ya':
    st.success('Situs memiliki informasi data pribadi terpampang pada halaman websitenya')
  elif pii == 'Tidak':
    st.error('Situs tidak memiliki informasi data pribadi terpampang pada halaman websitenya')

with col4: 
  importance = st.selectbox('Kepentingan', options = ['Ya', 'Tidak'], index=None)
  if importance == 'Ya':
    st.success('Situs dikategorikan penting')
  elif importance == 'Tidak':
    st.error('Situs dikategorikan tidak cukup penting')

with col5: 
  urgency = st.selectbox('Urgensi', options = ['Ya', 'Tidak'], index=None)
  if urgency == 'Ya':
    st.success('Situs memiliki urgensi tinggi')
  elif urgency == 'Tidak':
    st.error('Situs tidak memiliki urgensi tinggi')

col_a, col_b, col_c, col_d, col_e = st.columns(5)
if url and publicAccess and pii and importance and urgency:
  button = col_c.button('Cek Potensi Kerentanan')