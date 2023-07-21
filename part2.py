def scrape_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    asin = soup.find('th', text='ASIN').find_next('td').text.strip()
    manufacturer = soup.find('th', text='Manufacturer').find_next('td').text.strip()
    
    return product_description, asin, manufacturer

# Load the previously scraped data from the CSV file
loaded_products_data = []
with open('amazon_product_listings.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    loaded_products_data = list(reader)

# Scraping additional information for each product URL and updating the data
for product_data in loaded_products_data:
    product_url = product_data[0]
    description, asin, manufacturer = scrape_product_details(product_url)
    product_data.extend([description, asin, manufacturer])

# Saving the updated data to a new CSV file
with open('amazon_product_details.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Manufacturer'])
    writer.writerows(loaded_products_data)
