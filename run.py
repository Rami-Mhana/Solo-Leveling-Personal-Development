from app import create_app

app = create_app()

if __name__ == '__main__': # What is this? This line checks if the script is being run directly (not imported as a module). 
    # Use the Flask development server for quick testing only.
    app.run(host='0.0.0.0', port=5000, debug=True)