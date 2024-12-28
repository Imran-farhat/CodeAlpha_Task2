from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Sample FAQs (expand with common customer queries)
faqs = {
    "What is your return policy?": "Our return policy allows returns within 30 days of purchase.",
    "How can I track my order?": "You can track your order using the tracking link sent to your email.",
    "What payment methods do you accept?": "We accept Visa, MasterCard, PayPal, and more.",
    "Do you offer international shipping?": "Yes, we offer international shipping to select countries. Additional charges may apply.",
    "How do I reset my password?": "To reset your password, click on 'Forgot Password' on the login page and follow the instructions.",
    "Can I cancel or modify my order?": "Orders can be modified or canceled within 24 hours of placing them. Contact customer support for assistance.",
    "How do I contact customer support?": "You can reach customer support via email at support@example.com or call us at 1-800-123-4567.",
    "What are your working hours?": "Our working hours are Monday to Friday, 9 AM to 5 PM EST.",
    "Do you have a loyalty program?": "Yes, we have a loyalty program. You can earn points on purchases and redeem them for discounts.",
    "How do I apply a discount code?": "You can apply a discount code at checkout in the 'Promo Code' field."
}

questions = list(faqs.keys())
answers = list(faqs.values())

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(questions)

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query", "")

    if not user_query:
        return jsonify({"response": "Please provide a query."}), 400

    # Preprocess and vectorize user query
    user_vector = vectorizer.transform([user_query])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)
    max_index = similarity_scores.argmax()
    max_score = similarity_scores[0, max_index]

    # Confidence threshold
    if max_score > 0.5:
        response = answers[max_index]
    else:
        response = "I'm sorry, I didn't understand your question. Could you rephrase?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
