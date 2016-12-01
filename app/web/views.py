"""
This module implements view functions for web application.
"""
from . import web
from .forms import EmbedForm, ExtractForm, CapacityCalculateForm
from helpers.gc_file_helpers import gc_file_associations
from flask import flash, redirect, render_template, url_for, abort, request, \
    current_app
from app.common.helpers import find_coding_region, find_capacity,\
    embed_data, extract_data


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
    form = EmbedForm(gc_field=1)

    if form.validate_on_submit():
        if str(form.gc_field.data) not in gc_file_associations.keys():
            return render_template('errors/400.html', message='Enter a valid '
                                                              'genetic code.')
        try:
            msg = form.msg_field.data
            seq = form.dna_field.data
            coding_regions = find_coding_region(dna_seq=seq, frame=1,
                                                gc=form.gc_field.data)
            cap = find_capacity(dna_seq=seq, frame=1,
                                gc=form.gc_field.data)
            if (len(msg)*8) > cap:
                return render_template('errors/400.html',
                                       message='watermark length exceeds '
                                               'capacity.')
            wm_seq = embed_data(dna_seq=seq, frame=1, message=msg,
                                region=coding_regions, gc=form.gc_field.data)
            return render_template('result.html',
                                   message='Watermarked DNA:\n'+wm_seq)
        except Exception as e:
            return render_template('errors/400.html', message=str(e))
    return render_template('embed.html', form=form)


@web.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ExtractForm(gc_field=1)

    if form.validate_on_submit():
        if str(form.gc_field.data) not in gc_file_associations.keys():
            return render_template('errors/400.html', message='Enter a valid '
                                                              'genetic code.')
        try:
            wm_seq = form.dna_field.data
            coding_regions = find_coding_region(dna_seq=wm_seq, frame=1,
                                                gc=form.gc_field.data)
            e_msg = extract_data(wm_dna=wm_seq, frame=1,
                                 region=coding_regions, gc=form.gc_field.data)
            return render_template('result.html',
                                   message='Extracted message:\n'+e_msg)
        except Exception as e:
            return render_template('errors/400.html', message=str(e))
    return render_template('extract.html', form=form)


@web.route('/capacity', methods=['GET', 'POST'])
def cap_calculate():
    form = CapacityCalculateForm(gc_field=1)
    if form.validate_on_submit():
        if str(form.gc_field.data) not in gc_file_associations.keys():
            return render_template('errors/400.html', message='Enter a valid '
                                                              'genetic code.')
        try:
            seq = form.dna_field.data
            cap = find_capacity(dna_seq=seq, frame=1, )
            return render_template('result.html',
                                   message='Capacity: {ltr} alphabets (i.e. '
                                           '{bits} bits)'.format(
                                            ltr=int(cap/8), bits=cap))
        except Exception as e:
            return render_template('errors/400.html', message=str(e))
    return render_template('capacitycalc.html', form=form)
