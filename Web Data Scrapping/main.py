import requests
from bs4 import BeautifulSoup
import csv
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout, TooManyRedirects

def get_article_data(url):
    try:
        response = requests.get(url)
        print("Response status code:", response.status_code)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        print("HTML content:", soup.prettify())

        title_element = soup.find('h1')
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Title not found"

        subtitle_element = soup.find('h2')
        if subtitle_element:
            subtitle = subtitle_element.text.strip()
        else:
            subtitle = "No Subtitle"

        text_elements = soup.find_all('p')
        text = "\n".join([p.text.strip() for p in text_elements])

        image_urls = [img['src'] for img in soup.find_all('img', src=True)]
        num_images = len(image_urls)
        external_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
        num_external_links = len(external_links)

        author_name_element = soup.find('div', class_='ui-caption')
        if author_name_element:
            author_name = author_name_element.text.strip()
        else:
            author_name = "Author Name not found"

        author_url_element = soup.find('a',
                                       class_='ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal')
        if author_url_element:
            author_url = author_url_element.get('href')
        else:
            author_url = "Author URL not found"

        claps_element = soup.find('button',
                                  class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents')
        if claps_element:
            claps = int(claps_element.text.strip())
        else:
            claps = 0

        reading_time_element = soup.find('span', class_='readingTime')
        if reading_time_element:
            reading_time = reading_time_element.get('title')
        else:
            reading_time = "Reading Time not found"

        # keywords = soup.find('meta', attrs={'name': 'keywords'}).get('content')
        keywords_element = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_element:
            keywords = keywords_element.get('content')
        else:
            keywords = "Keywords not found"

        return [title, subtitle, text, num_images, image_urls, num_external_links, author_name, author_url, claps, reading_time, keywords]

    except (RequestException, ConnectionError, HTTPError, Timeout, TooManyRedirects) as e:
        print("Error:", e)
        return None

    except AttributeError as e:
        print("AttributeError:", e)
        print("URL:", url)
        print("Soup:", soup)
        return None

    except Exception as e:
        print("Error scraping article:", e)
        return None

def save_to_csv(data, filename):
    print("Data to be saved:", data)  # Debug statement
    print("Filename:", filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


def main(urls):
    header = ["Title", "Subtitle", "Text", "No. of images", "Image URLs", "No. of external links", "Author Name", "Author URL", "Claps", "Reading Time", "Keywords"]
    with open("scraping_results.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

    for url in urls:
        data = get_article_data(url)
        if data:
            print("Scraped:", data[0])
            save_to_csv(data, "scraping_results.csv")


if __name__ == "__main__":
    urls = [
        "https://www.indiblogger.in/post/sri-lakshmi-narasimmar-temple-avaniyapuram-tiruvannamalai-district-tamil-nadu"
        "https://www.indiblogger.in/post/african-tulip-tree",
        "https://www.indiblogger.in/post/self-worth-698da496e6",
        "https://www.animalarthouse.com/",
        "https://visual.ly/community/Infographics/animals/vic-west-pet-hospital-one-stop-animal-veterinary-care",
        "https://www.amazon.com/stores/page/6B20A11B-F085-4202-A36F-8FF4E822BD3E",
        "https://apps.apple.com/us/app/pre-k-preschool-learning-games/id1398891807",
        "https://www.bloggingfusion.com/listing/florida/florida-city-4/food-delivery-apps/spotneats",
        "https://www.afternic.com/forsale/terragame.com?utm_source=TDFS_DASLNC&utm_medium=parkedpages&utm_campaign=x_corp_tdfs-daslnc_base&traffic_type=TDFS_DASLNC&traffic_id=daslnc&",
        "https://www.washingtonpost.com/politics/",
        "https://mashable.com/",
        "https://www.reddit.com/r/news/comments/1cncwru/contractors_spraypainted_over_propalestinian/?rdt=50430",
        "https://www.bbc.co.uk/news/health-68900203",
        "https://www.bbc.com/news/articles/ck5k0874nzro",
        "https://www.bbc.co.uk/sport/football/68978816",
        "https://milkroad.com/news/ftx-reveals-plan-to-reimburse-creditors-most-will-receive-118-of-claims/",
        "https://milkroad.com/news/donald-trumps-potential-return-could-boost-bitcoin-standard-chartered/",
        "https://www.nature.com/articles/s41586-024-07238-x",
        "https://www.bbc.com/sport/articles/cmm3v9ny78eo",
        "https://www.nature.com/articles/s41586-024-07182-w",
        "https://www.investopedia.com/terms/a/articles-of-association.asp"
    ]
    main(urls)
