import streamlit as st
import requests

API_TOKEN = ""

st.set_page_config(
    page_title="News Aggregator",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)


def pretty(s: str) -> str:
    try:
        return dict(js="JavaScript")[s]
    except KeyError:
        try:
            return s.capitalize()
        except KeyError:
            pass


def run_search(query, lang, country, API_TOKEN):
    r = requests.get(f"https://gnews.io/api/v4/search?q={query}&lang={lang}&country={country}&token={API_TOKEN}")
    if r.status_code == 200:
        data_dump = r.json()
        articles = data_dump['articles']
        for article in articles:
            f"""## {article['source']['name']} | [{article['title']}]({article['url']})"""
            st.write(article['publishedAt'][0:10])
            st.write(article['content'].split('...')[0], "...")
            """\n\n\n"""
    else:
        st.write(r.status_code)
    return r


st.title("News Aggregator")

query = ''
_lang_filter = 'Any'
_country_filter = 'Any'

filters = st.multiselect('Filters',
                         options=['Topic', 'Country', 'Language'],
                         default=None, format_func=pretty)
if "Topic" in filters:
    query = st.text_area('Article topic to search for', height=2, max_chars=64).lower()

if "Language" in filters:
    lang = st.selectbox("Which language articles would you like to search?",
                        options=['All', 'English', 'Spanish'])
    if lang == "All":
        _lang_filter = "Any"
    elif lang == "English":
        _lang_filter = 'en'
    elif lang == "Spanish":
        _lang_filter = 'es'

if "Country" in filters:
    country = st.selectbox("Which country would you like to select articles from?",
                           options=['USA', 'UK', 'Canada'])
    if country == 'USA':
        _country_filter = 'us'
    elif country == 'UK':
        _country_filter = 'gb'
    elif country == 'Canada':
        _country_filter = 'ca'


submit_button = st.button("Run Search!")
if submit_button:
    st.write('Beginning search...')
    run_search(query, _lang_filter, _country_filter, API_TOKEN)
