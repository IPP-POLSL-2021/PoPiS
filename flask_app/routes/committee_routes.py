from flask import Blueprint, jsonify
from api_wrappers.committees import get_committees, get_committee_future_sitting, get_last_n_committee_sitting_dates, get_committee_stats, get_committee_member_details, get_committee_member_ages

committee_blueprint = Blueprint('committee_blueprint', __name__)

@committee_blueprint.route('/committees', methods=['GET'])
def get_all_committees():
    term = 10  # Default to current term
    committees = get_committees(term).json()
    return jsonify(committees), 200

@committee_blueprint.route('/committees/<code>', methods=['GET'])
def get_committee_details(code):
    term = 10  # Default to current term
    committee = get_committees(term).json()
    selected_committee = next((c for c in committee if c['code'] == code), None)
    if not selected_committee:
        return jsonify({'error': 'Committee not found'}), 404
    return jsonify(selected_committee), 200

@committee_blueprint.route('/committees/<code>/future-sitting', methods=['GET'])
def get_committee_future_sitting_route(code):
    term = 10  # Default to current term
    time = 7  # Default to one week
    sitting = get_committee_future_sitting(term, code, time)
    return jsonify({'next_sitting': sitting}), 200

@committee_blueprint.route('/committees/<code>/last-sittings/<count>', methods=['GET'])
def get_committee_last_sittings(code, count):
    term = 10  # Default to current term
    sittings = get_last_n_committee_sitting_dates(term, code, int(count))
    return jsonify({'last_sittings': sittings}), 200

@committee_blueprint.route('/committees/<code>/stats', methods=['GET'])
def get_committee_stats_route(code):
    term = 10  # Default to current term
    stats = get_committee_stats(term, code)
    return jsonify(stats), 200

@committee_blueprint.route('/committees/<code>/members/details', methods=['GET'])
def get_committee_member_details_route(code):
    term = 10  # Default to current term
    searched_info = 'edukacja'  # Default to education level
    members = get_committee_member_details({code: ['Member1', 'Member2']}, term, searched_info)
    return jsonify(members), 200

@committee_blueprint.route('/committees/<code>/members/ages', methods=['GET'])
def get_committee_member_ages_route(code):
    term = 10  # Default to current term
    searched_info = 'birthDate'  # Default to birth date
    ages_df, ages_dict = get_committee_member_ages({code: ['Member1', 'Member2']}, term, searched_info)
    return jsonify(ages_dict), 200
