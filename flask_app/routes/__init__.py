from flask import Blueprint, jsonify
from api_wrappers.MP import get_MPs, get_MP, get_name, get_status, get_reason, get_club, get_district, get_other
from api_wrappers.clubs import get_clubs, get_club, find_minimal_coalitions, print_coalitions_table
from api_wrappers.committees import get_committees, get_sittings, get_committee_future_sitting, get_last_n_committee_sitting_dates, get_committee_stats, get_committee_member_details, get_committee_member_ages
from api_wrappers.votings import get_votings, get_vote, search_votings, get_proceeding_votings, get_voting_details, get_mp_voting_details, analyze_voting_results, group_votes_by_club
from api_wrappers.interpelation import get_interpelations, get_interpelation, get_interpelation_body, get_reply_body, get_title, get_date, get_authors, get_receipent, get_replies, is_repeated_interpellation
from api_wrappers.proceedings import get_proceedings, get_proceeding
from api_wrappers.transcripts import get_statements, get_pdf_transcript, get_statement
from api_wrappers.videos import get_videos, get_today_videos, get_date_videos, get_video
import datetime

api_routes = Blueprint('api_routes', __name__)

# MP Routes
@api_routes.route('/mps', methods=['GET'])
def get_all_mps():
    term = 10  # Default to current term
    mps = get_MPs(term).json()
    return jsonify(mps), 200

@api_routes.route('/mps/<id>', methods=['GET'])
def get_mp_details(id):
    term = 10  # Default to current term
    mp = get_MP(term, id).json()
    return jsonify(mp), 200

@api_routes.route('/mps/<id>/name', methods=['GET'])
def get_mp_name(id):
    term = 10  # Default to current term
    name = get_name(term=term, id=id)
    return jsonify({'name': name}), 200

@api_routes.route('/mps/<id>/status', methods=['GET'])
def get_mp_status(id):
    term = 10  # Default to current term
    status = get_status(term=term, id=id)
    return jsonify({'status': status}), 200

@api_routes.route('/mps/<id>/reason', methods=['GET'])
def get_mp_reason(id):
    term = 10  # Default to current term
    reason = get_reason(term=term, id=id)
    return jsonify({'reason': reason}), 200

@api_routes.route('/mps/<id>/district', methods=['GET'])
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

@api_routes.route('/mps/<id>/other', methods=['GET'])
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

# Club Routes
@api_routes.route('/clubs', methods=['GET'])
def get_all_clubs():
    term = 10  # Default to current term
    clubs = get_clubs(term).json()
    return jsonify(clubs), 200

@api_routes.route('/clubs/<id>', methods=['GET'])
def get_club_details(id):
    term = 10  # Default to current term
    club = get_club(term, id).json()
    return jsonify(club), 200

@api_routes.route('/clubs/coalitions', methods=['GET'])
def get_minimal_coalitions():
    coalitions = find_minimal_coalitions()
    return jsonify([{
        'clubs': [c['name'] for c in coalition],
        'total_mps': sum(c['membersCount'] for c in coalition)
    } for coalition in coalitions]), 200

# Committee Routes
@api_routes.route('/committees', methods=['GET'])
def get_all_committees():
    term = 10  # Default to current term
    committees = get_committees(term)
    return jsonify(committees.json()), 200

@api_routes.route('/committees/<code>/sittings', methods=['GET'])
def get_committee_sittings(code):
    term = 10  # Default to current term
    sittings = get_sittings(term, code)
    return jsonify(sittings.json()), 200

@api_routes.route('/committees/<code>/future-sitting', methods=['GET'])
def get_committee_future_sitting(code):
    term = 10  # Default to current term
    sitting = get_committee_future_sitting(term, code)
    if sitting is None:
        return jsonify({'error': 'No future sittings found'}), 404
    return jsonify({'date': sitting if isinstance(sitting, list) else sitting.isoformat()}), 200

@api_routes.route('/committees/<code>/stats', methods=['GET'])
def get_committee_stats(code):
    term = 10  # Default to current term
    stats = get_committee_stats(term, code)
    return jsonify(stats), 200

# Voting Routes
@api_routes.route('/votings', methods=['GET'])
def get_all_votings():
    term = 10  # Default to current term
    votings = get_votings(term).json()
    return jsonify(votings), 200

@api_routes.route('/votings/<sitting>/<id>', methods=['GET'])
def get_voting_details(sitting, id):
    term = 10  # Default to current term
    voting = get_voting_details(term, sitting, id).json()
    return jsonify(voting), 200

@api_routes.route('/votings/search', methods=['GET'])
def search_votings():
    term = 10  # Default to current term
    votings = search_votings(term).json()
    return jsonify(votings), 200

