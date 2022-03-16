from bs4 import BeautifulSoup
import requests
import pymysql

def clean_string(string):
    clean_string = string.replace('\n', '').replace('\t', '').replace('\r', '').replace("'", " ").strip()
    return clean_string

def get_Projectlisting(searchitem,soup1):
        title = clean_string(searchitem.find('a', {'class': "JobSearchCard-primary-heading-link"}).text).strip()

        description = clean_string(searchitem.find('p', class_='JobSearchCard-primary-description').text).strip()

        List = searchitem.find('div', {'class': "JobSearchCard-primary-tags"})

        a_tags = List.findAll('a')
        Elist = ''
        skills_list = []
        for a in a_tags:
            skills_list.append(a.text)
            Elist = (','.join(skills_list))

        try:
            bid = clean_string(searchitem.find('div', class_='JobSearchCard-primary-price').text).strip()
        except:
            bid = 'NA'

        daysleft = clean_string(searchitem.find('span', {'class': "JobSearchCard-primary-heading-Days"}).text).strip()
        try:
            verified = clean_string(searchitem.find('div', class_='JobSearchCard-primary-heading-status Tooltip--top').text).strip()
        except:
            verified = 'NA'

        searchitems = soup1.find('span', {"itemprop": "addressLocality"})
        if searchitems is not None:
            location = searchitems.text
        else:
            location = 'NA'

        ProjID = soup1.findAll('p', class_="PageProjectViewLogout-detail-tags")
        for i in ProjID:
            if 'Project ID:' in str(i):
                PjtID = i.text.replace("Project ID:", "").replace("#", "")
                get_projectdata(title, description, Elist, bid, daysleft, verified, location, PjtID)
                return

def get_Bidderlisting(soup1):
    search_list = soup1.findAll('div', "FreelancerInfo-body")
    for searchlist in search_list:
        try:
            Freelancer_Name = clean_string(searchlist.find('a', {'class': "FreelancerInfo-username"}).text)
        except:
            Freelancer_Name ='NA'

        try:
            Description = clean_string(searchlist.find('p', {'class': "FreelancerInfo-about"})['data-descr-full'])
            if Description == '': Description='NA'
        except:
            Description='NA'

        try:
            Location = soup1.find('span', {'class': "FreelancerInfo-flag"})
            Freelancer_Location =clean_string(Location.find('span')['aria-label'])

        except:
            Freelancer_Location='NA'

        try:
            Bid_days = clean_string(soup1.find('span', {'class': "FreelancerInfo-price-detail"}).text)
        except:
            Bid_days='NA'

        try:
            Bid_amount = clean_string(soup1.find('div', {'class': "FreelancerInfo-price"}).text).replace(Bid_days, '')
        except:
            Bid_amount = 'NA'

        PjtID = soup1.findAll('p', class_="PageProjectViewLogout-detail-tags")
        for i in PjtID:
            if 'Project ID:' in str(i):
                PjtID = i.text.replace("Project ID:", "").replace("#", "")
                get_bidderdata(Freelancer_Name, Description, Freelancer_Location, Bid_amount, Bid_days, PjtID)
    return


def get_projectdata( title, description, Elist, bid, daysleft, verified, location, PjtID):
    sql = "INSERT INTO `projtable` (`title`,`description`,`skillset`,`bid`, `daysleft`,`verified`,`Location`,`projectID`) VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % (
        title, description, Elist, bid, daysleft, verified, location, PjtID)
    print(sql)
    Cursor.execute(sql)
    Con.commit()


def get_bidderdata(Freelancer_Name, Description, Freelancer_Location, Bid_amount, Bid_days, PjtID):
    sql1 = "INSERT INTO `bidders_details` (`Freelancer name`,`Description`,`Location`, `Bid`,`Duration of bid`,`Project ID`) VALUES ('%s', '%s', '%s','%s','%s','%s')" % (
            Freelancer_Name, Description, Freelancer_Location, Bid_amount, Bid_days, PjtID)
    print(sql1)
    Cursor.execute(sql1)
    Con.commit()


if __name__ == '__main__':
    https_proxy = "https://pptsdma:PpTsDMa2017@158.222.6.183:80"
    proxyDict = {
      "https": https_proxy,
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    Con = pymysql.connect(host="127.0.0.1", user="root", password="", db="hema_workdb", autocommit=True, charset='utf8')
    Cursor = Con.cursor()

    count =10
    total_results = 100
    while (count < total_results):
        count = count+1
        print(count)
        url = 'https://www.freelancer.com/jobs/regions/%s/' % count
        print(url)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        response = requests.get(url, headers=header).text
        soup = BeautifulSoup(response, 'html.parser')
        search_items = soup.findAll('div', {'class': 'JobSearchCard-item'})
        for searchitem in search_items:
            innerurl = searchitem.find('div', "JobSearchCard-primary-heading")
            for a in innerurl.find_all('a', href=True):
                if a.text:
                    UUrl = (a['href'])
                url_ = 'https://www.freelancer.com%s' % UUrl
                print(url_)
                response1 = requests.get(url_, headers=header).text
                soup1 = BeautifulSoup(response1, 'html.parser')
                get_Projectlisting(searchitem, soup1)
                get_Bidderlisting(soup1)
