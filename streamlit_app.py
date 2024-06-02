import streamlit as st

from src.body import plot_body_weight 

st.title("Weight data.")  # Display a title
st.write("This is a line plot of weight measures.")  # Display some text

st.pyplot(plot_body_weight())

# You can add more elements here, like:
# - Images: st.image("path/to/image.jpg")
# - Buttons: st.button("Click me!")
# - Checkboxes: st.checkbox("Select this")
# - Text input: name = st.text_input("Enter your name:")