@api_routes.route('/votings/<proceeding>', methods=['GET'])
def get_proceeding_votings(proceeding):
    term = 10  # Default to current term
    votings = get_proceeding_votings(term, proceeding).json()
    return jsonify(votings), 200

@api_routes.route('/votings/<proceeding>/<num>/analysis', methods=['GET'])
def analyze_voting(proceeding, num):
    term = 10  # Default to current term
    voting_details = get_voting_details(term, proceeding, num).json()
    analysis = analyze_voting_results(voting_details)
    return jsonify(analysis), 200

@api_routes.route('/votings/<proceeding>/<num>/club-breakdown', methods=['GET'])
def get_voting_club_breakdown(proceeding, num):
    term = 10  # Default to current term
    voting_details = get_voting_details(term, proceeding, num).json()
    breakdown = group_votes_by_club(voting_details)
    return jsonify(breakdown), 200

# Interpellation Routes
@api_routes.route('/interpellations', methods=['GET'])
def get_all_interpellations():
    term = 10  # Default to current term
    interpellations = get_interpelations(term).json()
    return jsonify(interpellations), 200

@api_routes.route('/interpellations/<num>', methods=['GET'])
def get_interpellation_details(num):
    term = 10  # Default to current term
    interpellation = get_interpelation(term, num).json()
    return jsonify(interpellation), 200

@api_routes.route('/interpellations/<num>/title', methods=['GET'])
def get_interpellation_title(num):
    term = 10  # Default to current term
    title = get_title(term, num)
    return jsonify({'title': title}), 200

@api_routes.route('/interpellations/<num>/authors', methods=['GET'])
def get_interpellation_authors(num):
    term = 10  # Default to current term
    authors = get_authors(term, num)
    return jsonify({'authors': authors}), 200

@api_routes.route('/interpellations/<num>/recipient', methods=['GET'])
def get_interpellation_recipient(num):
    term = 10  # Default to current term
    recipient = get_receipent(term, num)
    return jsonify({'recipient': recipient}), 200

@api_routes.route('/interpellations/<num>/replies', methods=['GET'])
def get_interpellation_replies(num):
    term = 10  # Default to current term
    replies = get_replies(term, num)
    return jsonify({
        'file_urls': replies[0],
        'html_replies': replies[1]
    }), 200

@api_routes.route('/interpellations/<num>/is-repeated', methods=['GET'])
def check_repeated_interpellation(num):
    term = 10  # Default to current term
    is_repeated = is_repeated_interpellation(term, num)
    return jsonify({'is_repeated': is_repeated}), 200

# Proceeding Routes
@api_routes.route('/proceedings', methods=['GET'])
def get_all_proceedings():
    term = 10  # Default to current term
    proceedings = get_proceedings(term).json()
    return jsonify(proceedings), 200

@api_routes.route('/proceedings/<id>', methods=['GET'])
def get_proceeding_details(id):
    term = 10  # Default to current term
    proceeding = get_proceeding(term, id).json()
    return jsonify(proceeding), 200

# Transcript Routes
@api_routes.route('/proceedings/<id>/<date>/transcripts', methods=['GET'])
def get_transcripts(id, date):
    term = 10  # Default to current term
    transcripts = get_statements(term, id, date).json()
    return jsonify(transcripts), 200

@api_routes.route('/proceedings/<id>/<date>/transcripts/pdf', methods=['GET'])
def get_transcript_pdf(id, date):
    term = 10  # Default to current term
    pdf_content = get_pdf_transcript(term, id, date)
    return pdf_content, 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename="transcript_{date}.pdf"'
    }

@api_routes.route('/proceedings/<id>/<date>/transcripts/<statement>', methods=['GET'])
def get_statement_details(id, date, statement):
    term = 10  # Default to current term
    statement_body = get_statement(term, id, date, statement)
    return jsonify({'statement': statement_body}), 200

# Video Routes
@api_routes.route('/videos', methods=['GET'])
def get_all_videos():
    term = 10  # Default to current term
    videos = get_videos(term).json()
    return jsonify(videos), 200

@api_routes.route('/videos/today', methods=['GET'])
def get_todays_videos():
    term = 10  # Default to current term
    videos = get_today_videos(term).json()
    return jsonify(videos), 200

@api_routes.route('/videos/<date>', methods=['GET'])
def get_videos_by_date(date):
    term = 10  # Default to current term
    videos = get_date_videos(term, date).json()
    return jsonify(videos), 200

@api_routes.route('/videos/<unid>', methods=['GET'])
def get_video_details(unid):
    term = 10  # Default to current term
    video = get_video(term, unid).json()
    return jsonify(video), 200

# Error handling
@api_routes.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@api_routes.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500
