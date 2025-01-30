import requests
import pandas as pd
from typing import List, Dict, Any, Optional
from itertools import combinations

def get_clubs(term):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/clubs')
    return response


def get_club(term: int, id: str) -> Dict[str, Any]:
    """
    Retrieve information about a specific club.
    
    Args:
        term (int): The parliamentary term
        id (str): The club's unique identifier
    
    Returns:
        Response Object
    """
    return requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/clubs/{id}')

def get_club_logo(term: int, id: str) -> bytes:
    """
    Retrieve a club's logo image.
    
    Args:
        term (int): The parliamentary term
        id (str): The club's unique identifier
    
    Returns:
        bytes: Logo image content
    """
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/clubs/{id}/logo')
    return response.content

def find_minimal_coalitions(
    term: int = 10, 
    threshold: int = 231, 
    max_combinations: Optional[int] = None
) -> List[List[Dict[str, Any]]]:
    """
    Find all minimal coalitions that meet or exceed the MP threshold.
    
    A minimal coalition is the smallest set of clubs that together have at least 
    the specified number of MPs, where removing any single club would reduce 
    the total MPs below the threshold.
    
    Args:
        term (int, optional): Parliamentary term to analyze. Defaults to 10.
        threshold (int, optional): Minimum number of MPs required. Defaults to 231.
        max_combinations (int, optional): Maximum number of clubs to consider in a coalition.
    
    Returns:
        List[List[Dict[str, Any]]]: A list of minimal coalitions, 
        where each coalition is a list of club dictionaries
    """
    # Retrieve clubs data
    clubs = get_clubs(term).json()
    
    # Sort clubs by member count in descending order
    clubs.sort(key=lambda x: x['membersCount'], reverse=True)
    
    # Set max combinations if not specified
    if max_combinations is None:
        max_combinations = len(clubs)
    
    minimal_coalitions = []
    minimal_coalition_names = set()
    
    # Try different coalition sizes
    for coalition_size in range(1, min(len(clubs) + 1, max_combinations + 1)):
        for coalition in combinations(clubs, coalition_size):
            # Calculate total MPs in this coalition
            total_mps = sum(club['membersCount'] for club in coalition)
            
            # Create a hashable representation of club names
            coalition_names = frozenset(club['name'] for club in coalition)
            
            # Check if coalition meets the threshold
            if total_mps >= threshold:
                # Check if this is a minimal coalition
                is_minimal = True
                for existing_names in minimal_coalition_names:
                    if existing_names.issubset(coalition_names):
                        is_minimal = False
                        break
                
                # Verify minimal nature by checking subset removals
                if is_minimal:
                    for club in coalition:
                        subset_coalition = [c for c in coalition if c != club]
                        subset_mps = sum(c['membersCount'] for c in subset_coalition)
                        if subset_mps < threshold:
                            is_minimal = True
                            break
                        is_minimal = False
                
                # Add if minimal and unique
                if is_minimal and coalition_names not in minimal_coalition_names:
                    minimal_coalitions.append(list(coalition))
                    minimal_coalition_names.add(coalition_names)
    
    return minimal_coalitions

def print_coalitions_table(coalitions: List[List[Dict[str, Any]]]):
    """
    Print minimal coalitions as a pandas DataFrame.
    
    Args:
        coalitions (List[List[Dict[str, Any]]]): List of minimal coalitions to print
    """
    # Prepare data for DataFrame
    coalition_data = []
    for i, coalition in enumerate(coalitions, 1):
        coalition_info = {
            'Coalition': i,
            'Clubs': ', '.join(club['name'] for club in coalition),
            'Total MPs': sum(club['membersCount'] for club in coalition)
        }
        coalition_data.append(coalition_info)
    
    # Create and display DataFrame
    df = pd.DataFrame(coalition_data)
    print(df.to_string(index=False))
    
    # Optional: Detailed club breakdown
    print("\nDetailed Club Breakdown:")
    for i, coalition in enumerate(coalitions, 1):
        print(f"\nCoalition {i}:")
        club_df = pd.DataFrame([
            {'Club': club['name'], 'MPs': club['membersCount']} 
            for club in coalition
        ])
        print(club_df.to_string(index=False))

if __name__ == "__main__":
    # Find and display minimal coalitions
    coalitions = find_minimal_coalitions()
    print_coalitions_table(coalitions)
