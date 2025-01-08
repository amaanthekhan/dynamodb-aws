from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)  # Use double underscores: __name__
app.config['SECRET_KEY'] = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'

# Create a DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'YourFitnessTrackerTable'
table = dynamodb.Table(table_name)

class FitnessForm(FlaskForm):
    activity_type = StringField('Activity Type', validators=[DataRequired()])
    duration = IntegerField('Duration (seconds)', validators=[DataRequired()])
    distance = IntegerField('Distance (meters)', validators=[DataRequired()])
    calories_burned = IntegerField('Calories Burned', validators=[DataRequired()])

class MockDatabase:
    def __init__(self):
        self.data = []

    def put_item(self, item):
        # Add a timestamp to the item
        item['Timestamp'] = datetime.now().isoformat()
        self.data.append(item)

    def query_items(self, user_id):
        return [item for item in self.data if item.get('UserID') == user_id]

# You can choose between using DynamoDB or a MockDatabase for testing.
# Replace the database variable with the appropriate choice.
database = MockDatabase()
# database = DynamoDBDatabase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_activity', methods=['GET', 'POST'])
def record_activity():
    form = FitnessForm()
    if form.validate_on_submit():
        activity_data = {
            'UserID': 'UserID123',  # Replace with the actual user ID
            'ActivityType': form.activity_type.data,
            'Duration': form.duration.data,
            'Distance': form.distance.data,
            'CaloriesBurned': form.calories_burned.data,
        }

        # Use the database to store data
        database.put_item(activity_data)

        return redirect(url_for('index'))
    return render_template('Recordactivity.html', form=form)

@app.route('/view_activities')
def view_activities():
    user_id = 'UserID123'  # Replace with the actual user ID
    items = database.query_items(user_id)
    return render_template('Viewactivities.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)




