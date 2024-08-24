from modules import *

def download_forex_data(startdate, enddate, currency, basecurrency, filename="forex_data.xlsx"):
    # Define the URL and the payload with user inputs
    url = "https://mcb.mu/webapi/mcb/ForexDataExcel"
    payload = {
        "StartDate": startdate,
        "EndDate": enddate,
        "CurrencyCode": currency,
        "BaseCurrency": basecurrency
    }

    try:
        # Make the POST request
        response = requests.post(url, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the content as an Excel file
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved as {filename}.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
