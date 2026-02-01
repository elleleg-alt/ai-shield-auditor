import streamlit as st

st.title("🎯 Test App")
st.write("If you can see this, Streamlit is working!")

name = st.text_input("Enter your name")
if name:
    st.success(f"Hello, {name}!")

if st.button("Click me"):
    st.balloons()
    st.write("Button clicked! ✅")
