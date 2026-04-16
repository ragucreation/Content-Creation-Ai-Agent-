import streamlit as st

val = st.chat_input("Test", accept_file=True)
if val:
    st.write(type(val))
    st.write(val)
