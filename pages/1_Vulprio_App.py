import streamlit as st
import os
import pandas as pd

# ---- Set Page Configuration ----
st.set_page_config(page_title="Vulprio App",
                   layout="wide",
                   page_icon='./images/app.png')

# ---- Define Empty Dictionaries ----
manualData = {'host': [],
              'public_access': [],
              'pii': [],
              'importance': [],
              'urgency': []}

uploadedData = {'host': [],
                'public_access': [],
                'pii': [],
                'importance': [],
                'urgency': []}

# ---- App Title ----
st.markdown(
"""
# 🔍 Vulprio 1.0
### *Risk Based Vulnerability Prioritization App using Machine Learning Model*
"""
)

# ---- Sidebar Addons ----
st.sidebar.header('')
st.sidebar.image("./images/TSDN_logo.png", use_column_width=True)

# ---- Input Data - Upload file Feature ----
uploaded_file = st.file_uploader('Choose a File: ') # Upload a file 'media/mountains.webp'
if uploaded_file:
  st.success('File is uploaded successfully')

  # save the file
  path = os.path.join('./upload', uploaded_file.name)
  with open(path, mode = 'wb') as f:
    f.write(uploaded_file.getbuffer()) # get all the file information in the bytes and save it in 'media/'

  # Read Uploaded File
  if 'xlsx' in uploaded_file.name:
    uploadedData = pd.read_excel(path)
  elif 'csv' in uploaded_file.name:
    uploadedData = pd.read_csv(path)
  else:
    st.error('Unknown uploaded file format!')

# ---- Input Data - Manual Feature ----
if "manual_input" not in st.session_state:
  st.session_state["manual_input"] = 0

if st.button('Manual Input Data'):
  st.session_state["manual_input"] += 1

runApp = st.button('Cek Potensi Kerentanan')

for num in range(1, st.session_state["manual_input"] + 1):
  col1, col2, col3, col4, col5 = st.columns(5)

  with col1:
    host = st.text_input(f'Link Host Situs / IP #{num}')
    if host:
      st.write('Situs yang hendak dideteksi kerentanan: ', host)

  with col2:
    public_access = st.selectbox(f'Akses Publik #{num}', options=['Ya', 'Tidak'], index=None)
    if public_access == 'Ya':
      st.success(f'Situs #{num} memiliki akses ke publik')
    elif public_access == 'Tidak':
      st.error(f'Situs #{num} tidak memiliki akses ke publik')

  with col3:
    pii = st.selectbox(f'Informasi Identifikasi Pribadi #{num}', options = ['Ya', 'Tidak'], index=None)
    if pii == 'Ya':
      st.success(f'Situs #{num} memiliki informasi data pribadi terpampang pada halaman websitenya')
    elif pii == 'Tidak':
      st.error(f'Situs #{num} tidak memiliki informasi data pribadi terpampang pada halaman websitenya')

  with col4:
    importance = st.selectbox(f'Kepentingan #{num}', options = ['Ya', 'Tidak'], index=None)
    if importance == 'Ya':
      st.success(f'Situs #{num} dikategorikan penting')
    elif importance == 'Tidak':
      st.error(f'Situs #{num} dikategorikan tidak cukup penting')

  with col5:
    urgency = st.selectbox(f'Urgensi #{num}', options = ['Ya', 'Tidak'], index=None)
    if urgency == 'Ya':
      st.success(f'Situs #{num} memiliki urgensi tinggi')
    elif urgency == 'Tidak':
      st.error(f'Situs #{num} tidak memiliki urgensi tinggi')

  manualData['host'].append(host)
  manualData['public_access'].append(public_access)
  manualData['pii'].append(pii)
  manualData['importance'].append(importance)
  manualData['urgency'].append(urgency)
  
st.markdown("---")

# ---- Input Data Preprocessing ----
st.subheader('The table below only for input data demonstration purpose')
input_df1 = pd.DataFrame(uploadedData)
input_df2 = pd.DataFrame(manualData)
inputData = pd.concat([input_df1, input_df2], ignore_index=True)
st.write(inputData)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)