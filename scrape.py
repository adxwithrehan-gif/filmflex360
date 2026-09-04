import json
import time
import requests

API_KEY = "df21e7b0441abeeba6adafe8345a84d4"
BASE_URL = "https://api.themoviedb.org/3/discover/movie"


def fetch_massive_tmdb_data():
  all_movies = []
  print(
      "Fetching massive movie database from TMDB (Movies & Series across"
      " pages)..."
  )

  # Multiple pages loop (Aap pages ki limit barha ya ghata sakte hain)
  for page in range(1, 51):  # 50 pages * 20 = 1000+ movies for testing
    url = f"{BASE_URL}?api_key={API_KEY}&page={page}&sort_by=popularity.desc"

    try:
      response = requests.get(url, timeout=15)
      if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if not results:
          break

        for item in results:
          title = item.get("title") or item.get("name")
          poster_path = item.get("poster_path")
          poster = (
              f"https://image.tmdb.org/t/p/w500{poster_path}"
              if poster_path
              else ""
          )
          rating = round(item.get("vote_average", 0), 1)
          year = (
              item.get("release_date", "2026")[:4]
              if item.get("release_date")
              else "2026"
          )
          overview = item.get("overview", "No description available.")

          all_movies.append({
              "title": title,
              "poster": poster,
              "rating": rating,
              "year": year,
              "description": overview,
              "download": f"https://www.google.com/search?q={title}+download",
          })

        print(
            f"Fetched page {page} successfully. Total collected:"
            f" {len(all_movies)}"
        )
        time.sleep(
            0.5
        )  # API block se bachne ke liye chota sa gap zaroori hai
      else:
        print(f"Failed on page {page}, Status code: {response.status_code}")
        break
    except Exception as e:
      print(f"Error on page {page}: {e}")
      break

  # JSON file mein save karna
  with open("movies.json", "w", encoding="utf-8") as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=4)

  print(
      f"\nSuccessfully saved total {len(all_movies)} movies to movies.json!"
  )


if __name__ == "__main__":
  fetch_massive_tmdb_data()