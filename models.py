from flask_sqlalchemy import SQLAlchemy
import re

db = SQLAlchemy()


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    phone_number = db.Column(db.String(), nullable=False)

    def validate_phone_number(phone_num: str) -> bool:
        """This checks that a number matches the international telephone number standard ITU-T E.164 and returns wherther or not it is a valid phone number.
        For more information, check https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s03.html

        Args:
            phone_num (str): The phone number to be tested.

        Returns:
            bool: Whether or not the provided phone number is valid.
        """
        regex = r"^\+(?:[0-9] ?){6,14}[0-9]$"

        return re.match(regex, phone_num)

    def __repr__(self):
        return f"<Item {self.name}>"
