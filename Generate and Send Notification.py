# Import Packages
import pandas as pd
import random 
import telepot
from datetime import datetime, date

# Define classes and functions

# Generate bold text for telegram
def bold_telegram(text):

    text = f"*{text}*"
    
    return text
    
# Convert a number to an ordinal number
def to_ordinal(number):

    last_digit = number[-1]
    
    if last_digit == '1':
        
        number = number + 'st'
        
    elif last_digit == '2':
        
        number = number + 'nd'
        
    elif last_digit == '3':
        
        number = number + 'rd'
        
    else:
        
        number = number + 'th'
        
    return number

# Format day number to remove leading 0 and convert to an ordinal number
def format_day_number(day_number):
    
    if day_number[0] == '0':
        
        day_number = day_number[1:]
        
    day_number = to_ordinal(day_number)
    
    return day_number

# Load dataset
df = pd.read_excel('Output\French Words - In Use.xlsx')

# Generate Notification

# Filter to only show rows that have not yet been seen by the user
df_not_seen = df[df['Already Seen'] == 'No']

# List of all row indexes that have not yet been seen by the user
index_not_seen = list(df_not_seen.index)

# Choose row index that will be seen next by the user
random_index = random.choice(index_not_seen)

# Recording that this word has now been seen by the user
df.iloc[random_index] = df.iloc[random_index].replace(to_replace = 'No', value = 'Yes')

# Row that will be seen next by the user
chosen_row = df_not_seen.iloc[random_index]

# The frequency of the chosen word (string format)
word_frequency = str(chosen_row['Rank Frequency'])

# The frequency of the chosen word (ordinal number) in bold text
word_frequency_ordinal = to_ordinal(word_frequency)
word_frequency_ordinal = bold_telegram(word_frequency_ordinal)

# Current date
current_datetime_day = datetime.now().strftime("%A") + ','
current_datetime_day_number = format_day_number(datetime.now().strftime("%d"))
current_datetime_month = datetime.now().strftime("%b")
current_datetime_year = datetime.now().strftime("%Y")

current_date = ' '.join((current_datetime_day, current_datetime_day_number, 
                         current_datetime_month, current_datetime_year))
current_date = bold_telegram(current_date)

# Current time
current_time = datetime.now().strftime("%H:%M")
current_time = bold_telegram(current_time)

# Number of words learnt by user since the beginning
number_of_words_learnt = str(len(df[df['Already Seen'] == 'Yes']))
number_of_words_learnt = bold_telegram(number_of_words_learnt + ' / 5000')

# Extracting key strings from chosen row and converting them to bold text
french_word = bold_telegram(chosen_row['French Word'])

meaning = bold_telegram(chosen_row['Meaning'])

parts_of_speech = bold_telegram(chosen_row['Parts of Speech'])

french_sentence = bold_telegram(chosen_row['French Sentence'])

english_sentence = bold_telegram(chosen_row['English Sentence'])

# Creating strings to show user
string_french_word = f"The new word: {french_word}"

string_meaning = f"This word means: {meaning}"

string_french_word_frequency = f"The frequency of this word in French: {word_frequency_ordinal}"

string_parts_of_speech = f"This word belongs to the part of speech category: {parts_of_speech}"

string_french_sentence = f"An example sentence: {french_sentence}"

string_english_sentence = f"The translation of this sentence: {english_sentence}"

seperator = '----------------------------------------------------'

string_current_date = f"Date: {current_date}"

string_current_time = f"Time: {current_time}"

string_words_learned = f"Words learnt: {number_of_words_learnt}"

# Combine all strings into one
notification_text = "\n\n".join((string_french_word, string_meaning, string_french_word_frequency, 
                                 string_parts_of_speech, string_french_sentence, string_english_sentence, seperator, 
                                 string_current_date, string_current_time, string_words_learned))

# Save main dataframe to an excel file
df.to_excel("Output\French Words - In Use.xlsx", index=False)

# Send Notification

# Enter id associated with my telegram group (French Words)
chat_id = "-753515307"

# Enter API key associated with my telegram bot (@FrenchWordGeneratorBot)
api_key = "5765466869:AAFOmJWFQR_jaBwaLBDf5iZslATvZnDu9Gg"

# Configure bot
bot = telepot.Bot(api_key)

# Send message
bot.sendMessage(chat_id, notification_text, parse_mode= 'Markdown')



