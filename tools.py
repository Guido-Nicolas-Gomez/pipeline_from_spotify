# Importaciones
import datetime
import pandas as pd
from sqlalchemy import Column, String, Integer, DateTime, Date
from sqlalchemy.orm import declarative_base
import pytz # to time zone

# Defining the class to inherit the class for create the table
Base = declarative_base()

# Defining the class to inherit the class for create the table
Base = declarative_base()

# Defining the class to create the table
class Played_list(Base):
    __tablename__ = 'played_list'
    id = Column(Integer(), primary_key = True, nullable = False, unique = True)
    played_at = Column(DateTime(25),  nullable = False, unique = True)
    timestamps = Column(Date(), nullable = False)
    artist_name = Column(String(80), nullable = False)
    song_name = Column(String(80), nullable = False)
    date_created = Column(DateTime(), default = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')))

    # To print
    def __repr__(self):
        
        return f"""Song:
        ID = {self.id}
        played_at = {self.played_at}
        timestamps = {self.timestamps}
        artist_name = {self.artist_name}
        song_name = {self.song_name}
        date_created = {self.date_created}"""


# Validation of the dataset
def check_if_valid_data(data: pd.DataFrame) -> bool:
    # Defining the datetime to track
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days = 1)

    # Check if the dataset is empty
    if data.empty:
        print('No song downloaded. Finishing excecution') # Empty datasets means that I dont hear any songs
        return False # No means an error!

    # Primary Key check (Duplicate check)
    if not(data['played_at'].is_unique):
        raise Exception("Primary Key check is violated")
    
    # Null values check
    if data.isnull().values.any():
        raise Exception("There are some nulls values")
    
    # Timestamp check
    convert_to_datetime_date = lambda x: datetime.datetime.strptime(x[:10], "%Y-%m-%d").date()
    day = data['played_at'].agg(convert_to_datetime_date)
    if (day < yesterday.date()).any():
        raise Exception("There is at least one song that is not from yesterday")


# funtion to convert the date elements from the dataframe to datetime object
def conver_played_at_to_datetime(date: str) -> object:
    return datetime.datetime.strptime(date[:-5], "%Y-%m-%dT%H:%M:%S")
