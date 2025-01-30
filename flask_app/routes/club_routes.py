from flask import Blueprint, jsonify
from api_wrappers.clubs import get_clubs, get_club, get_club_logo, find_minimal_coalitions, print_coalitions_table

club_blueprint = Blueprint('club_blueprint', __name__)

@club_blueprint.route('/clubs', methods=['GET'])
def get_all_clubs():
    term = 10  # Default to current term
    clubs = get_clubs(term).json()
    return jsonify(clubs), 200

@club_blueprint.route('/clubs/<id>', methods=['GET'])
def get_club_details(id):
    term = 10  # Default to current term
    club = get_club(term, id).json()
    return jsonify(club), 200

@club_blueprint.route('/clubs/<id>/logo', methods=['GET'])
def get_club_logo_route(id):
    term = 10  # Default to current term
    logo = get_club_logo(term, id)
    return logo, 200, {'Content-Type': 'image/jpeg'}

@club_blueprint.route('/clubs/coalitions', methods=['GET'])
def get_minimal_coalitions():
    coalitions = find_minimal_coalitions()
    print_coalitions_table(coalitions)
    return jsonify([{'clubs': [c['name'] for c in coalition]} for coalition in coalitions]), 200
