from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def scrape_job_details(keyword):
    base_url = 'https://www.shine.com/job-search/'
    search_url = f'{base_url}{keyword}'

    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all divs with the specified class for job cards
        job_cards = soup.find_all('div', {"class": "jobCard_jobCard__jjUmu"})

        job_list = []

        for job_card in job_cards:
            job_details = {}
            title_tag = job_card.find('h2').find('a')
            job_details['title'] = title_tag.get_text(strip=True)
            job_details['link'] = "https://www.shine.com" + title_tag['href']
            job_details['company'] = job_card.find('div', {"class": "jobCard_jobCard_cName__mYnow"}).find('span').get_text(strip=True)
            job_details['experience'] = job_card.find('div', {"class": "jobCard_jobCard_lists_item__YxRkV", "class": "jobCard_jobIcon__3FB1t"}).get_text(strip=True)
            job_details['location'] = job_card.find('div', {"class": "jobCard_jobCard_lists_item__YxRkV", "class": "jobCard_locationIcon__zrWt2"}).get_text(strip=True)
            job_details['job_type'] = job_card.find('li').get_text(strip=True)

            job_list.append(job_details)

        return job_list
    else:
        return None

@app.route('/jobs', methods=['POST'])
def get_job_details():
    try:
        data = request.get_json()
        keyword = data.get('keyword')  
        job_details = scrape_job_details(keyword)
    
        if job_details:
            return jsonify(job_details)
        else:
            return jsonify({'error': 'Failed to retrieve job details'}), 500
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
