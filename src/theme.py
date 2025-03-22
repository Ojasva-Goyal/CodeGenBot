import streamlit as st

def inject_custom_css(dark_mode: bool):
    """
    Inject custom CSS to apply dark or light mode.
    """
    if dark_mode:
        st.markdown(
            """
            <style>
            body, .main, .block-container {
                background-color: #0f0f0f !important;
                color: #FFFFFF !important;
            }
            textarea, input, .stRadio, .stSelectbox, .stTextArea {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            h1, h2, h3, h4, h5, h6, label, span, p {
                color: #FFFFFF !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            body, .main, .block-container {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            textarea, input, .stRadio, .stSelectbox, .stTextArea {
                background-color: #f8f8f8 !important;
                color: #000000 !important;
            }
            h1, h2, h3, h4, h5, h6, label, span, p {
                color: #000000 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
