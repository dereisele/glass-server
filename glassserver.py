import flask
import flask_sqlalchemy
import flask_restless
import media
import importer

app = flask.Flask(__name__)
app.config.from_json("config.json")
db = flask_sqlalchemy.SQLAlchemy(app)


class Show(db.Model):

    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    lang = db.Column(db.String(3))
    descr = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def __init__(self, title, lang, descr, image):
        self.title = title
        self.lang = lang
        self.descr = descr
        self.image = image


class ShowDetailed(Show):
    episode = db.relationship('Episode',
                              backref=db.backref('show'))


class Episode(db.Model):

    __tablename__ = "episodes"
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"))
    season = db.Column(db.Integer)
    episode = db.Column(db.Integer)
    title = db.Column(db.String(100))
    descr = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def __init__(self, show_id, season, episode, title, descr, image):
        self.show_id = show_id
        self.season = season
        self.episode = episode
        self.title = title
        self.descr = descr
        self.image = image


class Movie(db.Model):

    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(3))
    title = db.Column(db.String(100))
    descr = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def __init__(self, title, lang, descr, image):
        self.title = title
        self.lang = lang
        self.descr = descr
        self.image = image


class MediaPrefix(db.Model):

    __tablename__ = "mediaprefix"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200))
    name = db.Column(db.String(100))
    type = db.Column(db.Integer)

    def __init__(self, path):
        self.path = path


class MediaFile(db.Model):

    __tablename__ = "mediafiles"
    id = db.Column(db.Integer, primary_key=True)
    prefix_id = db.Column(db.Integer, db.ForeignKey("mediaprefix.id"))
    path = db.Column(db.String(200))

    def __init__(self, prefix_id, path):
        self.prefix_id = prefix_id
        self.path = path


db.create_all()
db.session.commit()
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Show)
manager.create_api(ShowDetailed, collection_name="showsdetailed")
manager.create_api(Episode, exclude_columns=["show_id"])
manager.create_api(Movie)
media.addRoutes(app)
imp = importer
#imp.setmyDB(db)
imp.auto()

if __name__ == "__main__":
    sh = Show("testShow", "en", "test show", "linktoimg")
    sh_id = Show.query.get(id)
    print(id)
    ep = Episode("3", "2", "3", "Episode", "test episode", "linktoimg")
    #db.session.add(sh)
    #db.session.add(ep)
    db.session.commit()
    app.run(host="0.0.0.0", port=1234, threaded=True)
