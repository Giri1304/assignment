import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listing(url, num_pages):
    all_products = []
    base_url = url.split('/s?')[0]
    
    for page_num in range(1, num_pages + 1):
        page_url = url + f"&ref=sr_pg_{page_num}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', {'data-asin': True})
        
        for product in products:
            product_url = base_url + product.find('a', class_='a-link-normal')['href']
            product_name = product.find('span', class_='a-text-normal').text.strip()
            product_price = product.find('span', class_='a-offscreen').text.strip()
            product_rating = product.find('span', class_='a-icon-alt')
            rating = product_rating.text.strip() if product_rating else "N/A"
            num_reviews = product.find('span', {'data-reviews-text': True}).text.strip()
            
            all_products.append([product_url, product_name, product_price, rating, num_reviews])
    
    return all_products

# URL for product listing pages
main_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Number of pages to scrape
num_pages_to_scrape = 20

# Scraping product listings from multiple pages
all_products_data = scrape_product_listing(main_url, num_pages_to_scrape)

# Saving the data to a CSV file
with open('amazon_product_listings.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
    writer.writerows(all_products_data)
