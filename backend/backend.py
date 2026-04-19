import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required,create_access_token,get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import random
import time
import uuid
from sqlalchemy.dialects.postgresql import UUID
import razorpay
from dotenv import load_dotenv

load_dotenv()

from flask_cors import CORS

app = Flask(__name__)
# Allow CORS for all origins in development, but allow restricting it via environment variable for production
CORS(app, resources={r"/api/*": {"origins": os.environ.get('ALLOWED_ORIGINS', '*')}})

# Configurations
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default-dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://srishti:srishti@127.0.0.1:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-jwt-key')


# Enable token blacklist
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# Razorpay Configuration
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_default')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'default_secret')
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# In-memory blacklist for demo (use Redis or DB in production)
blacklist = set()
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist
db = SQLAlchemy(app)

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = "user"
     
    id = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    
    # New fields
    user_type = db.Column(db.String(20), default="customer")  # customer, professional, admin
    is_verified = db.Column(db.Boolean, default=False)

    gender = db.Column(db.String(10), nullable=True)   # male, female, other
    dob = db.Column(db.Date, nullable=True)            # Date of birth
    profile_image = db.Column(db.String(255), nullable=True)  # URL or file path

    # Address fields
    address_line1 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
tokens = {}

class UserAddress(db.Model):
    __tablename__ = 'user_addresses'
      # <- specify schema here

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    
    line1 = db.Column(db.String(255), nullable=False)
    line2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(50), nullable=True) # e.g. Home, Office
    is_default = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Address {self.line1}, {self.city}>'
    
class UserSettings(db.Model):
    __tablename__ = 'user_settings'
      # schema

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    language = db.Column(db.String(20), default='en')
    notifications_enabled = db.Column(db.Boolean, default=True)
    theme_color = db.Column(db.String(20), default='light')  # light, dark, custom
    timezone = db.Column(db.String(50), default='UTC')
    privacy_mode = db.Column(db.Boolean, default=False)  # hide profile info
    font_size = db.Column(db.String(10), default='medium')  # small, medium, large
    background_image = db.Column(db.String(255), nullable=True)  # optional URL/path

    def __repr__(self):
        return f'<Settings {self.language}, Theme: {self.theme_color}>'


class UserProfile(db.Model):
      # <- specify schema here

    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    language = db.Column(db.String(50))
    bio = db.Column(db.Text)

class ServiceCategory(db.Model):
    __tablename__ = 'service_category'
    

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    starting_price = db.Column(db.Float)  # e.g., "Starting at $50"
    is_active = db.Column(db.Boolean, default=True)

    # Relationship
    services = db.relationship('Service', backref='category', lazy=True, cascade="all, delete-orphan")

    def to_dict(self, include_services=False):
        data = {
            "category_id": self.id,
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "starting_price": self.starting_price,
            "is_active": self.is_active
        }
        if include_services:
            data["services"] = [service.to_dict() for service in self.services]
        return data


class Service(db.Model):
    __tablename__ = 'service'
    

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    category_id = db.Column(db.String, db.ForeignKey('service_category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='service', lazy=True)
    def to_dict(self):
        return {
            "service_id": self.id,
            "name": self.name,
            "description": self.description,
            "base_price": self.base_price,
            "image_url": self.image_url,
            "is_active": self.is_active,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'
      # specify schema

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.String, db.ForeignKey('service.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # e.g., 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat()
        }
    
class Booking(db.Model):
      # <- specify schema here

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    service_id = db.Column(db.String, db.ForeignKey('service.id'))
    professional_id = db.Column(db.String, db.ForeignKey('user.id'),nullable=True)
    scheduled_time = db.Column(db.DateTime)
    status = db.Column(db.String(20))  # pending, confirmed, completed, canceled
    address = db.Column(db.Text)
    instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add this method
    def to_dict(self):
        return {
            "booking_id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "professional_id": self.professional_id,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "status": self.status,
            "address": self.address,
            "instructions": self.instructions,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
class BookingPayment(db.Model):
      # <- specify schema here

    id = db.Column(db.String, primary_key=True)
    booking_id = db.Column(db.String, db.ForeignKey('booking.id'))
    amount = db.Column(db.Float)
    method = db.Column(db.String(50))
    status = db.Column(db.String(20))  # paid, failed, pending
    transaction_id = db.Column(db.String(100))
    paid_at = db.Column(db.DateTime)

class Review(db.Model):
      # <- specify schema here

    id = db.Column(db.String, primary_key=True)
    booking_id = db.Column(db.String, db.ForeignKey('booking.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProfessionalProfile(db.Model):
      # <- specify schema here

    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    experience = db.Column(db.Integer)
    skills = db.Column(db.Text)
    documents = db.Column(db.Text)
    certification = db.Column(db.Text)

class AvailabilitySlot(db.Model):
      # <- specify schema here

    id = db.Column(db.String, primary_key=True)
    professional_id = db.Column(db.String, db.ForeignKey('user.id'))
    day_of_week = db.Column(db.Integer)  # 0=Mon ... 6=Sun
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

class Wallet(db.Model):
    __tablename__ = 'wallet'
      # <- specify schema here
    id = db.Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4,nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'),unique=True)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='wallet', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    type = db.Column(db.String(20))  # 'credit' or 'debit'
    amount = db.Column(db.Float)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    wallet_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.id'))  # <--- foreign key
    def to_dict(self):
        return {
            "transaction_id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "amount": self.amount,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }

class Payment(db.Model):
    __tablename__ = 'payment'
    

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    booking_id = db.Column(db.String, db.ForeignKey('booking.id'))
    amount = db.Column(db.Float)
    method = db.Column(db.String(50))  # wallet, card, upi, etc.
    status = db.Column(db.String(20))  # paid, failed, pending, refund_requested
    transaction_id = db.Column(db.String(100))
    paid_at = db.Column(db.DateTime)
    refund_reason = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            "payment_id": self.id,
            "user_id": self.user_id,
            "booking_id": self.booking_id,
            "amount": self.amount,
            "method": self.method,
            "status": self.status,
            "transaction_id": self.transaction_id,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "refund_reason": self.refund_reason
        }

class Subscription(db.Model):
    __tablename__ = 'subscription'
    

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)  # e.g., 30, 90
    description = db.Column(db.Text)

class ProfessionalRating(db.Model):
    __tablename__ = 'professional_rating'
    

    id = db.Column(db.String, primary_key=True)
    professional_id = db.Column(db.String, db.ForeignKey('user.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)  # 1-5 stars
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "professional_id": self.professional_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "review": self.review,
            "created_at": self.created_at.isoformat()
        }


class ProfessionalAvailability(db.Model):
    __tablename__ = 'professional_availability'
    

    id = db.Column(db.String, primary_key=True)
    professional_id = db.Column(db.String, db.ForeignKey('user.id'))
    available_from = db.Column(db.DateTime)
    available_to = db.Column(db.DateTime)
    status = db.Column(db.String(20))  # available, busy, on_leave

class Promo(db.Model):
    __tablename__ = "promo"
      # specify schema

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    discount = db.Column(db.Float, nullable=True)  # percentage discount
    valid_till = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "discount": self.discount,
            "valid_till": self.valid_till.isoformat() if self.valid_till else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Referral(db.Model):
    __tablename__ = "referral"
      # schema

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)  # who referred
    friend_email = db.Column(db.String(120), nullable=False)
    referral_code = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, accepted, rewarded
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "friend_email": self.friend_email,
            "referral_code": self.referral_code,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class FAQ(db.Model):
    __tablename__ = "faq"
    

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)


class SupportTicket(db.Model):
    __tablename__ = "support_ticket"
    

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open")  # open, in-progress, closed
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class SupportChat(db.Model):
    __tablename__ = "support_chat"
    

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    ticket_id = db.Column(db.String, db.ForeignKey("support_ticket.id"), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class IssueReport(db.Model):
    __tablename__ = "issue_report"
    

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.String, db.ForeignKey("service.id"), nullable=False)
    issue_type = db.Column(db.String(100), nullable=False)  # e.g., delay, quality, payment
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="reported")  # reported, in-progress, resolved
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class AppFeedback(db.Model):
    

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)  # 1–5
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "rating": self.rating,
            "message": self.message,
            "created_at": self.created_at.isoformat()
        }

class RevokedToken(db.Model):
    

    id = db.Column(db.String, primary_key=True)   # UUID
    jti = db.Column(db.String(255), unique=True) # JWT ID (from token)
    token = db.Column(db.Text, nullable=False)   # full token string if needed
    revoked_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class UserSubscription(db.Model):
    __tablename__ = 'user_subscription'
    

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    subscription_id = db.Column(db.String, db.ForeignKey('subscription.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

class WalletTransaction(db.Model):
      # <- specify schema here

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    type = db.Column(db.String(10))  # credit / debit
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
      # <- specify schema here

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminUser(db.Model):
      # <- specify schema here

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.Text)
    role = db.Column(db.String(50))
    last_login = db.Column(db.DateTime)

class OTP(db.Model):
      # <- specify schema here

    __tablename__ = 'otps'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = db.Column(db.String(15), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, phone_number, otp, expires_in_minutes=5):
        self.phone_number = phone_number
        self.otp = otp
        self.expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)

from flask import request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()

    required_fields = ['full_name', 'email', 'password', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Generate next ID (auto increment string ID)
    import uuid

    next_id = str(uuid.uuid4())

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Convert dob if provided
    dob_value = None
    if "dob" in data and data["dob"]:
        try:
            dob_value = datetime.strptime(data["dob"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format for dob (expected YYYY-MM-DD)'}), 400

    user = User(
        id=next_id,
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        password_hash=hashed_password,

        # New fields
        user_type=data.get('user_type', 'customer'),
        is_verified=data.get('is_verified', False),
        gender=data.get('gender'),
        dob=dob_value,
        profile_image=data.get('profile_image'),
        address_line1=data.get('address_line1'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        country=data.get('country'),
    )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id, expires_delta=timedelta(days=7))
    tokens[user.id] = token

    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user': {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'user_type': user.user_type,
            'is_verified': user.is_verified,
            'gender': user.gender,
            'dob': str(user.dob) if user.dob else None,
            'profile_image': user.profile_image,
            'address_line1': user.address_line1,
            'city': user.city,
            'state': user.state,
            'zip_code': user.zip_code,
            'country': user.country,
        }
    }), 201
# Login Route
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity=user.id, expires_delta=timedelta(days=7))
    tokens[user.id] = token
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone
        }
    }), 200

