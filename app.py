import streamlit as st

st.title("Hello 최 👋")
st.markdown(
    """ 
    This is a playground for you to try Streamlit and have fun. 

    **There's :rainbow[so much] you can build!**
    
    We prepared a few examples for you to get started. Just 
    click on the buttons above and discover what you can do 
    with Streamlit. 
    """
)

# GitHub Raw 이미지 URL 설정 (확장자에 맞춰 .png 또는 .jpg 변경 필요)
GITHUB_IMAGE_URL = "https://raw.githubusercontent.com/<사용자명>/<저장소명>/<브랜치명>/image1.png"

# 이미지 출력
st.image(
    GITHUB_IMAGE_URL,
    caption="GitHub에서 불러온 이미지",
    use_container_width=True
)

if st.button("Send balloons!"):
    st.balloons()
