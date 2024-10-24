#       ||   SHREE   ||       #


from flask import Flask, render_template, request, url_for , jsonify
import os
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
import uuid

app = Flask(__name__)


# Set path to your Dialogflow service account credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogueflow.json"

# Initialize the Dialogflow session
def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input
        )

        return response.query_result.fulfillment_text

@app.route('/')  # Home page route
def home():
    return render_template('index.html')

@app.route('/sip_calculator', methods=['GET', 'POST'])  # SIP Calculator route
def sip_calculator():
    if request.method == 'POST':  # Form submission
        monthly_investment = float(request.form['monthly_investment'])
        interest_rate = float(request.form['interest_rate']) / 100  # Convert to decimal
        years = int(request.form['years'])
        
        # Calculate future value
        months = years * 12
        future_value = monthly_investment * (((1 + interest_rate / 12) ** months - 1) / (interest_rate / 12)) * (1 + interest_rate / 12)
        
        return render_template('sip_result.html', future_value=round(future_value, 2), monthly_investment=monthly_investment, interest_rate = 100*interest_rate )

    return render_template('sip_calculator.html')  # Render form if GET request


@app.route('/chatbot', methods=['GET' , 'POST'])
def chatbot():
 if request.method == 'POST':
    user_message = request.json.get('message')
    project_id = 'investmentadvisory-wjvw'
    session_id = str(uuid.uuid4())  # You can set this to track conversations

    response_text = detect_intent_texts(project_id, session_id, [user_message], 'en')

    return jsonify({"response": response_text})
    
 return render_template('chatbot.html')

@app.route('/data_analysis')  # Chatbot page route
def data_analysis():            
    return render_template('data_analysis.html')

@app.route('/contact')  # Chatbot page route
def contact():
    return render_template('contact.html')


stocks = [
    {"id": 1, "name": "Apple Inc.", "symbol": "AAPL", "price": 150, "slug": "apple"},
    {"id": 2, "name": "Microsoft Corp.", "symbol": "MSFT", "price": 300, "slug": "microsoft"},
    {"id": 3, "name": "Google LLC", "symbol": "GOOGL", "price": 2800, "slug": "google"},
    {"id": 4, "name": "Amazon.com Inc.", "symbol": "AMZN", "price": 3500, "slug": "amazon"},
]

@app.route('/stocks')
def stock_list():
    return render_template('stocks.html', stocks=stocks)

@app.route('/stock/<string:post_slug>')
def stock_detail(post_slug):
    stock = next((s for s in stocks if s['slug'] == post_slug), None)
    return render_template('stock_detail.html', stock=stock)


if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0' ,port=6000)
