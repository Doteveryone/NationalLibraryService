from flask import request, render_template, send_from_directory, abort, redirect, url_for, flash
from nls import app, models, forms
from mongoengine import DoesNotExist
import openlibrary
import random

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/space')
def space():
    return render_template('space.html')    

@app.route('/libraries')
def libraries():
    libraries = models.Library.objects()
    return render_template('libraries.html', libraries=libraries)

@app.route('/books/<isbn>')
def book(isbn):
    # open_library = openlibrary.BookSearch()
    # results['books'] = open_library.get_by_title(query)

    #get the book
    search = openlibrary.Search()
    search.uri = openlibrary.SEARCH_URI
    results = search.get(**{'isbn': isbn})
    if len(results['docs']) > 0:
        book = results['docs'][0]
        print results['docs'][0]
    else:
        book = None

    #Get libraries it can be borrowed from (random 3 libraries)
    libraries = models.Library.objects()
    libraries_with_book = [ libraries[i] for i in sorted(random.sample(xrange(len(libraries)), 3)) ]

    return render_template('book.html', book=book, libraries_with_book=libraries_with_book)

@app.route('/libraries/<slug>')
def library(slug):
    try:
        library = models.Library.objects.get(slug=slug)
    except (DoesNotExist):
        abort(404)
    return render_template('library.html', library=library)

@app.route('/register')
def register_index():
    return render_template('register-index.html')

@app.route('/register/<id>')
def register_entry(id):
    try:
        library = models.Library.objects.get(id=id)
    except (DoesNotExist):
        abort(404)
    return render_template('register-entry.html', library=library)

@app.route('/register/search')
def register_search():
    query = request.args.get('q', False)
    libraries = []
    if query == '':
        query = False

    if query:
        libraries = models.Library.objects.search_text(query).order_by('$text_score')

    return render_template('register-search.html', query=query, libraries=libraries)

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/ask')
def ask():
    return render_template('ask.html', hide_footer=True)

@app.route('/reading-groups/start')
def reading_group_start():
    return render_template('reading-group-start.html')

@app.route('/search')
def search():
    query = request.args.get('q', False)
    results = {}
    if query == '':
        query = False

    if query:
        #libraries
        results['libraries'] = models.Library.objects.search_text(query).order_by('$text_score')

        #books
        open_library = openlibrary.BookSearch()
        results['books'] = open_library.get_by_title(query)

    return render_template('search.html', query=query, results=results)

@app.route('/analytics/collect', methods=['GET', 'POST'])
def analytics_collect():
    done = False
    if request.method == 'POST':
        done = True
    return render_template('analytics-collect.html', done=done)    