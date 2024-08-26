# Metal Band Scraper (`metal-band-stats`)

This project scrapes information about Metal bands using the `python-metallum` package. The scraped data is stored in an SQLite database and can be visualized using tools like Plotly or Matplotlib.

## Project Structure

```
metal_scraper/
│
├── main.py              # Main script to run the scraper
├── scraper.py           # Handles the scraping logic using python-metallum
├── db_manager.py        # Manages database interactions (e.g., saving, loading data)
├── visualizer.py        # Visualizes the scraped data using plotly/matplotlib
├── band_index_lookup.py  # Stores the metallumIndexLookup dictionary
├── config.py            # Configuration file for settings (DB credentials, etc.)
├── initialize_db.py     # Script to initialize the database
├── requirements.txt     # List of dependencies (python-metallum, sqlalchemy, plotly, etc.)
└── data/                # Folder for database or any temporary storage
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/metal_band_scraper.git
   cd metal_band_scraper
   ```

2. **Install Dependencies**:
   Create and activate a virtual environment, then install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

1. **Scraping Metal Band Information**:

   The main scraping logic is handled by `scraper.py`. To scrape a list of metal bands and store their information in the database, run the `main.py` script. For example:

   ```bash
   python main.py
   ```

   The script will:
   - Search for each band using `python-metallum`.
   - Use an index lookup (`band_index_lookup.py`) to handle multiple search results.
   - Save the band information and album details in the SQLite database.

2. **Band Lookup Example**:

   The `band_index_lookup.py` stores index lookups for bands with multiple results:
   ```python
   metallumIndexLookup = {
       'Angel': None,
       'Autopsy': 1,
       'Black Death': 6,
       ...
   }
   ```
   This dictionary is used in the scraper to ensure the correct band is selected from multiple search results.

3. **Database Storage**:

   The scraped data is stored in the SQLite database, using a schema defined in `db_manager.py`. Each band's information (name, bio, genre, country, albums, etc.) is saved as a JSON object within the database.

4. **Visualization**:

   After data is scraped and stored, it can be visualized using Plotly or Matplotlib. For example, you can visualize the number of bands by genre:
   ```python
   import plotly.express as px
   from db_manager import setup_db, BandInfo

   Session = setup_db(DATABASE_URL)
   session = Session()

   # Query bands from the database
   bands = session.query(BandInfo).all()

   # Count the number of bands by genre
   genres = [band.data["genre"] for band in bands]
   genre_counts = {}
   for genre in genres:
       genre_counts[genre] = genre_counts.get(genre, 0) + 1

   # Plot a bar chart of genre distribution
   fig = px.bar(x=list(genre_counts.keys()), y=list(genre_counts.values()), 
                labels={'x': 'Genre', 'y': 'Number of Bands'})
   fig.show()
   ```

## Future Enhancements

- Add parallel processing for faster scraping of large band lists.
- Extend database schema to normalize album data into a separate table.
- Improve error handling and implement a retry mechanism for failed scrapes.
