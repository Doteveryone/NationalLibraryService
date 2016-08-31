from flask import request, render_template, send_from_directory, abort, redirect, url_for, flash
from nls import app, models, forms
from mongoengine import DoesNotExist
import openlibrary
import random
import requests
import mechanize
from bs4 import BeautifulSoup

#very hacky film archive search
def archive_search(search_term):

    results = []

    url = 'http://collections-search.bfi.org.uk/web/search/simple'

    try:
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        br.open(url)
        br.form = list(br.forms())[0]
        br.form["Fields[0].Value"] = search_term
        response = br.submit()

        soup = BeautifulSoup(response.read(), "html.parser")

        for result in  soup.select('a.content.ais-float-dynamic'):
            title = result.select('span')[0].text
            link_split = result['href'].split('/')
            film_id = link_split[len(link_split) - 1]
            description = result.select('p')[0]
            results.append({'title': title, 'description': description, 'film_id': film_id})
    except:
        pass

    return results

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/space', methods=['GET', 'POST'])
def space():
    if request.method == 'POST':
        return redirect(url_for('space_library'))
    return render_template('space.html')

@app.route('/space/library')
def space_library():
    #Get libraries it can be borrowed from (random 3 libraries)
    libraries = models.Library.objects()
    libraries = [ libraries[i] for i in sorted(random.sample(xrange(len(libraries)), 3)) ]

    return render_template('space_library.html', libraries=libraries)

@app.route('/space/choose')
def space_choose():
    return render_template('space_choose.html')

@app.route('/space/confirmed')
def space_confirmed():
    return render_template('space_confirmed.html')

@app.route('/meeting')
def meeting():
    return render_template('meeting.html')

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

@app.route('/libraries')
def libraries():
    libraries = models.Library.objects()
    return render_template('libraries.html', libraries=libraries)

@app.route('/libraries/<slug>')
def library(slug):
    try:
        library = models.Library.objects.get(slug=slug)
    except (DoesNotExist):
        abort(404)
    return render_template('library.html', library=library, menu_item='home')

@app.route('/libraries/<slug>/events')
def library_events(slug):
    try:
        library = models.Library.objects.get(slug=slug)
        events = models.Event.objects(library=library).order_by('occurs_at')
    except (DoesNotExist):
        abort(404)
    return render_template('library_events.html', library=library, events=events, menu_item='events')

@app.route('/libraries/<slug>/pages')
def library_pages(slug):
    try:
        library = models.Library.objects.get(slug=slug)
    except (DoesNotExist):
        abort(404)
    return render_template('library_pages.html', library=library, menu_item='pages')

@app.route('/libraries/<slug>/pages/community-groups')
def library_page(slug):
    try:
        library = models.Library.objects.get(slug=slug)
    except (DoesNotExist):
        abort(404)
    return render_template('library_page.html', library=library, menu_item='pages')

@app.route('/libraries/<slug>/pledge', methods=['GET', 'POST'])
def library_pledge(slug):
    form = forms.PledgeForm()
    try:
        library = models.Library.objects.get(slug=slug)
    except (DoesNotExist):
        abort(404)

    done = False
    if request.method == 'POST':
        done = True

    return render_template('library_pledge.html', library=library, menu_item='notices', form=form, done=done)

@app.route('/libraries/<slug>/archive')
def library_archive(slug):
    try:
        library = models.Library.objects.get(slug=slug)
    except (DoesNotExist):
        abort(404)
    return render_template('library_archive.html', library=library, menu_item='archive')

@app.route('/events/<id>')
def event(id):
    try:
        event = models.Event.objects.get(id=id)
    except (DoesNotExist):
        abort(404)
    return render_template('event.html', event=event)

@app.route('/archive/<film_id>')
def archive(film_id):
    base_url = 'http://collections-search.bfi.org.uk/web/Details/ChoiceFilmWorks/'
    response = requests.get("%s/%s" % (base_url, film_id))
    soup = BeautifulSoup(response.text, "html.parser")
    details = soup.select('ul.content')[0]
    keys = details.select('div.label')
    values = details.select('div.value')

    title = values[1].text
    meta_data = []
    index = 0
    for value in values:
        meta_data.append((keys[index].text, values[index].text))    
        index += 1

    #Get libraries it can be watched from (random 3 libraries)
    libraries = models.Library.objects()
    libraries_with_archive = [ libraries[i] for i in sorted(random.sample(xrange(len(libraries)), 3)) ]

    #get some related books
    title_split = title.split(' ')
    books = []
    if len(title_split) >= 3:
        open_library = openlibrary.BookSearch()
        all_books = open_library.get_by_title("%s %s %s" % (title_split[0], title_split[1], title_split[2]))

        for i in range(0, 3):
            print i
            try:
                books.append(all_books[i])
            except:
                pass


    return render_template('archive.html', title=title, meta_data=meta_data, libraries_with_archive=libraries_with_archive, books=books)


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

        #events
        results['events'] = models.Event.objects.search_text(query).order_by('$text_score')

        #archive
        results['archive'] = archive_search(query)
        print results['archive']

    return render_template('search.html', query=query, results=results)

@app.route('/analytics/collect', methods=['GET', 'POST'])
def analytics_collect():
    done = False
    if request.method == 'POST':
        done = True
    return render_template('analytics-collect.html', done=done)    

@app.route('/local')
def local_index():
    return render_template('local-index.html')

@app.route('/local/culture-trail')
def local_culture_trail():
    return render_template('local-culture-trail.html')

@app.route('/local/search')
def local_search():
    return render_template('local-search.html')

@app.route('/email-example')
def email_example():
    return render_template('email-example.html')        