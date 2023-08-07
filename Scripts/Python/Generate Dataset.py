# Import Packages
import pandas as pd
import numpy as np
import re
import itertools
import string

pd.set_option('display.max_rows', 200)

from PyPDF2 import PdfFileReader
from pathlib import Path

# Define functions

# Find words in a string from a list of words
def words_in_string(word_list, a_string):
    
    set_matching_words = set(word_list).intersection(a_string.split())
    
    list_matching_words = list(set_matching_words)
        
    return list_matching_words

# Replace items in a list based on values in a dictionary
def replace(my_list, my_dict):
    
    new_list = [item if item not in my_dict else my_dict[item] for item in my_list]
    
    return new_list

# Generate list of strings generated from combination of all possible permutations of substrings from two lists
def permutations(list1, list2, separator = ''):
    
    permutations = list(itertools.product(list1, list2))
    
    permutations = [permutations[i][0] + separator + permutations[i][1] for i in range(0, len(permutations))]
    
    return permutations

# Extracting relevant strings
def relevant_strings_from_pdf(text_from_pdf):

    # Find strings containg specific sequence
    relevant_strings_from_pdf = re.findall("\n[ \w,.*'\-();0-9]+", text_from_pdf)

    # Generate strings used to seperate words by first letter
    alphabet_uppercase = list(string.ascii_uppercase)
    alphabet_lowercase = list(string.ascii_lowercase)
    alphabet_rows = []

    for upper, lower in zip(alphabet_uppercase, alphabet_lowercase):

        row_to_remove = "\n" + upper + lower

        alphabet_rows.append(row_to_remove)

    # Remove rows with strings used to seperate words by first letter
    relevant_strings_from_pdf = list(set(relevant_strings_from_pdf).difference(alphabet_rows))

    # Remove rows that are used to seperate pages
    relevant_strings_from_pdf = [row for row in relevant_strings_from_pdf if '\n Page ' not in row]

    # Remove rows with a blank space
    relevant_strings_from_pdf = [row for row in relevant_strings_from_pdf if row != '\n ']
    
    # Remove trailling letters of strings if they exist
    for index, relevant_string in enumerate(relevant_strings_from_pdf):
        
        if relevant_string[-1].isalpha() == True:
            
            relevant_strings_from_pdf[index] = re.sub('[a-zA-Z]+$', '', relevant_string)
            
        else:
            
            relevant_strings_from_pdf[index] = relevant_string

    return relevant_strings_from_pdf

# Flatten a list
def flatten_list(list_of_lists):
    
    return list(itertools.chain(*list_of_lists))

# Due to an error in the pdf, a specific replacement with respect to the rank frequency column is required
def make_specific_replacement_due_to_error_in_pdf(dataframe):
    
    # List of numbers from 1 to 5000
    first_5000_numbers = list(range(1, 5000))

    # List of numbers we have in our dataframe
    numbers_present = list(dataframe['Rank Frequency'])

    # Check to see if we have all 5000 words in dataframe
    check = list(set(first_5000_numbers).difference(numbers_present)) 

    # 'check' returns [4149], we are missing this number only

    # From looking at the pdf, turns out there are two words paired with 4436 (vingt-cinq and vingt-quatre)
    view_error = dataframe[dataframe['Rank Frequency'] == 4436]

    # vingt-quatre should paired with 4149
    
    # find index of vingt-quatre
    index_of_error = df.loc[df['French Word'] == 'vingt-quatre'].index[0]
    
    # Make the replacement
    dataframe.at[index_of_error,'Rank Frequency'] = 4149
    
    return dataframe

# Due to errors in the pdf (noticed due to mismatches between different sections within the pdf) 
# specific replacement with respect to typos are required
def make_specific_replacement_due_to_error_in_pdf_2(text_from_pdf):
    
    text_from_pdf = text_from_pdf.replace('2010 bien? adv well', '2010 ben adv well')
    
    text_from_pdf = text_from_pdf.replace('2084 résiderv to reside', '2084 résider v to reside')
    
    text_from_pdf = text_from_pdf.replace('3313 assdassinat nm murder, assassination', '3313 assassinat nm murder, assassination')

    return text_from_pdf

