import streamlit as st
#import pickle
import pandas as pd
import joblib
import overpy
from geopy.geocoders import Nominatim



#def load_model():
    #with open('saved_steps.pkl', 'rb') as file:
        #data = pickle.load(file)
    #return data


#data = load_model()
#model = data['model']
#le_location = data['le_location']
#le_proptype = data['le_proptype']
#le_furnishing= data['le_furnishing']
model = joblib.load('model')
le_location = joblib.load('le_location')
le_proptype = joblib.load('le_proptype')
le_furnishing = joblib.load('furnishing')
scaler = joblib.load('scaler')


geolocator = Nominatim (user_agent='web app')


def create_variables(x):
    try:
        x = f'{x}, Kuala Lumpur'
        lat = geolocator.geocode(x).raw['lat']
        lon = geolocator.geocode(x).raw['lon']
        api = overpy.Overpass()

        query1 = """(node["amenity"="place_of_worship"](around:5000,{lat},{lon});

                );out;
                """.format(lat=lat, lon=lon)
        result1 = api.query(query1)
        n_worship = len(result1.nodes)

        query2 = """(node["amenity"="school"](around:5000,{lat},{lon});

                );out;
                """.format(lat=lat, lon=lon)
        result2 = api.query(query2)
        n_schools = len(result2.nodes)

        query3 = """(node["amenity"="hospital"](around:5000,{lat},{lon});

                );out;
                """.format(lat=lat, lon=lon)
        result3 = api.query(query3)
        n_hospitals = len(result3.nodes)

        query4 = """(node["shop"="mall"](around:5000,{lat},{lon});

                );out;
                """.format(lat=lat, lon=lon)
        result4 = api.query(query4)
        n_malls = len(result4.nodes)

        query5 = """(node["amenity"="restaurant"](around:5000,{lat},{lon});

                );out;
                """.format(lat=lat, lon=lon)
        result5 = api.query(query5)
        n_restaurants = len(result5.nodes)

        return [n_worship, n_schools, n_hospitals, n_malls, n_restaurants]

    except:
        return [37, 19, 4, 4, 509.5]

def show_predict_page():
    st.title('Property Price Prediction for Kuala Lumpur')
    st.write('Enter Details Below')

    locations = (
        'Ampang',
        'Ampang Hilir',
        'Bandar Damai Perdana',
        'Bandar Menjalara',
        'Bandar Tasik Selatan',
        'Bangsar',
        'Bangsar South',
        'Batu Caves',
        'Brickfields',
        'Bukit Bintang',
        'Bukit Jalil',
        'Bukit Ledang',
        'Bukit Tunku (Kenny Hills)',
        'Chan Sow Lin',
        'Cheras',
        'City Centre',
        'Country Heights Damansara',
        'Damansara',
        'Damansara Heights',
        'Desa Pandan',
        'Desa Parkcity',
        'Desa Petaling',
        'Dutamas',
        'Federal Hill',
        'Jalan Ipoh',
        'Jalan Klang Lama (Old Klang Road)',
        'Jalan Kuching',
        'Jalan Sultan Ismail',
        'Jinjang',
        'Kepong',
        'Keramat',
        'Kl City',
        'Kl Eco City',
        'Kl Sentral',
        'KlCC',
        'Kuchai Lama',
        'Mid Valley City',
        'Mont Kiara',
        'Other',
        'OUG',
        'Pandan Indah',
        'Pandan Jaya',
        'Pandan Perdana',
        'Pantai',
        'Puchong',
        'Salak Selatan',
        'Segambut',
        'Sentul',
        'Seputeh',
        'Setapak',
        'Setiawangsa',
        'Sri Hartamas',
        'Sri Petaling',
        'Sungai Besi',
        'Sungai Penchala',
        'Sunway Spk',
        'Taman Desa',
        'Taman Duta',
        'Taman Melawati',
        'Taman Tun Dr Ismail',
        'Titiwangsa',
        'Wangsa Maju'
    )

    proptypes = (
        'Apartment',
        'Bungalow',
        'Condominium',
        'Flat',
        'Residential Land',
        'Semi-detached House',
        'Serviced Residence',
        'Terrace/Link House',
        'Townhouse'
    )

    furnishings = (
        'Fully Furnished',
        'Partly Furnished',
        'Unfurnished'
    )

    location = st.selectbox('Location (select "Other" if not listed below)', locations)
    other = st.text_input('If "Other" selected, enter location here (e.g. Wangsa Melawati)')
    proptype = st.selectbox('Property Type', proptypes)
    furnishing = st.selectbox('Furnishing', furnishings)
    size = st.number_input('Size (sq. ft)', step=250)
    room = st.number_input('Rooms', step=1)
    bathroom = st.number_input('Bathrooms', step=1)
    storeroom = st.number_input('Store Rooms', step=1)

    if location == 'Other':
        data = pd.DataFrame([[other, [0, 0, 0, 0, 0]]], columns=['Location', 'Variables'])
        data['Variables'] = data['Location'].apply(lambda x: create_variables(x))
        data['Places of Worship'] = data['Variables'].apply(lambda x: x[0])
        data['Schools'] = data['Variables'].apply(lambda x: x[1])
        data['Hospitals'] = data['Variables'].apply(lambda x: x[2])
        data['Malls'] = data['Variables'].apply(lambda x: x[3])
        data['Restaurants'] = data['Variables'].apply(lambda x: x[4])
    else:
        variables = pd.read_csv('Locations.csv')
        data = variables[variables['Location'] == location]

    worship = data['Places of Worship'].item()
    school = data['Schools'].item()
    hospital = data['Hospitals'].item()
    mall = data['Malls'].item()
    restaurant = data['Restaurants'].item()

    predict = st.button('Predict Price')
    if predict:
        x = pd.DataFrame(
            [[location, room, bathroom, proptype, size, furnishing, storeroom,\
             worship, school, hospital, mall, restaurant]],
            columns = ['Location', 'Rooms', 'Bathrooms', 'Property Type', \
            'Size', 'Furnishing', 'Store Rooms', 'Places of Worship',\
            'Schools', 'Hospitals', 'Malls', 'Restaurants']
        )

        numerical = ['Rooms', 'Bathrooms', 'Size', 'Store Rooms',\
        'Places of Worship','Schools', 'Hospitals', 'Malls', 'Restaurants']
        x[numerical] = scaler.transform(x[numerical])

        x['Location'] = le_location.transform(x['Location'])
        x['Property Type'] = le_proptype.transform(x['Property Type'])
        x['Furnishing'] = le_furnishing.transform(x['Furnishing'])

        predicted_price = model.predict(x)
        st.subheader(f'The predicted price is RM {predicted_price[0]:,.2f}')



show_predict_page()