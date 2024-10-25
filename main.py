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
    {"id": 5, "name": "Facebook Inc.", "symbol": "FB", "price": 340, "slug": "facebook"},
    {"id": 6, "name": "Tesla Inc.", "symbol": "TSLA", "price": 730, "slug": "tesla"},
    {"id": 7, "name": "Berkshire Hathaway", "symbol": "BRK.A", "price": 411000, "slug": "berkshire"},
    {"id": 8, "name": "NVIDIA Corporation", "symbol": "NVDA", "price": 220, "slug": "nvidia"},
    {"id": 9, "name": "Visa Inc.", "symbol": "V", "price": 235, "slug": "visa"},
    {"id": 10, "name": "Johnson & Johnson", "symbol": "JNJ", "price": 160, "slug": "johnson-johnson"},
    {"id": 11, "name": "Walmart Inc.", "symbol": "WMT", "price": 140, "slug": "walmart"},
    {"id": 12, "name": "Mastercard Inc.", "symbol": "MA", "price": 365, "slug": "mastercard"},
    {"id": 13, "name": "Procter & Gamble", "symbol": "PG", "price": 145, "slug": "procter-gamble"},
    {"id": 14, "name": "UnitedHealth Group", "symbol": "UNH", "price": 400, "slug": "unitedhealth"},
    {"id": 15, "name": "Home Depot", "symbol": "HD", "price": 325, "slug": "home-depot"},
    {"id": 16, "name": "Intel Corp.", "symbol": "INTC", "price": 55, "slug": "intel"},
    {"id": 17, "name": "Coca-Cola Co.", "symbol": "KO", "price": 60, "slug": "coca-cola"},
    {"id": 18, "name": "PepsiCo Inc.", "symbol": "PEP", "price": 150, "slug": "pepsico"},
    {"id": 19, "name": "Cisco Systems", "symbol": "CSCO", "price": 45, "slug": "cisco"},
    {"id": 20, "name": "Adobe Inc.", "symbol": "ADBE", "price": 530, "slug": "adobe"},
    {"id": 21, "name": "Netflix Inc.", "symbol": "NFLX", "price": 550, "slug": "netflix"},
    {"id": 22, "name": "Pfizer Inc.", "symbol": "PFE", "price": 38, "slug": "pfizer"},
    {"id": 23, "name": "PayPal Holdings", "symbol": "PYPL", "price": 225, "slug": "paypal"},
    {"id": 24, "name": "Comcast Corp.", "symbol": "CMCSA", "price": 50, "slug": "comcast"},
    {"id": 25, "name": "Verizon Comm.", "symbol": "VZ", "price": 57, "slug": "verizon"},
    {"id": 26, "name": "Toyota Motor Corp.", "symbol": "TM", "price": 180, "slug": "toyota"},
    {"id": 27, "name": "AT&T Inc.", "symbol": "T", "price": 30, "slug": "att"},
    {"id": 28, "name": "ExxonMobil Corp.", "symbol": "XOM", "price": 90, "slug": "exxonmobil"},
    {"id": 29, "name": "Chevron Corp.", "symbol": "CVX", "price": 100, "slug": "chevron"},
    {"id": 30, "name": "Shell plc", "symbol": "SHEL", "price": 45, "slug": "shell"},
    {"id": 31, "name": "Alibaba Group", "symbol": "BABA", "price": 160, "slug": "alibaba"},
    {"id": 32, "name": "Samsung Electronics", "symbol": "SSNLF", "price": 80, "slug": "samsung"},
    {"id": 33, "name": "Unilever plc", "symbol": "UL", "price": 55, "slug": "unilever"},
    {"id": 34, "name": "British American Tobacco", "symbol": "BTI", "price": 36, "slug": "british-american-tobacco"},
    {"id": 35, "name": "Sony Corporation", "symbol": "SONY", "price": 115, "slug": "sony"},
    {"id": 36, "name": "SoftBank Group", "symbol": "SFTBY", "price": 21, "slug": "softbank"},
    {"id": 37, "name": "BlackRock Inc.", "symbol": "BLK", "price": 850, "slug": "blackrock"},
    {"id": 38, "name": "Boeing Co.", "symbol": "BA", "price": 210, "slug": "boeing"},
    {"id": 39, "name": "Morgan Stanley", "symbol": "MS", "price": 75, "slug": "morgan-stanley"},
    {"id": 40, "name": "Delta Air Lines", "symbol": "DAL", "price": 39, "slug": "delta"},
    {"id": 41, "name": "Ford Motor Co.", "symbol": "F", "price": 20, "slug": "ford"},
    {"id": 42, "name": "General Motors", "symbol": "GM", "price": 45, "slug": "gm"},
    {"id": 43, "name": "Goldman Sachs", "symbol": "GS", "price": 330, "slug": "goldman-sachs"},
    {"id": 44, "name": "Zoom Video Comm.", "symbol": "ZM", "price": 340, "slug": "zoom"},
    {"id": 45, "name": "Tencent Holdings", "symbol": "TCEHY", "price": 75, "slug": "tencent"},
    {"id": 46, "name": "Shopify Inc.", "symbol": "SHOP", "price": 950, "slug": "shopify"},
    {"id": 47, "name": "Salesforce Inc.", "symbol": "CRM", "price": 225, "slug": "salesforce"},
    {"id": 48, "name": "Texas Instruments", "symbol": "TXN", "price": 185, "slug": "texas-instruments"},
    {"id": 49, "name": "Qualcomm Inc.", "symbol": "QCOM", "price": 130, "slug": "qualcomm"},
    {"id": 50, "name": "Square Inc.", "symbol": "SQ", "price": 200, "slug": "square"},
    {"id": 51, "name": "Snap Inc.", "symbol": "SNAP", "price": 50, "slug": "snap"},
    {"id": 52, "name": "Intuit Inc.", "symbol": "INTU", "price": 400, "slug": "intuit"},
    {"id": 53, "name": "Activision Blizzard", "symbol": "ATVI", "price": 95, "slug": "activision"},
    {"id": 54, "name": "Uber Technologies", "symbol": "UBER", "price": 45, "slug": "uber"},
    {"id": 55, "name": "Pinterest Inc.", "symbol": "PINS", "price": 55, "slug": "pinterest"},
    {"id": 56, "name": "Palantir Tech.", "symbol": "PLTR", "price": 28, "slug": "palantir"},
    {"id": 57, "name": "Lyft Inc.", "symbol": "LYFT", "price": 35, "slug": "lyft"},
    {"id": 58, "name": "ServiceNow Inc.", "symbol": "NOW", "price": 550, "slug": "servicenow"},
    {"id": 59, "name": "Spotify Tech.", "symbol": "SPOT", "price": 235, "slug": "spotify"},
    {"id": 60, "name": "Airbnb Inc.", "symbol": "ABNB", "price": 155, "slug": "airbnb"},
    {"id": 61, "name": "DoorDash Inc.", "symbol": "DASH", "price": 165, "slug": "doordash"},
    {"id": 62, "name": "Roku Inc.", "symbol": "ROKU", "price": 115, "slug": "roku"},
    {"id": 63, "name": "Datadog Inc.", "symbol": "DDOG", "price": 125, "slug": "datadog"},
    {"id": 64, "name": "CrowdStrike", "symbol": "CRWD", "price": 230, "slug": "crowdstrike"},
    {"id": 65, "name": "Snowflake Inc.", "symbol": "SNOW", "price": 350, "slug": "snowflake"},
    {"id": 66, "name": "DocuSign Inc.", "symbol": "DOCU", "price": 230, "slug": "docusign"},
    {"id": 67, "name": "Robinhood Markets", "symbol": "HOOD", "price": 20, "slug": "robinhood"},
    {"id": 68, "name": "Beyond Meat", "symbol": "BYND", "price": 110, "slug": "beyond-meat"},
    {"id": 69, "name": "Twilio Inc.", "symbol": "TWLO", "price": 300, "slug": "twilio"},
    {"id": 70, "name": "Etsy Inc.", "symbol": "ETSY", "price": 160, "slug": "etsy"},
    {"id": 71, "name": "Carvana Co.", "symbol": "CVNA", "price": 170, "slug": "carvana"},
    {"id": 72, "name": "Slack Technologies", "symbol": "WORK", "price": 40, "slug": "slack"},
    {"id": 73, "name": "Peloton Interactive", "symbol": "PTON", "price": 90, "slug": "peloton"},
    {"id": 74, "name": "ZoomInfo Tech.", "symbol": "ZI", "price": 75, "slug": "zoominfo"},
    {"id": 75, "name": "Coinbase Global", "symbol": "COIN", "price": 250, "slug": "coinbase"},
    {"id": 76, "name": "Robinhood Markets", "symbol": "HOOD", "price": 20, "slug": "robinhood"},
    {"id": 77, "name": "Wayfair Inc.", "symbol": "W", "price": 175, "slug": "wayfair"},
    {"id": 78, "name": "Chewy Inc.", "symbol": "CHWY", "price": 90, "slug": "chewy"},
    {"id": 79, "name": "GameStop Corp.", "symbol": "GME", "price": 180, "slug": "gamestop"},
    {"id": 80, "name": "Moderna Inc.", "symbol": "MRNA", "price": 210, "slug": "moderna"},
    {"id": 81, "name": "Carnival Corp.", "symbol": "CCL", "price": 22, "slug": "carnival"},
    {"id": 82, "name": "AMC Entertainment", "symbol": "AMC", "price": 13, "slug": "amc"},
    {"id": 83, "name": "Virgin Galactic", "symbol": "SPCE", "price": 25, "slug": "virgin-galactic"},
    {"id": 84, "name": "Wynn Resorts", "symbol": "WYNN", "price": 100, "slug": "wynn"},
    {"id": 85, "name": "DoorDash Inc.", "symbol": "DASH", "price": 165, "slug": "doordash"},
    {"id": 86, "name": "Okta Inc.", "symbol": "OKTA", "price": 240, "slug": "okta"},
    {"id": 87, "name": "Square Inc.", "symbol": "SQ", "price": 200, "slug": "square"},
    {"id": 88, "name": "Baidu Inc.", "symbol": "BIDU", "price": 185, "slug": "baidu"},
    {"id": 89, "name": "Bilibili Inc.", "symbol": "BILI", "price": 60, "slug": "bilibili"},
    {"id": 90, "name": "JD.com Inc.", "symbol": "JD", "price": 65, "slug": "jd"},
    {"id": 91, "name": "Tencent Music", "symbol": "TME", "price": 12, "slug": "tencent-music"},
    {"id": 92, "name": "Weibo Corp.", "symbol": "WB", "price": 53, "slug": "weibo"},
    {"id": 93, "name": "Meituan", "symbol": "3690.HK", "price": 245, "slug": "meituan"},
    {"id": 94, "name": "Xiaomi Corp.", "symbol": "1810.HK", "price": 22, "slug": "xiaomi"},
    {"id": 95, "name": "Huawei Tech.", "symbol": "HWTL", "price": 90, "slug": "huawei"},
    {"id": 96, "name": "TikTok", "symbol": "TIKTOK", "price": 50, "slug": "tiktok"},
    {"id": 97, "name": "ByteDance Ltd.", "symbol": "BD", "price": 250, "slug": "bytedance"},
    {"id": 98, "name": "Dell Technologies", "symbol": "DELL", "price": 90, "slug": "dell"},
    {"id": 99, "name": "ASML Holding", "symbol": "ASML", "price": 725, "slug": "asml"},
    {"id": 100, "name": "IBM Corp.", "symbol": "IBM", "price": 125, "slug": "ibm"}
]

@app.route('/stocks')
def stock_list():
    return render_template('stocks.html', stocks=stocks)

@app.route('/stock/<string:post_slug>')
def stock_detail(post_slug):
    stock = next((s for s in stocks if s['slug'] == post_slug), None)
    return render_template('stock_detail.html', stock=stock)


if __name__ == '__main__':
    app.run(debug=True)
