from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

def format_tag(tag):
    """Format the tag by replacing spaces with hyphens."""
    return tag.replace(' ', '-')

def fetch_most_voted_questions(tag='', site='stackoverflow', from_date=None, page=1, pagesize=10):
    formatted_tag = format_tag(tag)
    return fetch_questions(tag=formatted_tag, site=site, from_date=from_date, page=page, pagesize=pagesize, sort='votes')

def fetch_newest_questions(tag='', site='stackoverflow', from_date=None, page=1, pagesize=10):
    formatted_tag = format_tag(tag)
    return fetch_questions(tag=formatted_tag, site=site, from_date=from_date, page=page, pagesize=pagesize, sort='creation')

def fetch_questions(tag='', site='stackoverflow', from_date=None, page=1, pagesize=10, sort='votes'):
    api_url = 'https://api.stackexchange.com/2.3/questions'

    params = {
        'order': 'desc',
        'sort': sort,
        'tagged': tag,
        'site': site,
        'pagesize': pagesize,
        'fromdate': from_date,
        'page': page,
        'filter': '!9_bDDxJY5'
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            return data['items']
    
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tag = request.form.get('tag')
        num_days = int(request.form.get('num_days'))
        num_questions = int(request.form.get('num_questions'))
    else:
        return render_template('landingPage.html',  tag="", num_days="", num_questions="")
    from_date = int((datetime.now() - timedelta(days=num_days)).timestamp())
    
    # Fetch top voted questions
    most_voted_questions = fetch_most_voted_questions(tag=tag, from_date=from_date, pagesize=num_questions)
    
    # Fetch newest questions
    newest_questions = fetch_newest_questions(tag=tag, from_date=from_date, pagesize=num_questions)

    return render_template('index.html', most_voted_questions=most_voted_questions, newest_questions=newest_questions,
                           tag=tag, num_days=num_days, num_questions=num_questions)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
