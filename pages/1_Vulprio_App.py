from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import plotly.express as px
import duckdb as db
import streamlit as st
import pandas as pd
import os

# ---- Set Page Configuration ----
st.set_page_config(page_title="Vulprio App",
                   layout="wide",
                   page_icon='./images/app.png')

# ---- Define Empty Dictionaries ----
manualData = {'host': [],
              'akses_publik': [],
              'data_pribadi': [],
              'klasifikasi_data': [],
              'potensi_kerugian': [],
              'jumlah_pengguna': []}

uploadedData = {'host': [],
                'akses_publik': [],
                'data_pribadi': [],
                'klasifikasi_data': [],
                'potensi_kerugian': [],
                'jumlah_pengguna': []}

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
  
if 'run_app' not in st.session_state:
  st.session_state['run_app'] = False

def run_app_clicked():
  st.session_state['run_app'] = True

runApp = st.button('Cek Potensi Kerentanan', on_click=run_app_clicked)

for num in range(1, st.session_state["manual_input"] + 1):
  col1, col2, col3, col4, col5, col6 = st.columns(6)

  with col1:
    host = st.text_input(f'Link Host / IP #{num}')
    if host:
      st.caption(f'Host #{num} yang hendak dideteksi kerentanan: {host}')

  with col2:
    akses_publik = st.selectbox(f'Akses Publik #{num}', options=['Ya', 'Tidak'], index=0)
    if akses_publik == 'Ya':
      st.caption(f'Host #{num} memiliki akses ke publik')
    elif akses_publik == 'Tidak':
      st.caption(f'Host #{num} tidak memiliki akses ke publik')

  with col3:
    data_pribadi = st.selectbox(f'Informasi Data Pribadi #{num}', options = ['Ya', 'Tidak'], index=0)
    if data_pribadi == 'Ya':
      st.caption(f'Host #{num} menyimpan informasi data pribadi pengguna')
    elif data_pribadi == 'Tidak':
      st.caption(f'Host #{num} tidak menyimpan informasi data pribadi pengguna')

  with col4:
    klasifikasi_data = st.selectbox(f'Klasifikasi Data #{num}', options = ['Sangat Rahasia', 'Rahasia/Terbatas', 'Biasa'], index=0)
    if klasifikasi_data == 'Sangat Rahasia':
      st.caption(f'Data yang tersimpan pada host #{num} dikategorikan sangat rahasia')
    elif klasifikasi_data == 'Rahasia/Terbatas':
      st.caption(f'Data yang tersimpan pada host #{num} dikategorikan rahasia/terbatas')
    elif klasifikasi_data == 'Biasa':
      st.caption(f'Data yang tersimpan pada host #{num} dikategorikan biasa')

  with col5:
    potensi_kerugian = st.selectbox(f'Potensi Kerugian #{num}', options = ['Tinggi', 'Sedang', 'Rendah'], index=0)
    if potensi_kerugian == 'Tinggi':
      st.caption(f'Host #{num} memiliki potensi_kerugian tinggi (cth: menimbulkan korban jiwa)')
    elif potensi_kerugian == 'Sedang':
      st.caption(f'Host #{num} tidak memiliki potensi_kerugian sedang (cth: kerugian finansial)')
    elif potensi_kerugian == 'Rendah':
      st.caption(f'Host #{num} tidak memiliki potensi_kerugian rendah (cth: gangguan operasional)')
      
  with col6:
    jumlah_pengguna = st.selectbox(f'Jumlah Pengguna #{num}', options = ['Banyak', 'Sedang', 'Sedikit'], index=0)
    if jumlah_pengguna == 'Banyak':
      st.caption(f'Host #{num} memiliki jumlah pengguna banyak (> 5000)')
    elif jumlah_pengguna == 'Sedang':
      st.caption(f'Host #{num} memiliki jumlah pengguna sedang (>1000 & <=5000)')
    elif jumlah_pengguna == 'Sedikit':
      st.caption(f'Host #{num} memiliki jumlah pengguna sedikit (<=1000)')

  manualData['host'].append(host)
  manualData['akses_publik'].append(akses_publik)
  manualData['data_pribadi'].append(data_pribadi)
  manualData['klasifikasi_data'].append(klasifikasi_data)
  manualData['potensi_kerugian'].append(potensi_kerugian)
  
