from flask import request
from flask_restx import Resource
from models import db, Contact
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContactApi(Resource):
    def post(self):
        try:
            logger.info('New request recieved')

            # Ensure the name is a string and strip unnecessary white space
            data = request.get_json()
            name = str(data.get('name', '')).strip()
            description = str(data.get('description', '')).strip()
            phone_number = str(data.get('phoneNumber', '')).strip()

            # Validate name
            if not name:
                logger.error(f'Error creating contact: Name missing')
                return {'error': 'Name is required'}, 400
            
            # Validate phone number
            if not phone_number:
                logger.error(f'Error creating contact: Phone number missing')
                return {'error': 'Phone number is required'}, 400
            elif phone_number[0] != '+':
                logger.error(f'Error creating contact: Phone number does not start with country code')
                return {'error': 'Phone number must start with an international country code (+NNN)'}, 400
            elif not Contact.validate_phone_number(phone_number):
                logger.error(f'Error creating contact: Phone number is not in valid format')
                return {'error': 'Phone number does not appear to be valid, please check and resubmit'}, 400
            
            # Save to database
            contact = Contact(name=name, description=description, phone_number=phone_number)
            db.session.add(contact)
            db.session.commit()
            
            logger.info(f'Object created: {contact.name}')
            return {'id': contact.id, 'name': contact.name, 'description': contact.description, 'phoneNumber': contact.phone_number}, 201

        except Exception as e:
            logger.error(f'Error creating contact: {e}')
            return {'error': 'Internal server error'}, 500
        
    def get(self):
        try:
            logger.info('New GET contacts request recieved')
            contacts = Contact.query.all()
            contacts_data = [{'id': contact.id, 'name': contact.name, 'description': contact.description} for contact in contacts]
            return contacts_data, 200
        except Exception as e:
            logger.error(f'Error retrieving contacts: {e}')
            return {'error': 'Internal server error'}, 500