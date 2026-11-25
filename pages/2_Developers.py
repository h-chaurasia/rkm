import streamlit as st

from common import APP_TITLE, render_footer, render_header

st.set_page_config(page_title=f"Developers | {APP_TITLE}", page_icon="static/images/icar_1.png", layout="wide")

render_header()

st.markdown("### Developers")

DEVELOPERS = [
    {
        "name": "Dr. Himanshushekhar Chaurasia",
        "role": "Scientist (Computer Application & IT)",
        "org": "ICAR-Central Institute for Research on Cotton Technology",
        "email": "h.chaurasia@icar.org.in",
    },
    {
        "name": "Dr. N. Shanmugam",
        "role": "Head, Mechanical Processing Division",
        "org": "ICAR-Central Institute for Research on Cotton Technology",
        "email": "dr.shanmugam@gmail.com",
    },
]

cols = st.columns(2)
for col, dev in zip(cols, DEVELOPERS):
    with col:
        with st.container(border=True):
            st.markdown(f"**{dev['name']}**")
            st.write(dev["role"])
            st.write(dev["org"])
            st.markdown(f"✉️ [{dev['email']}](mailto:{dev['email']})")

render_footer()
