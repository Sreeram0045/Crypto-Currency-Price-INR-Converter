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

# This url leads to the website containing information about each cryptocurrency
url_rate = "https://coinmarketcap.com/"

result_rate = requests.get(url_rate).text

document_rate = Bsoup(result_rate, "html.parser")

tbody_rate = document_rate.find("tbody")
# founs the location of the dat ie;The data is located inside a table
trows_rate = tbody_rate.find_all(["tr"])
# created a dictionary to store the raw data
list_of_crypto_and_prices = {}
# for loop goes through each row of the table
# The data we need is situated in the 2nd coloumn and 3rd coloumn , the former contains name of the cryptocurrency and the latter contains the price(in dollars)
for items in trows_rate[:10]:
    name = items.contents[2]
    price = items.contents[3]
    correct_name = name.p.string
    correct_price = price.span.string
    list_of_crypto_and_prices[correct_name] = correct_price

# separates the key of the dictionary to a list
key_pair = list_of_crypto_and_prices.keys()
# separates the value of the dictionary to a list
value_pair = list_of_crypto_and_prices.values()
# strips the dollar sign form each of the prices which is located at the first position of the string
value_pair = [s[1:] for s in value_pair]
# replaces the comma in the price with a no space string
value_pair = [item.replace(",", "") for item in value_pair]
# the value is then converted to float
value_pair = [float(item) for item in value_pair]
# mutiplied with the conversion rate
value_pair = [item*data_INR for item in value_pair]

dict_of_converted_list = dict(zip(key_pair, value_pair))
# prints along with the rounded value
x = 1
print("Rank : Currency : Price in INR")
for key, value in dict_of_converted_list.items():
    rounded_value = round(value)
    print(f"{x} : {key} : {value}\u20B9 : \u2245 {rounded_value}\u20B9")
    x += 1
