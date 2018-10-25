import flightradar24


def get_all_airlines():
    fr = flightradar24.Api()
    airlines = fr.get_airlines()
    return airlines


def get_airline(airline_code):
    airline = 'THY'  # Turkish Airlines
    fr = flightradar24.Api()
    flights = fr.get_flights(airline)
    print(flights)

    for key, value in flights.items():
        if isinstance(value, list):
            print(value)