# Find all index positions of item in a list
def get_index_positions(list_of_elems, element):
    
    index_pos_list = []
    
    index_pos = 0
    
    while True:
        
        try:
            
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            
            # Add the index position in list
            index_pos_list.append(index_pos)
            
            index_pos += 1
            
        except ValueError as e:
            
            break
            
    return index_pos_list

# Generating more permutations for the parts of speech formatting: e.g. [POS A], [POS B] or [POS A],[POS B]
def add_parts_of_speech_formating_premutation(string):
    
    formatting_permutation = string.replace(', ', ',')
    
    formatting_permutations = [string, formatting_permutation]
    
    return formatting_permutations

# Sort list by another list
def sort_list_by_another_list(list_to_sort_by, list_to_sort):
    
    sorted_list = [x for _, x in sorted(zip(list_to_sort_by, list_to_sort))]
    
    return sorted_list

# Find matching items between two lists and maintain order of these items ('set()' may change the original order)
def find_matching_items_between_two_lists_and_maintain_order(list_to_maintain_order_of, list_to_check_for_matching_items):
    
    items_and_index = [(item, index) for index, item in enumerate(list_to_maintain_order_of)]
    
    list_matching_items = list(set(list_to_maintain_order_of) & set(list_to_check_for_matching_items))
    
    prior_index_of_items_in_list_to_maintain_order_of = [tup[1] for item in list_matching_items for tup in items_and_index if tup[0] == item]
    
    list_matching_items_order_maintained = sort_list_by_another_list(prior_index_of_items_in_list_to_maintain_order_of, list_matching_items)
    
    return list_matching_items_order_maintained

# Find text starting with a specified string and ending with a specified string
def find_text_starting_with_x_and_ending_with_y(full_text, starting_with, ending_with='|'):
        
    full_text_reduced = full_text[full_text.find(starting_with):]
        
    final_text = full_text_reduced[:full_text_reduced.find(ending_with)]
    
    return final_text

# Find strings without a specific item (e.g. asterisk, double dash etc.) as these normally signify where the sentences begin and end
def find_strings_without_a_specific_item(string, item):
        
    if item in string:
        
        output = 'Yes'
        
    else:
        
        output = 'No'
        
    return output

# Add missing items to strings (e.g. if string does not contain an asterisk, add it at the appropriate place)
def add_missing_items_to_strings(dataframe, column_with_strings, item, string_to_replace, string_to_replace_with):
    
    df_temp = pd.DataFrame()
    
    df_temp[column_with_strings] = dataframe[column_with_strings]

    df_temp['Check Item Missing'] = df_temp[column_with_strings].apply(lambda x: find_strings_without_a_specific_item(x, item))
    
    list_strings_original = list(df_temp[df_temp['Check Item Missing'] == 'No'][column_with_strings])
    
    list_strings_replace = [string.replace(string_to_replace, string_to_replace_with, 1) for string in list_strings_original]
    
    for original, replace in zip(list_strings_original, list_strings_replace):
    
        dataframe = dataframe.replace(to_replace = original, value = replace)
        
    return dataframe

# Remove new lines from a string
def remove_new_lines(string):
    
    string = string.replace('\n', '   ')
    
    string = re.sub(' +', ' ', string)
    
    return string

# Count number of substring in a string
def count_substring_in_string(main_string, sub_string):
    
    count = main_string.count(sub_string)
    
    return count

# Remove additional occurances of item in a string (e.g. more than one double dash)
def remove_additional_occurances_of_item_in_string(dataframe, column_with_strings, item, replace_with):
    
    df_temp = pd.DataFrame()
    
    df_temp[column_with_strings] = dataframe[column_with_strings]

    df_temp['Count'] = df_temp['String with Sentences'].apply(lambda x: count_substring_in_string(x, item))

    list_strings_original = df_temp[df_temp['Count'] > 1]['String with Sentences'].to_list()
    
    list_strings_replace = [item.replace('---', '--') for item in list_strings_original]
    
    for index, item in enumerate(list_strings_replace):
        
        parts = item.partition("--")
        
        list_strings_replace[index] = parts[0] + parts[1] + parts[2].replace("--", replace_with)
        
    for original, replace in zip(list_strings_original, list_strings_replace):
    
        dataframe = dataframe.replace(to_replace = original, value = replace)
        
    return dataframe

