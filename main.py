from flask import Flask, render_template, request, jsonify
import os
import json
import uuid
from google.cloud import dialogflow_v2 as dialogflow
from bsedata.bse import BSE
from google.oauth2 import service_account
import concurrent.futures
from dotenv import load_dotenv

app = Flask(__name__)

# Load configuration
# with open('dialogueflow.json') as config_file:
#     config = json.load(config_file)
    # api_key = config.get("ALPHA_VANTAGE_API_KEY")

load_dotenv()

google_project_id = os.getenv("GOOGLE_PROJECT_ID")
google_private_key = os.getenv("GOOGLE_PRIVATE_KEY")
google_client_email = os.getenv("GOOGLE_CLIENT_EMAIL")
google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_auth_uri = os.getenv("GOOGLE_AUTH_URI")
google_token_uri = os.getenv("GOOGLE_TOKEN_URI")
google_auth_provider_cert_url = os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL")
google_client_cert_url = os.getenv("GOOGLE_CLIENT_CERT_URL")

# Set path to your Dialogflow service account credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow.json"

# Create credentials using the service account information
credentials = service_account.Credentials.from_service_account_info({
    "type": "service_account",
    "project_id": google_project_id,
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": google_private_key.replace("\\n", "\n"),
    "client_email": google_client_email,
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
})

# Initialize the Dialogflow session
def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient( credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sip_calculator', methods=['GET', 'POST'])
def sip_calculator():
    if request.method == 'POST':
        monthly_investment = float(request.form['monthly_investment'])
        interest_rate = float(request.form['interest_rate']) / 100
        years = int(request.form['years'])
        
        # Calculate future value
        months = years * 12
        future_value = monthly_investment * (((1 + interest_rate / 12) ** months - 1) / (interest_rate / 12)) * (1 + interest_rate / 12)
        
        return render_template('sip_result.html', future_value=round(future_value, 2), monthly_investment=monthly_investment, interest_rate=100*interest_rate)

    return render_template('sip_calculator.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.json.get('message')
        project_id = 'investmentadvisory-wjvw'
        session_id = str(uuid.uuid4())
        response_text = detect_intent_texts(project_id, session_id, [user_message], 'en')
        return jsonify({"response": response_text})
    
    return render_template('chatbot.html')

@app.route('/data_analysis')
def data_analysis():
    return render_template('data_analysis.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

b = BSE(update_codes=True)

compscrips = [
    "500570",  # Tata Motors Ltd.
    "500325",  # Reliance Industries Ltd.
    "500312",  # ONGC Ltd.
    "500290",  # MRF Ltd.
    "500209",  # Infosys Ltd.
    "500180",  # HDFC Bank Ltd.
    "500112",  # State Bank of India
    "532174",  # ICICI Bank Ltd.
    "500510",  # Larsen & Toubro Ltd.
    "500696",  # Hindustan Unilever Ltd.
    "500034",  # Bajaj Finance Ltd.
    "500010",  # HDFC Ltd.
    "500247",  # Kotak Mahindra Bank Ltd.
    "500520",  # Mahindra & Mahindra Ltd.
    "532454",  # Bharti Airtel Ltd.
    "507685",  # Wipro Ltd.
    "532540",  # Tata Consultancy Services Ltd.
    "500820",  # Asian Paints Ltd.
    "500790",  # Nestlé India Ltd.
    "532538",  # UltraTech Cement Ltd.
    "500087",  # Cipla Ltd.
    "524715",  # Sun Pharmaceutical Industries Ltd.
    "541450",  # Adani Green Energy Ltd.
    "500300",  # Grasim Industries Ltd.
    "532755",  # Tech Mahindra Ltd.
    "542486",  # IndusInd Bank Ltd.
    "532898",  # Power Grid Corporation of India Ltd.
    "532555",  # NTPC Ltd.
    "500470",  # Tata Steel Ltd.
    "500440",  # Hindalco Industries Ltd.
    "500228",  # JSW Steel Ltd.
    "500113",  # Steel Authority of India Ltd.
    "532792",  # Cairn India Ltd.
    "532424",  # Godrej Consumer Products Ltd.
    "505200",  # Eicher Motors Ltd.
    "532977",  # Bajaj Auto Ltd.
    "532539",  # Minda Corporation Ltd.
    "500547",  # Bharat Petroleum Corporation Ltd.
    "532155",  # GAIL (India) Ltd.
    "540115",  # L&T Technology Services Ltd.
    "500550",  # Siemens Ltd.
    "505537",  # Zee Entertainment Enterprises Ltd.
    "540719",  # SBI Life Insurance Company Ltd.
    "540716",  # ICICI Lombard General Insurance Company Ltd.
    "532488",  # Divi's Laboratories Ltd.
    "500400",  # Tata Power Company Ltd.
    "532281",  # HCL Technologies Ltd.
    "500575",  # Voltas Ltd.
    "500477",  # Ashok Leyland Ltd.
    "532477"   # Union Bank of India
]

def fetch_stock_data(scrip_code):
    try:
        quote = b.getQuote(str(scrip_code))
        stock_data = {'name': quote["companyName"],
                      'price': quote["currentValue"],
                      'scripcode': quote["scripCode"],
                      'industry': quote["industry"],
                      'high': quote.get("dayHigh"),
                      'low': quote.get("dayLow"),
                      'yearhigh': quote.get("52weekHigh"),
                      'yearlow': quote.get("52weekLow"),
                      'market_cap': quote.get("marketCapFull"),
                      'totaltradedvalue': quote.get("totalTradedValue"),
                    }
        print(f"Fetched data for {scrip_code}: {stock_data}")
        return stock_data
    except Exception as e:
        print(f"Error fetching data for scrip code {scrip_code}: {e}")
        return None

@app.route('/stocks')
def stock_list():
    stocks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_stock_data, scrip): scrip for scrip in compscrips}
        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1):  # Start ID from 1
            result = future.result()
            
            if result:
                result['id'] = i
                stocks.append(result)
    return render_template("stocks.html", stocks=stocks )


