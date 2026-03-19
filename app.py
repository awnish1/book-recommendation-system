import streamlit as st
from app_logic import recommend,get_books

st.title("Book Recommendation System")

book_list=get_books()

selected_book=st.selectbox("Choose a book", book_list)

if st.button("Recommend"):
    recommendations=recommend(selected_book)

    st.subheader("Recommended Books:")

    cols=st.columns(5)

    for i,(title, image) in enumerate(recommendations):
        with cols[i]:
            st.image(image)
            st.caption(title)