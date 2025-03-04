from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

app = Flask(__name__)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Load English words list from file
with open("words_alpha.txt") as f:
    ENGLISH_WORDS = set(word.strip().lower() for word in f)

# Define custom positive & negative words
POSITIVE_WORDS = {
    "fire", "lit", "vibe", "vibed", "goat", "slayed", "based", "valid", "w", "fye", 
    "amazing", "awesome", "legend", "chill", "hype", "drip", "blessed", "thriving",
}

NEGATIVE_WORDS = {
    "discrimination", "discriminate", "hate", "racism", "racist", "violence", "abuse", "crime", "corruption", 
    "l", "mid", "sus", "clown", "flop", "trash", "cringe"
}

def is_valid_text(text):
    """Check if the text contains at least one valid English word or a proper name."""
    cleaned_text = re.sub(r"[^a-zA-Z\s]", "", text).strip()  # Remove special characters
    words_list = cleaned_text.split()  # Split into words
    
    # If at least one word is alphabetic, consider it valid
    return any(word.isalpha() for word in words_list)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    sentiment = ""

    if request.method == "POST":
        text = request.form.get("comment", "").strip().lower()

        if not text or not is_valid_text(text):
            sentiment = "Please enter a valid comment!"
        else:
            sentiment_score = analyzer.polarity_scores(text)["compound"]

            words = set(text.split())

            # Prioritize slang-based sentiment detection
            if words & NEGATIVE_WORDS:
                sentiment = "Negative 😠"
            elif words & POSITIVE_WORDS:
                sentiment = "Positive 😎🔥"
            elif sentiment_score >= 0.05:
                sentiment = "Positive 😊"
            elif sentiment_score <= -0.05:
                sentiment = "Negative 😠"
            else:
                sentiment = "Neutral 😐"

    return render_template("index.html", text=text, sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)

