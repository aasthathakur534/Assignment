import requests

def fetch_books():
    # Open Library Search API endpoint
    API_URL = "https://openlibrary.org/search.json"
    
    # Define query parameters
    params = {
        "q": "python programming",
        "fields": "key,title,author_name,first_publish_year",
        "limit": 10 # Limits API response to 5 items
    }
    
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()  # Check for HTTP request errors
        
        data = response.json()
        
        # Total matching records found across Open Library's entire database
        total_records_found = data.get("numFound", 0)
        
        # Safeguard list slicing to guarantee maximum 5 items are processed
        books = data.get("docs", [])[:10]
        
        print(f"Total matching books in Open Library database: {total_records_found}")
        print(f"Displaying top {len(books)} results:\n")
        
        for idx, book in enumerate(books, 1):
            title = book.get("title", "N/A")
            authors = ", ".join(book.get("author_name", ["Unknown Author"]))
            year = book.get("first_publish_year", "N/A")
            
            print(f"{idx}. Title: {title}")
            print(f"   Author: {authors}")
            print(f"   Publication year: {year}")
            print("-" * 50)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")

if __name__ == "__main__":
    fetch_books()