
import streamlit as st

st.set_page_config(page_title="About",
                   layout="wide",
                   page_icon='./images/about.png')
st.sidebar.image("./images/TSDN_logo.png", use_column_width=True)
st.markdown(
"""
# About

Aplikasi **Vulprio 1.0** ini dikembangkan oleh **Tim Avektive** yang beranggotakan 4 orang dalam rangka mengikuti **Turnamen Sains Data Nasional 2023**
""")

# Content
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.image('./images/TSDN_logo.png')
  st.markdown(
  """
  #### Aditya Rachman Putra
  
  - [Email](mailto:adityarputra@gmail.com)
  - [LinkedIn](https://www.linkedin.com/in/diardanoraihan/)   
  - [Github]()        
  """)

with col2:
  st.image('./images/TSDN_logo.png')
  st.markdown(
  """
  #### Bakti Satria Adhityatama
  
  - [Email](mailto:bakti.satria.a@gmail.com)
  - [LinkedIn](https://www.linkedin.com/in/diardanoraihan/)   
  - [Github]()        
  """)

with col3:
  st.image('./images/TSDN_logo.png')
  st.markdown(
  """
  #### Diardano Raihan
  
  - [Email](mailto:diardano@gmail.com)
  - [LinkedIn](https://www.linkedin.com/in/diardanoraihan/)   
  - [Github]()        
  """)

with col4:
  st.image('./images/TSDN_logo.png')
  st.markdown(
  """
  #### Syaiful Andy
  
  - [Email](mailto:syaifulandy@gmail.com)
  - [LinkedIn](https://www.linkedin.com/in/diardanoraihan/)   
  - [Github]()        
  """)
