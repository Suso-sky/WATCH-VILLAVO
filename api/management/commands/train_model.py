# train_model.py
import psycopg2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Train a model to classify robbery-related tweets'

    def handle(self, *args, **kwargs):
        conn = psycopg2.connect("dbname=watch_villavo user=django password=django host=localhost")
        cur = conn.cursor()
        cur.execute("SELECT tweet_text, is_robbery FROM tweets")  # Supongamos que tienes tweets etiquetados
        tweets = cur.fetchall()

        X = [row[0] for row in tweets]
        y = [row[1] for row in tweets]  # Etiquetas: 1 = robo, 0 = no robo

        # Preprocesar texto
        vectorizer = CountVectorizer()
        X_vec = vectorizer.fit_transform(X)

        # División de datos
        X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2)

        # Entrenamiento
        clf = MultinomialNB()
        clf.fit(X_train, y_train)

        accuracy = clf.score(X_test, y_test)
        self.stdout.write(self.style.SUCCESS(f'Model trained with accuracy: {accuracy}'))

        cur.close()
        conn.close()
