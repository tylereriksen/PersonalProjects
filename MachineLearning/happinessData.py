import requests
import pandas as pd


def get_countries(url):
    text = requests.get(url).text
    COUNTRIES = []
    FIND_STR = "<td style=\"font-weight: bold; font-size:15px\">"
    index = text.index(FIND_STR)

    CHECK = {"C&ocirc;te d'Ivoire": "Ivory Coast",
             "Cabo Verde": "Cape Verde",
             "Holy See": "Vatacan City"}

    while len(COUNTRIES) < 195:
        count = 0
        country_name = ""
        while text[index + len(FIND_STR) + count] != "<": #and text[index + len(FIND_STR) + count] != "(":
            country_name += text[index + len(FIND_STR) + count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]

        COUNTRIES.append(country_name.strip())
        text = text[index + len(FIND_STR) + len(country_name):]
        try:
            index = text.index(FIND_STR)
        except:
            index = -1
    COUNTRIES.sort()
    return COUNTRIES


def get_happiness(url):
    dictionary = {}
    text = requests.get(url).text
    FIND_STR = "/happiness/\" class=\"graph_outside_link\" id=\""
    text = text[text.index(FIND_STR) + len(FIND_STR): ]
    index = text.index(">")

    CHECK = {"Bosnia & Herz.": "Bosnia and Herzegovina",
             "Domin. Rep.": "Dominican Republic",
             "USA": "United States of America",
             "UK": "United Kingdom",
             "UA Emirates": "United Arab Emirates"}

    while len(dictionary.keys()) < 141:
        count = 0
        country_name = ""
        while text[index + 1 + count] != "<":
            country_name += text[index + 1 + count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]


        index = text.index("<td>")
        count = 0
        happiness = ""
        while text[index + 4 + count] != "\r":
            happiness += text[index + 4 + count]
            count += 1
        happiness = float(happiness)
        dictionary[country_name] = happiness

        try:
            text = text[text.index(FIND_STR) + len(FIND_STR):]
            index = text.index(">")
        except:
            index = -1

    return dictionary


def get_GDP(url):
    dictionary = {}
    text = requests.get(url).text
    FIND_STR = "/GDP_per_capita_current_dollars/\" class=\"graph_outside_link\" id=\""
    text = text[text.index(FIND_STR) + len(FIND_STR):]
    index = text.index(">")

    CHECK = {"USA": "United States of America",
             "UK": "United Kingdom",
             "Tr.&Tobago": "Trinidad and Tobago",
             "Ant.& Barb.": "Antigua and Barbuda",
             "Domin. Rep.": "Dominican Republic",
             "Eq. Guinea": "Equatorial Guinea",
             "St. Vincent & ...": "Saint Vincent and the Grenadines",
             "Bosnia & Herz.": "Bosnia and Herzegovina",
             "Papua N.G.": "Papua New Guinea",
             "S.T.&Principe": "Sao Tome and Principe",
             "Solomon Isl.": "Solomon Islands",
             "R. of Congo": "Congo (Congo-Brazzaville)",
             "G.-Bissau": "Guinea-Bissau",
             "DR Congo": "Democratic Republic of the Congo",
             "C.A. Republic": "Central African Republic"}

    while len(dictionary.keys()) < 176:
        count = 0
        country_name = ""
        while text[index + 1 + count] != "<":
            country_name += text[index + 1 + count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]

        index = text.index("<td>")
        count = 0
        happiness = ""
        while text[index + 4 + count] != "\r":
            happiness += text[index + 4 + count]
            count += 1
        happiness = float(happiness)
        dictionary[country_name] = happiness

        try:
            text = text[text.index(FIND_STR) + len(FIND_STR):]
            index = text.index(">")
        except:
            index = -1

    return dictionary


