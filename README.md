# Fiverr Review Scraper API

## Endpoint

BASE URL: fiver-review-api.vercel.app

**`GET /reviews/<username>/<sort>`**

- **`username`**: The Fiverr username of the seller.
- **`sort`**: Sort reviews by either `"relevant"` or `"recent"`.

### Query Parameters

- **`last_id`** (optional): The ID of the last review from the previous page, used for pagination.
- **`last_score`** (optional): The score of the last review from the previous page, used for pagination.

### Responses

- **Success (200 OK)**: Returns a JSON object with the review data.

  ```json
  {
    "reviews": [...]
  }
  ```

- **Error (400 Bad Request)**: Returned when an invalid sort parameter is provided.

  ```json
  {
    "Error": true,
    "Message": "Unexpected sort value. Expected: 'relevant' or 'recent'."
  }
  ```

- **Error (404 Not Found)**: Returned when the username is not found or the user data script is missing.

  ```json
  {
    "Error": true,
    "Message": "Wrong Username" // or "User data not found"
  }
  ```

- **Error (500 Internal Server Error)**: Returned when there is an error fetching or parsing data.

  ```json
  {
    "Error": true,
    "Message": "Internal Server Error"
  }
  ```

## Example Usage

To fetch the most relevant reviews for a user:

```
GET https://fiverr-review-api.vercel.app/reviews/username/relevant
```

To fetch recent reviews with pagination:

```
GET https://fiverr-review-api.vercel.app/reviews/username/recent?last_id=ID_OF_LAST_REVIEWS_ITEM&last_score=SCORE_OF_LAST_REVIEWS_ITEM
```
