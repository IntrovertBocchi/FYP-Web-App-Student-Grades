# run.py

# Import the Flask app factory function from the app package
from app import create_app

# Create an app instance using the factory pattern
app = create_app()

# If this script is run directly (not imported), start the Flask development server
if __name__ == '__main__':
    app.run(debug=True) # Enable debug mode for development (auto-reload + error tracebacks)