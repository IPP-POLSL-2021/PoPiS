import csv
import os
from datetime import datetime

from api_wrappers.clubs import get_clubs
from api_wrappers.committees import get_committees
from api_wrappers.groups import get_groups
from api_wrappers.interpelation import get_interpelations
from api_wrappers.MP import get_MPs
from api_wrappers.prints import get_prints
from api_wrappers.proceedings import get_proceedings, get_proceeding
from api_wrappers.processes import get_processes
from api_wrappers.terms import get_terms
from api_wrappers.transcripts import get_statements
from api_wrappers.videos import get_videos
from api_wrappers.votings import get_votings
from api_wrappers.written_questions import get_written_questions

def check_data_existence(term):
    print(f"Term {term}")
    """
    Check data existence for a given term across different API endpoints.
    Returns a dictionary with existence status for each endpoint.
    """
    results = {
        'term': term,
        'clubs': False,
        'committees': False,
        'groups': False,
        'interpelations': False,
        'mps': False,
        'prints': False,
        'proceedings': False,
        'processes': False,
        'transcripts': False,
        'videos': False,
        'votings': False,
        'written_questions': False
    }

    try:
        print("clubs")
        # Clubs
        clubs_data = get_clubs(term).json()
        results['clubs'] = len(clubs_data)
        print("committees")
        # Committees
        committees_data = get_committees(term)
        results['committees'] = len(committees_data)
        print("groups")
        # Groups
        groups_data = get_groups(term).json()
        results['groups'] = len(groups_data)
        print("interpelations")
        # Interpelations
        interpelations_data = get_interpelations(term).json()
        results['interpelations'] = len(interpelations_data)
        print("mps")
        # MPs
        mp_data = get_MPs(term).json()
        results['mps'] = len(mp_data)
        print("prints")
        # Prints
        prints_data = get_prints(term).json()
        results['prints'] = len(prints_data)
        print("proceedings")
        # Proceedings
        proceedings_data = get_proceedings(term)
        if proceedings_data:
            results['proceedings'] = len(proceedings_data.json())
        print("processes")
        # Processes
        processes_data = get_processes(term)
        if processes_data:
            results['processes'] = len(processes_data.json())
    
        print("transcripts")
        #Transcripts
        if proceedings_data:
            results['transcripts'] = "TODO"
        #    date = get_proceeding(term,1).json()[0]['dates'][0]
        #    transcripts_data = get_statements(term, 1, date)
        #    if transcripts_data:
        #        results['transcripts'] = len(transcripts_data.json())
        print("videos")
        # Videos
        videos_data = get_videos(term)
        if videos_data:
            results['videos'] = len(videos_data.json())
        print("votings")
        # Votings
        votings_data = get_votings(term)
        if votings_data:
            results['votings'] = len(votings_data.json())
        print("written_questions")
        # Written Questions
        written_questions_data = get_written_questions(term)
        if written_questions_data:
            results['written_questions'] = len(written_questions_data.json())

    except Exception as e:
        print(f"Error checking term {term}: {e}")

    return results

def generate_data_existence_report():
    """
    Generate a CSV report of data existence across terms.
    """
    # Get available terms
    terms_data = get_terms().json()
    terms = sorted([term['num'] for term in terms_data])

    # Prepare output directory
    output_dir = 'reports'
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f'data_existence_report_{timestamp}.csv')

    # Write report
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['term', 'clubs', 'committees', 'groups', 'interpelations', 
                      'mps', 'prints', 'proceedings', 'processes', 
                      'transcripts', 'videos', 'votings', 'written_questions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for term in terms:
            result = check_data_existence(term)
            writer.writerow(result)

    print(f"Data existence report generated: {filename}")

if __name__ == "__main__":
    generate_data_existence_report()
