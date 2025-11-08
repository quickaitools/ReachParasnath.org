from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
app.secret_key = 'parasnath-public-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reach_paras.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    vehicle_type = db.Column(db.String(10))
    price = db.Column(db.Integer)
    rating = db.Column(db.Float)
    rides_count = db.Column(db.Integer)
    location = db.Column(db.String(100))
    photo_url = db.Column(db.String(300))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    reviewer = db.Column(db.String(100))
    rating = db.Column(db.Float)
    text = db.Column(db.Text)
    created_at = db.Column(db.String(100))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    reporter = db.Column(db.String(100))
    text = db.Column(db.Text)
    created_at = db.Column(db.String(100))

# Create tables and manually add 30 drivers
with app.app_context():
    db.create_all()
    if Driver.query.count() == 0:
        drivers = [
            Driver(name="Ravi Kumar", phone="9876543210", vehicle_type="taxi", price=500, rating=4.5, rides_count=10, location="Madhuban", photo_url=""),
            Driver(name="Sunita Devi", phone="9123456789", vehicle_type="van", price=800, rating=4.2, rides_count=7, location="Isri Bazar", photo_url=""),
            Driver(name="Amit Singh", phone="9988776655", vehicle_type="taxi", price=600, rating=4.8, rides_count=15, location="Parasnath Station", photo_url=""),
            Driver(name="Neha Yadav", phone="9876543211", vehicle_type="van", price=750, rating=4.3, rides_count=12, location="Giridih", photo_url=""),
            Driver(name="Rajesh Kumar", phone="9876543212", vehicle_type="taxi", price=550, rating=4.6, rides_count=18, location="Koderma", photo_url=""),
            Driver(name="Pooja Singh", phone="9876543213", vehicle_type="van", price=700, rating=4.1, rides_count=9, location="Dhanbad", photo_url=""),
            Driver(name="Vikram Yadav", phone="9876543214", vehicle_type="taxi", price=620, rating=4.7, rides_count=20, location="Madhuban", photo_url=""),
            Driver(name="Kiran Devi", phone="9876543215", vehicle_type="van", price=780, rating=4.4, rides_count=11, location="Isri Bazar", photo_url=""),
            Driver(name="Manoj Kumar", phone="9876543216", vehicle_type="taxi", price=590, rating=4.5, rides_count=14, location="Parasnath Station", photo_url=""),
            Driver(name="Priya Singh", phone="9876543217", vehicle_type="van", price=820, rating=4.2, rides_count=8, location="Giridih", photo_url=""),
            Driver(name="Deepak Yadav", phone="9876543218", vehicle_type="taxi", price=610, rating=4.6, rides_count=16, location="Koderma", photo_url=""),
            Driver(name="Anjali Devi", phone="9876543219", vehicle_type="van", price=770, rating=4.3, rides_count=10, location="Dhanbad", photo_url=""),
            Driver(name="Suresh Kumar", phone="9876543220", vehicle_type="taxi", price=530, rating=4.7, rides_count=19, location="Madhuban", photo_url=""),
            Driver(name="Meena Singh", phone="9876543221", vehicle_type="van", price=790, rating=4.1, rides_count=7, location="Isri Bazar", photo_url=""),
            Driver(name="Arjun Yadav", phone="9876543222", vehicle_type="taxi", price=640, rating=4.5, rides_count=13, location="Parasnath Station", photo_url=""),
            Driver(name="Komal Devi", phone="9876543223", vehicle_type="van", price=760, rating=4.2, rides_count=9, location="Giridih", photo_url=""),
            Driver(name="Naveen Kumar", phone="9876543224", vehicle_type="taxi", price=580, rating=4.6, rides_count=17, location="Koderma", photo_url=""),
            Driver(name="Ritika Singh", phone="9876543225", vehicle_type="van", price=800, rating=4.3, rides_count=10, location="Dhanbad", photo_url=""),
            Driver(name="Harish Yadav", phone="9876543226", vehicle_type="taxi", price=610, rating=4.5, rides_count=15, location="Madhuban", photo_url=""),
            Driver(name="Divya Devi", phone="9876543227", vehicle_type="van", price=730, rating=4.2, rides_count=8, location="Isri Bazar", photo_url=""),
            Driver(name="Kamal Kumar", phone="9876543228", vehicle_type="taxi", price=560, rating=4.6, rides_count=18, location="Parasnath Station", photo_url=""),
            Driver(name="Sneha Singh", phone="9876543229", vehicle_type="van", price=790, rating=4.1, rides_count=7, location="Giridih", photo_url=""),
            Driver(name="Rohit Yadav", phone="9876543230", vehicle_type="taxi", price=630, rating=4.5, rides_count=14, location="Koderma", photo_url=""),
            Driver(name="Lata Devi", phone="9876543231", vehicle_type="van", price=770, rating=4.3, rides_count=9, location="Dhanbad", photo_url=""),
            Driver(name="Yash Kumar", phone="9876543232", vehicle_type="taxi", price=600, rating=4.6, rides_count=16, location="Madhuban", photo_url=""),
            Driver(name="Bhavna Singh", phone="9876543233", vehicle_type="van", price=810, rating=4.2, rides_count=10, location="Isri Bazar", photo_url=""),
            Driver(name="Tushar Yadav", phone="9876543234", vehicle_type="taxi", price=590, rating=4.5, rides_count=13, location="Parasnath Station", photo_url=""),
            Driver(name="Geeta Devi", phone="9876543235", vehicle_type="van", price=750, rating=4.1, rides_count=8, location="Giridih", photo_url=""),
            Driver(name="Varun Kumar", phone="9876543236", vehicle_type="taxi", price=620, rating=4.6, rides_count=17, location="Koderma", photo_url=""),
            Driver(name="Payal Singh", phone="9876543237", vehicle_type="van", price=780, rating=4.3, rides_count=9, location="Dhanbad", photo_url="")
        ]
        db.session.add_all(drivers)
        db.session.commit()
        print("✅ 30 dummy drivers added.")

