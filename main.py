import requests
from bs4 import BeautifulSoup
import re
import csv


def collect_vehicle_data2(url):
    print("method 2")
    try:
        data = {}
        # url = "https://ikman.lk//en/ad/suzuki-alto-lxi-2011-for-sale-ratnapura-7"
        data["url"] = url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.prettify())
        vehicles = soup.find("div", {"class": "ui-panel-content ui-panel-block"})  # left-section--PoAuT
        #

        title = vehicles.find("h1", {"itemprop": "name"})
        title = title.text
        data["title"] = title
        #
        date_time = vehicles.find("span", {"class": "date"})
        date_time = date_time.text
        data["date_time"] = date_time

        location = vehicles.find("span", {"class": "location"})
        location = location.text.split(',')
        area = location[0]
        district = location[1]
        data["area"] = area
        data["district"] = district

        price = vehicles.find("span", {"class": "amount"})

        price = re.sub("[^\d\.]", "", price.text)

        data["price"] = price
        # print(price)
        # print(vehicles.prettify())
        otherdata = []
        other_data = vehicles.find("div", {"itemprop": "description"})
        # otherdata = (other_data.text.split(' '))
        otherdata = str(other_data.find("p")).split('<br/>')
        data["other data"] = otherdata
        vehicle_details = vehicles.find("div", {"class": "item-properties"})
        for details in vehicle_details.find_all('dl'):
            feature = details.find('dt')
            value = details.find('dd')
            print(feature, value)
            data[feature.text] = value.text
        print(data)
        return data
    except Exception as e:
        print(e)



def collect_vehicle_data1(url):
    print("method 1")
    try:
        data = {}
        data["url"] = url
        # page = requests.get("https://ikman.lk/en/ad/mercedes-benz-c200-premiure-2019-for-sale-colombo")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        vehicles = soup.find("div", {"class": "left-section--PoAuT"})  # left-section--PoAuT

        header = soup.find("div", {"class": "header--3WCle"})
        title = header.find("h1", {"class": "title--3s1R8"})
        title = title.text
        data["title"] = title

        date_time_location = header.find("span", {"class": "sub-title--37mkY"})
        date_time_location = date_time_location.text
        date_time = date_time_location[0]
        data["date_time"] = date_time

        area = date_time_location[1]
        district = date_time_location[2]
        data["area"] = area
        data["district"] = district


        price = vehicles.find("div", {"class": "amount--3NTpl"})
        price = re.sub("[^\d\.]", "", price.get_text())
        data["price"] = price

        vehicle_data = vehicles.find('div', {
            "class": "ad-meta--17Bqm justify-content-flex-start--1Xozy align-items-normal--vaTgD flex-wrap-wrap--2PCx8 flex-direction-row--27fh1 flex--3fKk1"})
        # print(vehicle_data.prettify())
        # header--3WCle  two-columns--19Hyo
        for vehicle in vehicle_data.find_all('div', {"class": "two-columns--19Hyo"}):
            # print(vehicle.prettify())
            value = ""
            value2 = ""
            feature = vehicle.find('div', {"class": "word-break--2nyVq"})
            try:
                value = vehicle.find('a', {"class": "ad-meta-desktop--1Zyra"})
                value = value.find('span')

            except:
                value2 = vehicle.find_all('div', {"class": "word-break--2nyVq"})
                value2 = value2[1]

            print(feature.text)
            try:
                print(value.text)
                data[feature.text] = value.text
            except:
                print(value2.text)
                data[feature.text] = value2.text

        otherdata = []
        other_data = vehicles.find("div", {"class": "description--1nRbz"})
        for info in other_data.find_all('p'):
            otherdata.append(info.text)

        data["other data"] = otherdata

        return data
    except Exception as e:
        return collect_vehicle_data2(url)
        print(e)
#
#
#
#
#
# # url = "https://ikman.lk/en/ads/sri-lanka/cars?&page=3"
#

def write_csv(data):
    print("writer")
    print(data)
    with open('data2.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # print(data, "sdsd")
        try:
            writer.writerow([data['url'],
                             data['title'],
                             data['date_time'],
                             data['area'],
                             data['district'],
                             data['price'],
                             data['Brand:'],
                             data['Model:'],
                             data['Trim / Edition:'],
                             data['Model year:'],
                             data['Condition:'],
                             data['Transmission:'],
                             data['Body type:'],
                             data['Fuel type:'],
                             data['Engine capacity:'],
                             data['Mileage:'],
                             data['other data']

                             ])
        except:
            pass



count = 409
vehicleUrls = []
collection = {}
while True:
    try:
        url = 'https://ikman.lk/en/ads/sri-lanka/cars?&page=' + str(count)
        print(url)
        f = open("url2.txt", "a")
        f.write(url+"\n")
        f.close()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        vehicles = soup.find("ul", {"class": "list--3NxGO"})
        for vehicle in vehicles.findAll('li'):
            vehicle_name = vehicle.find('a', {"class": "card-link--3ssYv"}, href=True)
            vehicle_url = "https://ikman.lk/" + vehicle_name['href']
            #
            try:
              tocsv = collect_vehicle_data1(vehicle_url)
              collection[vehicle_url] = collect_vehicle_data1(vehicle_url)
              write_csv(tocsv)
            except:
                pass;
        print(count)
        count = count + 1;
        print(len(vehicleUrls))
        print(collection)
    except Exception as e:
        import json

        with open('result.json', 'w') as fp:
            json.dump(collection, fp)
        print(e)
        break;




# url = ""

# try:
#     data = {}
#     url = "https://ikman.lk//en/ad/suzuki-alto-lxi-2011-for-sale-ratnapura-7"
#     data["url"] = url
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, "html.parser")
#         # print(soup.prettify())
#     vehicles = soup.find("div", {"class": "ui-panel-content ui-panel-block"})  # left-section--PoAuT
#         #
#
#     title = vehicles.find("h1", {"itemprop": "name"})
#     title = title.text
#     data["title"] = title
#         #
#     date_time = vehicles.find("span", {"class": "date"})
#     date_time = date_time.text
#     data["date_time"] = date_time
#
#     location = vehicles.find("span", {"class": "location"})
#     location = location.text.split(',')
#     area = location[0]
#     district = location[1]
#     data["area"] = area
#     data["district"] = district
#
#     price = vehicles.find("span", {"class": "amount"})
#
#     price = re.sub("[^\d\.]", "", price.text)
#
#     data["price"] = price
#         # print(price)
#         # print(vehicles.prettify())
#     otherdata = []
#     other_data = vehicles.find("div", {"itemprop": "description"})
#         # otherdata = (other_data.text.split(' '))
#     otherdata = str(other_data.find("p")).split('<br/>')
#     data["other data"] = otherdata
#     vehicle_details = vehicles.find("div", {"class": "item-properties"})
#     for details in vehicle_details.find_all('dl'):
#         feature = details.find('dt')
#         value = details.find('dd')
#         feature = feature.text
#         value = value.text
#         print(feature)
#         print(value)
#         data[str(feature)] = str(value)
#         # return data
# except Exception as e:
#     print(e, "sdsdsd")
