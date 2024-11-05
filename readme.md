# Bitcoin Historical Data Scraping with Selenium in Python

## Overview
As a crypto enthusiast, I created this project to demonstrate how Python and Selenium can be used to automate the retrieval of Bitcoin’s historical price data from the CoinMarketCap website. My goal was to show how to efficiently collect all available data on Bitcoin’s prices from its inception, without manually browsing. The project uses a Chrome WebDriver to access the page, click the "Load More" button to gather all historical data entries, and finally saves the structured data into a CSV file format, ready for analysis and further insights.

## Requirements
To run this project, you need the following dependencies:
- **Selenium**: For automating the browser interactions.
- **Webdriver Manager**: To manage the ChromeDriver for Selenium.
- **CSV**: To save extracted data in CSV format.

You can install these packages using pip:
pip install selenium webdriver-manager

## Code Structure

1. **Initialize ChromeDriver with Options**  
   The script starts by configuring the Chrome WebDriver:
   - It installs and initializes the driver using `webdriver-manager`.
   - Sets options to ignore SSL errors and certificate warnings.
   - Opens Chrome in standard mode (not headless, allowing you to see the actions).

   service_obj = Service(ChromeDriverManager().install())
   options = Options()
   options.add_argument('--ignore-certificate-errors')
   options.add_experimental_option("detach", True)
   options.add_argument('--ignore-ssl-errors=yes')

   driver = webdriver.Chrome(service=service_obj, options=options)

2. **Access the Website and Set Up the CSV File**  
   The WebDriver navigates to the Bitcoin historical data page on CoinMarketCap. It creates and writes the headers to the CSV file before starting the data extraction.

   driver.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/")

   with open("btc_historical_data.csv", "w", newline='') as file:
       writer = csv.writer(file)
       writer.writerow(["count", "date", "price_open", "price_high", "price_low", "price_close", "volume", "market_cap"])

3. **Load More Data Using the "Load More" Button**  
   The data on CoinMarketCap is initially limited to a few entries. By clicking the "Load More" button repeatedly, the script loads the entire dataset. This is handled with an explicit wait to ensure the button is located before clicking it. The script will continue until the button is no longer visible, at which point all available data has been loaded.

   wait = WebDriverWait(driver, 20)
   load_more = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[2]/div/div[2]/div/div/div[2]/div/p[1]/button")))
   driver.execute_script("arguments[0].scrollIntoView();", load_more)

   while load_more:
       try:
           load_more.click()
           print("click done")
       except:
           print("The 'Load More' button is no longer visible. All data has been loaded.")
           break

4. **Extract and Write Data to CSV**  
   Once the entire dataset is loaded, the script extracts the data from each row of the table. Each row contains fields such as Date, Open, High, Low, Close, Volume, and Market Cap. The `get_btc_info` function iterates through each row, retrieves each cell’s data using Selenium, and appends the data to the CSV file.

   def get_btc_info():
       for index, row in enumerate(table_of_data, start=1):
           try:
               # Extract each cell data
               date = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[1]"))).text
               price_open = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[2]"))).text
               price_high = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[3]"))).text
               price_low = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[4]"))).text
               price_close = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[5]"))).text
               volume = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[6]"))).text
               market_cap = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[7]"))).text
               
               # Append to CSV
               btcDataList = [index, date, price_open, price_high, price_low, price_close, volume, market_cap]
               with open("btc_historical_data.csv", "a", newline='') as file:
                   writer = csv.writer(file)
                   writer.writerow(btcDataList)

               print(btcDataList)
           except Exception as e:
               print(f"Error on row {index}: {e}")

   get_btc_info()

5. **Execution and Results**  
   When executed, the script:
   - Loads the Bitcoin historical data page.
   - Iteratively clicks the "Load More" button until all data is displayed.
   - Extracts the data for each date, including the opening and closing prices, highest and lowest prices, volume, and market cap.
   - Saves the data to a CSV file (`btc_historical_data.csv`), which can later be used for data analysis or visualization.

### Conclusion
This project automates the retrieval of historical Bitcoin data from CoinMarketCap, providing a daily snapshot of prices, volume, and market capitalization for analysis. It demonstrates the use of Selenium for web scraping dynamic content, handling pagination via buttons, and saving structured data to a CSV file.

## Future Enhancements
- **Daily Automation**: Schedule the script to run daily for up-to-date data.
- **Error Handling**: Implement better error handling for cases where page structure might change.
- **Data Analysis**: Use the collected data to perform time series analysis or visualizations.
