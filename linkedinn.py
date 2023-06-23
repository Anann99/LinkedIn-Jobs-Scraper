import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Driver path
path = '/home/anann99/Documents/chromedriver_linux64 (1)/chromedriver'
service = Service(path)
driver = webdriver.Chrome(service=service)

# Maximize Window
driver.maximize_window()
driver.minimize_window()
driver.maximize_window()
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

# Rest of the code remains the same

# Enter the site
driver.get('https://www.linkedin.com/login')
time.sleep(2)

# User Credentials
user_name = 'anannya@truefoundry.com'
password = '!mA0987654321'
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(user_name)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
time.sleep(1)

# Login button
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(30)

# Jobs page
driver.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a/span').click()
time.sleep(3)
# Go to search results directly
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3568598652&f_E=3%2C4%2C5%2C6&f_TPR=r86400&geoId=103644278&keywords=(GPT%20OR%20LLM%20OR%20Generative%20AI)%20AND%20(Machine%20%20OR%20ML%20OR%20Data%20Science%20OR%20AI%20OR%20Software)&location=United%20States&refresh=true&start=50")
time.sleep(1)

# Get all links for these offers
links = []

# Navigate to the last page
last_page_button = driver.find_element(By.CSS_SELECTOR, 'li.artdeco-pagination__indicator--number:last-child button')
while last_page_button.text == '…':
    last_page_button.click()
    time.sleep(2)  # Add a delay to allow the page to load
    last_page_button = driver.find_element(By.CSS_SELECTOR, 'li.artdeco-pagination__indicator--number:last-child button')
last_page_number = int(last_page_button.text)

print(f'The last page number is: {last_page_number}')

print('Links are being collected now.')
try:
    for page in range(1, last_page_number + 1):
        time.sleep(2)
        jobs_block = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
        jobs_list = jobs_block.find_elements(By.CSS_SELECTOR, 'li.jobs-search-results__list-item')

        for job in jobs_list:
            all_links = job.find_elements(By.TAG_NAME, 'a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links:
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # Scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)

        print(f'Collecting the links in the page: {page - 1}')
        # Go to next page
        # Construct the CSS selector for the current page button
        page_button_selector = f"li.artdeco-pagination__indicator--number button[aria-label='Page {page}']"

        # Wait for the page button to be clickable
        page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, page_button_selector)))

        # Scroll to the page button element
        driver.execute_script("arguments[0].scrollIntoView();", page_button)

        # Click the page button
        page_button.click()

        # Wait for the page to load
        time.sleep(3)

except:
    pass

print('Found ' + str(len(links)) + ' links for job offers')

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = []
job_desc = []
job_req = []


# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i, link in enumerate(links):
    try:
        driver.get(links[i])
        time.sleep(2)
        # Click See more.
        driver.find_element(By.XPATH, '//*[@id="ember31"]').click()
        time.sleep(2)
    except:
        pass

    # Find the general information of the job offers
    contents = driver.find_elements(By.CLASS_NAME, 'p5')
    for content in contents:
        try:
            company = content.find_element(By.CLASS_NAME, "jobs-unified-top-card__company-name").text
            if company != "Crossover":
                job_title = content.find_element(By.TAG_NAME, "h1").text
                company_name = content.find_element(By.CLASS_NAME, "jobs-unified-top-card__company-name").text
                company_location = content.find_element(By.CLASS_NAME, "jobs-unified-top-card__bullet").text
                work_method = content.find_element(By.CLASS_NAME, "jobs-unified-top-card__workplace-type").text
                post_date = content.find_element(By.CLASS_NAME, "jobs-unified-top-card__posted-date").text
                work_time = content.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-insight").text
                
            # Find the element containing the job description
                try:
                   job_description_element = driver.find_element(By.ID, 'job-details')
                # Extract the text from the job description element
                   job_description_text = job_description_element.text
                except Exception as e:
                   print(e)
                   job_description_text = 'No description available'

                # Append the scraped information to the respective lists
                job_titles.append(job_title)
                company_names.append(company_name)
                company_locations.append(company_location)
                work_methods.append(work_method)
                post_dates.append(post_date)
                work_times.append(work_time)
                job_desc.append(job_description_text)
                job_req.append(link)

                print(f'Scraping the Job Offer {i + 1} DONE.')
        except:
            pass
        time.sleep(2)
    if i == 2:
        break


# Create a dictionary to store the keyword information
keyword_info = {
    'data science': [],
    'genai': [],
    'generative': [],
    'openai': [],
    'gpt': [],
    'chatgpt': [],
    'nlp': [],
    'bert': [],
    'hugging': [],
    'transformers': [],
    'llm': [],
    'gpu': [],
    'kubernetes': [],
    'tuning': []
}


# Iterate over job descriptions and check for keywords
for desc in job_desc:
    for keyword in keyword_info:
        if keyword.lower() in desc.lower():
            keyword_info[keyword].append('YES')
        else:
            keyword_info[keyword].append('NO')

# Create the dataframe
df = pd.DataFrame({
    'job_title': job_titles,
    'company_name': company_names,
    'company_location': company_locations,
    'work_method': work_methods,
    'post_date': post_dates,
    'work_time': work_times,
    'JD': job_desc,
    'job_link': job_req,
    **keyword_info  # Add keyword columns to the dataframe
})

df.head()

# Load the existing Excel file
existing_df = pd.read_excel('/home/anann99/Documents/linkedin_jobs.xlsx', sheet_name='freelance')

# Concatenate the existing and new dataframes with an empty row as separator
separator = pd.DataFrame([[''] * df.shape[1]], columns=df.columns)
combined_df = pd.concat([existing_df, separator, df], ignore_index=True)

# Write the combined dataframe to the Excel file
combined_df.to_excel('/home/anann99/Documents/linkedin_jobs.xlsx', sheet_name='freelance', index=False)

# Quit the driver
driver.quit()
