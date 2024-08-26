import time
from scraper.py import scrape_band_info
from db_manager import setup_db, save_band_info, band_already_scraped
from config import DATABASE_URL


def initialize_database():
    """
    Initialize the SQLite database by creating the necessary tables.
    """
    Session = setup_db(DATABASE_URL)  # This sets up the database connection and engine
    session = Session()

    # Create all tables based on the Base metadata
    session.bind.metadata.create_all(session.get_bind())

    session.close()
    print("Database initialized successfully!")


def main(band_list):
    """
    Main function to scrape data and store it in the database.

    Args:
        band_list (list): A list of metal bands to scrape.
    """
    Session = setup_db(DATABASE_URL)
    session = Session()

    for band in band_list:
        if not band_already_scraped(session, band):
            try:
                band_data = scrape_band_info(band)
                save_band_info(session, band_data)
                print(f"Scraped and saved data for {band}")
            except Exception as e:
                print(f"Error scraping {band}: {e}")
            time.sleep(1)  # To avoid overloading the API

    session.close()


if __name__ == "__main__":
    band_list = ["Metallica", "Iron Maiden", "Black Sabbath"]  # Example list of bands
    main(band_list)
