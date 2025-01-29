from flask import request
from flask_restful import Resource
from models import db, Contact
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContactApi (Resource):
    def post(self):
        try:
            # Ensure the name is a string and strip unnecessary white space
            data = request.get_json()
            name = str(data.get('name', '')).strip()
            description = str(data.get('description', '')).strip()
            phone_number = str(data.get('phoneNumber', '')).strip()

            if not name:
                return {'error': 'Name is required'}, 400
            if not phone_number:
                return {'error': 'Phone number is required'}, 400
            if phone_number[0] != '+':
                return {'error': 'Phone number must start with an international country code (+NNN)'}, 400
            if not Contact.validate_phone_number(phone_number):
                return {'error': 'Phone number does not appear to be valid, please check and resubmit'}, 400
            
            # Save to database
            contact = Contact(name=name, description=description, phone_number=phone_number)
            db.session.add(contact)
            db.session.commit()
            
            logger.info(f"Object created: {contact.name}")
            return {'id': contact.id, 'name': contact.name, 'description': contact.description, 'phoneNumber': contact.phone_number}, 201

        except Exception as e:
            logger.error(f"Error creating object: {e}")
            return {'error': 'Internal server error'}, 500
        
    def get(self):
        try:
            contacts = Contact.query.all()
            contacts_data = [{'id': contact.id, 'name': contact.name, 'description': contact.description} for contact in contacts]
            return contacts_data, 200
        except Exception as e:
            logger.error(f"Error retrieving objects: {e}")
            return {'error': 'Internal server error'}, 500