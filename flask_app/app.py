from flask import Flask, Blueprint, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register Blueprints
from routes.mp_routes import mp_blueprint
from routes.club_routes import club_blueprint
from routes.committee_routes import committee_blueprint

app.register_blueprint(mp_blueprint)
app.register_blueprint(club_blueprint)
app.register_blueprint(committee_blueprint)

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