@app.route('/stock/<int:scrip_code>')
def stock_detail(scrip_code):
    try:
        # Fetch stock details based on the scrip code
        stock = fetch_stock_data(scrip_code)
        if stock is not None:
            return render_template("stock_detail.html", stock=stock)
        return "Stock not found", 404  # Handle case where stock is not found
    except Exception as e:
        print(f"Error fetching details for {scrip_code}: {e}")
        return "An error occurred while fetching stock details.", 500

def get_additional_info(topic):
    with open('more_info.txt', 'r') as file:
        content = file.read()
    
    # Find the specific section based on the topic
    sections = content.split('\n# ')
    for section in sections:
        if section.startswith(topic):
            # Extract the paragraph (removing the topic name)
            # print(section)
            return section.replace(f"{topic}\n", "").strip()
    
    # print(f"No additional info found: {topic}")
    return "No additional information available."
    

@app.route('/advice', methods=['GET', 'POST'])
def personalized_advice():
    if request.method == 'POST':
        age = int(request.form['age'])
        income = int(request.form['income'])
        risk_tolerance = request.form['risk_tolerance']
        financial_goal = request.form['financial_goal']

        # Base advice
        advice = f"Based on your age: {age}, income: {income}, risk tolerance: {risk_tolerance}, and financial goal: {financial_goal}, here are some personalized recommendations:"

        # Define additional information
        additional_info = ""

        # Personalized investment advice based on user inputs
        if age < 30:
            if income > 1000000 and risk_tolerance == "high" and financial_goal == "long-term_investment":
                advice += "\n\nYou're young with a high income and risk tolerance. We recommend equity-heavy SIPs or high-growth mutual funds for wealth generation."
                additional_info = get_additional_info("SIP") + "\n\n" + get_additional_info("Mutual Funds")
            elif income <= 1000000 and risk_tolerance == "medium" and financial_goal == "short-term_savings":
                advice += "\n\nYou may consider balanced funds or short-term fixed deposits for preserving capital while seeking moderate growth."
                additional_info = get_additional_info("Balanced Funds") + "\n\n" + get_additional_info("Fixed Deposits")
            else:
                advice += "\n\nConsider a mix of moderate-risk SIPs or debt-equity balanced funds for steady long-term growth."
                additional_info = get_additional_info("Moderate-Risk SIPs") + "\n\n" + get_additional_info("Debt-Equity Balanced Funds")

        elif 30 <= age <= 50:
            if income > 1000000 and risk_tolerance == "medium" and financial_goal == "long-term_investment":
                advice += "\n\nWith a solid income and moderate risk tolerance, a balanced portfolio of equity and debt mutual funds is ideal for long-term wealth creation."
                additional_info = get_additional_info("Balanced Portfolio") + "\n\n" + get_additional_info("Mutual Funds")
            elif income <= 1000000 and risk_tolerance == "low" and financial_goal == "retirement":
                advice += "\n\nConsider conservative debt mutual funds or fixed-income schemes for retirement planning."
                additional_info = get_additional_info("Debt Mutual Funds") + "\n\n" + get_additional_info("Fixed-Income Schemes")
            else:
                advice += "\n\nA mix of balanced funds with a conservative tilt is recommended for capital protection with growth potential."
                additional_info = get_additional_info("Balanced Funds") + "\n\n" + get_additional_info("Conservative Investments")

        elif age > 50:
            if risk_tolerance == "low" and financial_goal == "retirement":
                advice += "\n\nAs you're nearing retirement, prioritize capital preservation with low-risk instruments like fixed deposits or senior citizen savings schemes."
                additional_info = get_additional_info("Fixed Deposits") + "\n\n" + get_additional_info("Senior Citizen Savings Schemes")
            else:
                advice += "\n\nIt's recommended to focus on debt-heavy mutual funds or annuity-based plans to ensure steady income during retirement."
                additional_info = get_additional_info("Debt-Heavy Mutual Funds") + "\n\n" + get_additional_info("Annuity Plans")

        else:
            advice += "\n\nWe recommend reviewing your profile with a financial advisor to tailor the best strategy for you."
            additional_info = get_additional_info("Financial Advisor")

        # Return the advice along with additional information
        return render_template('advice_result.html', advice=advice, additional_info=additional_info)

    # Default render if no POST request (GET request)
    return render_template('advice.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
