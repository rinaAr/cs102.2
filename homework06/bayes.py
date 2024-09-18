import numpy as np
from collections import defaultdict, Counter
import math

class NaiveBayesClassifier:

    def __init__(self, alpha=1.0):
        """
        Initialize the classifier with smoothing parameter alpha.
        Alpha is used for Laplace smoothing.
        """
        self.alpha = alpha
        self.class_prior = {}
        self.word_counts = {}
        self.class_word_totals = {}
        self.vocabulary = set()
        self.classes = []

    def fit(self, X, y):
        """
        Fit Naive Bayes classifier according to X (list of texts) and y (list of labels).
        X is the feature set (list of text documents), and y is the corresponding class labels.
        """
        # Calculate class priors P(class)
        self.classes = set(y)
        class_counts = Counter(y)
        total_samples = len(y)
        
        self.class_prior = {cls: count / total_samples for cls, count in class_counts.items()}
        
        # Initialize word count dictionaries for each class
        self.word_counts = {cls: defaultdict(int) for cls in self.classes}
        self.class_word_totals = {cls: 0 for cls in self.classes}
        
        for text, label in zip(X, y):
            words = text.split()  # Split each document into words
            for word in words:
                self.word_counts[label][word] += 1
                self.class_word_totals[label] += 1
                self.vocabulary.add(word)

    def predict(self, X):
        """
        Perform classification on an array of test vectors X.
        X is a list of text documents that need to be classified.
        Returns a list of predicted labels.
        """
        predictions = []
        for text in X:
            words = text.split()
            class_scores = {}
            
            for cls in self.classes:
                # Initialize log-probability with the log of the class prior
                log_prob = math.log(self.class_prior[cls])
                
                for word in words:
                    # Use Laplace smoothing to calculate P(word|class)
                    word_freq = self.word_counts[cls].get(word, 0)
                    word_prob = (word_freq + self.alpha) / (self.class_word_totals[cls] + self.alpha * len(self.vocabulary))
                    
                    # Add the log of the word's probability to the log-probability of the class
                    log_prob += math.log(word_prob)
                
                class_scores[cls] = log_prob
            
            # Predict the class with the highest log-probability
            predicted_class = max(class_scores, key=class_scores.get)
            predictions.append(predicted_class)
        
        return predictions

    def score(self, X_test, y_test):
        """
        Returns the mean accuracy on the given test data X_test and true labels y_test.
        """
        predictions = self.predict(X_test)
        correct_predictions = sum(1 for pred, true in zip(predictions, y_test) if pred == true)
        accuracy = correct_predictions / len(y_test)
        return accuracy
