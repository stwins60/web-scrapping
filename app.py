from bs4 import BeautifulSoup
import requests
import re
import random
import csv
import datetime
import pandas as pd
import sys
import argparse


DATE = datetime.datetime.now().strftime('%Y-%m-%d')
RAND_INT = str(random.randint(1, 100))
DATA = DATE + "_"+ RAND_INT + '.csv'

# Scrape and get data from indeed


def get_url(query, location):
    # # query = input('Enter the job title: ')
    # query = sys.argv[1]
    # # location = input('Enter the location: ')
    # location = sys.argv[2]

    url = f'https://www.indeed.com/jobs?q={query}&l={location}'

    return url


def get_data(data):

    title = data.find('h2', 'jobTitle').text
    company = data.find('span', 'companyName').text
    location = data.find('div', 'companyLocation').text
    job_description = data.find('div', 'job-snippet').text.strip()
    date = data.find('span', 'date').text

    job_list = {'title': title,'company': company, 'location': location,
                'description': job_description, 'date': date}        
            
    return job_list
    

def main(input1, input2):
    url = get_url(input1, input2)
    job_data = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('div','slider_container')
    
        for job in jobs:
            data = get_data(job)
            job_data.append(data)
        
        # url = soup.find('a', {'aria-label': 'Next'})
        # print(url)
        try:
            url = 'https://www.indeed.com' + soup.findAll('a', {'aria-label': 'Next'})[0].get('href')
            # print(len(url))
        except IndexError:
            print('No more pages')
            break
    # print(job_data)   

    df = pd.DataFrame(job_data, columns=['title','company', 'location', 'description', 'date'])
    
    print(df)
    df.to_csv(DATA, index=False)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position', help='Enter the job title: ', type=str)
    parser.add_argument('location', help='Enter the location: ', type=str)
    args = parser.parse_args()
    main(args.position, args.location)
    


