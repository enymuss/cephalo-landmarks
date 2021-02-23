import streamlit as st
import os

def run_intro_app():
    with open(os.path.join(os.getcwd(), "pages", "introduction", "introduction.md")) as f:
        st.markdown(f.read())

if __name__ == "__main__":
    run_intro_app()
