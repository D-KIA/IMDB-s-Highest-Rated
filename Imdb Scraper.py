from selenium import webdriver
from selenium.webdriver.common.by import By
from csv import writer

# Class for Flipkart Scraping
class IMDB:

    # Constants
    base_url = 'https://www.imdb.com/chart/top/'
    driver = webdriver.Chrome()
    driver.get(base_url)

    def __init__(self, max_rank):
        self.max_rank = max_rank

    # Make new CSV
    def new_csv(self):
        f = open('IMDB.csv', 'w', encoding='utf8')  ## opening file in write mode
        thewriter = writer(f)
        headers = ['Rank', 'Name', 'Release', 'Director', 'Stars']  ## Adding Headers
        thewriter.writerow(headers)

    # Add to existing CSV
    def add_csv(self, data):
        f = open('IMDB.csv', 'a', encoding='utf8')  ## opening file in write mode
        thewriter = writer(f)
        thewriter.writerow(data)

    # Movie Scraper
    def scraper(self):
        self.new_csv()

        try:
            top = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/span/div/div/div[3]/table/tbody').\
                find_elements(By.TAG_NAME, 'tr')
        except Exception as e:
            top = []
            print(e)

        r = 0
        while r < self.max_rank:

            # Getting Rank
            try:
                rank = int(top[r].find_element(By.CSS_SELECTOR, 'td[class="titleColumn"]').text.split('.')[0])
            except:
                rank = None

            # Getting Movie name
            try:
                name = top[r].find_elements(By.TAG_NAME, 'a')[1].text
            except:
                name = None

            # Getting Release Date
            try:
                release = int(top[r].find_element(By.CSS_SELECTOR, 'span[class="secondaryInfo"]').text[1:-1])
            except:
                release = None

            # Getting Director's name
            try:
                director = top[r].find_element(By.CSS_SELECTOR, 'td[class="titleColumn"]').\
                    find_element(By.TAG_NAME, 'a').get_attribute('title').split(',')[0][:-6]
            except:
                director = None

            # Getting Star Rating
            try:
                stars = float(top[r].find_element(By.CSS_SELECTOR, 'td[class="ratingColumn imdbRating"]').text)
            except:
                stars = None

            content = [rank, name, release, director, stars]

            self.add_csv(content)
            r += 1

# Main
try:
    print('Just press "Enter" for top 50')
    max_rank = int(input('Till which rank do you need: '))
except:
    print('Using Default Value(50)')
    max_rank = 50           #<----- Default Value

test = IMDB(max_rank).scraper()
