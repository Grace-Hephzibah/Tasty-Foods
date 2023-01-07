import streamlit as st
import test
from PIL import Image

t = test.result()

foods = t.food()

favicon = Image.open("imgs/logo.png")
st.set_page_config(page_title='Tasty Foods', page_icon = favicon)

st.markdown("<h1 style='text-align: center;'>Tasty Foods 🍜</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Food Recommendation System 😋 </h1>", unsafe_allow_html=True)

st.write("-----------------")
st.write('''###### Explore My Code Here: https://github.com/Grace-Hephzibah/Food-Recommender''')
st.write('''###### Kaggle: https://www.kaggle.com/code/gracehephzibahm/food-recommendation-system-easy-comprehensive/''')

st.write("-----------------")
food_choice = st.selectbox("Pick a Food ", foods)
st.write("------------------")

c1, c2, c3 = st.columns(3)

m1, m2, m3 = t.query(food_choice)

with c1:
    st.subheader("Simple Content Based Filtering")
    st.write("Recommends food based on similar foods")
    st.write("------------------")
    for index, ele in enumerate(m1):
        st.write(index,ele.title())
    st.write("------------------")

with c2:
    st.subheader("Collaborative Based Filtering")
    st.write("Recommends food based on similar users")
    st.write("------------------")
    if m3 == None:
        st.write("**Less user ratings for this food item !!!**")
        st.write("So, the recommender cannot pull any recommendations ")
    else:
        for index, ele in enumerate(m3):
            st.write(index, ele.title())

    st.write("------------------")

with c3:
    st.subheader("Advanced Content Based Filtering")
    st.write("Recommends food based on similar foods and its features")
    st.write("------------------")
    for index, ele in enumerate(m2):
        st.write(index, ele.title())
    st.write("------------------")

st.write("------------------")
st.subheader("✨ By Grace Hephzibah For SheBuilds Hackathon ✨")
st.write("------------------")