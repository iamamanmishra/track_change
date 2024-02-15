# Import necessary modules and packages
import os

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import logging

from sqlalchemy import Column, Integer, String, Float

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Create Flask application instance
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure database URI and other settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')  # SQLite database URI
app.config['JWT_SECRET_KEY'] = 'secret'  # JWT secret key
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'  # Mail server settings
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '2a5bc6c3707466'
app.config['MAIL_PASSWORD'] = 'db072675ad9ba9'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Initialize Flask extensions
db = SQLAlchemy(app)  # SQLAlchemy database object
ma = Marshmallow(app)  # Marshmallow object for object serialization
jwt = JWTManager(app)  # JWT manager object for handling JWT tokens
mail = Mail(app)  # Mail object for sending emails


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Data dropped!')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=3.285e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name='Venus',
                   planet_type='Class K',
                   home_star='Sol',
                   mass=4.867e24,
                   radius=3760,
                   distance=67.24e6)

    earth = Planet(planet_name='Earth',
                   planet_type='Class M',
                   home_star='Sol',
                   mass=5.972e24,
                   radius=3959,
                   distance=92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='Test',
                     last_name='User',
                     email='testuser@mailinator.com',
                     password='password')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')


# Define route handlers

@app.route('/')
def home_page():
    """
    Home Page Route

    This route returns a welcome message when the root URL is accessed.
    """
    logging.info('Home page accessed')
    logging.info('Request details are: {}'.format(request.form))
    return jsonify(message='Welcome to Planetary API!')  # Welcome message


@app.route('/planets', methods=['GET'])
def planets():
    """
    Planets Route

    This route returns a JSON response containing details of all planets in the database.
    """
    logging.info(request)
    logging.info('Planets route accessed')
    logging.info('Request details are: {}'.format(request.form))
    planets_list = Planet.query.all()  # Retrieve all planets from the database
    result = planets_schema.dump(planets_list)  # Serialize planets data
    return jsonify(result)  # Return serialized planets data


@app.route('/register', methods=['POST'])
def register():
    """
    Register Route

    This route allows users to register by providing their information via a POST request.
    """
    logging.info(request)
    logging.info('Register route accessed')
    logging.info('Request details are: {}'.format(request.form))
    email = request.form['email']  # Get email from form data
    test = User.query.filter_by(email=email).first()  # Check if email already exists
    if test:
        logging.info("response sent = That email already exists")
        return jsonify("That email already exists"), 409  # Return message if email already exists
    else:
        first_name = request.form['first_name']  # Get first name from form data
        last_name = request.form['last_name']  # Get last name from form data
        password = request.form['password']  # Get password from form data
        user = User(first_name=first_name, last_name=last_name, email=email,
                    password=password)  # Create new user object
        db.session.add(user)  # Add user to the database session
        db.session.commit()  # Commit changes to the database
        logging.info("response sent = User created successfully")
        return jsonify(message="User created successfully"), 201  # Return success message


@app.route('/login', methods=['POST'])
def login():
    """
    Login Route

    This route allows users to log in by providing their email and password via a POST request.
    """
    logging.info(request)
    logging.info('Login route accessed')
    logging.info('Request details are: {}'.format(request.form))
    if request.is_json:
        email = request.json['email']  # Get email from JSON data
        password = request.json['password']  # Get password from JSON data
    else:
        email = request.form['email']  # Get email from form data
        password = request.form['password']  # Get password from form data

    test = User.query.filter_by(email=email,
                                password=password).first()  # Check if user exists with provided credentials
    if test:
        access_token = create_access_token(identity=email)  # Create JWT access token
        logging.info("response sent = Login successful!")
        return jsonify(message='Login successful!',
                       access_token=access_token)  # Return success message with access token
    else:
        logging.info("response sent = Bad email or password")
        return jsonify(message='Bad email or password'), 401  # Return error message for invalid credentials


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    """
    Retrieve Password Route

    This route allows users to retrieve their password by providing their email address.
    """
    logging.info(request)
    logging.info('Retrieve password route accessed')
    logging.info('Request details are: {}'.format(request.form))
    user = User.query.filter_by(email=email).first()  # Retrieve user with provided email
    if user:
        msg = Message('Your planetary API password is ' + user.password,
                      sender="admin@planetary-api.com",
                      recipients=[email])  # Compose email message with password
        mail.send(msg)  # Send email
        logging.info("response sent = Password sent to {}".format(email))
        return jsonify(message="Password sent to " + email)  # Return success message
    else:
        logging.info("response sent = That email doesn't exist")
        return jsonify(mesage="That email doesn't exist")  # Return error message for non-existent email


