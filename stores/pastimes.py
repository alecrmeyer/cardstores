from bs4 import BeautifulSoup
import requests

class Pastimes:
    url_base = 'https://www.pastimes.net/products/search?q='

    # Convert card text to the url 
    def query_to_url(self, url, query):
        ret = url + query.replace(" ", "+") + "&c=1"
        return ret

    # return X from the phrase "X In Stock"
    def get_quant_from_text(self, text):
        split_text = text.split()
        if split_text[0] == "Out":
            return 0
        else: 
            return split_text[0]

    def get_card(self, card_name):
        total_count = 0
        url = self.query_to_url(self.url_base, card_name)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html5lib')
        products = soup.find('div', class_='products-container browse')
        all_items = products.find_all('div', class_='inner')
        for card in all_items:
            name = card.find('h4', class_='name small-12 medium-4')
            if name != None and name.text == card_name:
                variants = card.find('div', class_='variants')
                quantities = variants.find_all('span', class_ = 'variant-short-info variant-qty')
                for quantity in quantities:
                    count = self.get_quant_from_text(quantity.text.strip())
                    total_count += int(count)
        return total_count


        