@app.route('/api/auth/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # JWT ID (unique identifier)
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

otp_store = {}
# Dummy email and SMS sender (replace with real integration)
def send_sms(phone, otp):
    print(f"Sending SMS to {phone}: Your OTP is {otp}")

def send_email(email, otp):
    print(f"Sending Email to {email}: Your OTP is {otp}")

@app.route('/api/auth/otp/send', methods=['POST'])
def send_otp():
    data = request.get_json()
    contact = data.get('contact')
    contact_type = data.get('contact_type')  # 'email' or 'phone'
    print(data)
    if not contact or contact_type not in ['email', 'phone']:
        return jsonify({'message': 'Invalid contact or contact_type'}), 400

    otp = str(random.randint(100000, 999999))
    timestamp = int(time.time())

    # Store OTP (simulate with dictionary; use Redis or DB in real-world)
    otp_store[contact] = {'otp': otp, 'timestamp': timestamp}

    # Send OTP
    if contact_type == 'phone':
        send_sms(contact, otp)
    elif contact_type == 'email':
        send_email(contact, otp)

    return jsonify({'message': f'OTP sent to {contact_type}', 'status': 'success'}), 200

def generate_token(phone_number, expires_in=60):
    payload = {
        'phone': phone_number,
        'exp': datetime.utcnow() + timedelta(minutes=expires_in)
    }
    secret_key = os.getenv('JWT_SECRET', 'your-jwt-secret-key')  # fallback if .env not loaded
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

@app.route('/api/auth/otp/verify', methods=['POST'])
def verify_otp():
    data = request.get_json()
    phone_number = data.get('phone_number')
    otp_code = data.get('otp')
    email = data.get('email')
    print(email)
    if not phone_number or not otp_code:
        if not email:
            return jsonify({'error': 'Phone number or email and OTP are required'}), 400
    # token = generate_token(phone_number)
    if email in otp_store:
        # token = gener  ate_token(email)
        otp = otp_store[email]
        del otp_store[email]
        if otp == otp_code:
            return jsonify({
        'message': 'OTP verified successfully'
    }), 200
        else:
            return jsonify({'error': 'Invalid OTP'}), 400

    # otp_entry = OTP.query.filter_by(phone_number=phone_number, otp=otp_code).first()

    # if not otp_entry:
    #     return jsonify({'error': 'Invalid OTP'}), 400

    # if otp_entry.expires_at < datetime.utcnow():
    #     return jsonify({'error': 'OTP expired'}), 400

    # Mark OTP as used (optional)
    # db.session.delete(otp_entry)
    # db.session.commit()

    # Optional: Generate auth token after OTP verification
    

    return jsonify({
        'message': 'OTP verified successfully'    }), 200

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password_without_otp():
    data = request.get_json()
    phone_number = data.get('phone_number')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not all([phone_number, old_password, new_password]):
        return jsonify({'error': 'Phone number, old password, and new password are required'}), 400

    user = User.query.filter_by(phone=phone_number).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not check_password_hash(user.password_hash, old_password):
        return jsonify({'error': 'Old password is incorrect'}), 401

    user.password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()

    return jsonify({'message': 'Password has been updated successfully'}), 200
def decode_token(tokens, token):
    if token in list(tokens.values()):
        for key in list(tokens.keys()):
            if tokens[key]==token:

                return {"id":key}
            
    return {"id":""}
   
@app.route('/api/auth/user', methods=['GET'])
def get_user_info():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Authorization token required'}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = decode_token(token)
        phone_number = payload.get('phone_number')
        user = User.query.filter_by(phone=phone_number).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'id': user.id,
            'phone': user.phone,
            'email': user.email,
            'full_name': user.full_name,
            'created_at': user.created_at.isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Invalid or expired token'}), 401


@app.route('/api/user/profile', methods=['GET'])
def get_user_profiles():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Authorization token required'}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = decode_token(tokens, token)  # only token needed here
        user = User.query.filter_by(id=payload['id']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "gender": user.gender if hasattr(user, "gender") else None,
            "dob": user.dob.isoformat() if getattr(user, "dob", None) else None,
            "profile_image": user.profile_image if hasattr(user, "profile_image") else None,
            "address": {
                "line1": getattr(user, "address_line1", None),
                "city": getattr(user, "city", None),
                "state": getattr(user, "state", None),
                "zip_code": getattr(user, "zip_code", None),
                "country": getattr(user, "country", None)
            },
            "created_at": user.created_at.isoformat() if user.created_at else None
        }), 200

    except Exception as e:
        return jsonify({'error': 'Invalid or expired token'}), 401

    
