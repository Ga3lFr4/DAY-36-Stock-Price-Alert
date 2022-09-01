import requests
from datetime import timedelta, date
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = ""
NEWS_API_KEY = ""

TWILIO_SID = ""
TWILIO_AUTH = ""
TWILIO_PHONE = "+"
MY_PHONE = "+"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API_KEY
}

TODAY = date.today()
YESTERDAY = str(TODAY - timedelta(days=1))
DAY_BEFORE_YESTERDAY = str(TODAY - timedelta(days=2))


stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()

stock_data = stock_response.json()["Time Series (Daily)"]

yesterday_close_price = float(stock_data[YESTERDAY]["4. close"])
day_before_yesterday_close_price = float(stock_data[DAY_BEFORE_YESTERDAY]["4. close"])

# STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the
# two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.


def calculate_stock_price_difference():
    positive_or_negative = None
    difference = round(((yesterday_close_price - day_before_yesterday_close_price) / yesterday_close_price) * 100, 4)
    if difference > 0:
        positive_or_negative = "positive"
    elif difference < 0:
        positive_or_negative = "negative"
    return positive_or_negative, abs(difference)


variation = calculate_stock_price_difference()[1]


def change_symbol():
    var_symbol = ""
    if calculate_stock_price_difference()[0] == "positive":
        var_symbol = "🔺"
    elif calculate_stock_price_difference()[0] == "negative":
        var_symbol = "🔻"
    return var_symbol


symbol = change_symbol()


# STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
# HINT 1: Think about using the Python Slice Operator


def get_news():
    news_params = {
        "q": COMPANY_NAME,
        "from": DAY_BEFORE_YESTERDAY,
        "apiKey": NEWS_API_KEY
    }
    news_reponse = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_reponse.raise_for_status()
    news_data = news_reponse.json()
    articles = news_data["articles"][0:3]
    return articles


def send_messages():
    for article in top_articles:
        headline = article["title"]
        brief = article["description"]
        twilio_message = f"{STOCK}: {symbol}{variation}%\n" \
                         f"Headline: {headline}\n" \
                         f"Brief: {brief}"
        client = Client(TWILIO_SID, TWILIO_AUTH)
        client.messages \
            .create(
                body=twilio_message,
                from_=TWILIO_PHONE,
                to=MY_PHONE,
            )


# STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
# HINT 1: Consider using a List Comprehension.


calculate_stock_price_difference()
change_symbol()
if variation > 5:
    top_articles = get_news()
    send_messages()
else:
    print("not enough var")

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

