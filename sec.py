import pandas as pd
import matplotlib.pyplot as plt

# Define companies and date range
companies = ["Apple Inc. (AAPL)", "Microsoft Corporation (MSFT)", 
             "Alphabet Inc. (GOOGL)", "Amazon.com Inc. (AMZN)"]
months = pd.date_range(start="2022-01-01", periods=24, freq="ME")

# Define the exact stock prices used in the plot
data = {
    "Apple Inc. (AAPL)": [
        97.82026173, 101.88161554, 104.01741307, 110.39439735, 112.31094443, 108.96068781,
        113.04683282, 116.65436896, 113.88022051, 115.31845134, 117.39962315, 115.34342173,
        118.48414107, 122.87090597, 124.34619425, 124.54340891, 123.97889235, 126.87806388,
        122.08714254, 119.49802525, 120.42387705, 117.53537659, 121.36746752, 123.71821724
    ],
    "Microsoft Corporation (MSFT)": [
        134.41575349, 130.31863846, 132.17548632, 136.21751314, 140.45410248, 138.52483453,
        140.89370926, 143.96176144, 146.7663635, 143.15339857, 145.19723359, 148.72429891,
        150.9073101, 153.9780728, 156.15836109, 158.44567383, 160.16723196, 162.4317755,
        165.33186052, 163.81940193, 166.05358738, 168.6529446, 170.86126557, 172.9969441
    ],
    "Alphabet Inc. (GOOGL)": [
        62.1261966, 63.89818384, 66.441947, 68.57909857, 67.75824574, 70.65528727,
        73.34513689, 74.03292622, 75.86593487, 76.6370026, 78.72410248, 79.51976015,
        81.49361354, 83.6021313, 86.14693703, 87.80105823, 88.60767497, 91.4744792,
        90.61714524, 92.9369274, 94.07212029, 96.11895898, 98.42119588, 100.47836555
    ],
    "Amazon.com Inc. (AMZN)": [
        178.97503466, 176.08540354, 179.89532183, 181.96200842, 185.79267359, 188.58311588,
        192.32469715, 193.75264714, 195.94531115, 198.67533519, 200.57283513, 203.62142933,
        205.56499872, 208.79232918, 210.53426427, 213.87124096, 215.67849731, 218.36526918,
        219.98775129, 222.56932406, 225.98757321, 228.11780639, 231.26792759, 233.42932558
    ]
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
plt.savefig("graph.png")  # Save the image to the same directory as the HTML file
