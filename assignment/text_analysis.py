import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import json
import os
import glob
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set()
stop_words_folder = "StopWords"
stop_words_files = glob.glob(f"{stop_words_folder}/*.txt")
for file_path in stop_words_files:
    with open(file_path, 'r') as file:
        words = file.readlines()
        stop_words.update(word.strip() for word in words)

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()
    return set(word.strip() for word in words)

positive_words = load_word_list('MasterDictionary/positive-words.txt')
negative_words = load_word_list('MasterDictionary/negative-words.txt')

def calculate_sentiment_scores(text):
    sentences = sent_tokenize(text)
    words = [word.lower() for word in word_tokenize(text) if word.isalnum()]
    
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

def calculate_readability_metrics(text):
    sentences = sent_tokenize(text)
    words = [word.lower() for word in word_tokenize(text) if word.isalnum()]
    total_words = len(words)
    total_sentences = len(sentences)
    complex_words = [word for word in words if syllable_count(word) > 2]
    average_sentence_length = total_words / total_sentences
    percentage_complex_words = len(complex_words) / total_words
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    avg_words_per_sentence = total_words / total_sentences
    average_word_length = sum(len(word) for word in words) / total_words
    
    return average_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, average_word_length, len(complex_words), total_words

def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count += 1
    return count

def count_personal_pronouns(text):
    personal_pronouns = re.findall(r'\b(?:I|we|my|ours|us)\b', text, flags=re.IGNORECASE)
    return len(personal_pronouns)

def text_analysis(text):
    cleaned_text = ' '.join(word for word in word_tokenize(text) if word.lower() not in stop_words)
    
    positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment_scores(cleaned_text)
    
    average_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, average_word_length, complex_word_count, total_words = calculate_readability_metrics(cleaned_text)
    
    personal_pronoun_count = count_personal_pronouns(text)
    
    syllables_per_word = sum(syllable_count(word) for word in word_tokenize(cleaned_text)) / total_words
    
    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score,
        'average_sentence_length': average_sentence_length,
        'percentage_complex_words': percentage_complex_words,
        'fog_index': fog_index,
        'avg_words_per_sentence': avg_words_per_sentence,
        'average_word_length': average_word_length,
        'complex_word_count': complex_word_count,
        'word_count': total_words,
        'syllables_per_word': syllables_per_word,
        'personal_pronouns': personal_pronoun_count
    }

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

folder_path = 'extracted_articles'
file_list = os.listdir(folder_path)

analysis_results_list = []

inputDf = pd.read_excel('Input.xlsx')

column_names = {
    'URL_ID': 'URL_ID',
    'URL': 'URL',
    'positive_score': 'Positive Score',
    'negative_score': 'Negative Score',
    'polarity_score': 'Polarity Score',
    'subjectivity_score': 'Subjectivity Score',
    'average_sentence_length': 'Average Sentence Length',
    'percentage_complex_words': 'Percentage of Complex Words',
    'fog_index': 'Fog Index',
    'avg_words_per_sentence': 'Average Words Per Sentence',
    'average_word_length': 'Average Word Length',
    'complex_word_count': 'Complex Word Count',
    'word_count': 'Word Count',
    'syllables_per_word': 'Syllables Per Word',
    'personal_pronouns': 'Personal Pronouns Count'
}

for index, row in inputDf.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    file_name = f"{url_id}.txt"
    file_path = os.path.join(folder_path, file_name)
    print(f"Performing analysis for {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            analysis_result = text_analysis(text)
            analysis_result['URL_ID'] = url_id
            analysis_result['URL'] = url
            analysis_results_list.append(analysis_result)
            print(f"Analysis result for {file_name}:")
            print(analysis_result)
            print("--------------------------------------------------")
    except FileNotFoundError:
        print(f"File {file_name} not found. Skipping.")
        error_result = {'URL_ID': url_id, 'URL': url}
        for key in column_names.keys():
            if key not in ['URL_ID', 'URL']:
                error_result[key] = '404 Error'
        analysis_results_list.append(error_result)

df = pd.DataFrame(analysis_results_list)

column_order = ['URL_ID', 'URL'] + [col for col in df.columns if col not in ['URL_ID', 'URL']]
df = df[column_order]

df.rename(columns=column_names, inplace=True)

output_file_path = "Output.xlsx"
df.to_excel(output_file_path, index=False)

print(f"Analysis results saved to {output_file_path}")