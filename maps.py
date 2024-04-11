import requests

def get_distanse(origin, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"
    response = requests.get(url)
    data =  response.json()

    if data['status'] == 'OK':
        distance = data['rows'][0]['elements'][0]['distance']['text']
        return distance
    else:
        return "error"

api_key = "" #вставь сюда апи с гугл мапс дистант матрикс

distance = get_distanse('origin', 'destination', api_key)