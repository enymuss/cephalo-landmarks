import streamlit as st
from pages.introduction.page import run_intro_app
from pages.preterm.page import run_preterm_app
from pages.cephalo_landmarks.page import run_cephalo_app

model_names = ["Introduction", "Cephalometric Landmarks", "Preterm"]

option = st.sidebar.selectbox('Which model to show?', model_names, index=1)

if option is "Introduction":
    run_intro_app()
    st.sidebar.success('To continue choose a model from the list.')
elif option is "Cephalometric Landmarks":
    run_cephalo_app()
elif option is "Preterm":
    run_preterm_app()
else:
    st.write("None")
