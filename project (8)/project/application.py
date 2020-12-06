import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# helper files
from helpers import apology


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///kpop.db")


@app.route("/")
def index():
    """Show the home page"""
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    """Accept user input to database"""

    # variables to use for max allowed number of inputs (+1 because range)
    songs_max = 29
    versions_max = 11

    # if form's been submitted, it's big SQL time
    if request.method == "POST":

        # deal with artist input
        artist = request.form.get("dropdown")

        # in case disbled Javascript, check inputs
        if not request.form.get("dropdown"):
            return apology("please select artist", 400)
        if not request.form.get("album"):
            return apology("please enter album title", 400)
        if not request.form.get("album_url"):
            return apology("please enter album logo url", 400)
        if not request.form.get("song1"):
            return apology("please add at least 1 song", 400)
        if not request.form.get("version1"):
            return apology("please add at least 1 version", 400)
        if not request.form.get("version_url1"):
            return apology("please add at least 1 version with image url", 400)
        if not request.form.get("version_description1"):
            return apology("please add at least 1 version with description", 400)

        # if it's a new artist, switch to new artist
        if artist == "other":
            artist = request.form.get("new_artist")
            if not artist:
                return apology("missing new artist name", 400)

        # see if artist is in database
        artist_info = db.execute("SELECT id FROM artists WHERE name = ?", artist)

        # if new artist, enter into db first
        if not (artist_info):
            db.execute("INSERT INTO artists (name, artist_photo_url) VALUES (?, ?)", artist, request.form.get("new_artist_url"))
            # repeat query to get new info
            artist_info = db.execute("SELECT id FROM artists WHERE name = ?", artist)

        # get artist id for future use
        artist_id = artist_info[0].get("id")

        # grab album input
        album = request.form.get("album")
        alb_photo_url = request.form.get("album_url")

        # see if the album exists in the database yet
        new_album_info = db.execute("SELECT id FROM albums WHERE title = ?", album)

        # if it's not there already, insert into db
        if not (new_album_info):
            db.execute("INSERT INTO albums (title, artist_id, album_photo_url) VALUES (?, ?, ?)", album, artist_id, alb_photo_url)
            # repeat the query to get new info
            new_album_info = db.execute("SELECT id FROM albums WHERE title = ?", album)

        # get the album id for future use
        new_album_id = new_album_info[0].get("id")

        # deal with tracklist input
        for i in range(1, songs_max):
            song = request.form.get("song"+str(i))

            # if there's a song, add it to database
            if song:
                db.execute("INSERT INTO songs (song, album_id, artist_id) VALUES (?,?,?)", song, new_album_id, artist_id)

        # deal with versions input
        for j in range(1, versions_max):
            ver_name = request.form.get("version"+str(j))
            ver_desc = request.form.get("version_description"+str(j))
            ver_url = request.form.get("version_url"+str(j))

            # if there's a version, add it to database
            if ver_name:
                db.execute("INSERT INTO versions (version, album_id, description, version_photo_url) VALUES (?,?,?,?)",
                           ver_name, new_album_id, ver_desc, ver_url)

        # redirect user to index
        return redirect("/")

    # no form yet, just show page
    else:
        # get info for artists dropdown
        artists_info = db.execute("SELECT name FROM artists")
        artists = []
        for row in artists_info:
            artists.append(row["name"])
        artists.append("other")

        # make the page
        return render_template("add.html", artists=artists, songs_max=songs_max, versions_max=versions_max)


