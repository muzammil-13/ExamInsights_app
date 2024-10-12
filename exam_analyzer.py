# exam_analyzer.py
import PyPDF2
import nltk
from collections import Counter
import re

class ExamAnalyzer:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def analyze(self, pdf_path):
        text = self.extract_text_from_pdf(pdf_path)
        questions = self.extract_questions(text)
        frequent_topics = self.identify_frequent_topics(questions)
        return {
            'frequent_topics': frequent_topics,
            'question_count': len(questions)
        }

    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page in range(reader.numPages):
                text += reader.getPage(page).extractText()
        return text

    def extract_questions(self, text):
        # Simple question extraction (assumes questions end with '?')
        return re.findall(r'[A-Z][^.!?]*\?', text)

    def identify_frequent_topics(self, questions):
        words = []
        for question in questions:
            words.extend([word.lower() for word in nltk.word_tokenize(question) 
                          if word.isalnum() and word.lower() not in self.stopwords])
        return Counter(words).most_common(10)