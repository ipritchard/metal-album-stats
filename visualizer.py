import plotly.express as px
from sqlalchemy.orm import sessionmaker
from db_manager import BandInfo


def visualize_bands_by_genre(session):
    """
    Visualize the number of bands by genre.

    Args:
        session: The database session.
    """
    bands = session.query(BandInfo).all()
    genres = [band.data["genre"] for band in bands]

    genre_counts = {}
    for genre in genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    fig = px.bar(x=list(genre_counts.keys()), y=list(genre_counts.values()),
                 labels={'x': 'Genre', 'y': 'Number of Bands'})
    fig.show()
