from flask import Flask, render_template, request, jsonify
import os
import json
import uuid
from google.cloud import dialogflow_v2 as dialogflow
from bsedata.bse import BSE
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load configuration
with open('dialogueflow.json') as config_file:
    config = json.load(config_file)
    api_key = config.get("ALPHA_VANTAGE_API_KEY")

# Set path to your Dialogflow service account credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow.json"

# Initialize the Dialogflow session
def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
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
        
        return render_template('sip_result.html', future_value=round(future_value, 2), monthly_investment=monthly_investment, interest_rate=100 * interest_rate)

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

# Initialize BSE and prepare for fetching stock data
b = BSE(update_codes=True)
compscrips = ["512026", "538537", "532139", "532336", "533676", "520073", "505725", "539843", "539785", "542383", "520086", "506808", "500337", "533022", "532529", "523606", "507155", "509438", "522229", "500207", "500530", "542727", "500429", "508807", "517354", "538970", "539201", "540133", "532432", "515043", "524709", "500124", "507753", "532937", "511605", "538635", "511676", "532461", "539254", "540145", "508954", "540425", "500173", "520119", "500193", "530023", "516030", "500268", "500264", "500490", "500093", "539290", "506197", "532906", "533193", "532729", "532610", "511243", "533156", "508933", "526725", "511218", "500420", "532343", "533148", "539018", "532686", "540649", "522029", "524774", "533336", "524648", "532067", "526608", "516064", "532616", "507789", "501298", "500280", "500087", "532794", "519105", "532842", "534748", "530075", "531426", "541276", "500119", "520008", "532323", "520059", "539042", "524520", "533477", "532134", "532741", "532515", "530699", "524394", "542684", "532348", "506390", "505200", "531449", "511333", "539660", "531847", "500402", "526650", "590062", "504084", "532457", "590115", "519602", "542669", "522295", "539221", "501150", "502180", "531633", "502175", "506618", "500439", "540125", "530355", "500136", "532424", "500547", "511413", "517334", "541741", "532955", "500400", "540717", "532155", "511076", "500425", "500825", "524280", "503031", "523838", "534328", "522073", "505400", "590134", "532345", "511628", "531859", "539469", "522108", "506194", "505163", "532370", "505036", "523736", "500306", "532810", "532661", "590065", "524109", "540980", "507410", "532633", "523708", "532240", "590030", "513517", "517421", "531092", "530307", "507526", "530011", "500414", "532365", "507944", "506685", "539594", "531921", "538920", "500440", "540777", "540776", "532488", "506642", "514043", "531179", "533761", "532875", "530879", "541269", "532742", "506248", "523207", "532650", "508906", "540795", "500002", "530131", "524332", "517500"]


@app.route('/stocks')
def stock_list():
    stocks = [ ]  # Clear the stocks list before each request
    for key in compscrips:
        try:
            quote = b.getQuote(key)
            stocks.append({
                'id': len(stocks) + 1,
                'name': quote["companyName"],
                'price': quote["currentValue"],
                'scripcode': quote["scripCode"]
            })
        except Exception as e:
            print(f"Error fetching data for scrip code {key}: {e}")

    return render_template("stocks.html", stocks=stocks)

@app.route('/stock/<string:post_slug>')
def stock_detail(post_slug):
    return render_template("stock_detail.html")

@app.route('/generate_stock_graph')
def generate_stock_graph():
    # Define companies and date range
    companies = ["Apple Inc. (AAPL)", "Microsoft Corporation (MSFT)", 
                 "Alphabet Inc. (GOOGL)", "Amazon.com Inc. (AMZN)"]
    months = pd.date_range(start="2022-01-01", periods=24, freq="M")

    # Define the exact stock prices used in the plot
    data = {
        "Apple Inc. (AAPL)": [97.82, 101.88, 104.01, 110.39, 112.31, 108.96,
                              113.04, 116.65, 113.88, 115.32, 117.40, 115.34,
                              118.48, 122.87, 124.35, 124.54, 123.98, 126.87,
                              122.08, 119.50, 120.42, 117.54, 121.37, 123.72],
        "Microsoft Corporation (MSFT)": [134.42, 130.32, 132.18, 136.22, 140.45, 138.52,
                                          140.89, 143.96, 146.77, 143.15, 145.20, 148.72,
                                          150.91, 153.98, 156.16, 158.45, 160.17, 162.43,
                                          165.33, 163.82, 166.05, 168.65, 170.86, 173.00],
        "Alphabet Inc. (GOOGL)": [62.13, 63.90, 66.44, 68.58, 67.76, 70.66,
                                  73.35, 74.03, 75.87, 76.64, 78.72, 79.52,
                                  81.49, 83.60, 86.15, 87.80, 88.61, 91.47,
                                  90.62, 92.94, 94.07, 96.12, 98.42, 100.48],
        "Amazon.com Inc. (AMZN)": [178.98, 176.09, 179.90, 181.96, 185.79, 188.58,
                                   192.32, 193.75, 195.95, 198.68, 200.57, 203.62,
                                   205.56, 208.79, 210.53, 213.87, 215.68, 218.37,
                                   219.99, 222.57, 225.99, 228.12, 231.27, 233.43]
    }

    # Create DataFrame for stock prices
    df = pd.DataFrame(data, index=months)

    # Plotting
    plt.figure(figsize=(12, 6))
    for company in companies:
        plt.plot(df.index, df[company], label=company, marker='o')  # Plot each company's prices

    # Customize the plot
    plt.title("Stock Prices Over the Last 2 Years (Monthly Data)")
    plt.xlabel("Date")
    plt.ylabel("Stock Price (USD)")
    plt.legend(title="Companies")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to an image file
    plt.savefig("static/graph.png")  # Save the image to the static directory
    plt.close()  # Close the plot to free up memory

    return jsonify({"status": "success", "image": "static/graph.png"})

if __name__ == '__main__':
    app.run(debug=True)
