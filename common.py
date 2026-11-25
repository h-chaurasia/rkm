"""Shared header/footer and constants used across every page."""
import streamlit as st

APP_TITLE = "RKMPred: Machine Learning based Yarn Tenacity Predictor"
ICAR_LOGO = "static/images/icar_1.png"


def render_header():
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.image(ICAR_LOGO, width=90)
    with col_title:
        st.markdown(f"<h1 style='margin-top:0; text-align:center;'>{APP_TITLE}</h1>", unsafe_allow_html=True)
    st.divider()


def render_footer():
    st.markdown(
        """
        <hr>
        <p style='text-align:center; color:grey; font-size:0.85em;'>
        &copy; 2026 ICAR-Central Institute for Research on Cotton Technology (CIRCOT), Mumbai. All rights reserved.
        </p>
        """,
        unsafe_allow_html=True,
    )