def get_social(url):
    dictionary = {}
    text = requests.get(url).text
    text = text[text.index("<strong>Country</strong>"):]
    FIND_STR = "<td width=\"164\">"
    text = text[text.index(FIND_STR) + len(FIND_STR):]
    index = text.index(">")

    CHECK = {"Korea, South": "South Korea",
             "Cote D&#8217;Ivoire": "Ivory Coast"}

    while len(dictionary.keys()) < 128:
        count = 0
        country_name = ""
        while text[count] != "<":
            country_name += text[count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]

        NEW_STR = "<td width=\"215\">"
        index = text.index(NEW_STR)
        count = 0
        happiness = ""
        while text[index + len(NEW_STR) + count] != "<":
            happiness += text[index + len(NEW_STR) + count]
            count += 1
        happiness = float(happiness)
        dictionary[country_name] = happiness

        try:
            text = text[text.index(FIND_STR) + len(FIND_STR):]
            index = text.index(">")
        except:
            index = -1

    return dictionary


def get_life(url):
    dictionary = {}
    text = requests.get(url).text
    FIND_STR = "{\"country\":\""
    text = text[text.index(FIND_STR) + len(FIND_STR):]
    CHECK = {"Cabo Verde": "Cape Verde",
             "Brunei Darussalam": "Brunei",
             "DR Congo": "Democratic Republic of the Congo"}
    index = 0

    while index != -1:
        count = 0
        country_name = ""
        while text[count] != "\"":
            country_name += text[count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]

        NEW_STR = "\"hdi2019\":"
        index = text.index(NEW_STR)
        count = 0
        happiness = ""
        while text[index + len(NEW_STR) + count] != "}":
            happiness += text[index + len(NEW_STR) + count]
            count += 1
        happiness = float(happiness)
        dictionary[country_name] = happiness

        try:
            index = text.index(FIND_STR)
            text = text[index + len(FIND_STR): ]
        except:
            index = -1

    return dictionary


def get_crime(url):
    dictionary = {}
    text = requests.get(url).text
    FIND_STR = "<a to=\"[object Object]\""
    text = text[text.index(FIND_STR) + len(FIND_STR):]
    index = text.index(">")

    CHECK = {"Czech Republic": "Czechia"}

    while len(dictionary.keys()) < 136:
        count = 0
        country_name = ""
        while text[index + 1 + count] != "<":
            country_name += text[index + 1 + count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]

        index = text.index("<td>")
        count = 0
        happiness = ""
        while text[index + 4 + count] != "<":
            happiness += text[index + 4 + count]
            count += 1
        happiness = float(happiness)
        dictionary[country_name] = happiness

        try:
            text = text[text.index(FIND_STR) + len(FIND_STR):]
            index = text.index(">")
        except:
            index = -1

    return dictionary


def get_growth(url):
    dictionary = {}
    text = requests.get(url).text
    FIND_STR = "/Economic_growth/\" class=\"graph_outside_link\" id=\""
    text = text[text.index(FIND_STR) + len(FIND_STR):]
    index = text.index(">")

    CHECK = {"USA": "United States of America",
             "UK": "United Kingdom",
             "UA Emirates": "United Arab Emirates",
             "Tr.&Tobago": "Trinidad and Tobago",
             "Ant.& Barb.": "Antigua and Barbuda",
             "Domin. Rep.": "Dominican Republic",
             "Eq. Guinea": "Equatorial Guinea",
             "St. Vincent & ...": "Saint Vincent and the Grenadines",
             "Bosnia & Herz.": "Bosnia and Herzegovina",
             "Papua N.G.": "Papua New Guinea",
             "S.T.&Principe": "Sao Tome and Principe",
             "Solomon Isl.": "Solomon Islands",
             "R. of Congo": "Congo (Congo-Brazzaville)",
             "G.-Bissau": "Guinea-Bissau",
             "DR Congo": "Democratic Republic of the Congo",
             "C.A. Republic": "Central African Republic"}

    while len(dictionary.keys()) < 175:
        count = 0
        country_name = ""
        while text[index + 1 + count] != "<":
            country_name += text[index + 1 + count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]

        index = text.index("<td>")
        count = 0
        happiness = ""
        while text[index + 4 + count] != "\r":
            happiness += text[index + 4 + count]
            count += 1
        happiness = float(happiness)
        dictionary[country_name] = happiness

        try:
            text = text[text.index(FIND_STR) + len(FIND_STR):]
            index = text.index(">")
        except:
            index = -1

    return dictionary


