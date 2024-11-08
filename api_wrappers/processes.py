import requests

def get_processes(term):
    """Returns a list of legislative processes."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/processes')
    return response

def get_process(term, num):
    """Returns information about a process for a given print number."""
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/processes/{num}')
    return response

if __name__ == "__main__":
    # Example usage
    processes = get_processes(10).json()
    if processes:
        print(f"First process title: {processes[0]['title']}")
        print(f"Description: {processes[0].get('description', 'No description')}")
