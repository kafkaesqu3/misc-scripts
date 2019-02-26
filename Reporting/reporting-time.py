import csv
import argparse
import sys

# REPORTING TIME!
# Swiss-army knife for moving raw data into a format suitable for reports

# DEFINE CONSTANTS HERE

# define where our data is inside the csv file
ip_column_no=0
proto_column_no = 1
port_column_no = 2
title_column_no = 3

# returns a dict, where the key is the title
# the value of each dict is a list of tuples
# the tuple contains the affected IP address, protocol, and port #
def parse_location_data(data): 
    global title_column_no
    # run through the data, convert row to tuple, add it to list for dict where title is the key
    parsed_data = {}
    for line in data: 
        title = line[title_column_no]
        ip_address = line[ip_column_no]
        port = int(line[port_column_no])
        if port != 0: 
            proto_port = " [" + line[proto_column_no] + "/" + str(port) + "]"
        else: 
            proto_port = ""
        # try: 
        #     port = int(line[proto_port_column_no].split('/')[0])
        # except: 
        #     print("Some of these ports arent numbers. Check your dataset; it may not be what is expected")
        #     sys.exit()
        #proto = line[proto_port_column_no].split('/')[1]         
        #data = tuple([ip_address, proto, port])
        data = tuple([ip_address, proto_port])


        if title in parsed_data: 
            parsed_data[title].append(data)
        else: 
            parsed_data.update({title:[data]})
    return parsed_data

# given CSV data, returns each unique title in the data set
def find_titles(data):
    try: 
        global title_column_no
        titles = []
        for row in data: 
            if row[title_column_no] not in titles:
                titles.append(row[title_column_no])
        titles.sort()
        return titles
    except: 
        print("Input data either isn't a CSV, or isn't formatted correctly!")
        sys.exit()


# converts tab-delimited file to comma-delimited
# this will overwrite the file if it already exists
def convert_to_csv(in_text, outfile):
        with open(outfile, "w+") as out_csv:
            out_writer = csv.writer(out_csv, quoting=csv.QUOTE_ALL)
            for row in in_text:
                out_writer.writerow(row)

def main (): 
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-t", "--titles", action='store_true', help="Print unique titles", required=False)
    argparser.add_argument("-c", "--csv", action='store_true', help="Convert a tab delimited file to a CSV", required=False)
    argparser.add_argument("-l", "--location", action='store_true', help="Parse Location info from CSV data")
    argparser.add_argument("-i", "--input", help="Input file", required=True)
    argparser.add_argument("-o", "--output", help="Output file", required=False)
    argparser.add_argument("--no-markdown", help="Don't print output with markup", action='store_true')

    arguments = argparser.parse_args()

    file_data = open(arguments.input, 'r')

    # convert to CSV
    if arguments.csv: 
        if not arguments.output: 
            print("You need to specify an output file with -o [file]")
            sys.exit()

        csv_data = csv.reader(file_data, delimiter = '\t')
    
        convert_to_csv(csv_data, arguments.output)
        sys.exit()

    # get titles
    if arguments.titles: 
        csv_data = list(csv.reader(file_data))
        titles = find_titles(csv_data)
        for title in titles: print title
        sys.exit()

    # print Location
    if arguments.location: 
        csv_data = list(csv.reader(file_data))
        parsed_data = parse_location_data(csv_data)

        titles = find_titles(csv_data)
        if not arguments.output: 
            print("You need to specify an output file with -o [file]")
            sys.exit()

        with open(arguments.output, 'w+') as output: 
            for title in titles: 
                if arguments.no_markdown: 
                    bold_markup = ""
                    list_markup = ""
                else: 
                    bold_markup = "**"
                    list_markup = "* "

                output.write("{0}{1}{2}\n\n".format(bold_markup, title, bold_markup))
                locations_raw = parsed_data[title]
                for location in locations_raw: 
                    ip_address = location[0]
                    #protocol = location[1].upper()
                    #port = location[2]
                    proto_port = location[1].upper()
                    #if port == 0: 
                    #    output.write("{0}{1}\n".format(list_markup, ip_address))
                    #else: 
                    output.write("{0}{1}{2}\n".format(list_markup, ip_address, proto_port))
                output.write('\n\n')

if __name__ == "__main__":
    main()
