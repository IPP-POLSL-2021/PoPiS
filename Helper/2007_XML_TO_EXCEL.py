import csv 
import xml.etree.ElementTree as ET 

def get_all_committee_names(root):
    committee_names = set()
    ns = root.tag.split('}')[0] + '}'
    
    # Scan all districts for committee names
    districts = root[0][1:]  # Skip first element which is header
    for district in districts:
        for elem in district:
            if elem.tag == f"{ns}listy":
                for child in elem:
                    if child.tag == f"{ns}kwy-nazwa":
                        committee_names.add(child.text)
    
    return sorted(list(committee_names))  # Sort for consistent ordering

def parseXML(xmlfile):
    try:
        # create element tree object
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        okregi = []
        ns = root.tag.split('}')[0] + '}'
        
        # Get all unique committee names from all districts
        committee_names = get_all_committee_names(root)
        print(f"Found {len(committee_names)} committees")
        
        # Process each district (skip first as it's header)
        districts = root[0][1:]  # Skip first element which is header
        
        for district in districts:
            try:
                okrag = []
                
                # Find valid votes element (g-wazne)
                for elem in district:
                    if elem.tag == f"{ns}wyn_jns":
                        for child in elem:
                            if child.tag == f"{ns}g-wazne":
                                valid_votes = child.text
                                okrag.append(valid_votes)
                                break
                        break
                
                # Get committee votes in the same order as names
                committee_votes = ['0'] * len(committee_names)  # Initialize with zeros
                for elem in district:
                    if elem.tag == f"{ns}listy":
                        committee_name = None
                        votes = None
                        
                        for child in elem:
                            if child.tag == f"{ns}kwy-nazwa":
                                committee_name = child.text
                            elif child.tag == f"{ns}lst-gz":
                                votes = child.text
                                
                        if committee_name and votes:
                            try:
                                idx = committee_names.index(committee_name)
                                committee_votes[idx] = votes
                            except ValueError:
                                print(f"Error: Committee name not found in master list: {committee_name}")
                
                if valid_votes:  # Only add district if we found valid votes
                    okrag.extend(committee_votes)
                    okregi.append(okrag)
                    
            except (IndexError, AttributeError) as e:
                print(f"Error processing district: {e}")
                continue
        
        return okregi, committee_names
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return [], []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [], []

def savetoCSV(results, committee_names, filename): 
    if not results:
        print("No results to save")
        return

    # Create fields with actual committee names
    fields = ['Głosy Ważne'] + committee_names

    try:
        # writing to csv file 
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(results) 
        
        print(f"CSV file '{filename}' created successfully with {len(results)} districts and {len(committee_names)} committees.")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def main(): 
    # parse xml file 
    wybory, committee_names = parseXML('2007.xml') 
    
    if wybory:
        print(f"\nProcessed {len(wybory)} districts successfully")
        print("Committee names:", committee_names)
        print("First district data (sample):", wybory[0] if wybory else "No data")
        savetoCSV(wybory, committee_names, '2007.csv')
    else:
        print("No data was processed successfully")
    
if __name__ == "__main__": 
    main()
