from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, HiddenField
from wtforms.validators import InputRequired, Optional, NumberRange, URL


class AddCupcake(FlaskForm):

    flavor = StringField("Flavor",
                       validators=[InputRequired()])
    size = SelectField("Size",
                       choices=[('Small', 'Small'),  ('Medium', 'Medium'),  ('Large', 'Large')])
    rating = IntegerField("Rating",
                       validators=[InputRequired(), NumberRange(min=0, max=5, message="Pick a rating 0-5")])
    image = StringField("Image",
                       validators=[Optional(), URL(require_tld=True, message="Must be valid URL")])

