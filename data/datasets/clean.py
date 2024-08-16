import csv
import sys

def clean_positive_employers_en():
    input_file = sys.path[0] + '/positive_employers_en.csv'
    output_file = sys.path[0] + '/../cleaned/2014_12_31.csv'

    # Clear the output file at the beginning
    open(output_file, 'w').close()

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Skip the first line
        next(reader)

        # Write the header for the cleansed CSV
        writer.writerow(['Employer', 'Address', 'Positions', 'Province'])

        curr_province = ""

        # Write the cleansed data to the CSV
        for row in reader:
            # check if row is province
            if(row[1] == ""):
                curr_province = row[0]
                continue

            if(row[0].strip() == "Employer" 
               or row[1].strip() == "Address" 
               or (row[2].strip() == "Positions") or (row[2].strip() == "Position Approved")):
                continue

            if len(row) != 3:
                continue

            employer = row[0].strip()
            address = row[1].strip()
            positions = row[2].strip()
            
            writer.writerow([employer, address, positions, curr_province])

def clean_2015():
    input_file = sys.path[0] + '/2015_positive_employers_en.csv'
    output_file = sys.path[0] + '/../cleaned/2015.csv'

    # Clear the output file at the beginning
    open(output_file, 'w').close()

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header for the cleansed CSV
        writer.writerow(['Employer', 'Address', 'Positions', 'Province'])

        curr_province = ""

        # Write the cleansed data to the CSV
        for row in reader:
            # check if row is province
            if(row[1] == ""):
                curr_province = row[0]
                continue

            if(row[0].strip() == "Employer" 
               or row[1].strip() == "Address" 
               or (row[2].strip() == "Positions") or (row[2].strip() == "Position Approved")):
                continue

            if len(row) != 3:
                continue

            employer = row[0].strip()
            address = row[1].strip()
            positions = row[2].strip()
            
            writer.writerow([employer, address, positions, curr_province])

def clean_2016():
    input_file = sys.path[0] + '/2016_positive_employer_en.csv'
    output_file = sys.path[0] + '/../cleaned/2016.csv'

    # Clear the output file at the beginning
    open(output_file, 'w').close()

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # skip the first line
        next(reader)
        # skip the header
        next(reader)

        # Write the header for the cleansed CSV
        writer.writerow(['Province', 'Employer', 'Address', 'Positions', 'NOC 2011', 'NOC Name',])

        curr_province = ""
        same_employer = ""

        # Write the cleansed data to the CSV
        for row in reader:
            # check if row has province
            if(row[0] != ""):
                curr_province = row[0]
            
            if(row[1] != ""):
                same_employer = row[1]

            if len(row) != 5 or row[3] == '':
                continue

            # Province/Territory,Employer,Address,Occupations under NOC 2011,Positions Approved

            if(row[1] == ""):
                employer = same_employer
            else:
                employer = row[1].strip()
            address = row[2].strip()
            occupation = row[3].strip()
            positions = row[4].strip()

            noc_2011 = occupation.split("-")[0]
            noc_name = occupation.split("-")[1]
            writer.writerow([curr_province, employer, address, positions, noc_2011, noc_name])

def clean_2017(input_path, output_path):
    input_file = sys.path[0] + input_path
    output_file = sys.path[0] + output_path

    # Clear the output file at the beginning
    open(output_file, 'w').close()

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # skip the first line
        next(reader)
        # skip the header
        next(reader)

        # Write the header for the cleansed CSV
        writer.writerow(['Province', 'Employer', 'Address', 'Positions', 'Stream', 'NOC 2011', 'NOC Name',])

        curr_province = ""
        same_employer = ""

        # Write the cleansed data to the CSV
        for row in reader:
            # check if row has province
            if(row[0] != ""):
                curr_province = row[0]
            
            # Province/Territory,Stream,Employer,Address,Occupations under NOC 2011,Positions Approved
            if(row[2] != ""):
                same_employer = row[2]

            if(row[1] != ""):
                same_stream = row[1].strip()

            if len(row) != 6 or row[3] == '':
                continue


            if(row[2] == ""):
                employer = same_employer
            else:
                employer = row[2].strip()
            
            if(row[1] == ""):
                stream = same_stream
            else:
                stream = row[2].strip()

            address = row[3].strip()
            occupation = row[4].strip()
            positions = row[5].strip()

            noc_2011 = occupation.split("-")[0]
            noc_name = occupation.split("-")[1]
            writer.writerow([curr_province, employer, address, positions, stream, noc_2011, noc_name])

# clean_positive_employers_en()
# clean_2015()
# clean_2016()
# clean_2017('/2017q1q2_positive_en.csv', '/../cleaned/2017_06_30.csv')
# clean_2017('/2017q3_positive_employer_stream_en.csv', '/../cleaned/2017_09_30.csv')
# clean_2017('/2017q4_positive_employer_en.csv', '/../cleaned/2017_12_31.csv')
# clean_2017('/2018q1_positive_employer_en.csv', '/../cleaned/2018_03_31.csv')
# clean_2017('/2018q2_positive_employer_en.csv', '/../cleaned/2018_06_30.csv')
# clean_2017('/2018q3_positive_en.csv', '/../cleaned/2018_09_30.csv')
# clean_2017('/2018q4_positive_en.csv', '/../cleaned/2018_12_31.csv')
