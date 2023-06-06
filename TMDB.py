import requests


class Tmdb:
    """
    A class for interacting with The Movie Database (TMDb) API.

    Args:
        api_key (str): The API key for accessing TMDb API.
        api_read_access_token (str): The read access token for authorization.

    Attributes:
        url_search (str): The base URL for movie search endpoint.
        url_movie (str): The base URL for movie details endpoint.
        api_key (str): The API key for accessing TMDb API.
        api_read_access_token (str): The read access token for authorization.
        headers (dict): The request headers containing authorization details.

    """

    def __init__(self) -> None:
        self.url_search = "https://api.themoviedb.org/3/search/movie"
        self.api_key = "API KEY"
        self.api_read_access_token = "API READ ACCESS TOKEN"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_read_access_token}",
        }

    def movie_input(self, movie):
        """
        Search for movies based on the provided query.

        Args:
            query (str): The search query for movies.

        Returns:
            list or str: A list of movie data dictionaries if movies are found,
                or a string message indicating no movie found with the given title.

        """
        params = {"query": movie}
        response = requests.get(
            self.url_search, headers=self.headers, params=params, timeout=5
        )
        data = response.json()
        if data["total_results"] > 0:
            results = data["results"]
            return results
        else:
            results = "No movie found with that title."
            return results

    def clean_results(self, results):
        """
        Clean the movie search results by extracting required data.

        Args:
            results (list): The list of movie search results.

        Returns:
            list: A list of dictionaries containing cleaned movie data.

        """
        result_list = []
        for result in results:
            release_date = result.get("release_date")
            poster_path = result.get("poster_path")
            title = result.get("title")
            movie_id = result.get("id")

            if release_date and poster_path and title and movie_id:
                movie_data = {
                    "title": title,
                    "release_date": release_date,
                    "id": movie_id,
                    "poster_path": poster_path,
                }
                result_list.append(movie_data)
        return result_list

    def movie_id(self, id):
        """
        Get movie details by its ID.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            dict: The dictionary containing the movie details.

        """
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}?api_key={self.api_key}",
            timeout=5,
        )
        data = response.json()
        return data
