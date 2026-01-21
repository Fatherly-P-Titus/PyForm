import sys
import logging

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from PIL import Image
import uuid

from config import Config
from models import db, User


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)


app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
app.config.from_object(Config)
CORS(app)
db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_nigerian_phone(phone):
    try:
        parsed = phonenumbers.parse(phone, "NG")
        return phonenumbers.is_valid_number(parsed)
    except:
        return False

@app.route('/')
def home():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        data = request.form
        
        # Validate required fields
        required_fields = ['first_name', 'surname', 'email', 
                          'phone_number', 'home_address', 'gender', 'date_of_birth']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Validate email
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email address'}), 400
        
        # Validate Nigerian phone number
        if not validate_nigerian_phone(data['phone_number']):
            return jsonify({'error': 'Invalid Nigerian phone number. Format: +2348012345678 or 08012345678'}), 400
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                # Generate unique filename
                ext = file.filename.rsplit('.', 1)[1].lower()
                image_filename = f"{uuid.uuid4()}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                
                # Resize and save image
                img = Image.open(file)
                img.thumbnail((500, 500))
                img.save(filepath)
        
        # Parse date
        try:
            dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        new_user = User(
            image_filename=image_filename,
            first_name=data['first_name'],
            middle_name=data.get('middle_name'),
            surname=data['surname'],
            last_name=data.get('last_name'),
            email=data['email'],
            phone_number=data['phone_number'],
            home_address=data['home_address'],
            gender=data['gender'],
            date_of_birth=dob,
            facebook_username=data.get('facebook_username'),
            twitter_username=data.get('twitter_username'),
            instagram_username=data.get('instagram_username')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful!',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/debug/test')
def debug_test():
    """
    Test endpoint for debugging
    """
    # Set a breakpoint here by clicking left of line number
    debug_data = {
        'app_debug': app.debug,
        'environment': app.config.get('ENV'),
        'database_path': app.config['SQLALCHEMY_DATABASE_URI'],
        'upload_folder': app.config['UPLOAD_FOLDER']
    }
    
    # This will appear in VS Code debug console when breakpoint hits
    print("Debug endpoint accessed")
    app.logger.debug(f"Debug data: {debug_data}")
    
    return jsonify({
        'status': 'debug_mode_active',
        'data': debug_data,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logging.info("Database tables created")
    
    # Development settings
    app.run(
        debug=True,  # Enable debug mode
        host='0.0.0.0',
        port=5000,
        use_reloader=True,  # Auto-reload on code changes
        use_debugger=True,  # Enable Flask's debugger
        threaded=True
    )



