# Libraries which we are using to extract the data
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from app.models.dbmodels import Job_Details
from app.config.dbconfig import SessionLocal
import requests

# Portal link we are using to extract the data
url = 'https://www.naukri.com/content-writing-jobs?k=content%20writing&nignbevent_src=jobsearchDeskGNB'

# Create ChromeOptions object
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')  # Optional: Run Chrome in headless mode

# Create the WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

# Access the URL
driver.get(url)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

# Creating a blank dataframe
df_list = [pd.DataFrame()]

# Parsing the class using beatiful soup and then saving the data into job_elems

job_elems = soup.find_all('div', class_='cust-job-tuple layout-wrapper lay-2 sjw__tuple')
print(len(job_elems))

# Iterating through classes using loop to extract the required data


for job_elem in job_elems:

    # Extracting the Title
    URL = job_elem.find('div', class_='row1').find('a', class_='title').get('href')

    Title = job_elem.find('div', class_='row1')

    # Extracting the Company Name
    Company = job_elem.find('div', class_='row2')

    # Extracting the Rating
    rating_span = job_elem.find('span', class_='main-2')
    if rating_span is None:
        continue
    else:
        Ratings = rating_span.text

    # Extracting the Job_description
    job_description = job_elem.find('div', class_='row4')

    # Extracting the Salary offered
    Salary = job_elem.find('span', class_='ni-job-tuple-icon ni-job-tuple-icon-srp-rupee sal')
    if Salary is None:
        continue
    else:
        Salary = Salary.text

    # Extracting the Location for the job
    Location = job_elem.find('span', class_='ni-job-tuple-icon ni-job-tuple-icon-srp-location loc')
    if Location is None:
        continue
    else:
        Location = Location.text

    # Appending the data into data frame
    df = pd.DataFrame({'URL': URL, 'Title': Title.text, 'Company': Company.text, 'Ratings': Ratings,
                       'Job_description': job_description.text, 'Salary': Salary, 'Location': Location}, index=[0])
    df_list.append(df)
# Null value treatment

final_data = pd.concat(df_list)
with SessionLocal() as session:
    # Iterate through the DataFrame and store each row in the database
    for _, row in final_data.iterrows():
        job_details = Job_Details(
            url=row['URL'],
            title=row['Title'],
            company=row['Company'],
            ratings=row['Ratings'],
            job_description=row['Job_description'],
            salary=row['Salary'],
            location=row['Location']
        )
        session.add(job_details)

    # Commit the changes to the database
    session.commit()
