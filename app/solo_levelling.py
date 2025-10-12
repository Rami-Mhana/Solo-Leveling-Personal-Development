from flask import Flask, render_template, request, make_response
import os

# Creating flask application
app = Flask(__name__, template_folder='templates')  # Remove template_folder parameter

# We need to add an endpoint to the application, or routing process.

# Each function is an endpoint.
# Simple default routing | Indexing routing
@app.route('/') # Root
def index():
    response = make_response("Null")
    response.status_code = 301
    return "RM WAS HERE"

# Core feature
@app.route('/register')
def register():
    response = make_response("Join the adventure! Register here.")
    response.status_code = 200
    return response

@app.route('/other')
def other_page():
    some_text = "This is other page" 
    return render_template('other.html', text=some_text)

def search_form():
    return render_template

@app.route('/search')
def search():
    # Get search parameters from URL
    search_term = request.args.get('q', '')
    filter_by = request.args.get('filter', 'all')
    sort_by = request.args.get('sort', 'relevance')
    
    # Use in your search logic
    results = perform_search(search_term, filter_by, sort_by)
    return f"Found {len(results)} results for '{search_term}'"

def perform_search(term, filter_by, sort_by):
    items = [
        {"name": "Flask tutorial", "category": "web"},
        {"name": "Python basics", "category": "programming"},
        {"name": "Django guide", "category": "web"}
    ]
    
    # Filter logic
    filtered = [item for item in items if term.lower() in item["name"].lower()]
    if filter_by != "all":
        filtered = [item for item in filtered if item["category"] == filter_by]
    
    return filtered
    
# The player status page - FIXED ROUTE
@app.route('/player_info') # Core feature
def player_status():
    return render_template('player_status.html')  # Make sure this file exists in templates/

# Core feature
@app.route('/login') 
def login():
    response = make_response("This is Rami")
    response.status_code = 222
    response.headers['content-type'] = 'Apprentice -> Master'
    return response

# Core feature
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    name = "rami"
    return render_template('dashboard.html', name_player=name)

@app.route('/greet/<name>')
def greet(name):
    return f"hello {name}"

@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f"{greeting}, {name}"
    else:
        return "Fuck it"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)