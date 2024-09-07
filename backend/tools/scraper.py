from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Define the tool using the @tool decorator
@tool
def get_markdown_from_url(url: str) -> str:
    """Fetch HTML content from a URL and convert it to markdown."""
    try:
        # Send an HTTP request to the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the raw HTML of the page
        raw_html = str(soup)

        # Convert the HTML to Markdown
        markdown_text = md(raw_html)

        # Return the markdown formatted text
        return markdown_text.strip()

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the URL: {e}"