@app.route("/albums", methods=["GET", "POST"])
def albums():
    """Gather and display all albums"""

    # if something's been clicked, display all versions
    if request.method == "POST":

        # get album id from button, use it to get database info
        album_id = request.form.get("album_id")
        versions = db.execute("SELECT version, description, version_photo_url FROM versions WHERE album_id = ?", album_id)
        all_songs = db.execute("SELECT song FROM songs WHERE album_id = ?", album_id)

        # gather tracklist of the album
        tracklist = []
        for song in all_songs:
            tracklist.append(song.get("song"))

        # also include the album's own title
        album_info = db.execute("SELECT title FROM albums WHERE id = ?", album_id)
        album_title = album_info[0].get("title")

        # also include artist's name
        artist_info = db.execute("SELECT name FROM artists JOIN albums on albums.artist_id = artists.id WHERE albums.id = ?", album_id)
        artist_name = artist_info[0].get("name")

        # make the versions page
        return render_template("versions.html", versions=versions, tracklist=tracklist, album_title=album_title, artist_name=artist_name)

    # otherwise just show page of albums
    else:
        artist_id = request.args.get("artist_id")
        # if we're coming from the artists page (w/ id), only display that artist's albums
        if artist_id:
            # create SQL request for all the album data
            albums = db.execute(
                "SELECT albums.title, albums.id, albums.album_photo_url, artists.name FROM albums JOIN artists ON albums.artist_id = artists.id WHERE artists.id = ? ORDER BY albums.title", artist_id)

            # create the albums page
            return render_template("albums.html", albums=albums)

        # otherwise show all albums
        else:
            # create SQL request for all the album data
            albums = db.execute(
                "SELECT albums.title, albums.id, albums.album_photo_url, artists.name FROM albums JOIN artists ON albums.artist_id = artists.id ORDER BY albums.title")

            # create the albums page
            return render_template("albums.html", albums=albums)


@app.route("/artists")
def artists():
    """Gather and display artists"""

    # create SQL request for all the artist data
    artists = db.execute("SELECT name, id, artist_photo_url FROM artists ORDER BY name")

    # create the artists page
    return render_template("artists.html", artists=artists)


@app.route("/search", methods=["GET", "POST"])
def search():
    """Make search page, deal with inputs"""

    # if form's been submitted, return the desired info
    if request.method == "POST":

        # check for proper submission
        if not request.form.get("input"):
            return apology("please enter info", 400)

        # save as variable for convenience
        input = "%"+request.form.get("input")+"%"

        # gather relevant data
        # placeholder tutorial from https://realpython.com/prevent-python-sql-injection/
        songs = db.execute(
            "SELECT DISTINCT song, album_id, artists.name FROM songs JOIN artists ON songs.artist_id = artists.id WHERE song LIKE %s", (input))
        artists = db.execute(
            "SELECT DISTINCT name, artists.id FROM artists WHERE name LIKE %s", (input))
        albums = db.execute(
            "SELECT DISTINCT title, albums.id, artists.name FROM albums JOIN artists ON albums.artist_id = artists.id WHERE title LIKE %s", (input))

        # if there's no info yet, put "no results" so no blank search results
        # used google search for Python equivalent of NULL
        nr = {}
        if not songs:
            nr['songs'] = "no results"
        if not artists:
            nr['artists'] = "no results"
        if not albums:
            nr['albums'] = "no results"

        # send the information to the new page
        return render_template("searched.html", songs=songs, artists=artists, albums=albums, nr=nr)

    else:
        # create the search page
        return render_template("search.html")


@app.route("/songs")
def songs():
    """Gather and display songs"""

    # if something's been clicked, display all versions
    if request.method == "POST":

        # get album id from button, use it to get database info
        album_id = request.form.get("album_id")
        versions = db.execute("SELECT version, description, version_photo_url FROM versions WHERE album_id = ?", album_id)
        all_songs = db.execute("SELECT song FROM songs WHERE album_id = ?", album_id)

        # gather tracklist of the album
        tracklist = []
        for song in all_songs:
            tracklist.append(song.get("song"))

        # also include the album's own title
        album_info = db.execute("SELECT title FROM albums WHERE id = ?", album_id)
        album_title = album_info[0].get("title")

        # make the page
        return render_template("versions.html", versions=versions, tracklist=tracklist, album_title=album_title)

    # or just display the page
    else:
        # create SQL request for all the songs data
        songs = db.execute(
            "SELECT songs.song, artists.name, albums.title, songs.album_id FROM songs JOIN artists ON songs.artist_id = artists.id JOIN albums ON songs.album_id = albums.id ORDER BY songs.song")

        # create the songs page
        return render_template("songs.html", songs=songs)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
