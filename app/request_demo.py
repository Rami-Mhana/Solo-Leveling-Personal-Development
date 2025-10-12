from flask import Flask, request

app = Flask(__name__)

# GET request with query parameters
@app.route('/search')
def search():
    # Access query parameters
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    return f"Searching for '{query}' in category '{category}'"

# POST request with form data
@app.route('/login', methods=['GET', 'POST']) # Allow these methods.
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return f"Welcome {username}! Login successful."
    
    return '''
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    '''

# JSON request handling
@app.route('/api/users', methods=['POST'])
def create_user():
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        return {
            'status': 'success',
            'message': f'User {name} created',
            'email': email
        }, 201
    return {'error': 'Request must be JSON'}, 400

if __name__ == '__main__':
    app.run(debug=True)