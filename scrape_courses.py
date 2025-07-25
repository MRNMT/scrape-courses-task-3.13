import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_courses():
    url = "https://test-scrape-site.onrender.com/courses.html"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    course_divs = soup.find_all('div', class_='course')

    courses = []
    for course in course_divs:
        course_code = course.get('data-id', 'N/A')
        title = course.find('h3').get_text(strip=True) if course.find('h3') else 'N/A'
        instructor_text = course.find('p').get_text(strip=True) if course.find('p') else 'N/A'
        # instructor_text is like "Instructor: Dr. Ada Lovelace" so we split on ":"
        instructor = instructor_text.split(":", 1)[1].strip() if ":" in instructor_text else instructor_text
        credits = course.find('span', class_='credits').get_text(strip=True).replace('Credits: ', '') if course.find('span', class_='credits') else 'N/A'
        duration = course.find('span', class_='duration').get_text(strip=True).replace('Duration: ', '') if course.find('span', class_='duration') else 'N/A'
        level = course.find('span', class_='level').get_text(strip=True).replace('Level: ', '') if course.find('span', class_='level') else 'N/A'

        courses.append({
            'Course Code': course_code,
            'Course Title': title,
            'Instructor': instructor,
            'Credits': credits,
            'Duration': duration,
            'Level': level
        })

    # Convert to DataFrame
    df = pd.DataFrame(courses)

    # Save to Excel
    excel_filename = "courses_data.xlsx"
    df.to_excel(excel_filename, index=False)

    print(f"Scraped {len(courses)} courses and saved to {excel_filename}")

if __name__ == "__main__":
    scrape_courses()
