
import logging  
from urllib.parse import urlparse  # For parsing URLs into components

# Configure logging to show INFO level messages and above
logging.basicConfig(level=logging.INFO)

# Function to validate if a given string is a correct format for URL
def is_valid_url(url):
    parsed_url = urlparse(url)  # Breaks the URL into components (scheme, netloc, path, etc.)
    # This returns True just if both scheme (e.g., http/https) and netloc (domain) are present!
    return all([parsed_url.scheme, parsed_url.netloc])


