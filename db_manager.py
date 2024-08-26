from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BandInfo(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    data = Column(JSON)  # Store the entire scraped band data as JSON


def setup_db(db_url: str):
    """
    Setup the database.

    Args:
        db_url (str): The database URL.
    """
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def save_band_info(session, band_data: dict):
    """
    Save the band information to the database.

    Args:
        session: The database session.
        band_data (dict): The scraped band data.
    """
    band = BandInfo(name=band_data["name"], data=band_data)
    session.add(band)
    session.commit()


def band_already_scraped(session, band_name: str) -> bool:
    """
    Check if the band has already been scraped.

    Args:
        session: The database session.
        band_name (str): The name of the band.

    Returns:
        bool: True if the band is in the database, False otherwise.
    """
    return session.query(BandInfo).filter_by(name=band_name).first() is not None
