from metallum import band_search
from band_index_lookup import metallum_index_lookup


def scrape_band_info(band_name: str) -> dict:
    """
    Scrape band information using python-metallum, handling index lookup for multiple results.

    Args:
        band_name (str): The name of the metal band.

    Returns:
        dict: A dictionary with the band's information, albums, release dates, reviews, lyrics, etc.
    """
    band_search_results = band_search(band_name)

    # Handle cases where no results or multiple results are returned
    if len(band_search_results) == 1:
        band_info = band_search_results[0].get()
    elif len(band_search_results) == 0:
        return {"error": f"No results found for band '{band_name}'"}
    else:
        band_index = metallum_index_lookup.get(band_name)
        if band_index is None:
            return {"error": f"Band '{band_name}' not found in Metallum archives."}
        band_info = band_search_results[band_index].get()

    # Extract band information
    band_data = {
        "name": band_info.name,
        "bio": band_info.bio,
        "genre": band_info.genre,
        "country": band_info.country,
        "formed_in": band_info.formed_in,
        "albums": []
    }

    for album in band_info.albums:
        album_data = {
            "title": album.title,
            "release_date": album.release_date,
            "reviews": album.reviews,
            "lyrics": album.lyrics
        }
        band_data["albums"].append(album_data)

    return band_data
