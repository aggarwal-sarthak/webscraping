from bs4 import BeautifulSoup
import requests
import pandas as pd

# EXTRACTION OF PRODUCT NAME
def get_ProductName(soup):
    try:
        # PRODUCT NAME
        title_string = soup.find("span", attrs={"id": 'productTitle'}).string.strip()
    except AttributeError:
        title_string = "N/A"

    return title_string


# EXTRACTION OF PRODUCT PRICE
def get_ProductPrice(soup):
    try:
        # PRODUCT PRICE
        price = soup.find("span", attrs={'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={'class':"a-offscreen"}).string.strip()
    except AttributeError:
        try:
            # ANY SALE IF AVAILABLE
            price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()
        except:
            price = "N/A"

    return price


# EXTRACTION OF PRODUCT RATING
def get_ProductRating(soup):
    try:
        # PRODUCT RATING
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = "New To Amazon"

    return rating


# EXTRACTION OF SELLER NAME
def get_SellerName(soup):
    try:
        # STOCK AVAILABILITY
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

        if available == "In stock":
            # SELLER NAME
            available = soup.find("div", attrs={'id':"merchant-info"}).find("a", attrs={'class':"a-link-normal"}).find("span").string.strip()
    except AttributeError:
        # OUT OF STOCK (IF)
        available = "Out Of Stock"

    return available



if __name__ == '__main__':
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # GIVEN URL
    URL = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

    # HTTP REQUEST
    webpage = requests.get(URL, headers=HEADERS)

    # SOUP WITH HTML METADATA
    soup = BeautifulSoup(webpage.content, "html.parser")

    # LINKS OF AVAILABLE OBJECTS
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
    # STORING LINKS IN LIST
    links_list = []

    # EXTRACTION OF LINKS
    for link in links:
        links_list.append(link.get('href'))

    # DICTIONARY FOR STORING IN CSV
    d = {"Product Name": [], "Price": [], "Ratings (Out Of 5)": [], "Seller Name": []} 
    i = 0

    # EXTRACTION OF PRODUCT DETAILS
    for link in links_list:
        print("Product "+str(i+1))

        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        i += 1

        # DISPLAY REQUIRED INFO
        d["Product Name"].append(get_ProductName(new_soup))
        d["Price"].append(get_ProductPrice(new_soup))
        d["Ratings (Out Of 5)"].append(get_ProductRating(new_soup))
        d["Seller Name"].append(get_SellerName(new_soup))

    # CONVERSION OF DICTIONARY TO CSV
    amazon_df = pd.DataFrame(d)
    amazon_df.to_csv("Data.csv", index=False)