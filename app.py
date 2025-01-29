from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import Config
from models import db, Contact
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(
        app,
        version="0.1",
        title="Contacts API",
        description="A small Flask-based API for adding contacts to a SQLite server.",
    )
    db.init_app(app)
    with app.app_context():
        db.create_all()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    contact_model = api.model(
        "Contact",
        {
            "name": fields.String(required=True, description="The name of the contact"),
            "description": fields.String(description="A description of the contact"),
            "phoneNumber": fields.String(
                required=True,
                description="The phone number of the contact, must be in international format",
            ),
        },
    )

    ns = api.namespace("Contacts", description="Add and retrieve contacts")

    @ns.route("/api")
    class ContactApi(Resource):
        @api.doc(
            description="Create a new contact",
            responses={
                201: "Contact successfully created",
                400: "Validation Error",
                500: "Internal Server Error",
            },
        )
        @api.expect(contact_model)
        def post(self):
            try:
                logger.info("New request recieved")

                # Ensure the name is a string and strip unnecessary white space
                data = request.get_json()
                name = str(data.get("name", "")).strip()
                description = str(data.get("description", "")).strip()
                phone_number = str(data.get("phoneNumber", "")).strip()

                # Validate name
                if not name:
                    logger.error("Error creating contact: Name missing")
                    return {"error": "Name is required"}, 400

                # Validate phone number
                if not phone_number:
                    logger.error("Error creating contact: Phone number missing")
                    return {"error": "Phone number is required"}, 400
                elif phone_number[0] != "+":
                    logger.error(
                        "Error creating contact: Phone number does not start with country code"
                    )
                    return {
                        "error": "Phone number must start with an international country code (+NNN)"
                    }, 400
                elif not Contact.validate_phone_number(phone_number):
                    logger.error(
                        "Error creating contact: Phone number is not in valid format"
                    )
                    return {
                        "error": "Phone number does not appear to be valid, please check and resubmit"
                    }, 400

                # Save to database
                contact = Contact(
                    name=name, description=description, phone_number=phone_number
                )
                db.session.add(contact)
                db.session.commit()

                logger.info(f"Object created: {contact.name}")
                return {
                    "id": contact.id,
                    "name": contact.name,
                    "description": contact.description,
                    "phoneNumber": contact.phone_number,
                }, 201

            except Exception as e:
                logger.error(f"Error creating contact: {e}")
                return {"error": "Internal server error"}, 500

        @api.doc(
            description="Get all contacts",
            responses={201: "Success", 500: "Internal Server Error"},
        )
        def get(self):
            try:
                logger.info("New GET contacts request recieved")
                contacts = Contact.query.all()
                contacts_data = [
                    {
                        "id": contact.id,
                        "name": contact.name,
                        "description": contact.description,
                    }
                    for contact in contacts
                ]
                return contacts_data, 200
            except Exception as e:
                logger.error(f"Error retrieving contacts: {e}")
                return {"error": "Internal server error"}, 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