# Extract french and english sentences from string
def extract_sentences(string):
    
    string_clean = string.strip()

    sentence_french = re.search('\*(.*)\--', string_clean).group(1)
    sentence_french = sentence_french.replace('*', '')
    sentence_french = sentence_french.strip()

    start_of_english_sentence = '--' 
    sentence_english = string_clean[string_clean.find(start_of_english_sentence):]
    sentence_english = sentence_english.replace('--', '') 
    sentence_english = re.sub('[0-9]+$', '', sentence_english)
    sentence_english = sentence_english.strip()
        
    return sentence_french, sentence_english

# Create pdf file reader object
pdf = PdfFileReader('French Words Book.pdf')

# Define pages to extract text from
page_range = range(475, 575)

relevant_strings = []

# For each page, do the following:
for page_number in page_range:
    
    # Find the page 
    page_object = pdf.getPage(page_number)
    
    # Extract text from the page
    text_from_pdf = page_object.extractText()
        
    # Modify start of text as required
    if page_range.index(page_number) == 0:
        
        find_text = "\nAa"
        
        text_from_pdf = text_from_pdf[text_from_pdf.find(find_text):]
        
    else:
        
        text_from_pdf = "\n" + text_from_pdf

    # Extract relevant strings from the text
    relevant_strings_from_page = relevant_strings_from_pdf(text_from_pdf)
            
    # Save relevent strings from page to list
    relevant_strings.append(relevant_strings_from_page)

relevant_strings = flatten_list(relevant_strings)

# Dictionary of different parts of speech and their abbreviations
dict_parts_of_speech = {'adj':'adjective', 'adv':'adverb', 'conj':'conjunction', 'det':'determiner',
                  'intj':'interjection', 'n':'noun', 'nadj':'noun/adjective', 'prep':'preposition',
                  'pro':'pronoun', 'v':'verb'}

# List of the different parts of speech 
parts_of_speech_short = list(dict_parts_of_speech.keys())
parts_of_speech_long = list(dict_parts_of_speech.values())

# Dictionary of different features and their abbreviations
dict_features = {'f':'(feminine)', 'i':'(invariable)', 'm':'(masculine)', 'pl':'(plural)',
                '(' + 'f' + ')':'(no distinct feminine)', '(' + 'pl' + ')':'(no distinct plural)'}

# List of the different features
features_short = list(dict_features.keys())
features_long = list(dict_features.values())

# Generate all possible permutations of parts of speech + features (x2)
feature_permutations_short = features_short + permutations(features_short, features_short)
feature_permutations_short = [item.replace(")(", "") for item in feature_permutations_short]

feature_permutations_long = features_long + permutations(features_long, features_long, '')
feature_permutations_long = [item.replace(")(", " ") for item in feature_permutations_long]

permutations_short = permutations(parts_of_speech_short, feature_permutations_short)
permutations_long = permutations(parts_of_speech_long, feature_permutations_long, ' ')

# Append original parts of speech list to permutations list
parts_of_speech_and_features_short = parts_of_speech_short + permutations_short
parts_of_speech_and_features_long = parts_of_speech_long + permutations_long

# Creating new dictionary with original parts of speech and all permutations
dict_parts_of_speech_and_features = {parts_of_speech_and_features_short[i]:parts_of_speech_and_features_long[i] 
                                     for i in range(len(parts_of_speech_and_features_short))}

# Initalising dataframe
df = pd.DataFrame()

# Initalising lists for different 
numbers = []
words_french = []
words_english = []
parts_of_speech_short = []
parts_of_speech_long = []
sentences_french = []
sentences_english = []

