import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route("/reviews/<username>/<sort>")
def review(username, sort):
    if sort not in ["relevant", "recent"]:
        return jsonify({
            "Error": True,
            "Message": "Unexpected sort value, Expected: relevant or recent"
        }), 400  # Return 400 Bad Request

    scraper = cloudscraper.create_scraper(browser="chrome")
    try:
        r = scraper.get(f"https://www.fiverr.com/{username}")
        if r.status_code == 404:
            return jsonify({"Error": True, "Message": "Wrong Username"}), 404

        soup = BeautifulSoup(r.text, "html.parser")
        userData = soup.find("script", id="perseus-initial-props")
        if userData:
            userData = json.loads(userData.text)
            userID = userData['seller']['user']['id']
            url = "https://www.fiverr.com/seller_page/api/reviews?user_id={}&as_seller=true".format(userID)

            # Fetch all reviews with optional pagination
            last_id = request.args.get("last_id")
            last_score = request.args.get("last_score")
            if last_id and last_score:
                url = f"https://www.fiverr.com/seller_page/api/reviews?user_id={userID}&as_seller=true&last_star_rating_id={last_id}&last_review_id={last_id}&last_score={last_score}&sort_by={sort}&page_size=100"

            res = scraper.get(url)
            res.raise_for_status()  # Raise an exception for HTTP errors
            return jsonify(res.json())

        return jsonify({
            "Error": True,
            "Message": "Failed to retrieve user data"
        }), 500  # Return 500 Internal Server Error

    except Exception:
        return jsonify({
            "Error": True,
            "Message": "An unexpected error occurred"
        }), 500

if __name__ == "__main__":
    # Directly specify the port number
    app.run(host='0.0.0.0', port=3000)
