from flask import Blueprint, jsonify
from api_wrappers.MP import get_MPs, get_MP, get_name, get_status, get_reason, get_club, get_district, get_other

mp_blueprint = Blueprint('mp_blueprint', __name__)

@mp_blueprint.route('/mps', methods=['GET'])
def get_all_mps():
    term = 10  # Default to current term
    mps = get_MPs(term).json()
    return jsonify(mps), 200

@mp_blueprint.route('/mps/<id>', methods=['GET'])
def get_mp_details(id):
    term = 10  # Default to current term
    mp = get_MP(term, id).json()
    return jsonify(mp), 200

@mp_blueprint.route('/mps/<id>/name', methods=['GET'])
def get_mp_name(id):
    term = 10  # Default to current term
    name = get_name(term=term, id=id)
    return jsonify({'name': name}), 200

@mp_blueprint.route('/mps/<id>/status', methods=['GET'])
def get_mp_status(id):
    term = 10  # Default to current term
    status = get_status(term=term, id=id)
    return jsonify({'status': status}), 200

@mp_blueprint.route('/mps/<id>/reason', methods=['GET'])
def get_mp_reason(id):
    term = 10  # Default to current term
    reason = get_reason(term=term, id=id)
    return jsonify({'reason': reason}), 200

@mp_blueprint.route('/mps/<id>/district', methods=['GET'])
def get_mp_district(id):
    term = 10  # Default to current term
    district_num = get_district(term=term, id=id, mode='district_num')
    district_name = get_district(term=term, id=id, mode='district_name')
    voivodeship = get_district(term=term, id=id, mode='voivodeship')
    return jsonify({
        'district_num': district_num,
        'district_name': district_name,
        'voivodeship': voivodeship
    }), 200

@mp_blueprint.route('/mps/<id>/other', methods=['GET'])
def get_mp_other_info(id):
    term = 10  # Default to current term
    birth_date = get_other(term=term, id=id, mode='birth_date')
    birth_location = get_other(term=term, id=id, mode='birth_location')
    profession = get_other(term=term, id=id, mode='profession')
    education_level = get_other(term=term, id=id, mode='education_level')
    number_of_votes = get_other(term=term, id=id, mode='number_of_votes')
    
    return jsonify({
        'birth_date': birth_date.isoformat() if isinstance(birth_date, datetime.date) else birth_date,
        'birth_location': birth_location,
        'profession': profession,
        'education_level': education_level,
        'number_of_votes': number_of_votes
    }), 200
