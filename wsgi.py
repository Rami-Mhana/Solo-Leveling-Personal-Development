from app import create_app

app = create_app()


if __name__ == '__main__':
    # Use the Flask development server for quick testing only.
    app.run(host='0.0.0.0', port=5000, debug=True)
