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
    """Converts a base64 text string back to an image URL."""
    image_data = base64.b64decode(text)
    image = Image.open(io.BytesIO(image_data))

    # Convert image to base64 for HTML embedding
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # Use PNG or JPEG
    encoded_image = base64.b64encode(buffered.getvalue()).decode()

    return f"data:image/png;base64,{encoded_image}"

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
    Determines if the given birthdate matches the encoded date in the National ID.

    Args:
        national_id (str): 14-digit National ID.
        birthdate (str): Birthday of the individual in YYYY-MM-DD format.

    Returns:
        bool: True if the birthdate matches the National ID, False otherwise.
    """
    if len(national_id) != 14 or not national_id.isdigit():
        return False  # Invalid national ID format
    
    date_str = birthdate.split('-')
    YYMMDD = date_str[0][-2:] + date_str[1].zfill(2) + date_str[2].zfill(2)
    
    # The birthdate is encoded in positions 2-7 (index 1-6) in the national ID
    return national_id[1:7] == YYMMDD


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
