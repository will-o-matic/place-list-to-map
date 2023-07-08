import csv

# Function to extract street address from full address
def get_street_address(full_address):
    return full_address.split(',')[0]

# Read from the CSV file
with open('business_info.csv', 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    next(reader, None)  # Skip the header

    # Open the text file in write mode
    with open('business_info.txt', 'w', encoding='utf-8') as outfile:

        for row in reader:
            business_name = row[0]
            notes_emoji = row[1]
            full_address = row[2]
            street_address = get_street_address(full_address)

            # Write to the text file
            outfile.write(f'{business_name} {notes_emoji}\n')
            outfile.write(f'{street_address}\n')
            outfile.write('\n')  # Blank line after each entry
