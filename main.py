from bs4 import BeautifulSoup as Bsoup
import requests
import re

# ie; conversion means the url which provvides conversion so named all the varaibles related to it with _conversion
url_conversion = "https://www.extravelmoney.com/rates/"

result_conversion = requests.get(url_conversion).text

document_conversion = Bsoup(result_conversion, "html.parser")

tbody_conversion = document_conversion.find("tbody")

trow_conversion = tbody_conversion.find("tr")

data = trow_conversion.find("td", string=re.compile(r'INR'))
# this finds INR even if it is a part of another word
# if we use this string=re.compile(r'\bINR\b') it will only find INR as a standalone word
data = data.string
data = data.replace("INR", "")
data_INR = float(data)
# data_INR contains the conversion rate into Indian Rupees

# going to get the crypto information
url_rate = "https://coinmarketcap.com/"

result_rate = requests.get(url_rate).text

document_rate = Bsoup(result_rate, "html.parser")

tbody_rate = document_rate.find("tbody")

trows_rate = tbody_rate.find_all(["tr"])

list_of_crypto_and_prices = {}
for items in trows_rate[:10]:
    name = items.contents[2]
    price = items.contents[3]
    correct_name = name.p.string
    correct_price = price.span.string
    list_of_crypto_and_prices[correct_name] = correct_price

key_pair = list_of_crypto_and_prices.keys()

value_pair = list_of_crypto_and_prices.values()

value_pair = [s[1:] for s in value_pair]

value_pair = [item.replace(",", "") for item in value_pair]

value_pair = [float(item) for item in value_pair]

value_pair = [item*data_INR for item in value_pair]

dict_of_converted_list = dict(zip(key_pair, value_pair))

x = 1

print("Rank : Currency : Price in INR")
for key, value in dict_of_converted_list.items():
    print(f"{x} : {key} : {value}₹")
    x = x+1
