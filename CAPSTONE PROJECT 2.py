import requests
from bs4 import BeautifulSoup
from datetime import datetime

def check_website_availability(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking website availability: {e}")
        return False

def check_phishing_website(url):
    try:
        # Check website availability
        if not check_website_availability(url):
            return "Website is not available on the internet"

        # Get Alexa rank
        alexa_rank = get_alexa_rank(url)

        # Check if rank is above average and website is available over a long time
        if alexa_rank is not None:
            if alexa_rank > 100000 and is_website_old(url):
                return "Not a phishing website"
            else:
                return "Phishing website"
        else:
            return "Alexa rank not available"
    except Exception as e:
        print(f"Error checking phishing website: {e}")
        return "Error occurred"

def get_alexa_rank(url):
    try:
        alexa_url = f"https://www.alexa.com/siteinfo/{url}"
        response = requests.get(alexa_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            rank_element = soup.find("div", class_="rank-global")
            if rank_element:
                rank = rank_element.text.strip().replace(',', '')  # Remove commas from rank
                return int(rank)
        return None
    except Exception as e:
        print(f"Error fetching Alexa rank: {e}")
        return None

def is_website_old(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            creation_date = datetime.strptime(response.headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
            current_date = datetime.now()
            time_difference = (current_date - creation_date).days
            if time_difference >= 365:  # Check if website is older than 1 year
                return True
        return False
    except Exception as e:
        print(f"Error checking website creation date: {e}")
        return False

# Example usage
website_url = "https://www.google.com"  # Replace with the URL of the website you want to check
print("Checking website availability...")
if check_website_availability(website_url):
    print("Website is available.")
    print("Checking if it's a phishing website...")
    result = check_phishing_website(website_url)
    print("Result:", result)
else:
    print("Website is not available.")
