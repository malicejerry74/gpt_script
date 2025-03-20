import streamlit as st
from generate import generate_script
# 标题
st.title('vidio_generator')
# 侧边栏
with st.sidebar:
    openai_api_key = st.text_input('请输入openai api密钥', type='password')
    st.markdown('[获取密钥方式](https://auth.openai.com/log-in)')
# 主页面
subject = st.text_input('请输入视频的主题')
vidio_length = st.number_input('请输入视频的大致时长（单位：分钟）', min_value=0.1, value=1.0, step=0.1)
creativity = st.slider('请输入视频的创造力（数字小更严谨，数字大更多样）', min_value=0.1, max_value=1.0, value=0.7, step=0.1)
submit = st.button('提交')

if submit and not openai_api_key:
    st.info('请输入你的密钥')
    st.stop()
if submit and not subject:
    st.info('请输入你的主题')
    st.stop()
if vidio_length <=0.1:
    st.info('视频时长应该大于或等于0.1')
    st.stop()
if submit:
    with st.spinner('ai正在思考，请稍等..'):
        search_result, title, script = generate_script(subject, vidio_length, creativity, openai_api_key)
        st.success('视频脚本生成成功！')

    st.subheader('标题')
    st.write(title)

    st.subheader('脚本')
    st.write(script)

    with st.expander('维基百科搜索结果'):
        st.info(search_result)

