from flask import Flask, render_template, request
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from haversine import haversine

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_excel(file)

        geolocator = Nominatim(user_agent="my_app")

        total_distance = 0
        for index, row in df.iterrows():
            loc1 = geolocator.geocode(str(row['CEP_Partida']))
            loc2 = geolocator.geocode(str(row['CEP_Chegada']))
            if loc1 and loc2:
                coords_1 = (loc1.latitude, loc1.longitude)
                coords_2 = (loc2.latitude, loc2.longitude)
                distance = haversine(coords_1, coords_2)
                total_distance += distance

        return render_template('index.html', result=total_distance)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)