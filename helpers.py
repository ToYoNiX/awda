import requests
import base64
import io

from flask import redirect, render_template, session
from functools import wraps
from PIL import Image


def image_to_text(img_file):
    """Converts an image to a base64-encoded text string."""
    return base64.b64encode(img_file.read()).decode('utf-8')


def text_to_image(text):
    """Converts a base64 text string back to an image."""
    image_data = base64.b64decode(text)
    image = Image.open(io.BytesIO(image_data))
    return image


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def is_eligible(national_id, birthdate):
    """
    Determines if the given birthday relates appropriately to the National ID issue date.
    
    Args:
        national_id_date (str): Date the National ID was issued in YYYY-MM-DD format.
        birthdate (str): Birthday of the individual in YYYY-MM-DD format.
        
    Returns:
        bool: True if the person is eligible based on their birthday and ID issuance date, False otherwise.
    """
    date_str = birthdate.split('-')
    if date_str[0][-2:] + date_str[1].lstrip('0') + date_str[2].lstrip('0') in national_id:
        return True
    else:
        return False


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
