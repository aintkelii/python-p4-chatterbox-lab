from app import app, db

from models import Message  # Import your model
import pytest
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()  # This creates the tables
        yield client
        db.drop_all()  # Clean up after tests

class TestApp:
    def test_message_creation(self, client):
        # Test with the database properly set up
        test_message = Message(username="Liza", body="Hello 👋")
        db.session.add(test_message)
        db.session.commit()
        
        # Now your tests can query the messages table

class TestApp:
    '''Flask application in app.py'''

    def setup_method(self):
        # Ensure tables are created before each test and clean up any existing test messages
        with app.app_context():
            db.create_all()
            m = Message.query.filter(
                Message.body == "Hello 👋"
                ).filter(Message.username == "Liza")
            for message in m:
                db.session.delete(message)
            db.session.commit()

    def test_has_correct_columns(self):
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():

            app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():

            response = app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            assert(response.content_type == 'application/json')

            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()


    def test_updates_body_of_message_in_database(self):
        '''updates the body of a message in the database.'''
        with app.app_context():

            # Ensure there is at least one message in the database
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            db.session.add(hello_from_liza)
            db.session.commit()

            m = Message.query.first()
            id = m.id
            body = m.body

            app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            g = Message.query.filter_by(body="Goodbye 👋").first()
            assert(g)

            # Clean up: revert the change and delete the test message
            g.body = body
            db.session.add(g)
            db.session.commit()
            db.session.delete(g)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        '''returns data for the updated message as JSON.'''
        with app.app_context():

            # Ensure there is at least one message in the database
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            db.session.add(hello_from_liza)
            db.session.commit()

            m = Message.query.first()
            id = m.id
            body = m.body

            response = app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Goodbye 👋")

            g = Message.query.filter_by(body="Goodbye 👋").first()
            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)


