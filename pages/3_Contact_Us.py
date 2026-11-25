import streamlit as st

from common import APP_TITLE, render_footer, render_header

st.set_page_config(page_title=f"Contact Us | {APP_TITLE}", page_icon="static/images/icar_1.png", layout="centered")

render_header()

st.markdown("### Contact Us")

CONTACTS = [
    {
        "role": "Director",
        "org": "ICAR-CIRCOT, Mumbai",
        "email": "director-circot@icar.org.in",
    },
    {
        "role": "Head, Mechanical Processing Division",
        "org": "ICAR-CIRCOT, Mumbai",
        "email": "dr.shanmugam@gmail.com",
    },
]

cols = st.columns(2)
for col, contact in zip(cols, CONTACTS):
    with col:
        with st.container(border=True):
            st.markdown(f"**{contact['role']}**")
            st.write(contact["org"])
            st.markdown(f"✉️ [{contact['email']}](mailto:{contact['email']})")

render_footer()
