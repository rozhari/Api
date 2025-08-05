from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return "🎵 Spotify Downloader API is online!"

@app.route("/api/spotify/track")
def spotify_track():
    url = request.args.get("url")
    if not url or "spotify.com" not in url:
        return jsonify({"error": "Invalid or missing Spotify track URL"}), 400

    try:
        response = requests.get(f"https://spotidownloader.com/?url={url}")
        soup = BeautifulSoup(response.text, "html.parser")
        link = soup.find("a", class_="button is-success is-fullwidth")["href"]
        title = soup.find("p", class_="title").text.strip()

        return jsonify({
            "success": True,
            "title": title,
            "download": link
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/spotify/playlist")
def spotify_playlist():
    url = request.args.get("url")
    if not url or "/playlist/" not in url:
        return jsonify({"error": "Invalid or missing Spotify playlist URL"}), 400

    try:
        response = requests.get(f"https://spotidownloader.com/?url={url}")
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div.box")

        songs = []
        for item in items:
            title = item.find("p", class_="title")
            link = item.find("a", class_="button is-success is-fullwidth")
            if title and link:
                songs.append({
                    "title": title.text.strip(),
                    "download": link["href"]
                })

        return jsonify({
            "success": True,
            "data": songs
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
