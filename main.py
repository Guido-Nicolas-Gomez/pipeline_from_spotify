# Importaciones
import requests
import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tools import Base, Played_list, check_if_valid_data, conver_played_at_to_datetime


# Constants
DATA_BASE_LOCATION = "sqlite:///my_tracks.db"
USER_ID = 'guido.simoca'
TOKEN = 'token de seguridad' # https://developer.spotify.com/console/get-recently-played/


if __name__ == '__main__':

    # -------------------EXTRACT--------------------

    # header for the request acording to spotify
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
    }

    # Defining the datetime to track
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days = 1)
    yesterday_unix = int(yesterday.timestamp())*1000 # To convert in unix tamstamp

    # Requests
    r = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={yesterday_unix}", headers=headers)

    # Data
    data = r.json()

    # -------------------TRANSFORM--------------------

    # Extract Fields
    played_at = [i['played_at'] for i in data['items']]
    timestamps = [i[:10] for i in played_at]
    artist_name = [i['track']['album']['artists'][0]['name'] for i in data['items']]
    song_name = [i['track']['name'] for i in data['items']]

    # Convert to dic
    song_dic = {
        'played_at': played_at,
        'timestamps': timestamps,
        'artist_name': artist_name,
        'song_name': song_name
    }

    # Convert to DataFrame
    song_df = pd.DataFrame(song_dic)

    # Check of dataset
    check_if_valid_data(song_df)

    # -------------------LOADING--------------------

    # Creating engine
    engine = create_engine(DATA_BASE_LOCATION, echo = True)
    # creating data base
    Base.metadata.create_all(engine)

    # Declarate session
    Session = sessionmaker()
    local_session = Session(bind = engine)

    # Loading de data
    try:
        for i in song_df.values:
            song = Played_list(
                                    played_at = conver_played_at_to_datetime(i[0]),
                                    timestamps = datetime.datetime.strptime(i[1],"%Y-%m-%d").date(),
                                    artist_name = i[2],
                                    song_name = i[3]
                            )
            local_session.add(song)
        local_session.commit()
    except:
        print("Los datos no pudiern cargarse, posiblemente ya esten cargados")
    finally:
        local_session.close()
