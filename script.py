from bs4 import BeautifulSoup
import http.client
import csv

data = []
fields = ['digital_humanities', 'network_science', 'computational_social_science', 'social_networks', 'modeling_and_simulation']

for field in fields:
    url = f"/citations?view_op=search_authors&hl=en&mauthors=label:{field}"
    conn = http.client.HTTPSConnection('scholar.google.com')
    conn.request('GET', url)
    obj = conn.getresponse()
    text = obj.read()
    soup = BeautifulSoup(text, 'lxml')
    
    divs = soup.findAll('div', class_='gsc_1usr')
    
    researcher_names = [item.find('h3', class_='gs_ai_name').text for item in divs]
    researcher_ids = [item.find('a', href=True)['href'].split('=')[2] for item in divs]
    
    researcher_fields_list = [item.findAll('a', class_='gs_ai_one_int') for item in divs]
    researcher_fields = []
    for tags in researcher_fields_list:
        temp=[]
        for tag in tags:
            temp.append(tag.text)
        while len(temp) < 5:
            temp.append('')
        researcher_fields.append(temp)
        
    researcher_citations = []
    for link in researcher_ids:
        num_citations = {1991: '', 1992: '', 1993: '', 1994: '', 1995: '', 1996: '', 1997: '', 1998: '', 1999: '', 2000: '', 2001: '', 2002: '', 2003: '', 2004: '', 2005: '', 2006: '', 2007: '', 2008: '', 2009: '', 2010: '', 2011: '', 2012: '', 2013: '', 2014: '', 2015: '', 2016: '', 2017: '', 2018: '', 2019: '', 2020: '', 2021: '', 2022: '', 2023: ''}
        temp_url = f'/citations?hl=en&user={link}'
        temp_conn = http.client.HTTPSConnection('scholar.google.com')
        temp_conn.request('GET', temp_url)
        temp_obj = temp_conn.getresponse()
        temp_text = temp_obj.read()
        temp_soup = BeautifulSoup(temp_text, 'html.parser')
        stats_div = temp_soup.findAll('div', class_='gsc_md_hist_b')
        years_list = [item.findAll('span', {'class': 'gsc_g_t'}) for item in stats_div]
        years = [int(span.text.strip()) for span in years_list[0]]
        citations_list = [item.findAll('span', {'class': 'gsc_g_al'}) for item in stats_div]
        citations = [int(span.text.strip()) for span in citations_list[0]]
        for year in years:
            if year in num_citations:
                index = years.index(year)
                num_citations[year] = citations[index]
        researcher_citations.append(num_citations)
    
    for i in range(10):
        temp=[]
        temp.append(researcher_names[i])
        temp.append(researcher_ids[i])
        temp.extend(researcher_fields[i])
        temp.extend(researcher_citations[i].values())
        data.append(temp)
    
    next_link=soup.findAll('button')[2]['onclick'].split('\\')[9][3:]
    
    for count in range(10, 100, 10):
        new_url = f"/citations?view_op=search_authors&hl=en&mauthors=label:{field}&after_author={next_link}&astart={str(count)}"
        conn = http.client.HTTPSConnection('scholar.google.com')
        conn.request('GET', new_url)
        obj = conn.getresponse()
        text = obj.read()
        soup = BeautifulSoup(text, 'lxml')
    
        divs = soup.findAll('div', class_='gsc_1usr')
    
        researcher_names = [item.find('h3', class_='gs_ai_name').text for item in divs]
        researcher_ids = [item.find('a', href=True)['href'].split('=')[2] for item in divs]
    
        researcher_fields_list = [item.findAll('a', class_='gs_ai_one_int') for item in divs]
        researcher_fields = []
        for tags in researcher_fields_list:
            temp=[]
            for tag in tags:
                temp.append(tag.text)
            while len(temp) < 5:
                temp.append('')
            researcher_fields.append(temp)
            
        researcher_citations = []
        for link in researcher_ids:
            num_citations = {1991: '', 1992: '', 1993: '', 1994: '', 1995: '', 1996: '', 1997: '', 1998: '', 1999: '', 2000: '', 2001: '', 2002: '', 2003: '', 2004: '', 2005: '', 2006: '', 2007: '', 2008: '', 2009: '', 2010: '', 2011: '', 2012: '', 2013: '', 2014: '', 2015: '', 2016: '', 2017: '', 2018: '', 2019: '', 2020: '', 2021: '', 2022: '', 2023: ''}
            temp_url = f'/citations?hl=en&user={link}'
            temp_conn = http.client.HTTPSConnection('scholar.google.com')
            temp_conn.request('GET', temp_url)
            temp_obj = temp_conn.getresponse()
            temp_text = temp_obj.read()
            temp_soup = BeautifulSoup(temp_text, 'html.parser')
            stats_div = temp_soup.findAll('div', class_='gsc_md_hist_b')
            years_list = [item.findAll('span', {'class': 'gsc_g_t'}) for item in stats_div]
            years = [int(span.text.strip()) for span in years_list[0]]
            citations_list = [item.findAll('span', {'class': 'gsc_g_al'}) for item in stats_div]
            citations = [int(span.text.strip()) for span in citations_list[0]]
            for year in years:
                if year in num_citations:
                    index = years.index(year)
                    num_citations[year] = citations[index]
            researcher_citations.append(num_citations)
    
        for i in range(10):
            temp=[]
            temp.append(researcher_names[i])
            temp.append(researcher_ids[i])
            temp.extend(researcher_fields[i])
            temp.extend(researcher_citations[i].values())
            data.append(temp)
        
        next_link=soup.findAll('button')[2]['onclick'].split('\\')[9][3:]

non_duplicated_data = []
for l in data:
    if l not in non_duplicated_data:
        non_duplicated_data.append(l)

header = ['author_name', 'author_id', 'field_of_expertise_1', 'field_of_expertise_2', 'field_of_expertise_3', 'field_of_expertise_4', 'field_of_expertise_5', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for row in non_duplicated_data:
        writer.writerow(row)