st.markdown("---")

if (runApp or st.session_state['run_app']):
  
  # ---- Read Input Data ----
  st.subheader('The flow logic below only for QA purpose')
  input_df1 = pd.DataFrame(uploadedData)
  input_df2 = pd.DataFrame(manualData)
  df_input = pd.concat([input_df1, input_df2], ignore_index=True)
  if df_input.shape[0] != 0:
    with st.expander("Input Data"):
      df_input
  else:
    st.error(':warning: Tidak ada input data')

  # ---- Input Data Preprocessing -----
  # Remove rows with null values in the 'Age' column
  df_input = df_input[(df_input['host'] != '') & (df_input['host'] != None)]
  with st.expander('Simple Data Cleaning'):
    st.dataframe(df_input)

  # ---- Read Database ----
  df_base = pd.read_csv('dataset/dataset.csv')

  # ---- Query to Database ----
  df_model = db.sql(f"""
            SELECT DISTINCT
              input_data.host, 
              database.cve_id, 
              database.epss,
              database.cvss,
              database.ransomware,
              database.cisa_kev
            FROM
              df_input AS input_data
              LEFT JOIN
                df_base AS database
                  ON input_data.host = database.host
            ORDER BY 
              1 ASC,
              2 ASC
            """).df()
  with st.expander('Query result to be used as data for modeling'):
    df_model

  # --- Feature Engineering ----
  # df_model.set_index(['host', 'cve_id'], inplace=True)
  # standardize = MinMaxScaler()
  # df_std = pd.DataFrame(standardize.fit_transform(df_model))
  # with st.expander('Feature Engineering (Index: Host & CVE, Normalization: MinMaxScaler)'):
  #   df_std
  
  df_model['likelihood'] = (df_model['epss'] + df_model['ransomware'] + df_model['cisa_kev']) * 100 / 3
  df_model['impact'] = df_model['cvss'] * 10
  df_model['risk_score'] = (df_model['likelihood'] + df_model['impact']) / 2
  with st.expander('Feature Engineering Step 1: Risk Score Calculation'):
    df_model
    
    

  # ---- Modeling ----
  # k = 4 # Choose the number of clusters (k)
  # kmeans = KMeans(n_clusters=k, random_state=42) # Initialize the KMeans model
  # kmeans.fit(df_std) # Fit the model to the data
  # df_model['cluster'] = [str(cluster) for cluster in kmeans.labels_] # Get cluster assignments
  # df_model = df_model.sort_values(by='cluster').reset_index()
  # df_result = df_input.join(df_model.set_index('host'), on='host').reset_index(drop=True)
  # with st.expander('Output Model using KMeans Clustering (K: 4)'):
  #   df_result

  # ---- Visualization
  # Create a scatter plot using Plotly Express
  # st.markdown("### Result:")
  # filter_1, filter_2, filter_3, filter_4, filter_5 = st.columns(5)
  # host = filter_1.multiselect(label='Host', options = df_result.host.unique(), default=df_result.host.unique())
  # cluster = filter_2.multiselect(label='Cluster', options=df_result.cluster.unique(), default=df_result.cluster.unique())
  # akses_publik = filter_3.multiselect(label='Akses Publik', options=df_result.akses_publik.unique(), default=df_result.akses_publik.unique())

  # df_selection = df_result.query(
  #     "cluster == @cluster & akses_publik == @akses_publik"
  # )
  # color_map = {'0': 'red', '1': 'green', '2': 'blue', '3': 'black'}
  # fig = px.scatter(df_selection, x='epss', y='cvss', color = 'cluster', color_discrete_map=color_map, hover_data=['host', 'cve_id'], title='Scatter Plot')
  # fig.update_xaxes(title_text='EPSS (Threat)')
  # fig.update_yaxes(title_text='CVSS (Severity)')

  # # Show the scatter plot in Streamlit
  # st.plotly_chart(fig)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)