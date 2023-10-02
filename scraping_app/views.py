from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

def scrape_data(request):
    url = 'https://tradingeconomics.com/commodity/wool'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx responses

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the div with id 'ctl00_ContentPlaceHolder1_ctl00_ctl01_Panel1'
            panel_div = soup.find('div', {'id': 'ctl00_ContentPlaceHolder1_ctl00_ctl01_Panel1'})

            if panel_div:
                # Extract the content of the specific div
                div_content = panel_div

                # Find the table within the div
                table = div_content.find('table')

                if table:
                    # Extract table headers
                    headers = [header.text.strip() for header in table.find_all('th')]

                    # Extract table rows
                    rows = []
                    for row in table.find_all('tr')[1:]:  # Skip the header row
                        row_data = [data.text.strip() for data in row.find_all('td')]
                        rows.append(row_data)

                    # Create a JSON response with key-value pairs
                    response_data = {}
                    for i in range(1, len(headers)):  # Skip the first (blank) header
                        key = headers[i].lower().replace(" ", "_")  # Convert header to lowercase and replace spaces with underscores for keys
                        value = rows[0][i]
                        
                        # Convert AUD/100Kg to INR/100Kg for the unit field
                        if key == "unit":
                            response_data[key] = "INR/100Kg"
                        elif key == "actual" or key == "previous" or key == "highest" or key == "lowest":
                            try:
                                value_in_aud_100kg = float(value)
                                value_in_inr_100kg = round(value_in_aud_100kg * 50, 2)  # Convert to INR/100Kg
                                response_data[key] = str(value_in_inr_100kg)
                            except ValueError:
                                response_data[key] = value
                        else:
                            response_data[key] = value

                    # Return the JSON response with indentation for readability
                    return JsonResponse(response_data, json_dumps_params={'indent': 4})

    except requests.exceptions.RequestException as e:
        # Handle any request exceptions here
        return JsonResponse({'error': f'Failed to fetch data from the website: {str(e)}'})

    except Exception as e:
        # Handle other exceptions here
        return JsonResponse({'error': f'An error occurred: {str(e)}'})

    # If the scraping fails, return an error
    return JsonResponse({'error': 'Failed to scrape data from the website'})