# Iterating across all string
for row in relevant_strings:
        
    # Extract number
    number = re.search("[0-9]+", row).group(0)
    numbers.append(int(number))
        
    # Extract French word
    row = row.replace(number, "")
        
    substrings = row.split()
    
    word_french = substrings[0]
    words_french.append(word_french)
            
    # Extract part of speech
    substrings = substrings[1:]
    
    substrings = [substring.split(',') for substring in substrings]
    substrings = flatten_list(substrings)

    list_poc_short = find_matching_items_between_two_lists_and_maintain_order(substrings, parts_of_speech_and_features_short)
    list_poc_long = replace(list_poc_short, dict_parts_of_speech_and_features)
       
    string_poc_short = ', '.join(list_poc_short)
    string_poc_long = ', '.join(list_poc_long)
    
    parts_of_speech_short.append(string_poc_short)
    parts_of_speech_long.append(string_poc_long)
    
    # Extract English word
    substrings = [item for item in substrings if item not in list_poc_short]
    substrings = [',' if item == "" else item for item in substrings]
    
    word_english = ' '.join(substrings)
    word_english = word_english.replace(" ,", ",")
    words_english.append(word_english)

# Adding list to dataframe
df['Rank Frequency'] = numbers
df['French Word'] = words_french
df['Meaning'] = words_english
df['Parts of Speech (Abbreviated)'] = parts_of_speech_short
df['Parts of Speech'] = parts_of_speech_long

# Due to an error in the pdf, a specific replacement with respect to the rank frequency column is required
df = make_specific_replacement_due_to_error_in_pdf(df)

# Sort values by rank frequency column
df = df.sort_values('Rank Frequency')

# Define pages to extract text from
page_range = range(17, 476)

# Initiate string to add text too
text_from_pdf = ''

# For each page, do the following:
for page_number in page_range:
    
    # Find the page 
    page_object = pdf.getPage(page_number)
    
    # Extract text from the page
    text_from_pdf += page_object.extractText()
    
text_from_pdf = make_specific_replacement_due_to_error_in_pdf_2(text_from_pdf)

# Create a dataframe to find sentences
df_find_sentences = pd.DataFrame()

# Copy over the Rank Frequency column from original dataframe
df_find_sentences['Rank Frequency'] = df['Rank Frequency']

# Generate strings to search for in text 
df_find_sentences['Number and Word'] = df.apply(lambda x: f"{x['Rank Frequency']} {x['French Word']} ", axis = 1)

# Find strings with sentences
df_find_sentences['String with Sentences'] = df_find_sentences['Number and Word'].apply(lambda x: find_text_starting_with_x_and_ending_with_y(text_from_pdf, x))

# Add asterisks at the appropriate place to strings without asterisks
df_find_sentences = add_missing_items_to_strings(df_find_sentences, 'String with Sentences', '*', '\n', '\n*')

# Remove new lines from a string
df_find_sentences['String with Sentences'] = df_find_sentences['String with Sentences'].apply(lambda x: remove_new_lines(x))

# Add double dashes at the appropriate place to strings without double dashes
df_find_sentences = add_missing_items_to_strings(df_find_sentences, 'String with Sentences', ' --', ' - ', ' -- ')

# Remove additional occurances of double dashes after the first occurance (and replace them with commas)
df_find_sentences = remove_additional_occurances_of_item_in_string(df_find_sentences, 'String with Sentences', '--', ', ')

# Extract French sentences
df_find_sentences['French Sentence'] = df_find_sentences['String with Sentences'].apply(lambda x: extract_sentences(x)[0])

# Extract English sentences
df_find_sentences['English Sentence'] = df_find_sentences['String with Sentences'].apply(lambda x: extract_sentences(x)[1])

df_find_sentences = remove_additional_occurances_of_item_in_string(df_find_sentences, 'String with Sentences', '--', ', ')

# Create a new dataframe only for sentences
df_sentences = df_find_sentences[['Rank Frequency', 'French Sentence', 'English Sentence']]

# Merge sentences dataframe with original dataframe
df = pd.merge(df, df_sentences, on='Rank Frequency')

# Initialise a new column to record which rows have already been used by the application 
# (i.e. user has already recieved a message pertaining to that word)
df['Already Seen'] = ['No'] * df.shape[0]

# Save main dataframe to an excel file
df.to_excel("Output\French Words.xlsx", index=False)

# Save find sentences dataframt to an excel file
df_find_sentences.to_excel("Output\Find Sentences.xlsx", index=False)

