"""
This module implements view functions for web application.
"""
import unicodedata
from . import web
from .forms import EmbedForm, ExtractForm, CapacityCalculateForm
from helpers.gc_file_helpers import gc_file_associations
from flask import flash, redirect, render_template, url_for, abort, request, \
    current_app
from ..common.app_helpers import find_coding_region, find_capacity,\
    embed_data, extract_data
from helpers.helper_functions import dna_from_json, load_sequence_choices, \
    get_chosen_file_path


@web.route('/shutdown')
def server_shutdown():
    """
    Shutdown application server.
    :return:
    """
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@web.route('/', methods=['GET'])
def index():
    # TODO: redirect to project index page.
    return render_template('index.html')


@web.route('/embed', methods=['GET', 'POST'])
def embed():
    """
    This function handles the web view for embed data form.
    User provides DNA sequence, Genetic code and input message in form of
    alphanumeric string and watermarked sequence is returned to the user.
    :return:
    """
    form = EmbedForm(gc_field=1)
    form.dna_choice_field.choices = [('#', 'Select')] + load_sequence_choices()

    if form.validate_on_submit():
        # check submitted form
        if str(form.gc_field.data) not in gc_file_associations.keys():
            return render_template('errors/400.html', message='Enter a valid '
                                                              'genetic code.')
        try:
            # Check if choices are valid
            if form.dna_choice_field.data != '#':
                # load sequence
                gc = str(form.gc_field.data)
                seq = dna_from_json(file_path=get_chosen_file_path(
                    key=form.dna_choice_field.data))['dna']
                if form.msg_field.data is None or form.msg_field.data == '':
                    flash('Please add a watermark message')
                    return render_template('embed.html', form=form)
                else:
                    msg = str(form.msg_field.data)
                print('here0')
            elif form.dna_field.data != '':
                msg = str(form.msg_field.data)
                seq = str(form.dna_field.data)
                gc = str(form.gc_field.data)
            else:
                flash("Please choose or enter some DNA sequence")
                return render_template('embed.html', form=form)
            coding_regions = find_coding_region(dna_seq=seq, frame=1, gc=gc)
            cap = find_capacity(dna_seq=seq, frame=1, gc=gc)
            if (len(msg)*8)+2 > cap:
                flash('Watermark message length exceeds storage capacity.')
                return render_template('embed.html', form=form)
            wm_seq = embed_data(dna_seq=seq, frame=1, message=msg,
                                region=coding_regions, gc=gc)
            # Present results to the user.
            return render_template('result.html',
                                   message='Watermarked DNA:\n'+wm_seq)
        except Exception as e:
            return render_template('errors/400.html', message=str(e))
    # on get request, present the form
    return render_template('embed.html', form=form)


@web.route('/extract', methods=['GET', 'POST'])
def extract():
    """
    This function handles the web view for extract data form.
    User provides watermarked DNA sequence, Genetic code and watermark
    message extracted from watermarked DNA sequence is returned to the user.
    :return:
    """
    form = ExtractForm(gc_field=1)

    if form.validate_on_submit():
        # Check submitted form.
        if str(form.gc_field.data) not in gc_file_associations.keys():
            # Make sure that valid genetic code is entered
            return render_template('errors/400.html',
                                   message='Enter a valid genetic code.')
        try:
            # extract the data.
            wm_seq = str(form.dna_field.data)
            coding_regions = find_coding_region(dna_seq=wm_seq, frame=1,
                                                gc=str(form.gc_field.data))
            e_msg = extract_data(wm_dna=wm_seq, frame=1,
                                 region=coding_regions,
                                 gc=str(form.gc_field.data))
            # Present results to the user.
            return render_template('result.html',
                                   message='Extracted message:\n'+e_msg)
        except Exception as e:
            return render_template('errors/400.html', message=str(e))
    # on GET request, present the form.
    return render_template('extract.html', form=form)


@web.route('/capacity', methods=['GET', 'POST'])
def cap_calculate():
    """
    This function handles the web view for capacity calculate form.
    User provides input DNA sequence, Genetic code and he is presented with
    the storage capacity (i.e. how long watermark can be stored in the given
    DNA).
    :return:
    """
    form = CapacityCalculateForm(gc_field=1)
    form.dna_choice_field.choices = [('#', 'Select')] + load_sequence_choices()
    if form.validate_on_submit():
        # Check submitted form
        if str(form.gc_field.data) not in gc_file_associations.keys():
            # Make sure that valid genetic code is entered
            return render_template('errors/400.html',
                                   message='Enter a valid genetic code.')
        try:
            if form.dna_choice_field.data != '#':
                seq = dna_from_json(file_path=get_chosen_file_path(
                    key=form.dna_choice_field.data))['dna']
                gc = str(form.gc_field.data)
            elif form.dna_field.data != '':
                seq = str(form.dna_field.data)
                gc = str(form.gc_field.data)
            else:
                flash("Please choose or enter some DNA sequence")
                return render_template('embed.html', form=form)
            # calculate capacity for the form.
            cap = find_capacity(dna_seq=seq, frame=1, gc=gc)
            # Present results to the user.
            return render_template(
                'result.html',
                message='Capacity: {ltr} alphabets (i.e. {bits} bits)'.format(
                                            ltr=int(cap/8), bits=cap))
        except FileNotFoundError:
            return render_template('errors/400.html',
                                   message='Requested file not found in db.')
        except Exception as e:
            return render_template('errors/400.html', message=str(e))
    # on GET request, present the form.
    return render_template('capacitycalc.html', form=form)