# Public routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/api/drivers')
def list_drivers():
    vehicle = request.args.get('vehicle', 'both')
    sort = request.args.get('sort', 'rating_desc')
    search = request.args.get('search', '').strip().lower()

    query = Driver.query

    if vehicle in ('taxi', 'van'):
        query = query.filter_by(vehicle_type=vehicle)

    if search:
        query = query.filter(Driver.name.ilike(f"%{search}%"))

    if sort == 'rating_desc':
        query = query.order_by(Driver.rating.desc(), Driver.rides_count.desc())
    elif sort == 'name_asc':
        query = query.order_by(Driver.name.asc())
    elif sort == 'price_asc':
        query = query.order_by(Driver.price.asc())

    drivers = query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'phone': d.phone,
        'vehicle_type': d.vehicle_type,
        'price': d.price,
        'rating': d.rating,
        'rides_count': d.rides_count,
        'location': d.location,
        'photo_url': d.photo_url
    } for d in drivers])

@app.route('/api/drivers/<int:driver_id>')
def get_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    return jsonify({
        'id': driver.id,
        'name': driver.name,
        'phone': driver.phone,
        'vehicle_type': driver.vehicle_type,
        'price': driver.price,
        'rating': driver.rating,
        'rides_count': driver.rides_count,
        'location': driver.location,
        'photo_url': driver.photo_url
    })

@app.route('/api/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        driver_id = request.args.get('driver_id')
        reviews = Review.query.filter_by(driver_id=driver_id).order_by(Review.created_at.desc()).all()
        return jsonify([{
            'id': r.id,
            'driver_id': r.driver_id,
            'reviewer': r.reviewer,
            'rating': r.rating,
            'text': r.text,
            'created_at': r.created_at
        } for r in reviews])

    data = request.get_json()
    review = Review(
        driver_id=data['driver_id'],
        reviewer=data.get('reviewer', ''),
        rating=float(data['rating']),
        text=data['text'],
        created_at=datetime.utcnow().isoformat()
    )
    db.session.add(review)
    db.session.commit()

    avg = db.session.query(db.func.avg(Review.rating)).filter_by(driver_id=review.driver_id).scalar()
    driver = Driver.query.get(review.driver_id)
    driver.rating = round(avg, 2)
    db.session.commit()

    return jsonify({'status': 'ok'})

@app.route('/api/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'GET':
        driver_id = request.args.get('driver_id')
        reports = Report.query.filter_by(driver_id=driver_id).order_by(Report.created_at.desc()).all()
        return jsonify([{
            'id': r.id,
            'driver_id': r.driver_id,
            'reporter': r.reporter,
            'text': r.text,
            'created_at': r.created_at
        } for r in reports])

    data = request.get_json()
    report = Report(
        driver_id=data['driver_id'],
        reporter=data.get('reporter', ''),
        text=data['text'],
        created_at=datetime.utcnow().isoformat()
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'status': 'ok'})

# Info pages
@app.route('/privacy')
def privacy():
    return "<h1>Privacy Policy</h1><p>Coming soon.</p>"

@app.route('/terms')
def terms():
    return "<h1>Terms of Use</h1><p>Coming soon.</p>"

@app.route('/best-time')
def best_time():
    return "<h1>Best Time to Visit</h1><p>October to March is ideal.</p>"

@app.route('/temples')
def temples():
    return "<h1>Temples Guide</h1><p>Explore the sacred sites across Parasnath Hill.</p>"

if __name__ == '__main__':
    app.run(debug=True)