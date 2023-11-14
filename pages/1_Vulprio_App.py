import streamlit as st
import pandas as pd

st.set_page_config(page_title="Vulprio App",
                   layout="wide",
                   page_icon='./images/app.png')

inputData = {'url': [], 
          'publicAccess': [], 
          'pii': [],
          'importance': [], 
          'urgency': []}

st.markdown(
"""
# Vulprio 1.0 - *Vulnerability Detection and Prioritization App*
"""
)

st.sidebar.image("./images/TSDN_logo.png", use_column_width=True)

if "num_inputs" not in st.session_state:
    st.session_state["num_inputs"] = 1

if st.button('Tambah Data Input'):
    st.session_state["num_inputs"] += 1


# addInput = st.button('Tambah Data Input', key = 1)
runApp = st.button('Cek Potensi Kerentanan')

st.markdown(
"""
---
"""
)

for num in range(1, st.session_state["num_inputs"] + 1):
  col1, col2, col3, col4, col5 = st.columns(5)

  with col1:
    url = st.text_input(f'Link URL Situs #{num}')
    if url:
      st.write('Situs yang hendak dideteksi kerentanan: ', url)

  with col2:
    publicAccess = st.selectbox(f'Akses Publik #{num}', options=['Ya', 'Tidak'], index=None)
    if publicAccess == 'Ya':
      st.success('Situs memiliki akses ke publik')
    elif publicAccess == 'Tidak':
      st.error('Situs tidak memiliki akses ke publik')

  with col3:
    pii = st.selectbox(f'Informasi Identifikasi Pribadi #{num}', options = ['Ya', 'Tidak'], index=None)
    if pii == 'Ya':
      st.success('Situs memiliki informasi data pribadi terpampang pada halaman websitenya')
    elif pii == 'Tidak':
      st.error('Situs tidak memiliki informasi data pribadi terpampang pada halaman websitenya')

  with col4:
    importance = st.selectbox(f'Kepentingan #{num}', options = ['Ya', 'Tidak'], index=None)
    if importance == 'Ya':
      st.success('Situs dikategorikan penting')
    elif importance == 'Tidak':
      st.error('Situs dikategorikan tidak cukup penting')

  with col5:
    urgency = st.selectbox(f'Urgensi #{num}', options = ['Ya', 'Tidak'], index=None)
    if urgency == 'Ya':
      st.success('Situs memiliki urgensi tinggi')
    elif urgency == 'Tidak':
      st.error('Situs tidak memiliki urgensi tinggi')

  inputData['url'].append(url)
  inputData['publicAccess'].append(publicAccess)
  inputData['pii'].append(pii)
  inputData['importance'].append(importance)
  inputData['urgency'].append(urgency)


st.json(inputData)


# the code below is successful!!!
# temp = []
# for num in range(1, st.session_state["num_inputs"] + 1):
#     new = st.text_input(label=f"Filter #{num}")
#     st.write(new)
#     temp.append(new)

# st.write(temp)