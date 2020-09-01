#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import logging
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref
from sqlalchemy.orm import query
from forms import *
from datetime import datetime
from config import SQLALCHEMY_DATABASE_URI
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# TODO√: connect to a local postgresql database
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

# shows = db.Table(
#   "shows",
#   db.Column("artist_id", db.Integer, db.ForeignKey("artist.id"), primary_key=True),
#   db.Column("venue_id", db.Integer, db.ForeignKey("venue.id"), primary_key=True),
#   db.Column("date", db.DateTime, nullable=False, default=datetime.utcnow)
# )


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default="a Venue")
    city = db.Column(db.String, nullable=False, default="Detroit")
    state = db.Column(db.String, nullable=False, default="Mechigan")
    address = db.Column(db.String, nullable=False,
                        default="1000 University Dr")
    phone = db.Column(db.String, nullable=False, default="2480001234")
    image_link = db.Column(db.String)
    genres = db.Column(db.String, nullable=False, default="Hip Hop")
    facebook_link = db.Column(
        db.String, nullable=False, default="www.facebook.com/v")
    website = db.Column(db.String, nullable=False, default="www.website.com")
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(
        db.String, nullable=False, default="a description")

    shows = db.relationship(
        "Show",
        backref=db.backref("venues", lazy=True)
    )

    def __repr__(self):
        return f'<Venue {self.id} name: {self.name}>'

    # TODO√: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default="an artist")
    city = db.Column(db.String, nullable=False, default="Detroit")
    state = db.Column(db.String, nullable=False, default="Mechigan")
    phone = db.Column(db.String, nullable=False, default="2480001234")
    genres = db.Column(db.String, nullable=False, default="Hiphop")
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(
        db.String, nullable=False, default="www.facebook.com/a")

    shows = db.relationship(
        "Show",
        backref=db.backref("artists", lazy=True)
    )

    # TODO√: implement any missing fields, as a database migration using Flask-Migrate


migration = Migrate(app, db)

# TODO√ Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO√: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    data = []
    venues = Venue.query.all()
    cities = set([(v.city, v.state) for v in venues])

    for c in cities:
        data.append({
            "city": c[0],
            "state": c[1],
            "venues": []
        })

    now = datetime.now()
    for v in venues:
        n_upcoming_shows = 0
        shows = Show.query.filter_by(venue_id=v.id).all()
        for s in shows:
            if s.start_time > now:
                n_upcoming_shows += 1
        for venue in data:
            if v.city == venue["city"]:
                venue["venues"].append({
                    "id": v.id,
                    "name": v.name,
                    "num_upcoming_shows": n_upcoming_shows
                })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO√: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    term = request.form.get("search_term").lower()
    venues = Venue.query.all()
    now = datetime.now()
    response = {
        "count": 0,
        "data": []
    }
    # response = {
    #     "count": 0,
    #     "data": [{
    #         "id": 2,
    #         "name": "The Dueling Pianos Bar",
    #         "num_upcoming_shows": 0,
    #     }]
    # }
    for v in venues:
        if term in v.name.lower():
            n_upcoming_shows = 0
            shows = Show.query.filter_by(venue_id=v.id).all()
            for s in shows:
                if s.start_time < now:
                    continue
                n_upcoming_shows += 1
            response["count"] += 1
            response["data"].append({
                "id": v.id,
                "name": v.name,
                "num_upcoming_shows": n_upcoming_shows
            })
    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get('search_term', ''))


