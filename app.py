import streamlit as st

import streamlit as st

st.title("Page 1")

import streamlit as st

def page_2():
    st.title("Page 2")

pg = st.navigation(["page_1.py", page_2])
pg.run()
