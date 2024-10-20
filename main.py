#       ||   SHREE   ||       #

from flask import Flask, render_template, request

app = Flask(__name__)

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
        
        return render_template('sip_result.html', future_value=round(future_value, 2))

    return render_template('sip_calculator.html')  # Render form if GET request


if __name__ == '__main__':
    app.run(debug=True)
