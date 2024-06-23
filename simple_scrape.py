import requests

def scrape_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        return f"An error occurred: {e}"

# Example usage
url = "https://cleanmybuilding.co/"
html_content = scrape_html(url)
print(html_content)
