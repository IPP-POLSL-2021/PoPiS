"""
API Wrappers for Polish Sejm (Parliament) API

This package provides a collection of modules to interact with the Sejm API, 
allowing easy access to various parliamentary data such as:
- Members of Parliament (MPs)
- Clubs and Committees
- Votings and Proceedings
- Interpellations and Written Questions
- And more

Usage Example:
```python
from api_wrappers import MP, clubs, committees

# Get information about an MP
mp_details = MP.get_MP(10, 241)

# Find minimal coalitions
coalition_details = clubs.find_minimal_coalitions()

# Get committee statistics
committee_stats = committees.get_committee_stats(10)
```

Each module corresponds to a specific type of parliamentary data and provides 
functions to retrieve and process information from the Sejm API.

Modules:
- MP: Member of Parliament information
- clubs: Parliamentary club details
- committees: Committee information
- groups: Bilateral groups
- interpelation: Interpellation details
- prints: Parliamentary prints
- proceedings: Parliamentary proceedings
- processes: Legislative processes
- terms: Parliamentary terms
- transcripts: Proceeding transcripts
- videos: Video transmissions
- votings: Voting information
- written_questions: Written parliamentary questions
"""

# Import all modules to make them easily accessible
from . import (
    MP,
    clubs,
    committees,
    groups,
    interpelation,
    prints,
    proceedings,
    processes,
    terms,
    transcripts,
    videos,
    votings,
    written_questions
)

# Optional: Define what gets imported with `from api_wrappers import *`
__all__ = [
    'MP',
    'clubs',
    'committees',
    'groups',
    'interpelation',
    'prints',
    'proceedings',
    'processes',
    'terms',
    'transcripts',
    'videos',
    'votings',
    'written_questions'
]
