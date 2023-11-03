import streamlit as st
import app
import sys
import cv2
import numpy as np
import dlib
from imutils import face_utils
import playsound
import math
import time
from streamlit_lottie import st_lottie
import requests


def main():

    # Set the title of your app
    st.set_page_config(page_title="Sleep Burster 🙅‍♂️")
    # Add content to the sidebar
    st.sidebar.title("Developed with ❤ ")
    #st.sidebar.write("Burst Your Sleep and Drive With Us Safely ❤ ")

    # Add contributors and their LinkedIn profiles to the sidebar
    st.sidebar.subheader("Contributors:")


    contributors = [
        {"name": "Abhishek", "linkedin": "https://www.linkedin.com/in/abhishek-jayan-890a59251/", 
        "image_url": "https://github.com/shivamsengupta/Sleep_Burster/blob/master/abhishek.jpeg?raw=true"},

        {"name": "Anjali", "linkedin": "https://www.linkedin.com/in/anjali-k-b63634249/", 
        "image_url": "https://github.com/shivamsengupta/Sleep_Burster/blob/master/1693822316668.jpeg?raw=true"},

        {"name": "Acquin", "linkedin": "https://www.linkedin.com/in/acquin-joseph-a27321178/", 
        "image_url": "https://github.com/shivamsengupta/Sleep_Burster/blob/master/acquin.jpeg?raw=true"},

        {"name": "Bala", "linkedin": "https://www.linkedin.com/in/balakumar-ramkumar-2711571b1/", 
        "image_url": "https://github.com/shivamsengupta/Sleep_Burster/blob/master/bala.jpeg?raw=true"},

        {"name": "Shivam", "linkedin": "https://www.linkedin.com/in/shivam-sen-gupta/", 
        "image_url": "https://github.com/shivamsengupta/Sleep_Burster/blob/master/SHIVAM.jpg?raw=true"},
    ]

    # for contributor in contributors:
    #     st.sidebar.image(contributor["image_url"], width=50)
    #     st.sidebar.markdown(f"[{contributor['name']}]({contributor['linkedin']})")
        
    # Display contributors in two columns in the sidebar
    columns = st.sidebar.columns(3)
    for contributor in contributors:
        with columns[contributors.index(contributor) % 3]:
            st.markdown(f'<img src="{contributor["image_url"]}" style="border-radius: 50%;" width="70">', unsafe_allow_html=True)
            st.markdown(f"[{contributor['name']}]({contributor['linkedin']})")

    # Main content in the body of the app    
    name,road_type="",""
    a1=0
    st.title("SLEEP BURSTER 🙅‍♂️")
    st.write("Burst Your Sleep and Drive With Us Safely ❤ ")
    
    st.snow()

    url = "https://assets9.lottiefiles.com/packages/lf20_M9p23l.json"
    lottie_json = requests.get(url).json()
    # Display the animation in Streamlit with custom dimensions
    st_lottie(lottie_json, loop=True, width=300, height=300)
    

    name=st.text_input("Enter Your Name")
    road_type=st.selectbox("Road Type",("Highway","Non-Highway"))   
    
    threshold_active,threshold_drowsy=0.0,0.0

    if(st.button("GO 🏎")):
        if(name and road_type):
            cap=cv2.VideoCapture(0)
            if(road_type=="Highway"):
                threshold_active=0.25
                threshold_drowsy=0.15
            else:
                threshold_active=0.30
                threshold_drowsy=0.20
            app.bny(cap,name,threshold_active,threshold_drowsy,road_type)
        else:
            st.write("Please, enter your name and road type before pressing GO !!!")


if __name__=="__main__":
    main()




