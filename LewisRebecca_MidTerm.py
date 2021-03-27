#Rebecca Lewis
#October 6, 2019
#DSC 540
#Mid Term Project
#Usage: This script reads in a data file containing reviews for beers and cleans the data.

from csv import reader
import pprint
from datetime import datetime
from fuzzywuzzy import process

def get_rdr(file_name):
    ''' This function returns a list for a given file name'''
    rdr = reader(open(file_name, 'rb'))
    return rdr

def new_zip_data(data_rows, header_rows):
    '''This function combines a list of data with a list of headers'''
    new_data = []

    #create lists that contain the abbreviated and meaningful header names
    for row in data_rows[1:]:
        new_row = []
        for i, d in enumerate(row):
            new_row.append(d)
        new_data.append(new_row)

    #combine the list of headers with the dataa
    new_zip_data = []
    for  drow in new_data:
        new_zip_data.append(zip(header_rows, drow))

    return new_zip_data

def print_sample(datalist, index=0):
    '''Formats the list of data into a pretty format to print to the screen. The user can send the index of the
    item they want to print or the function will use 0 by default.  '''
    for row in datalist[index]:
        print 'Question: {[1]}\nAnswer: {}'.format(row[0], row[1])

def clean_data(datalist):
    '''Cleans the data by adding a derived key, grouping the beers by style, and converting a relative time in seconds to
    datetime format'''
    new_data = []
    styles = ['Lager', 'IPA', 'Stout', 'Ale', 'Bock', 'Pilsner', 'Other']

    for row in datalist:
        new_row = []
        new_key = ['derived_key', 'Derived Key'],'%s-%s-%s-%s' % (row[0][1], row[12][1], row[6][1], row[2][1])
        new_row.append(new_key)
        for i, d in enumerate(row):
            if d[0][0] == 'review_time':
                new_item = ['review_datetime_derived', 'Derived Review Date and Time'], datetime.utcfromtimestamp(float(d[1])).strftime('%Y-%m-%d %H:%M:%S')
                new_row.append(new_item)
            if d[0][0] == 'beer_style':
                if process.extractOne(d[1], styles) is not None:
                    new_group =  ['derived_group', 'Derived Group'], process.extractOne(d[1], styles)[0]
                else:
                    new_group = ['derived_group', 'Derived Group'], 'Other'
                new_row.append(new_group)
            new_row.append(d)
        new_data.append(new_row)

    return new_data

def find_missing_data(datalist):
    '''Finds elements with missing or null data.  Returns a string with No Missing Data or a dictionary containing the items with
    missing data'''
    Missing_Answer = False

    for row in datalist:
        for answer in row:
            if answer[1] is None:
                Missing_Answer = True

    na_count = {}

    for row in datalist:
        for resp in row:
            question = resp[0][1]
            answer = resp[1]
            if answer == 'NA':
                if question in na_count.keys():
                    na_count[question] += 1
                else:
                    na_count[question] = 1

    if Missing_Answer or na_count <> {}:
        print 'Missing Values: '.format(na_count)
    else:
        print 'No Missing or Null Values'

def find_duplicates(datalist):
    '''Finds elements with duplicates based on derived key.  Returns a string with No Duplicates or a count of duplicates'''
    set_of_keys = set([row[0][1] for row in datalist])

    uniques = [row for row in datalist if not set_of_keys.remove(row[0][1])]

    if len(set_of_keys)==0:
        print 'No Duplicates'
    else:
        print 'Number of Duplicates: {}'.format(len(set_of_keys))

def is_number(s):
    '''Function to determine if a number is present in a string by attempting to convert it to a float.
    Returns true or false'''
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_datetime(s):
    '''Function to determine if a string is a datetime by attempting to convert it.  Returns true or false'''
    try:
        datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False

def data_distribution(datalist):
    '''Returns the distribution of data by type to find any mismatched data types.  By using this function, I was
    able to determine that the digit and date criteria presented in the text would not work for my dataset.  Prints
    a dictionary with the fields and their types.'''

    datatypes = {}
    start_dict = {'digit':0, 'boolean':0, 'empty':0, 'time_related':0, 'text':0, 'unknown':0}

    for row in datalist:
        for resp in row:
            question = resp[0][1]
            answer = resp[1]
            key = 'unknown'
            if is_number(answer):
                key = 'digit'
            elif answer in ['Yes','No','True','False']:
                key = 'boolean'
            elif answer.isspace():
                key = 'empty'
            elif is_datetime(answer):
                key = 'time_related'
            else:
                key = 'text'
            if question not in datatypes.keys():
                datatypes[question] = start_dict.copy()
            datatypes[question][key] += 1

    pprint.pprint(datatypes)

def main():

    #open files
    data_rdr, header_rdr = get_rdr('beer_short.csv'), get_rdr('beer_headers.csv')

    #read in data and header files
    data_rows = [d for d in data_rdr]
    header_rows = [h for h in header_rdr if h[0] in data_rows[0]]

    #combine the data and header files
    zipped_data = new_zip_data(data_rows, header_rows)

    #clean the data
    formatted_data = clean_data(zipped_data)

    #search for missing data and duplicates
    find_missing_data(formatted_data)
    find_duplicates(formatted_data)

    #review the distribution of data
    data_distribution(formatted_data)

    #print in readable format
    print_sample(formatted_data)


if __name__ == '__main__':
    main()

    #used this to test for dupes and determine unique key
    # set_of_keys = set(['%s-%s-%s-%s' % (x[0][1], x[13][1], x[7][1], x[3][1]) for x in formatted_data])
    # uniques = [x for x in formatted_data if not set_of_keys.remove('%s-%s-%s-%s' % (x[0][1], x[13][1], x[7][1], x[3][1]))]
    #
    # print set_of_keys

    # used this to group by style
    # styles = ['Lager', 'IPA', 'Stout', 'Ale', 'Bock', 'Pilsner', 'Other']
    #
    # new_data = []
    #
    # #add new key and group to each row
    # for row in formatted_data:
    #     new_row = []
    #     new_key = ['derived_key', 'Derived Key'],'%s-%s-%s-%s' % (row[0][1], row[13][1], row[7][1], row[3][1])
    #     new_row.append(new_key)
    #     for i, d in enumerate(row):
    #         if d[0][0] == 'beer_style':
    #             if process.extractOne(d[1], styles) is not None:
    #                 new_group =  ['derived_group', 'Derived Group'], process.extractOne(d[1], styles)[0]
    #             else:
    #                 new_group = ['derived_group', 'Derived Group'], 'Other'
    #             new_row.append(new_group)
    #         new_row.append(d)
    #     new_data.append(new_row)
    #
    # pprint.pprint(new_data[0])
