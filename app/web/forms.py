"""
This module contains the declarations for the Forms used in web application.
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField
from wtforms.validators import number_range, input_required


class EmbedForm(FlaskForm):
    """
    Form for extraction of insertion of watermark in DNA sequence
    """
    dna_field = StringField('DNA string', validators=[input_required()])
    gc_field = IntegerField('Genetic code', validators=[input_required(),
                                                        number_range(1, 42)])
    msg_field = StringField('Enter message', validators=[input_required()])
    submit = SubmitField('Embed')


class ExtractForm(FlaskForm):
    """
    Form for extraction of Data from DNA sequence
    """
    dna_field = StringField('Watermarked DNA', validators=[input_required()])
    gc_field = IntegerField('Genetic code', validators=[input_required(),
                                                        number_range(1, 42)])

    submit = SubmitField('Extract')


class CapacityCalculateForm(FlaskForm):
    """
    Form for calculating capacity for given DNA sequence
    """
    dna_field = StringField('DNA Sequence', validators=[input_required()])
    gc_field = IntegerField('Genetic code', validators=[input_required(),
                                                        number_range(1, 42)])

    submit = SubmitField('Calculate')
