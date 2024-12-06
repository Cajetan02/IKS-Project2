
# Indian Artisans E-Commerce

This is a simple e-commerce website that aggregates products from Indian artisans and displays them on a minimalistic platform.

## How to Run Locally

1. Install Python 3.x and required libraries:
    ```bash
    pip install flask beautifulsoup4 requests sqlite3
    ```

2. Run the application:
    ```bash
    python app.py
    ```

3. Open your browser and go to `http://127.0.0.1:5000/` to view the products.

## Notes

- The website scrapes product data from the following sources:
    - Runway India
    - Amazon Karigar
    - Gaatha
    - Chanderiyaan
    - ExclusiveLane
- The data is stored in an SQLite database (`products.db`).
- The product data is displayed in a simple, minimalistic layout.
    