@app.route('/planet_details/<int:planet_id>', methods=['GET'])
def planet_details(planet_id: int):
    """
    Planet Details Route

    This route returns details of a specific planet identified by its ID.
    """
    logging.info(request)
    logging.info('Planet details route accessed')
    logging.info('Request details are: {}'.format(request.form))
    planet = Planet.query.filter_by(planet_id=planet_id).first()  # Retrieve planet with provided ID
    if planet:
        result = planet_schema.dump(planet)  # Serialize planet data
        logging.info("response sent = {}".format(result))
        return jsonify(result)  # Return serialized planet data
    else:
        logging.info("response sent = That planet doesn't exist")
        return jsonify(message="That planet doesn't exist"), 404  # Return error message for non-existent planet


@app.route('/add_planet', methods=['POST'])
@jwt_required()
def add_planet():
    """
    Add Planet Route

    This route allows authenticated users to add a new planet by providing its details via a POST request.
    """
    logging.info(request)
    logging.info('Add planet route accessed')
    logging.info('Request details are: {}'.format(request.form))
    planet_name = request.form['planet_name']  # Get planet name from form data
    test = Planet.query.filter_by(planet_name=planet_name).first()  # Check if planet with the same name already exists
    if test:
        logging.info("response sent = There is already a planet by that name")
        return jsonify("There is already a planet by that name"), 409  # Return message if planet with same name exists
    else:
        planet_type = request.form['planet_type']  # Get planet type from form data
        home_star = request.form['home_star']  # Get home star from form data
        mass = request.form['mass']  # Get mass from form data
        radius = request.form['radius']  # Get radius from form data
        distance = request.form['distance']  # Get distance from form data

        new_planet = Planet(planet_name=planet_name,
                            planet_type=planet_type,
                            home_star=home_star,
                            mass=mass,
                            radius=radius,
                            distance=distance)  # Create new planet object
        db.session.add(new_planet)  # Add planet to the database session
        db.session.commit()  # Commit changes to the database
        logging.info("response sent = Planet Added!")
        return jsonify(message="Planet Added!"), 201  # Return success message


@app.route('/update_planet', methods=['PUT'])
@jwt_required()
def update_planet():
    """
    Update Planet Route

    This route allows authenticated users to update details of an existing planet by providing its ID and new details
    via a PUT request.
    """
    logging.info(request)
    logging.info('Update planet route accessed')
    logging.info('Request details are: {}'.format(request.form))
    planet_id = int(request.form['planet_id'])  # Get planet ID from form data
    planet = Planet.query.filter_by(planet_id=planet_id).first()  # Retrieve planet with provided ID
    if planet:
        planet.planet_name = request.form['planet_name']  # Update planet name
        planet.planet_type = request.form['planet_type']  # Update planet type
        planet.home_star = request.form['home_star']  # Update home star
        planet.mass = float(request.form['mass'])  # Update mass
        planet.radius = float(request.form['radius'])  # Update radius
        planet.distance = float(request.form['distance'])  # Update distance
        db.session.commit()  # Commit changes to the database
        logging.info("response sent = You updated a planet")
        return jsonify("You updated a planet"), 202  # Return success message
    else:
        logging.info("response sent = That planet doesn't exist")
        return jsonify("That planet doesn't exist"), 404  # Return error message for non-existent planet


@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def remove_planet(planet_id: int):
    """
    Remove Planet Route

    This route allows authenticated users to remove a planet identified by its ID.
    """
    logging.info(request)
    logging.info('Remove planet route accessed')
    logging.info('Request details are: {}'.format(request.form))
    planet = Planet.query.filter_by(planet_id=planet_id).first()  # Retrieve planet with provided ID
    if planet:
        db.session.delete(planet)  # Delete planet from the database
        db.session.commit()  # Commit changes to the database
        logging.info("response sent = You deleted a planet!")
        return jsonify("You deleted a planet!"), 202  # Return success message
    else:
        logging.info("response sent = That planet doesn't exist")
        return jsonify("That planet doesn't exist"), 404  # Return error message for non-existent planet


# Define database models
class User(db.Model):
    __tablename__ = 'users'  # Table name
    id = Column(Integer, primary_key=True)  # User ID
    first_name = Column(String)  # User's first name
    last_name = Column(String)  # User's last name
    email = Column(String, unique=True)  # User's email (unique)
    password = Column(db.String)  # User's password


class Planet(db.Model):
    __tablename__ = 'planets'  # Table name
    planet_id = Column(Integer, primary_key=True)  # Planet ID
    planet_name = Column(String)  # Planet name
    planet_type = Column(String)  # Planet type
    home_star = Column(String)  # Home star of the planet
    mass = Column(Float)  # Mass of the planet
    radius = Column(Float)  # Radius of the planet
    distance = Column(Float)  # Distance from the planet to its home star


# Define Marshmallow schemas for serialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')  # Fields to include in serialization


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius',
                  'distance')  # Fields to include in serialization


# Initialize schema objects
user_schema = UserSchema()  # Schema for single user
users_schema = UserSchema(many=True)  # Schema for multiple users
planet_schema = PlanetSchema()  # Schema for single planet
planets_schema = PlanetSchema(many=True)  # Schema for multiple planets

# If this script is executed directly, run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