def send_password_reset_email(email, token):
    reset_link = f"https://urbanease.com/reset-password/{token}"
    print(f"[EMAIL] Send to {email}: Reset your password using {reset_link}")
    # Integrate with real email service here

def send_sms_reset_link(phone_number, token):
    reset_link = f"https://urbanease.com/reset-password/{token}"
    print(f"[SMS] Send to {phone_number}: Reset your password using {reset_link}")
    # Integrate with SMS API (Twilio, etc.)

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    phone_number = data.get('phone_number')

    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    elif phone_number:
        user = User.query.filter_by(phone_number=phone_number).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Generate a reset token or link (you can use JWT or UUID)
    reset_token = str(uuid.uuid4())
    user.reset_token = reset_token
    db.session.commit()

    if email:
        send_password_reset_email(email, reset_token)
    elif phone_number:
        send_sms_reset_link(phone_number, reset_token)

    return jsonify({'message': 'Password reset instructions sent'}), 200

def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = decode_token(tokens, token)
        print(payload)
        return User.query.filter_by(id=payload.get('id')).first()
    except:
        return None


@app.route('/api/user/profile', methods=['PUT'])
def update_user_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Authorization token required'}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = decode_token(tokens, token)
        print(payload)
        user = User.query.filter_by(id=payload['id']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()

        # Update fields if provided
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "email" in data:
            user.email = data["email"]
        if "phone" in data:
            user.phone = data["phone"]
        if "user_type" in data:
            user.user_type = data["user_type"]
        if "is_verified" in data:
            user.is_verified = data["is_verified"]
        if "gender" in data:
            user.gender = data["gender"]
        if "dob" in data:
            try:
                user.dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({'error': 'Invalid dob format. Use YYYY-MM-DD'}), 400
        if "profile_image" in data:
            user.profile_image = data["profile_image"]
        if "address_line1" in data:
            user.address_line1 = data["address_line1"]
        if "city" in data:
            user.city = data["city"]
        if "state" in data:
            user.state = data["state"]
        if "zip_code" in data:
            user.zip_code = data["zip_code"]
        if "country" in data:
            user.country = data["country"]

        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'phone': user.phone,
                'user_type': user.user_type,
                'is_verified': user.is_verified,
                'gender': user.gender,
                'dob': str(user.dob) if user.dob else None,
                'profile_image': user.profile_image,
                'address_line1': user.address_line1,
                'city': user.city,
                'state': user.state,
                'zip_code': user.zip_code,
                'country': user.country
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Invalid or expired token'}), 401

@app.route('/api/user/addresses', methods=['GET'])
def get_addresses():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    addresses = UserAddress.query.filter_by(user_id=user.id).all()
    return jsonify([{
        "id": addr.id,
        "line1": addr.line1,
        "line2": addr.line2,
        'city': addr.city,
        'state': addr.state,
        'zipcode': addr.zipcode,
        'country': addr.country,
        'label': addr.label,
        'is_default': addr.is_default,
        'created_at': addr.created_at.isoformat()
    } for addr in addresses]), 200

@app.route('/api/user/addresses', methods=['POST'])
def add_address():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    new_address = UserAddress(
        user_id=user.id,
        line1=data.get('line1'),
        line2=data.get('line2'),
        city=data.get('city'),
        state=data.get('state'),
        zipcode=data.get('zipcode'),
        country=data.get('country', 'India'),
        label=data.get('label'),
        is_default=data.get('is_default', False)
    )

    db.session.add(new_address)
    db.session.commit()

    return jsonify({
        "message": "Address added successfully",
        "address": {
            "id": new_address.id,
            "line1": new_address.line1,
            "line2": new_address.line2,
            "city": new_address.city,
            "state": new_address.state,
            "zipcode": new_address.zipcode,
            "country": new_address.country,
            "is_default": new_address.is_default
        }
    }), 201

@app.route('/api/user/address/<string:address_id>', methods=['PUT'])
def update_address(address_id):
    user = get_current_user()
    address = UserAddress.query.filter_by(id=address_id, user_id=user.id).first()

    if not address:
        return jsonify({'error': 'Address not found'}), 404

    data = request.get_json()
    address.line1 = data.get('line1', address.line1)
    address.line2 = data.get('line2', address.line2)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.zipcode = data.get('zipcode', address.zipcode)
    address.country = data.get('country', address.country)
    address.is_default = data.get('is_default', address.is_default)

    db.session.commit()
    return jsonify({'message': 'Address updated successfully'}), 200

@app.route('/api/user/address/<string:address_id>', methods=['GET'])
def get_address(address_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    # Find the address by ID and user_id (so users can't see others' addresses)
    address = UserAddress.query.filter_by(id=address_id, user_id=user.id).first()

    if not address:
        return jsonify({'error': 'Address not found'}), 404

    return jsonify({
        "id": str(address.id),
        "line1": address.line1,
        "line2": address.line2,
        "city": address.city,
        "state": address.state,
        "zipcode": address.zipcode,
        "country": address.country,
        "is_default": address.is_default
    }), 200

@app.route('/api/user/address/<string:address_id>', methods=['DELETE'])
def delete_address(address_id):
    user = get_current_user()
    address = UserAddress.query.filter_by(id=address_id, user_id=user.id).first()

    if not address:
        return jsonify({'error': 'Address not found'}), 404

    db.session.delete(address)
    db.session.commit()
    return jsonify({'message': 'Address deleted successfully'}), 200

@app.route('/api/user/settings', methods=['GET'])
def get_user_settings():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    settings = UserSettings.query.filter_by(user_id=user.id).first()
    if not settings:
        return jsonify({'error': 'Settings not found'}), 404

    return jsonify({
        "language": settings.language,
        "notifications_enabled": settings.notifications_enabled,
        "theme_color": settings.theme_color,
        "timezone": settings.timezone,
        "privacy_mode": settings.privacy_mode,
        "font_size": settings.font_size,
        "background_image": settings.background_image
    }), 200

@app.route('/api/user/settings', methods=['PUT'])
def update_user_settings():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    settings = UserSettings.query.filter_by(user_id=user.id).first()
    if not settings:
        settings = UserSettings(user_id=user.id)

    data = request.get_json()

    settings.language = data.get('language', settings.language)
    settings.notifications_enabled = data.get('notifications_enabled', settings.notifications_enabled)
    settings.theme_color = data.get('theme_color', settings.theme_color)
    settings.timezone = data.get('timezone', settings.timezone)
    settings.privacy_mode = data.get('privacy_mode', settings.privacy_mode)
    settings.font_size = data.get('font_size', settings.font_size)
    settings.background_image = data.get('background_image', settings.background_image)

    db.session.add(settings)
    db.session.commit()

    return jsonify({
        'message': 'Settings updated successfully',
        'settings': {
            "language": settings.language,
            "notifications_enabled": settings.notifications_enabled,
            "theme_color": settings.theme_color,
            "timezone": settings.timezone,
            "privacy_mode": settings.privacy_mode,
            "font_size": settings.font_size,
            "background_image": settings.background_image
        }
    }), 200

# -------------------- SERVICES --------------------
@app.route('/api/services', methods=['GET'])
def list_service_categories():
    try:
        categories = ServiceCategory.query.filter_by(is_active=True).all()
        result = []
        for cat in categories:
            result.append({
                "category_id": cat.id,
                "name": cat.name,
                "description": cat.description,
                "image_url": cat.image_url,
                "starting_price": cat.starting_price,
                "is_active": cat.is_active,
                "number_of_services": len(cat.services),
                "services": [service.to_dict() for service in cat.services]  # include child services
            })
        return jsonify({"categories": result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/<category_id>', methods=['GET'])
def get_services_in_category(category_id):
    try:
        category = ServiceCategory.query.filter_by(id=category_id, is_active=True).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404

        services_list = [
            {
                "service_id": svc.id,
                "name": svc.name,
                "description": svc.description,
                "base_price": svc.base_price,
                "image_url": svc.image_url,
                "is_active": svc.is_active
            }
            for svc in category.services if svc.is_active
        ]

        return jsonify({
            "category_id": category.id,
            "name": category.name,
            "description": category.description,
            "image_url": category.image_url,
            "starting_price": category.starting_price,
            "is_active": category.is_active,
            "number_of_services": len(services_list),
            "services": services_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/service/<service_id>', methods=['GET'])
def service_details(service_id):
    try:
        service = Service.query.filter_by(id=service_id, is_active=True).first()
        if not service:
            return jsonify({"error": "Service not found"}), 404

        return jsonify({
            "service_id": service.id,
            "name": service.name,
            "description": service.description,
            "base_price": service.base_price,
            "image_url": service.image_url,
            "is_active": service.is_active,
            "category_id": service.category_id,
            "category_name": service.category.name if service.category else None
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/service', methods=['POST'])
def create_service():
    try:
        data = request.get_json()
        required_fields = ['category_id', 'name', 'base_price']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        service = Service(
            id=generate_uuid(),
            category_id=data['category_id'],
            name=data['name'],
            description=data.get('description'),
            base_price=data['base_price'],
            image_url=data.get('image_url'),
            is_active=data.get('is_active', True)
        )
        db.session.add(service)
        db.session.commit()

        return jsonify({"message": "Service created successfully", "service": service.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/service/<service_id>', methods=['PUT'])
def update_service(service_id):
    try:
        service = Service.query.filter_by(id=service_id).first()
        if not service:
            return jsonify({"error": "Service not found"}), 404

        data = request.get_json()
        service.name = data.get("name", service.name)
        service.description = data.get("description", service.description)
        service.base_price = data.get("base_price", service.base_price)
        service.image_url = data.get("image_url", service.image_url)
        service.is_active = data.get("is_active", service.is_active)
        service.category_id = data.get("category_id", service.category_id)

        db.session.commit()

        return jsonify({"message": "Service updated successfully", "service": service.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/service/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    try:
        service = Service.query.filter_by(id=service_id).first()
        if not service:
            return jsonify({"error": "Service not found"}), 404

        db.session.delete(service)
        db.session.commit()

        return jsonify({"message": "Service deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_uuid():
    return str(uuid.uuid4())

@app.route('/api/seed/services', methods=['POST'])
def seed_services():
    try:
        # 1️⃣ Clear existing data
        Service.query.delete()
        ServiceCategory.query.delete()
        db.session.commit()

        # 2️⃣ Service Categories
        categories_data = [
            {
                "name": "Cleaning Services",
                "description": "Premium home, room, and appliance cleaning packages.",
                "image_url": "assets/premium/sweeping-mopping.png",
                "starting_price": 125
            },
            {
                "name": "Organization & Prep",
                "description": "Professional garment care, organization, and kitchen prep.",
                "image_url": "assets/premium/laundry.png",
                "starting_price": 125
            }
        ]

        categories = []
        for cat_data in categories_data:
            cat = ServiceCategory(
                id=generate_uuid(),
                name=cat_data["name"],
                description=cat_data["description"],
                image_url=cat_data["image_url"],
                starting_price=cat_data["starting_price"],
                is_active=True
            )
            db.session.add(cat)
            categories.append(cat)
        db.session.commit()

        # 3️⃣ Services per Category
        services_data = {
            "Cleaning Services": [
                {"name": "Bathroom Cleaning", "description": "Inside and rim, washbasin, visible tiles, floor sweeping and mopping.", "base_price": 150},
                {"name": "Fridge Cleaning", "description": "Interior surfaces, shelves, basic deodorising, wiping exterior.", "base_price": 150},
                {"name": "Dusting And Wiping", "description": "Dusting of furniture, shelves, corners, and light fixtures.", "base_price": 125},
                {"name": "Sweeping And Mopping", "description": "Sweeping and mopping floors, removing loose dirt.", "base_price": 125},
                {"name": "Pre-party Express Clean", "description": "90 mins living room, kitchen, bathroom, floor mop.", "base_price": 375},
                {"name": "After-party Express Clean", "description": "Spill cleanup, trash disposal, kitchen reset, mopping.", "base_price": 375},
                {"name": "Windows Cleaning", "description": "Dust removal from window mesh, wiping accessible sills.", "base_price": 125},
                {"name": "Kitchen Cleaning", "description": "Countertops, cabinet exteriors, stove top, sink.", "base_price": 150},
                {"name": "Balcony", "description": "Sweeping and mopping, wiping railings and parapet.", "base_price": 125},
                {"name": "Fan Cleaning", "description": "Dust removal from blades and motor body (Ladder required).", "base_price": 125},
                {"name": "Kitchen Cabinet", "description": "Interior and exterior wipe, reorganizing contents.", "base_price": 750}
            ],
            "Organization & Prep": [
                {"name": "Packing And Unpacking", "description": "Clothes, toys, kitchen items, labelling boxes.", "base_price": 125},
                {"name": "Utensils", "description": "Washing, drying, and placing utensils in rack.", "base_price": 125},
                {"name": "Kitchen Preparation", "description": "Chopping veggies, kneading dough, sorting ingredients.", "base_price": 125},
                {"name": "Complete Wardrobe", "description": "Emptying, interior cleaning, folding and rearranging clothes.", "base_price": 750},
                {"name": "Ironing And Folding", "description": "Neat pressing and folding for daily wear garments.", "base_price": 125},
                {"name": "Laundry", "description": "Machine wash, detergent loading, hanging to dry.", "base_price": 125}
            ]
        }

        for cat in categories:
            for svc in services_data.get(cat.name, []):
                service = Service(
                    id=generate_uuid(),
                    category_id=cat.id,
                    name=svc["name"],
                    description=svc["description"],
                    base_price=svc["base_price"],
                    image_url="assets/premium/default.png",
                    is_active=True
                )
                db.session.add(service)

        db.session.commit()
        return jsonify({"message": "Custom 17 Snappito services seeded successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/service/book', methods=['POST'])
def book_service():
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()

        # Required fields in request
        required_fields = ['service_id', 'scheduled_time', 'address']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({'error': f'Missing fields: {missing}'}), 400

        # Validate service exists
        service = Service.query.filter_by(id=data['service_id'], is_active=True).first()
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        # Optional professional assignment
        professional_id = data.get('professional_id')

        # Convert scheduled_time string to datetime
        scheduled_time = datetime.fromisoformat(data['scheduled_time'])

        # Create Booking
        booking = Booking(
            id=generate_uuid(),
            user_id=user.id,
            service_id=service.id,
            professional_id=professional_id,
            scheduled_time=scheduled_time,
            status='pending',
            address=data['address'],
            instructions=data.get('instructions'),
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(booking)
        db.session.commit()

        # ✅ Update or create ProfessionalProfile if professional_id is provided
        if professional_id:
            prof_profile = ProfessionalProfile.query.filter_by(user_id=professional_id).first()
            if not prof_profile:
                prof_profile = ProfessionalProfile(
                    user_id=professional_id,
                    experience=data.get('experience', 0),
                    skills=data.get('skills', ''),
                    documents=data.get('documents', ''),
                    certification=data.get('certification', '')
                )
                db.session.add(prof_profile)
            else:
                # Update existing profile
                prof_profile.experience = data.get('experience', prof_profile.experience)
                prof_profile.skills = data.get('skills', prof_profile.skills)
                prof_profile.documents = data.get('documents', prof_profile.documents)
                prof_profile.certification = data.get('certification', prof_profile.certification)

            db.session.commit()

        # Optional: handle payment
        if 'payment' in data:
            payment_data = data['payment']
            payment = BookingPayment(
                id=generate_uuid(),
                booking_id=booking.id,
                amount=payment_data.get('amount', service.base_price),
                method=payment_data.get('method', 'cash'),
                status=payment_data.get('status', 'pending'),
                transaction_id=payment_data.get('transaction_id'),
                paid_at=datetime.now(timezone.utc) if payment_data.get('status') == 'paid' else None
            )
            db.session.add(payment)
            db.session.commit()

        return jsonify({
            'message': 'Service booked successfully',
            'booking_id': booking.id,
            'service_id': service.id,
            'scheduled_time': booking.scheduled_time.isoformat(),
            'status': booking.status,
            'professional_id': professional_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/service/reviews/<service_id>', methods=['GET'])
def get_service_reviews(service_id):
    try:
        reviews = Feedback.query.filter_by(service_id=service_id).all()
        return jsonify([r.to_dict() for r in reviews])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/service/reviews/<service_id>', methods=['POST'])
def add_service_review(service_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    rating = data.get("rating")
    comment = data.get("comment", "")

    if not rating or not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    review = Feedback(
        id=str(uuid.uuid4()),
        user_id=user.id,
        service_id=service_id,
        rating=rating,
        comment=comment,
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review added successfully", "review": review.to_dict()}), 201


# -------------------- SEARCH & DISCOVERY --------------------
@app.route('/api/search', methods=['GET'])
def search_services():
    query = request.args.get('query') or request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'query' or 'q' is required"}), 400

    services = Service.query.filter(
        Service.is_active == True,
        Service.name.ilike(f"%{query}%") | Service.description.ilike(f"%{query}%")
    ).all()

    return jsonify({
        "query": query,
        "results": [s.to_dict() for s in services]
    }), 200

@app.route('/api/popular-services', methods=['GET'])
def popular_services():
    # Example: order by number of bookings (most booked services)
    services = Service.query.filter_by(is_active=True).all()
    
    # If you have Booking model, count bookings per service
    popular = sorted(services, key=lambda s: len(s.bookings), reverse=True)[:10]

    return jsonify({
        "popular_services": [s.to_dict() for s in popular]
    }), 200

@app.route('/api/nearby-services', methods=['GET'])
def nearby_services():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius_km = request.args.get('radius', 5, type=float)

    if lat is None or lng is None:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # Example: if Service has latitude and longitude
    services = Service.query.filter_by(is_active=True).all()
    
    def distance(svc):
        # simple placeholder: use geopy.distance for real calculation
        return ((getattr(svc, 'lat', 0) - lat)**2 + (getattr(svc, 'lng', 0) - lng)**2)**0.5
    
    nearby = [s for s in services if distance(s) <= radius_km]

    return jsonify({
        "nearby_services": [s.to_dict() for s in nearby]
    }), 200

@app.route('/api/recommendations', methods=['GET'])
def recommendations():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    # Example logic: recommend top services from user's previous categories
    # Get last 5 bookings
    recent_bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.created_at.desc()).limit(5).all()
    booked_categories = {b.service.category_id for b in recent_bookings}

    # Recommend active services from these categories
    recommended = Service.query.filter(
        Service.is_active==True,
        Service.category_id.in_(booked_categories)
    ).limit(10).all()

    return jsonify({
        "user_id": user.id,
        "recommendations": [s.to_dict() for s in recommended]
    }), 200

# -------------------- BOOKINGS --------------------
@app.route('/api/bookings', methods=['GET'])
def list_bookings():
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        
        bookings = Booking.query.filter_by(user_id=user.id).all()
        return jsonify([b.to_dict() for b in bookings])
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
@app.route('/api/booking/<booking_id>', methods=['GET'])
def booking_details(booking_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    return jsonify({
        "booking_id": booking.id,
        "service_id": booking.service_id,
        "professional_id": booking.professional_id,
        "scheduled_time": booking.scheduled_time.isoformat(),
        "status": booking.status,
        "address": booking.address,
        "instructions": booking.instructions,
        "created_at": booking.created_at.isoformat()
    }), 200

@app.route('/api/booking/cancel', methods=['POST'])
def cancel_booking():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    booking_id = data.get('booking_id')
    if not booking_id:
        return jsonify({'error': 'booking_id is required'}), 400

    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    if booking.status in ['completed', 'canceled']:
        return jsonify({'error': f'Cannot cancel a booking with status {booking.status}'}), 400

    booking.status = 'canceled'
    db.session.commit()
    return jsonify({'message': 'Booking canceled successfully'}), 200

@app.route('/api/booking/reschedule', methods=['POST'])
def reschedule_booking():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    booking_id = data.get('booking_id')
    new_time_str = data.get('new_scheduled_time')
    if not booking_id or not new_time_str:
        return jsonify({'error': 'booking_id and new_scheduled_time are required'}), 400

    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    if booking.status in ['completed', 'canceled']:
        return jsonify({'error': f'Cannot reschedule a booking with status {booking.status}'}), 400

    booking.scheduled_time = datetime.fromisoformat(new_time_str)
    db.session.commit()
    return jsonify({'message': 'Booking rescheduled successfully', 'new_scheduled_time': booking.scheduled_time.isoformat()}), 200

from flask import send_file
import io
from reportlab.pdfgen import canvas

@app.route('/api/booking/invoice/<booking_id>', methods=['GET'])
def generate_invoice(booking_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    # Generate PDF dynamically
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Invoice for Booking: {booking.id}")
    p.drawString(100, 780, f"Service ID: {booking.service_id}")
    p.drawString(100, 760, f"Scheduled Time: {booking.scheduled_time.isoformat()}")
    p.drawString(100, 740, f"Status: {booking.status}")
    p.drawString(100, 720, f"Address: {booking.address}")
    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"invoice_{booking.id}.pdf", mimetype='application/pdf')

@app.route('/api/booking/feedback', methods=['POST'])
def submit_feedback():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    booking_id = data.get('booking_id')
    rating = data.get('rating')
    comment = data.get('comment', '')

    if not booking_id or rating is None:
        return jsonify({'error': 'booking_id and rating are required'}), 400

    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    # Assume Feedback model exists with booking_id FK
    feedback = Feedback(
        id=str(uuid.uuid4()),
        user_id=user.id,
        service_id=booking.service_id,
        rating=rating,
        comment=comment,
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback submitted successfully', 'feedback_id': feedback.id}), 201

# -------------------- PAYMENT & WALLET --------------------
@app.route('/api/wallet', methods=['GET'])
def get_wallet_balance():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    wallet = Wallet.query.filter_by(user_id=user.id).first()
    balance = wallet.balance if wallet else 0.0

    return jsonify({
        "user_id": user.id,
        "balance": balance
    }), 200


@app.route('/api/wallet/add', methods=['POST'])
def add_money():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    amount = data.get('amount')
    if not amount or amount <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400

    # Get or create wallet
    wallet = Wallet.query.filter_by(user_id=user.id).first()
    if not wallet:
        wallet = Wallet(user_id=user.id)  # UUID auto-generated
        db.session.add(wallet)
        db.session.flush()  # ensures wallet.id is available

    wallet.balance += amount

    # Create transaction
    txn = Transaction(
        wallet_id=wallet.id,  # wallet UUID
        user_id=user.id,      # user UUID
        type='credit',
        amount=amount,
        description='Wallet top-up'
    )
    db.session.add(txn)
    db.session.commit()

    return jsonify({
        "message": "Money added successfully",
        "balance": wallet.balance,
        "wallet_id": str(wallet.id),
        "user_id": str(user.id)
    }), 200


@app.route('/api/payment/razorpay/create-order', methods=['POST'])
def create_razorpay_order():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    amount = data.get('amount')
    if not amount or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400

    # Razorpay amount is in Paise (1 INR = 100 Paise)
    razorpay_amount = int(amount * 100)
    
    try:
        order = razorpay_client.order.create({
            'amount': razorpay_amount,
            'currency': 'INR',
            'payment_capture': 1,
            'receipt': f'receipt_{str(uuid.uuid4())[:8]}'
        })
        return jsonify({
            'order_id': order['id'],
            'amount': amount,
            'key_id': RAZORPAY_KEY_ID
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/payment/razorpay/verify', methods=['POST'])
def verify_razorpay_payment():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')
    amount = data.get('amount')

    try:
        # Verify Payment Signature
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        # Process Wallet update after successful verification
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        if not wallet:
            wallet = Wallet(user_id=user.id)
            db.session.add(wallet)
            db.session.flush()

        wallet.balance += amount
        
        txn = Transaction(
            wallet_id=wallet.id,
            user_id=user.id,
            type='credit',
            amount=amount,
            description=f'Top-up via Razorpay ({razorpay_payment_id})'
        )
        db.session.add(txn)
        db.session.commit()

        return jsonify({'message': 'Payment verified and wallet updated', 'balance': wallet.balance}), 200
    except Exception as e:
        return jsonify({'error': 'Signature verification failed'}), 400


@app.route('/api/wallet/transactions', methods=['GET'])
def wallet_transactions():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    transactions = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.created_at.desc()).all()
    return jsonify([{
        "transaction_id": t.id,
        "type": t.type,
        "amount": t.amount,
        "description": t.description,
        "created_at": t.created_at.isoformat()
    } for t in transactions]), 200

@app.route('/api/payment/charge', methods=['POST'])
def make_payment():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    amount = data.get('amount')
    booking_id = data.get('booking_id')
    method = data.get('method')  # e.g., wallet, card, upi

    if not all([amount, booking_id, method]):
        return jsonify({'error': 'amount, booking_id, and method are required'}), 400

    # Example: deduct from wallet if method is wallet
    if method == 'wallet':
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        if not wallet or wallet.balance < amount:
            return jsonify({'error': 'Insufficient wallet balance'}), 400
        wallet.balance -= amount

    payment = Payment(
        id=str(uuid.uuid4()),
        user_id=user.id,
        booking_id=booking_id,
        amount=amount,
        method=method,
        status='paid',
        transaction_id=str(uuid.uuid4()),
        paid_at=datetime.now(timezone.utc)
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({"message": "Payment successful", "payment_id": payment.id}), 200

@app.route('/api/payment/refund', methods=['POST'])
def request_refund():
    # wallet not updated
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    payment_id = data.get('payment_id')
    reason = data.get('reason', '')

    if not payment_id:
        return jsonify({'error': 'payment_id is required'}), 400

    payment = Payment.query.filter_by(id=payment_id, user_id=user.id).first()
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    payment.status = 'refund_requested'
    payment.refund_reason = reason
    db.session.commit()

    return jsonify({"message": "Refund requested", "payment_id": payment.id}), 200

@app.route('/api/subscription', methods=['POST'])
def create_subscription():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["name", "price", "duration_days", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        # Create subscription plan
        subscription = Subscription(
            id=str(uuid.uuid4()),
            name=data["name"],
            price=float(data["price"]),
            duration_days=int(data["duration_days"]),
            description=data["description"]
        )

        db.session.add(subscription)
        db.session.commit()

        return jsonify({
            "message": "Subscription plan created successfully",
            "subscription": {
                "id": subscription.id,
                "name": subscription.name,
                "price": subscription.price,
                "duration_days": subscription.duration_days,
                "description": subscription.description
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/subscriptions/seed', methods=['POST'])
def seed_subscriptions():
    try:
        # Optional: clear existing plans
        Subscription.query.delete()
        db.session.commit()

        plans = [
            {
                "name": "UrbanEase Basic Monthly",
                "price": 199,
                "duration_days": 30,
                "description": "Priority booking and 5% discount on all services."
            },
            {
                "name": "UrbanEase Premium Monthly",
                "price": 299,
                "duration_days": 30,
                "description": "Includes 10% discount and 1 free reschedule per month."
            },
            {
                "name": "UrbanEase Family Plan",
                "price": 499,
                "duration_days": 60,
                "description": "Covers 4 family members with shared wallet and 10% off."
            },
            {
                "name": "UrbanEase Premium Quarterly",
                "price": 799,
                "duration_days": 90,
                "description": "10% discount + free cancellations."
            },
            {
                "name": "UrbanEase Pro Quarterly",
                "price": 999,
                "duration_days": 90,
                "description": "15% discount, unlimited rescheduling."
            },
            {
                "name": "UrbanEase Student Plan",
                "price": 299,
                "duration_days": 60,
                "description": "Discounted plan for students, 10% off cleaning & repairs."
            },
            {
                "name": "UrbanEase Premium Half-Yearly",
                "price": 1299,
                "duration_days": 180,
                "description": "15% discount, free pest control once in 6 months."
            },
            {
                "name": "UrbanEase Annual",
                "price": 1999,
                "duration_days": 365,
                "description": "20% discount + free service voucher worth ₹500."
            },
            {
                "name": "UrbanEase Pro Annual",
                "price": 2499,
                "duration_days": 365,
                "description": "25% discount, unlimited rescheduling, premium support."
            },
            {
                "name": "UrbanEase Lifetime",
                "price": 9999,
                "duration_days": 3650,
                "description": "Lifetime membership with 30% discount on all services."
            }
        ]

        created = []
        for plan in plans:
            subscription = Subscription(
                id=str(uuid.uuid4()),
                name=plan["name"],
                price=plan["price"],
                duration_days=plan["duration_days"],
                description=plan["description"]
            )
            db.session.add(subscription)
            created.append({
                "id": subscription.id,
                "name": subscription.name,
                "price": subscription.price,
                "duration_days": subscription.duration_days,
                "description": subscription.description
            })

        db.session.commit()

        return jsonify({
            "message": "10 subscription plans seeded successfully",
            "subscriptions": created
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    plans = Subscription.query.all()
    return jsonify([{
        "plan_id": p.id,
        "name": p.name,
        "price": p.price,
        "duration_days": p.duration_days,
        "description": p.description
    } for p in plans]), 200

@app.route('/api/subscribe', methods=['POST'])
def subscribe_plan():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    plan_id = data.get('plan_id')
    payment_method = data.get('payment_method')

    if not all([plan_id, payment_method]):
        return jsonify({'error': 'plan_id and payment_method are required'}), 400

    plan = Subscription.query.filter_by(id=plan_id).first()
    if not plan:
        return jsonify({'error': 'Subscription plan not found'}), 404

    # Example: Deduct from wallet if payment_method == wallet
    if payment_method == 'wallet':
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        if not wallet or wallet.balance < plan.price:
            return jsonify({'error': 'Insufficient wallet balance'}), 400
        wallet.balance -= plan.price

    # Create subscription record
    user_sub = UserSubscription(
        id=str(uuid.uuid4()),
        user_id=user.id,
        subscription_id=plan.id,
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc) + timedelta(days=plan.duration_days)
    )
    db.session.add(user_sub)
    db.session.commit()

    return jsonify({"message": f"Subscribed to {plan.name}", "subscription_id": user_sub.id}), 200

# -------------------- PROFESSIONALS --------------------
# 1. Get available professionals for a service
@app.route('/api/professionals/<service_id>', methods=['GET'])
def get_available_professionals(service_id):
    try:
        bookings = Booking.query.filter_by(service_id=service_id).all()
        professional_ids = [b.professional_id for b in bookings if b.professional_id]
        print(professional_ids)
        professionals = ProfessionalProfile.query.filter(
            ProfessionalProfile.user_id.in_(professional_ids)
        ).all()
        print(professionals)
        return jsonify([{
            "user_id": p.user_id,
            "experience": p.experience,
            "skills": p.skills,
            "certification": p.certification
        } for p in professionals])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2. Get professional profile
@app.route('/api/professional/<id>', methods=['GET'])
def get_professional_profile(id):
    try:
        profile = ProfessionalProfile.query.get(id)
        if not profile:
            return jsonify({"error": "Professional not found"}), 404
        return jsonify({
            "user_id": profile.user_id,
            "experience": profile.experience,
            "skills": profile.skills,
            "documents": profile.documents,
            "certification": profile.certification
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3. Rate professional
@app.route('/api/professional/rate', methods=['POST'])
def rate_professional():
    try:
        data = request.get_json()
        rating = ProfessionalRating(
            id=str(uuid.uuid4()),
            professional_id=data['professional_id'],
            user_id=data['user_id'],
            rating=data['rating'],
            review=data.get('review', '')
        )
        db.session.add(rating)
        db.session.commit()
        return jsonify({"message": "Rating submitted", "rating": rating.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4. Assign professional (Admin/Staff only)
@app.route('/api/professional/assign', methods=['POST'])
def assign_professional():
    try:
        data = request.get_json()
        booking = Booking.query.get(data['booking_id'])
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        booking.professional_id = data['professional_id']
        booking.status = "confirmed"
        db.session.commit()

        return jsonify({"message": "Professional assigned", "booking_id": booking.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 5. Check availability
@app.route('/api/professional/availability', methods=['POST'])
def check_availability():
    try:
        data = request.get_json()
        professional_id = data['professional_id']
        date_time = datetime.fromisoformat(data['scheduled_time'])

        availability = ProfessionalAvailability.query.filter(
            ProfessionalAvailability.professional_id == professional_id,
            ProfessionalAvailability.available_from <= date_time,
            ProfessionalAvailability.available_to >= date_time,
            ProfessionalAvailability.status == "available"
        ).first()

        return jsonify({"available": bool(availability)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 6. Get professional earnings (dashboard)
@app.route('/api/professional/earnings', methods=['GET'])
def get_professional_earnings():
    try:
        professional_id = request.args.get("professional_id")
        bookings = Booking.query.filter_by(
            professional_id=professional_id,
            status="completed"
        ).all()

        total_earnings = sum([b.service.base_price for b in bookings if b.service])
        completed_jobs = len(bookings)

        return jsonify({
            "professional_id": professional_id,
            "total_earnings": total_earnings,
            "completed_jobs": completed_jobs
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- MARKETING & NOTIFICATIONS --------------------
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()

        return jsonify([{
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat()
        } for n in notifications]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/seed/promos', methods=['POST'])
def seed_promos():
    try:
        promos_data = [
            {
                "title": "Festive Offer",
                "description": "Get 20% off on Home Cleaning",
                "image_url": "https://example.com/festive.jpg",
                "discount": 20,
                "valid_till": datetime(2025, 12, 31, tzinfo=timezone.utc)
            },
            {
                "title": "First Booking",
                "description": "Flat $10 off on your first booking",
                "image_url": "https://example.com/first.jpg",
                "discount": 10,
                "valid_till": datetime(2025, 11, 30, tzinfo=timezone.utc)
            }
        ]

        for p in promos_data:
            promo = Promo(**p)
            db.session.add(promo)

        db.session.commit()
        return jsonify({"message": "Promos seeded successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/promos', methods=['GET'])
def get_promos():
    try:
        promos = Promo.query.filter_by(is_active=True).all()
        return jsonify([{
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "image_url": p.image_url,
            "discount": p.discount,
            "valid_till": p.valid_till.isoformat() if p.valid_till else None
        } for p in promos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/referral', methods=['POST'])
def refer_friend():
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        friend_email = data.get('friend_email')
        referral_code = data.get('referral_code')
        if not friend_email:
            return jsonify({'error': 'friend_email required'}), 400

        referral = Referral(
            id=generate_uuid(),
            user_id=user.id,
            friend_email=friend_email,
            status='pending',
            referral_code=referral_code,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(referral)
        db.session.commit()

        return jsonify({"message": "Referral sent successfully", "referral_id": referral.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/share', methods=['POST'])
def share_app():
    try:
        data = request.get_json()
        channel = data.get("channel")  # email, whatsapp, sms
        recipient = data.get("recipient")
        message = data.get("message", "Check out UrbanEase! Download now.")

        if not channel or not recipient:
            return jsonify({"error": "channel and recipient required"}), 400

        # Simulate sharing (in production, integrate email/SMS/WhatsApp APIs)
        return jsonify({
            "message": f"App shared via {channel}",
            "recipient": recipient,
            "content": message
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -------------------- SUPPORT --------------------
# 1. Get FAQ list
@app.route('/api/help/faqs', methods=['GET'])
def get_faqs():
    try:
        faqs = FAQ.query.all()
        return jsonify([{"id": f.id, "question": f.question, "answer": f.answer} for f in faqs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2. Create Support Ticket
@app.route('/api/help/ticket', methods=['POST'])
def create_ticket():
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        ticket = SupportTicket(
            id=generate_uuid(),
            user_id=user.id,
            subject=data["subject"],
            description=data["description"],
        )
        db.session.add(ticket)
        db.session.commit()

        return jsonify({"message": "Ticket created", "ticket_id": ticket.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 3. Get Ticket Status
@app.route('/api/help/tickets', methods=['GET'])
def get_tickets():
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        tickets = SupportTicket.query.filter_by(user_id=user.id).all()
        return jsonify([{
            "id": t.id,
            "subject": t.subject,
            "status": t.status,
            "created_at": t.created_at.isoformat()
        } for t in tickets])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4. Start Support Chat
@app.route('/api/help/chat', methods=['POST'])
def start_chat():
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        chat = SupportChat(
            id=generate_uuid(),
            ticket_id=data["ticket_id"],
            user_id=user.id,
            message=data["message"]
        )
        db.session.add(chat)
        db.session.commit()

        return jsonify({"message": "Message sent", "chat_id": chat.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 5. Report Service Issue
@app.route('/api/help/report-issue', methods=['POST'])
def report_issue():
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        issue = IssueReport(
            id=generate_uuid(),
            user_id=user.id,
            service_id=data["service_id"],
            issue_type=data["issue_type"],
            description=data["description"]
        )
        db.session.add(issue)
        db.session.commit()

        return jsonify({"message": "Issue reported", "issue_id": issue.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# -------------------- UTILITIES --------------------
revoked_tokens = []
# 1. Get App Configuration
@app.route('/api/settings/app', methods=['GET'])
def get_app_settings():
    try:
        config = {
            "app_name": "UrbanEase",
            "currency": "INR",
            "support_email": "support@urbanease.com",
            "features": {
                "wallet": True,
                "referrals": True,
                "subscriptions": True
            }
        }
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2. Check App Version
@app.route('/api/version', methods=['GET'])
def check_version():
    try:
        version_info = {
            "latest_version": "1.2.0",
            "minimum_supported_version": "1.0.0",
            "force_update": False
        }
        return jsonify(version_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3. General App Feedback
@app.route('/api/feedback', methods=['POST'])
def app_feedback():
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        if not data or 'rating' not in data:
            return jsonify({'error': 'Rating is required'}), 400

        feedback = AppFeedback(
            id=generate_uuid(),
            user_id=user.id,
            rating=data['rating'],
            message=data.get('message'),
            created_at=datetime.now(timezone.utc)
        )

        db.session.add(feedback)
        db.session.commit()

        return jsonify({
            'message': 'App feedback submitted successfully',
            'feedback': feedback.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



# 4. Secure Logout
@app.route('/api/logout', methods=['POST'])
def logouts():
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        token = data.get("token")

        if not token:
            return jsonify({"error": "Token is required"}), 400

        # Ideally store revoked tokens in DB or Redis
        # revoked_tokens.add(token)

        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5001, debug=True)
