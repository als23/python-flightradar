import csv
import json


def load_csv(file_path):
    return_list = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            return_list.append(row)
    return return_list


def load_json(file_path):
    with open(file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)
    return data


def process_all_flights(list_airports, list_countries, list_flights):

    # Node table
    countries_dict = {}
    for country in list_countries:
        country_code = country['alpha-2']
        name = country['name']

        countries_dict[country_code] = name

    airports_dict = {}
    list_all_airports = []
    for airports in list_airports:
        iata = airports['iata']
        iso = airports['iso']
        continent = airports['continent']
        airports_dict[iata] = [iso, continent]

        if iso in countries_dict:
            country_name = countries_dict[iso]

        list_all_airports.append([iata, iso, country_name, continent])

    # Edge table
    list_countries_appears = {}
    countries_appears = 0

    list_all_flights = []

    for flights in list_flights:
        from_airport = flights[1]
        to_airport = flights[2]
        capacity = flights[4]
        if capacity == "Heavy":
            airplane_capacity = 309
        elif capacity == "Medium":
            airplane_capacity = 184
        elif capacity == "Light":
            airplane_capacity = 11

        list_all_flights.append([from_airport, to_airport, 'Directed', airplane_capacity])
        # print(from_airport + ',' + to_airport + ',' + str(airplane_capacity))

        # Statistics Only
        from_airport_country = airports_dict[from_airport][0]
        to_airport_country = airports_dict[to_airport][0]
        if from_airport_country not in list_countries_appears:
            list_countries_appears[from_airport_country] = country_name
            countries_appears += 1
        if to_airport_country not in list_countries_appears:
            list_countries_appears[to_airport_country] = country_name
            countries_appears += 1

    # Process nodes(airports) csv
    csv_nodes = 'dataset_processed/1-nodes-airports.csv'
    with open(csv_nodes, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id', 'label', 'country_iso', 'country_name', 'continent'])
        for airport in list_all_airports:
            airport_code = airport[0]
            airports_country_iso = airport[1]
            airport_country_name = airport[2]
            airport_continent = airport[3]
            #print(airport_code + ',' + airports_country_iso + ',' + airport_country_name + ',' + airport_continent)
            writer.writerow([airport_code, airport_code, airports_country_iso, airport_country_name, airport_continent])

    # Process edge(flights) csv
    csv_edges = 'dataset_processed/1-edges-flights.csv'
    with open(csv_edges, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['source', 'target', 'type', 'capacity'])
        for flight in list_all_flights:
            from_airport = flight[0]
            to_airport = flight[1]
            directed = flight[2]
            airplane_capacity = flight[3]
            #print(from_airport + ',' + to_airport + ',' + directed + ',' + str(airplane_capacity))
            writer.writerow([from_airport, to_airport, directed, str(airplane_capacity)])

    print('Countries appears: ' + str(countries_appears) + '/' + str(len(list_countries)))


file_output = 'dataset_processed/output.csv'
list_flights = load_csv(file_output)
#print(list_flights)

file_airports = 'dataset/airports_data.json'
list_airports = load_json(file_airports)
#print(list_airports)

file_countries = 'dataset/countries_data.json'
list_countries = load_json(file_countries)
#print(list_countries)

process_all_flights(list_airports, list_countries, list_flights)


def process_international_flights(list_airports, list_countries, list_flights):
    airports_dict = {}
    for airports in list_airports:
        iata = airports['iata']
        iso = airports['iso']
        continent = airports['continent']

        airports_dict[iata] = [iso, continent]

    countries_dict = {}
    for country in list_countries:
        country_code = country['alpha-2']
        name = country['name']

        countries_dict[country_code] = name

    international_flights = []
    domestic_flight = 0
    international_flight = 0

    list_countries_appears = {}
    countries_appears = 0

    for flights in list_flights:
        from_airport = flights[1]
        to_airport = flights[2]
        capacity = flights[4]
        if capacity == "Heavy":
            airplane_capacity = 309
        elif capacity == "Medium":
            airplane_capacity = 184
        elif capacity == "Light":
            airplane_capacity = 11

        if from_airport in airports_dict:
            if to_airport in airports_dict:
                from_airport_country = airports_dict[from_airport][0]
                from_airport_continent = airports_dict[from_airport][1]
                to_airport_country = airports_dict[to_airport][0]
                to_airport_continent = airports_dict[to_airport][1]

                # Country list
                if from_airport_country not in list_countries_appears:
                    if from_airport_country in countries_dict:
                        country_name = countries_dict[from_airport_country]
                        list_countries_appears[from_airport_country] = [country_name, from_airport_continent]
                        countries_appears += 1
                    else:
                        print('Country not found: ' + from_airport_country + ',' + from_airport)

                if to_airport_country not in list_countries_appears:
                    if to_airport_country in countries_dict:
                        country_name = countries_dict[to_airport_country]
                        list_countries_appears[to_airport_country] = [country_name, to_airport_continent]
                        countries_appears += 1
                    else:
                        print('Country not found: ' + to_airport_country + ',' + to_airport)

                # Flight list
                if from_airport_country != to_airport_country:
                    international_flights.append([from_airport_country, to_airport_country, 'Directed', airplane_capacity])
                    international_flight += 1
                else:
                    domestic_flight += 1
            else:
                print('Airport not found:' + to_airport)
        else:
            print('Airport not found:' + from_airport)

    # Process nodes(countries) csv
    csv_nodes = 'dataset_processed/2-nodes-countries.csv'
    with open(csv_nodes, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id', 'label', 'continent'])
        for key, value in list_countries_appears.items():
            country_code = key
            country_name = value[0]
            country_continent = value[1]
            #print(country_code + ',' + country_name + ',' + country_continent)
            writer.writerow([country_code, country_name, country_continent])

    # Process edge(international flights) csv
    csv_edges = 'dataset_processed/2-edges-international-flights.csv'
    with open(csv_edges, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['source', 'target', 'type', 'capacity'])
        for flight in international_flights:
            from_airport_country = flight[0]
            to_airport_country = flight[1]
            directed = flight[2]
            airplane_capacity = flight[3]
            #print(from_airport_country + ',' + to_airport_country + ',' + directed + ',' + str(airplane_capacity))
            writer.writerow([from_airport_country, to_airport_country, directed, str(airplane_capacity)])

    print('Domestic flights: ' + str(domestic_flight) + '/' + str(len(list_flights)))
    print('International flights: ' + str(international_flight) + '/' + str(len(list_flights)))
    print('Countries appears: ' + str(countries_appears) + '/' + str(len(list_countries)))
    #return international_flights



#file_output = 'dataset_processed/output.csv'
#list_flights = load_csv(file_output)
# print(list_flights)

#file_airports = 'dataset/airports_data.json'
#list_airports = load_json(file_airports)
# print(list_airports)

#file_countries = 'dataset/countries_data.json'
#list_countries = load_json(file_countries)
# print(list_countries)

#process_international_flights(list_airports, list_countries, list_flights)


