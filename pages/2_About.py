import streamlit as st

st.set_page_config(page_title="Home",
                   layout="wide",
                   page_icon='./images/home.png')
st.title('YOLO v5 Object Detection App')
st.caption('This is web application demonstrate Object Detection')

# Content
st.markdown(
"""
### This App detects objects from Images
- Automatically detects 20 objects from image
- [Click here for App](/YOLO_for_image/)

These are the object that our model will detect:
- person 
- car 
- chair 
- bottle 
- pottedplant 
- bird 
- dog 
- sofa 
- bicycle 
- horse 
- boat 
- motorbike 
- cat 
- tvmonitor 
- cow 
- sheep 
- aeroplane 
- train 
- diningtable 
- bus
            
""")
