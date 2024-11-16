from dotenv import load_dotenv
import os
from scraperr.clients.netflix_auth import NetflixClient
from scraperr.logger import logger


load_dotenv()  # Loads variables from .env into the environment

netflix_user: str = os.getenv('NETFLIX_USER', "")
netflix_pw: str = os.getenv('NETFLIX_PW', "")
netflix_url: str = os.getenv('NETFLIX_URL', "")
netflix_profile: str = os.getenv('NETFLIX_PROFILE', "")



def main() -> None:
    """Get list of trending movies from Netflix."""
    netflix = NetflixClient()
    netflix.login(
        url=netflix_url,
        username=netflix_user,
        password=netflix_pw,
        profile=netflix_profile,
    )


if __name__ == "__main__":
    main()
