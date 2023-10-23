# AI Challenge | Web scraping with Generative AI!
# Blog: https://blogs.sap.com/2023/10/23/ai-challenge-web-scraping-with-generative-ai/
# Online app: https://gen-ai-challenge-web-data-extraction.streamlit.app/
# Created by: Sergiu Iatco | October, 2023
# https://www.linkedin.com/in/sergiuiatco/

import pandas as pd
import streamlit as st
# from streamlit_extras.add_vertical_space import add_vertical_space
from utility_settings import SaveResultsCsvJson
from sap_blog_statistics import SapBlogStatistics


def f_init_session():
    if 'df_file' not in st.session_state:
        st.session_state['df_file'] = pd.DataFrame()
    if 'df_results' not in st.session_state:
        st.session_state['df_results'] = pd.DataFrame()
    if 'df_ok_sum' not in st.session_state:
        st.session_state['df_ok_sum'] = pd.DataFrame()
    if 'df_ok_count' not in st.session_state:
        st.session_state['df_ok_count'] = pd.DataFrame()
    if 'df_ok' not in st.session_state:
        st.session_state['df_ok'] = pd.DataFrame()


def f_web_scraping(p_file_name):
    bls = SapBlogStatistics(p_file_name)
    bls.mt_iter_file()
    bls.mt_rename_cols(['url', 'OK', 'comments', 'likes', 'views'])
    bls.mt_convert_cols_to_int(['comments', 'likes', 'views'])
    df_file = bls.df_file
    df_results = bls.df_results
    ok_dict = bls.mt_calculate_totals()
    df_ok_sum = ok_dict['df_ok_sum']
    df_ok_count = ok_dict['df_ok_count']
    return df_file, df_results, df_ok_sum, df_ok_count, ok_dict


def f_download_button(p_df):
    lc_obj_save = SaveResultsCsvJson(p_df)
    lc_obj_save.generate_json_text_files()
    return lc_obj_save


def f_extract(p_file_name):
    df_file, df_results, df_ok_sum, df_ok_count, df_ok = f_web_scraping(p_file_name)
    st.session_state['df_file'] = df_file
    st.session_state['df_results'] = df_results
    st.session_state['df_ok_sum'] = df_ok_sum
    st.session_state['df_ok_count'] = df_ok_count
    st.session_state['df_ok'] = df_ok


f_init_session()

st.title("SAP Blog Statistics")
st.write('AI Challenge | Web scraping with Generative AI! 🤖')
st.write('Is it possible? Share the solution! 🤖')
st.write('For now, you can collect statistics with Python code. 🐍 😊')

bt_side_sel = st.sidebar.selectbox("Select an option",
                                   ['SAP AI Gen State',
                                    'SAP HANA ML Cloud Challenge 2022',
                                    'Upload SAP blog list'])

with st.sidebar:
#    add_vertical_space(1)
    st.markdown(
        '📖 Read the [blog](https://blogs.sap.com/2023/10/23/ai-challenge-web-scraping-with-generative-ai/)')

st.write(f'**{bt_side_sel}**')
if bt_side_sel == 'Upload SAP blog list':
    uploaded_file_disabled = False
else:
    uploaded_file_disabled = True

file_name = None
if bt_side_sel == 'SAP AI Gen State':
    file_name = 'sap_blog_url_ai_state_20231002.csv'

elif bt_side_sel == 'SAP HANA ML Cloud Challenge 2022':
    file_name = 'sap_blog_url_hana_ml_challenge_202211.csv'

uploaded_file = st.file_uploader("Choose a file", disabled=uploaded_file_disabled)

if uploaded_file is not None:
    file_name = uploaded_file

bt_extract_disabled = False
if bt_side_sel == 'Upload SAP blog list':
    if uploaded_file is None:
        bt_extract_disabled = True


st.button("Extract Statistics", disabled=bt_extract_disabled, on_click=f_extract, args=(file_name,), key='bt_extract')

obj_save = f_download_button(st.session_state['df_results'])

# st.write('List of Blogs')
# st.dataframe(st.session_state['df_file'], column_config={"url": st.column_config.LinkColumn("URL",
#                                                                                             help="Click 🎈"),
#                                                          })
st.write('Blog Statistics')
st.dataframe(st.session_state['df_results'], column_config={"url": st.column_config.LinkColumn("URL",
                                                                                               width='large',
                                                                                               help="Click 🎈"),
                                                            })
st.write('Statistics Total')
st.dataframe(st.session_state['df_ok_sum'])
st.write('Blog Reading Success Y/N')
st.dataframe(st.session_state['df_ok_count'])

col1, col2, = st.columns(2)
with col1:
    st.download_button(label="Download CSV",
                       data=obj_save.text,
                       file_name=obj_save.text_file)

with col2:
    st.download_button(label="Download JSON",
                       data=obj_save.json,
                       file_name=obj_save.json_file)
