import sys
import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, inputs, abort

app = Flask(__name__)
api = Api(app)

# --- DATABASE CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
# This suppresses a warning from SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- DATABASE MODEL ---
class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(100), nullable=False)  # db.String automatically creates a VARCHAR
    date = db.Column(db.Date, nullable=False)


# --- RESOURCES (API ENDPOINTS) ---
class EventToday(Resource):
    def get(self):
        # 1. Get today's actual date
        today = datetime.date.today()

        # 2. Query the database for events matching today
        events = EventModel.query.filter(EventModel.date == today).all()

        # 3. Format the results into a list of dictionaries
        return [{"id": e.id, "event": e.event, "date": str(e.date)} for e in events]


class Event(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('event', type=str, help="The event name is required!", required=True, location='form')
        parser.add_argument('date', type=inputs.date,
                            help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                            required=True, location='form')
        args = parser.parse_args()

        new_event = EventModel(
            event=args['event'],
            date=args['date'].date()
        )
        db.session.add(new_event)
        db.session.commit()

        return {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }

    def get(self):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time and end_time:
            try:
                start_date = datetime.datetime.strptime(start_time, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_time, "%Y-%m-%d").date()
            except ValueError:
                abort(400, message="Wrong date format. Use YYYY-MM-DD")

            events = EventModel.query.filter(
                EventModel.date >= start_date,
                EventModel.date <= end_date
            ).all()
        else:
            events = EventModel.query.all()

        return [{"id": e.id, "event": e.event, "date": str(e.date)} for e in events]

    def delete(self):
        # Delete all records in the EventModel table
        EventModel.query.delete()
        db.session.commit()

        return {"message": "All events have been deleted!"}


class EventByID(Resource):
    def get(self, event_id):
        # 1. Query the database for the specific ID
        event = EventModel.query.filter(EventModel.id == event_id).first()

        # 2. If the event doesn't exist, return a JSON 404 error
        if event is None:
            return {"message": "The event doesn't exist!"}, 404

        # 3. If it does exist, return the event details formatted as JSON
        return {
            "id": event.id,
            "event": event.event,
            "date": str(event.date)
        }

    def delete(self, event_id):
        # 1. Try to find the event by its ID
        event = EventModel.query.filter(EventModel.id == event_id).first()

        # 2. If it doesn't exist, return the 404 error
        if event is None:
            return {"message": "The event doesn't exist!"}, 404

        # 3. If it does exist, delete it from the session and commit
        db.session.delete(event)
        db.session.commit()

        # 4. Return the success message
        return {"message": "The event has been deleted!"}


# --- MAP ENDPOINTS ---
api.add_resource(EventToday, '/event/today')
api.add_resource(Event, '/event')
api.add_resource(EventByID, '/event/<int:event_id>')

# --- RUN APPLICATION ---
if __name__ == '__main__':
    # Initialize the database table before the server starts
    with app.app_context():
        db.create_all()

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
