from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import duckdb as db
import pandas as pd
import numpy as np
import os

# ---- Set Page Configuration ----
st.set_page_config(page_title="Vulprio App",
                   layout="centered",
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

runApp = st.button('Prioritaskan Kerentanan', on_click=run_app_clicked)

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
  manualData['jumlah_pengguna'].append(jumlah_pengguna)

st.markdown("---")

if (runApp or st.session_state['run_app']):

  # ---- Read Input Data ----
  input_df1 = pd.DataFrame(uploadedData)
  input_df2 = pd.DataFrame(manualData)
  df_input = pd.concat([input_df1, input_df2], ignore_index=True)
  input_1, input_2 = st.columns(2)
  if df_input.shape[0] != 0:

    # ---- Input Data Preprocessing -----
    # Remove rows with null values in the 'Age' column
    df_input = df_input[(df_input['host'] != '') & (df_input['host'] != None)]

    # ---- Read Database ----
    df_base = pd.read_csv('dataset/dataset.csv')

    # ---- Query to Database ----
    df_prep = db.sql(f"""
              SELECT DISTINCT
                input_data.host,
                CASE
                  WHEN LOWER(input_data.akses_publik) = 'ya' THEN 2
                  ELSE 1
                END AS akses_publik,
                CASE
                  WHEN LOWER(input_data.data_pribadi) = 'ya' THEN 2
                  ELSE 1
                END AS data_pribadi,
                CASE input_data.klasifikasi_data
                  WHEN 'Sangat Rahasia' THEN 2
                  WHEN 'Rahasia/Terbatas' THEN 1.5
                  WHEN 'Biasa' THEN 1
                END AS klasifikasi_data,
                CASE input_data.potensi_kerugian
                  WHEN 'Tinggi' THEN 2
                  WHEN 'Sedang' THEN 1.5
                  WHEN 'Rendah' THEN 1
                END AS potensi_kerugian,
                CASE input_data.jumlah_pengguna
                  WHEN 'Banyak' THEN 2
                  WHEN 'Sedang' THEN 1.5
                  WHEN 'Sedikit' THEN 1
                END AS jumlah_pengguna,
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
              WHERE
                1 = 1
                AND database.cve_id IS NOT NULL
              ORDER BY
                1 ASC,
                7 ASC
              """).df()

    # --- Feature Engineering ----
    # Feature 1: Risk Score Calculation
    df_prep['likelihood'] = (df_prep['epss'] + df_prep['ransomware'] + df_prep['cisa_kev']) * 100 / 3
    df_prep['impact'] = df_prep['cvss'] * 10
    df_prep['risk_score'] = (df_prep['likelihood'] + df_prep['impact']) / 2

    # Feature 2: Asset Score Calculation
    df_prep['asset_score'] = (df_prep['akses_publik'] + df_prep['data_pribadi'] + df_prep['klasifikasi_data'] + df_prep['potensi_kerugian'] + df_prep['jumlah_pengguna']) * 10

    # Feature 3: Priority Score Calculation
    df_prep['prio_score'] = (df_prep['risk_score'] + df_prep['asset_score']) / 2

    # Feature 4: Feature Standardization (Normalization)
    columns = ['host', 'cve_id', 'prio_score']
    df_model = df_prep[columns]
    df_model.set_index(['host', 'cve_id'], inplace=True)
    standardize = MinMaxScaler()
    df_std = pd.DataFrame(standardize.fit_transform(df_model))

    # ---- Kmeans Modeling ----
    k = 4 # Choose the number of clusters (k)
    kmeans = KMeans(n_clusters=k, random_state=42) # Initialize the KMeans model
    kmeans.fit(df_std) # Fit the model to the data
    df_prep['cluster'] = [str(cluster) for cluster in kmeans.labels_] # Get cluster assignments

    # ---- Output Result ----
    st.markdown("## Overview")
    df_result = df_input.join(df_prep[['host', 'cve_id', 'epss', 'cvss', 'ransomware', 'cisa_kev', 'risk_score', 'asset_score', 'prio_score', 'cluster']].set_index('host'), on = 'host').reset_index(drop=True).sort_values('cluster')
    
    # ---- Query to Database ----
    df_result_stat = db.sql(f"""
              SELECT 
                cluster,
                COUNT(*) AS vul_count,
                COUNT(DISTINCT host) AS host_count,
                COUNT(DISTINCT cve_id) AS cve_count,
                AVG(risk_score) AS risk_score_avg,
                AVG(asset_score) AS asset_score_avg,
                AVG(prio_score) AS prio_score_avg 
              FROM
                df_result
              GROUP BY 
                1
              """).df()
    
    df_result_stat['rank'] = df_result_stat['prio_score_avg'].rank(ascending=False)
    
    cl_0, cl_1, cl_2, cl_3 = st.columns(4)
    
    cl_0.markdown("#### Cluster 0")
    cl_0.metric(label='Temuan Kerentanan', value=df_result_stat[df_result_stat['cluster'] == '0'].vul_count)
    cl_0.metric(label='Rata" Risk Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '0'].risk_score_avg, 1))
    cl_0.metric(label='Rata" Asset Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '0'].asset_score_avg, 1))
    cl_0.metric(label='Rata" Priority Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '0'].prio_score_avg, 1))
    
    cl_1.markdown("#### Cluster 1")
    cl_1.metric(label='Temuan Kerentanan', value=df_result_stat[df_result_stat['cluster'] == '1'].vul_count)
    cl_1.metric(label='Rata" Risk Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '1'].risk_score_avg, 1))
    cl_1.metric(label='Rata" Asset Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '1'].asset_score_avg, 1))
    cl_1.metric(label='Rata" Priority Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '1'].prio_score_avg, 1))

    cl_2.markdown("#### Cluster 2")
    cl_2.metric(label='Temuan Kerentanan', value=df_result_stat[df_result_stat['cluster'] == '2'].vul_count)
    cl_2.metric(label='Rata" Risk Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '2'].risk_score_avg, 1))
    cl_2.metric(label='Rata" Asset Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '2'].asset_score_avg, 1))
    cl_2.metric(label='Rata" Priority Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '2'].prio_score_avg, 1))
    
    cl_3.markdown("#### Cluster 3")
    cl_3.metric(label='Temuan Kerentanan', value=df_result_stat[df_result_stat['cluster'] == '3'].vul_count)
    cl_3.metric(label='Rata" Risk Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '3'].risk_score_avg, 1))
    cl_3.metric(label='Rata" Asset Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '3'].asset_score_avg, 1))
    cl_3.metric(label='Rata" Priority Score', value=np.round(df_result_stat[df_result_stat['cluster'] == '3'].prio_score_avg, 1))
    
    st.markdown("## Analisis ")
    filter_1, filter_2 = st.columns(2)
    cluster = filter_1.multiselect(label='Pilih Cluster:', options=df_result.cluster.unique(), default=df_result.cluster.unique())
    df_selection = df_result.query(
        "cluster == @cluster"
    ).reset_index(drop=True)
    
    # Numeric Metric Visualization

    # Univariate Kmeans Clustering Visualization
    color_map = {'0': 'brown', '1': 'green', '2': 'blue', '3': 'orange'}
    fig_1 = px.scatter(
      data_frame=df_selection,
      x='prio_score',
      y=np.zeros(df_selection.shape[0]),
      color = 'cluster',
      color_discrete_map=color_map
      # hover_data=['cluster', 'host', 'cve_id', 'prio_score', 'risk_score', 'asset_score'],
      )
    fig_1.update_layout(
      title='Cluster Temuan Kerentanan berdasarkan Skor Prioritas',
      title_x=0.22,  # Horizontal center
      title_y=0.95,    # Top
      legend=dict(
        x=0.65, 
        y=1, 
        traceorder='normal', 
        orientation='h'
        )
      )
    fig_1.update_traces(
      marker=dict(
        size=12,
        line=dict(
          width=1
          )
        ),
      customdata =np.stack((df_selection['host'], df_selection['cluster']), axis=-1),
      hovertemplate='Host: %{custom_data[0]}<br>Host: %{host}<br>CVE ID: {cve_id}<br>Prio Score: {prio_score}<br>Risk Score: {risk_score}<br>Asset Score: {asset_score}'
      )
    fig_1.update_xaxes(title_text='Priority Score (0-100)')
    fig_1.update_yaxes(title_text='Temuan Kerentanan', showticklabels = False)
    st.plotly_chart(fig_1)

    fig_2 = px.box(df_selection, x="cluster", y="prio_score", color="cluster",
                notched=True, # used notched shape
                title="Boxplot Cluster Temuan Kerentanan",
                color_discrete_map=color_map
                # hover_data=["day"] # add day column to hover data
                )
    fig_2.update_layout(
      title='Boxplot Cluster Temuan Kerentanan',
      title_x=0.3,  # Horizontal center
      title_y=0.95    # Top
      )
    fig_2.update_xaxes(title_text='Cluster', tickvals=[0, 1, 2, 3])
    fig_2.update_yaxes(title_text='Priority Score (0-100)')
    st.plotly_chart(fig_2)

    # Table Output
    with st.expander('Output details:'):
      st.dataframe(df_selection)
    
    st.markdown("## Rekomendasi")
    cluster_prio = df_result_stat[df_result_stat['rank'] == 1]['cluster'].to_list()[0]
    st.warning(f":warning: :warning: Berdasarkan hasil analisis, kami merekomendasikan untuk melakukan perbaikan segera pada hasil temuan kerentanan di cluster {cluster_prio} :warning: :warning:")
  else:
    st.error(':warning: Tidak ada input data')

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)