def get_political(url):
    dictionary = {}
    text = requests.get(url).text
    FIND_STR = "/wb_political_stability/\" class=\"graph_outside_link\" id=\""
    text = text[text.index(FIND_STR) + len(FIND_STR):]
    index = text.index(">")

    CHECK = {"USA": "United States of America",
             "UK": "United Kingdom",
             "UA Emirates": "United Arab Emirates",
             "Tr.&Tobago": "Trinidad and Tobago",
             "Ant.& Barb.": "Antigua and Barbuda",
             "Domin. Rep.": "Dominican Republic",
             "Eq. Guinea": "Equatorial Guinea",
             "St. Vincent & ...": "Saint Vincent and the Grenadines",
             "Bosnia & Herz.": "Bosnia and Herzegovina",
             "Papua N.G.": "Papua New Guinea",
             "S.T.&Principe": "Sao Tome and Principe",
             "Solomon Isl.": "Solomon Islands",
             "R. of Congo": "Congo (Congo-Brazzaville)",
             "G.-Bissau": "Guinea-Bissau",
             "DR Congo": "Democratic Republic of the Congo",
             "C.A. Republic": "Central African Republic"}

    while len(dictionary.keys()) < 194:
        count = 0
        country_name = ""
        while text[index + 1 + count] != "<":
            country_name += text[index + 1 + count]
            count += 1

        if country_name in CHECK.keys():
            country_name = CHECK[country_name]

        index = text.index("<td>")
        count = 0
        happiness = ""
        while text[index + 4 + count] != "\r":
            happiness += text[index + 4 + count]
            count += 1
        happiness = float(happiness)
        dictionary[country_name] = happiness

        try:
            text = text[text.index(FIND_STR) + len(FIND_STR):]
            index = text.index(">")
        except:
            index = -1

    return dictionary


def put_into_dataframe(data, countries):
    insert_list = [None] * len(countries)
    for country in data.keys():
        if country in countries:
            index = countries.index(country)
            insert_list[index] = data[country]
        else:
            PRINT = True
            for c in countries:
                if country in c:
                    index = countries.index(c)
                    insert_list[index] = data[country]
                    PRINT = False
            if PRINT:
                print(country)

    return insert_list


def main():
    COUNTRIES = get_countries('https://www.worldometers.info/geography/alphabetical-list-of-countries/')

    MASTER_DICT = {"Countries": COUNTRIES}

    HAPPINESS = get_happiness("https://www.theglobaleconomy.com/rankings/happiness/")
    GDP = get_GDP("https://www.theglobaleconomy.com/rankings/GDP_per_capita_current_dollars/")
    SOCIAL = get_social("https://www.mapsofworld.com/answers/economics/countries-perform-better-social-progress-index/#")
    LIFE = get_life("https://worldpopulationreview.com/country-rankings/standard-of-living-by-country")
    CRIME = get_crime("https://worldpopulationreview.com/country-rankings/crime-rate-by-country")
    POLITICAL = get_political("https://www.theglobaleconomy.com/rankings/wb_political_stability/")
    GROWTH = get_growth("https://www.theglobaleconomy.com/rankings/Economic_growth/")

    insert_happy = put_into_dataframe(HAPPINESS, COUNTRIES)
    insert_GDP = put_into_dataframe(GDP, COUNTRIES)
    insert_growth = put_into_dataframe(GROWTH, COUNTRIES)
    insert_social = put_into_dataframe(SOCIAL, COUNTRIES)
    insert_life = put_into_dataframe(LIFE, COUNTRIES)
    insert_crime = put_into_dataframe(CRIME, COUNTRIES)
    insert_political = put_into_dataframe(POLITICAL, COUNTRIES)

    MASTER_DICT["Happiness"] = insert_happy
    MASTER_DICT["GDP"] = insert_GDP
    MASTER_DICT["Growth"] = insert_growth
    MASTER_DICT["Social"] = insert_social
    MASTER_DICT["Life"] = insert_life
    MASTER_DICT["Crime"] = insert_crime
    MASTER_DICT["Political"] = insert_political
    df = pd.DataFrame(MASTER_DICT)
    return df.dropna().reset_index(drop=True)


if __name__ == '__main__':
    df = main()
    df.to_pickle("./country_data.pkl")
