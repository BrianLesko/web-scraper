from bs4 import BeautifulSoup
import streamlit as st
import requests
import bs4 as bs4
from gui_cusomizations import about
from gui_cusomizations import hide_streamlit_header_footer
import numpy as np

def scrape_text_from(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ''
            for p in soup.find_all('p'):
                text += p.text
            return text
        else:
            st.write("An Error Occurred: Unable to fetch the webpage.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

def get_links_from(url):
    from urllib.parse import urlparse, urljoin
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    parsed_url = urlparse(url)
    domain = parsed_url.scheme + '://' + parsed_url.netloc
    print('Domain root is: ', domain)
    links = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(domain, link['href']) 
        links.append(full_url)
    return links

def main():
    hide_streamlit_header_footer()

    with st.sidebar:
        about()

    st.title('Web Scraper')
    #url = st.text_input("Paste a URL here")

    url = st.chat_input("Paste a URL here")
    
    if url: 
        st.chat_message("user").write(url)

        links = get_links_from(url)
        text = scrape_text_from(url)

        response_1 = "This Website containts " + str(len(text)) + " characters and " + str(len(links)) + " links"

        st.chat_message("assistant").write(response_1)

        response_2 = 'The first words are: " ' + text[:50] + ' ..." '

        st.chat_message("assistant").write(response_2)

        response_3 = 'Would you like to download the text or links?'

        st.chat_message("assistant").write(response_3)

        col1,  col2, gap, col3, col4 = st.columns([.5,1,.5,1,.5])
        with col2:
            text_file = text
            file_name = "text fronm" + url + ".txt"
            st.download_button(
                label="Download Text as .txt",data=text_file,
                file_name=file_name,
                mime="text/plain"
                )
        with col3:
            csv_links = '\n'.join(np.array(links).flatten())
            file_name = "links_from_" + url.replace("://", "_").replace("/", "_") + ".txt"
            st.download_button(
                label="Download Links as .txt",data=csv_links,
                file_name=file_name,
                mime="text/plain"
                )
main()