def format_genres(genres_from_db):
    ignored_symbols = ["{", "}"]
    result = genres_from_db
    for i in ignored_symbols:
        result = result.replace(i, "")
    return result.split(",")


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue_info = Venue.query.filter_by(id=venue_id).first()
    genres_list = format_genres(venue_info.genres)
    # ignored_symbols = ["{", "}"]
    # for i in ignored_symbols:
    #     genres_list = genres_list.replace(i, "")
    # genres_list = genres_list(genres_list)
    data = {
        "id": venue_id,
        "name": venue_info.name,
        "genres": genres_list,
        "address": venue_info.address,
        "city": venue_info.city,
        "state": venue_info.state,
        "phone": venue_info.phone,
        "website": venue_info.website,
        "facebook_link": venue_info.facebook_link,
        "seeking_talent": venue_info.seeking_talent,
        "image_link": venue_info.image_link,
        "past_shows": [],
        "upcoming_shows": []
    }
    shows = Show.query.filter_by(venue_id=venue_id).all()
    for show in shows:
        artist_info = Artist.query.filter_by(id=show.artist_id).first()
        show_details = {
            "artist_id": artist_info.id,
            "artist_name": artist_info.name,
            "artist_image_link": artist_info.image_link,
            "start_time": format_datetime(str(show.start_time))
        }
        if show.start_time > datetime.now():
            data["upcoming_shows"].append(show_details)
        else:
            data["past_shows"].append(show_details)
    data["upcoming_shows_count"] = len(data["upcoming_shows"])
    data["past_shows_count"] = len(data["past_shows"])
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO√: insert form data as a new Venue record in the db, instead
    # TODO√: modify data to be the data object returned from db insertion
    user_input = request.form
    query = Venue.query.filter_by(name=user_input["name"]).first()
    if query:
        flash("This venue is already posted!")
    else:
        new_venue = Venue(
            name=user_input["name"],
            city=user_input["city"],
            state=user_input["state"],
            address=user_input["address"],
            phone=user_input["phone"],
            genres=user_input["genres"],
            facebook_link=user_input["facebook_link"]
        )
        try:
            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            flash(f"genres: {new_venue.genres}")
        except Exception as e:
            flash(f"Err posting {new_venue.name}: {e}")
            db.session.rollback()
        finally:
            db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO√: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        item_to_delete = Venue.query.filter_by(id=venue_id).first()
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f"Venue '{item_to_delete.name}' deleted.")
    except Exception as e:
        flash(f"Error: {e}")
        db.session.rollback()
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for("index"))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO√: replace with real data returned from querying the database
    data = []
    artists = Artist.query.all()
    for a in artists:
        data.append({
            "id": a.id,
            "name": a.name
        })
    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO√: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # response = {
    #     "count": 1,
    #     "data": [{
    #         "id": 4,
    #         "name": "Guns N Petals",
    #         "num_upcoming_shows": 0,
    #     }]
    # }
    term = request.form.get("search_term").lower()
    artists = Artist.query.all()
    response = {
        "count": 0,
        "data": []
    }
    now = datetime.now()
    for a in artists:
        if term not in a.name.lower():
            continue
        shows = Show.query.filter_by(artist_id=a.id).all()
        n_upcoming_shows = 0
        for s in shows:
            if s.start_time > now:
                n_upcoming_shows += 1
        response["count"] += 1
        response["data"].append({
            "id": a.id,
            "name": a.name,
            "num_upcoming_shows": n_upcoming_shows
        })
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO√: replace with real venue data from the venues table, using venue_id
    # data1 = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "past_shows": [{
    #         "venue_id": 1,
    #         "venue_name": "The Musical Hop",
    #         "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }

    artist_info = Artist.query.filter_by(id=artist_id).first()
    now = datetime.now()
    print(f"artist genres type: {type(artist_info.genres)}, value: {artist_info.genres}")
    artist_genres = artist_info.genres if isinstance(
        artist_info.genres, list) else format_genres(artist_info.genres)
    data = {
        "id": artist_info.id,
        "name": artist_info.name,
        "genres": artist_genres,
        "city": artist_info.city,
        "state": artist_info.state,
        "phone": artist_info.phone,
        "image_link": artist_info.image_link,
    }
    shows = Show.query.filter_by(artist_id=artist_info.id).all()
    upcoming_shows = []
    past_shows = []
    for s in shows:
        venue = Venue.query.filter_by(id=s.venue_id).first()
        show_details = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": format_datetime(str(s.start_time))
        }
        if s.start_time > now:
            upcoming_shows.append(show_details)
        else:
            past_shows.append(show_details)
    data["upcoming_shows"] = upcoming_shows
    data["past_shows"] = past_shows
    data["upcoming_shows_count"] = len(upcoming_shows)
    data["past_shows_count"] = len(past_shows)

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist_info = Artist.query.filter_by(id=artist_id).first()
    artist = {
        "id": artist_info.id,
        "name": artist_info.name,
        "genres": artist_info.genres,
        "city": artist_info.city,
        "state": artist_info.state,
        "phone": artist_info.phone,
        "facebook_link": artist_info.facebook_link
    }
        # "seeking_venue": artist_info.seeking_venue,
        # "seeking_description": artist_info.seeking_description,
        # "image_link": artist_info.image_link,
        # "website": artist_info.website,
    # TODO√: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO√: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist_to_edit = Artist.query.filter_by(id=artist_id).first()
    user_input = request.form
    artist_to_edit.name = user_input["name"]
    artist_to_edit.city = user_input["city"]
    artist_to_edit.state = user_input["state"]
    artist_to_edit.phone = user_input["phone"]
    artist_to_edit.genres = user_input["genres"]
    artist_to_edit.facebook_link = user_input["facebook_link"]
    try:
        db.session.add(artist_to_edit)
        db.session.commit()
        flash(f"Artist id '{artist_to_edit.id}' has been updated!")
    except Exception as e:
        flash(f"Error updating artist id '{artist_to_edit.id}': {e}")
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue_info = Venue.query.filter_by(id=venue_id).first()
    venue = {
        "id": venue_info.id,
        "name": venue_info.name,
        "genres": venue_info.genres,
        "address": venue_info.address,
        "city": venue_info.city,
        "state": venue_info.state,
        "phone": venue_info.phone,
        "website": venue_info.website,
        "facebook_link": venue_info.facebook_link,
        "seeking_talent": venue_info.seeking_talent,
        "seeking_description": venue_info.seeking_description,
        "image_link": venue_info.image_link
    }
    # TODO√: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO√: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue_to_edit = Venue.query.filter_by(id=venue_id).first()
    user_input = request.form
    venue_to_edit.name = user_input["name"]
    venue_to_edit.city = user_input["city"]
    venue_to_edit.state = user_input["state"]
    venue_to_edit.address = user_input["address"]
    venue_to_edit.phone = user_input["phone"]
    venue_to_edit.genres = user_input["genres"]
    venue_to_edit.facebook_link = user_input["facebook_link"]
    try:
        db.session.add(venue_to_edit)
        db.session.commit()
        flash(f"Venue id '{venue_to_edit.id}' has been updated!")
    except Exception as e:
        flash(f"Error updating venue id '{venue_to_edit.id}': {e}")
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO√: insert form data as a new Venue record in the db, instead
    # TODO√: modify data to be the data object returned from db insertion
    user_input = request.form
    name = user_input["name"]
    # check if the new name is existing in db
    query = Artist.query.filter_by(name=name).first()
    if query:
        flash("This artist is already posted!")
    else:
        new_artist = Artist(
            name=user_input["name"],
            genres=user_input["genres"],
            city=user_input["city"],
            state=user_input["state"],
            phone=user_input["phone"],
            facebook_link=user_input["facebook_link"],
        )
        try:
            db.session.add(new_artist)
            db.session.commit()
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
        except Exception as e:
            flash(f"error while posting new artist:{e}")
            db.session.rollback()
        finally:
            db.session.close()
    # TODO√: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO√: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # data = [{
    #     "venue_id": 1,
    #     "venue_name": "The Musical Hop",
    #     "artist_id": 4,
    #     "artist_name": "Guns N Petals",
    #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    # }]
    shows = Show.query.all()
    data = []
    for s in shows:
        venue = Venue.query.filter_by(id=s.venue_id).first()
        artist = Artist.query.filter_by(id=s.artist_id).first()
        data.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": format_datetime(str(s.start_time))
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO√: insert form data as a new Show record in the db, instead
    user_input = {
        "artist_id": request.form["artist_id"],
        "venue_id": request.form["venue_id"],
        "start_time": request.form["start_time"],
    }
    err_items = []
    artist = Artist.query.filter_by(id=user_input["artist_id"]).first()
    venue = Venue.query.filter_by(id=user_input["venue_id"]).first()
    if not artist:
        err_items.append("artist_id")
    if not venue:
        err_items.append("venue_id")
    if err_items:
        flash(f"following ID(s) not found: {','.join(err_items)}")    
    # on successful db insert, flash success
    else:
        new_show = Show(
            artist_id = user_input["artist_id"],
            venue_id = user_input["venue_id"],
            start_time = user_input["start_time"]
        )
        try:
            db.session.add(new_show)
            db.session.commit()
            flash('Show was successfully listed!')
        except Exception as e:
            print(f"db err: {e}")
            flash("Show was not listed, error occured!")
        finally:
            db.session.close()
    # TODO√: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
