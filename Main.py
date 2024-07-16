import requests
from bs4 import BeautifulSoup
import urllib3

# Disable the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url="https://hprera.nic.in/PublicDashboard/GetFilteredProjectsPV?DistrictList%5B0%5D.Selected=false&DistrictList%5B0%5D.Value=18&DistrictList%5B1%5D.Selected=false&DistrictList%5B1%5D.Value=24&DistrictList%5B2%5D.Selected=false&DistrictList%5B2%5D.Value=20&DistrictList%5B3%5D.Selected=false&DistrictList%5B3%5D.Value=23&DistrictList%5B4%5D.Selected=false&DistrictList%5B4%5D.Value=25&DistrictList%5B5%5D.Selected=false&DistrictList%5B5%5D.Value=22&DistrictList%5B6%5D.Selected=false&DistrictList%5B6%5D.Value=26&DistrictList%5B7%5D.Selected=false&DistrictList%5B7%5D.Value=21&DistrictList%5B8%5D.Selected=false&DistrictList%5B8%5D.Value=15&DistrictList%5B9%5D.Selected=false&DistrictList%5B9%5D.Value=17&DistrictList%5B10%5D.Selected=false&DistrictList%5B10%5D.Value=16&DistrictList%5B11%5D.Selected=false&DistrictList%5B11%5D.Value=19&PlottedTypeList%5B0%5D.Selected=false&PlottedTypeList%5B0%5D.Value=P&PlottedTypeList%5B1%5D.Selected=false&PlottedTypeList%5B1%5D.Value=F&PlottedTypeList%5B2%5D.Selected=false&PlottedTypeList%5B2%5D.Value=M&ResidentialTypeList%5B0%5D.Selected=false&ResidentialTypeList%5B0%5D.Value=R&ResidentialTypeList%5B1%5D.Selected=false&ResidentialTypeList%5B1%5D.Value=C&ResidentialTypeList%5B2%5D.Selected=false&ResidentialTypeList%5B2%5D.Value=M&AreaFrom=&AreaUpto=&SearchText="

child_url="https://hprera.nic.in/Project/ProjectRegistration/PromotorDetails_PreviewPV"

def web_scrape(url,child_url):

    page1 = requests.get(url,verify=False)  #sends HTTP GET request to url and verify is set to false because it is use ignore SSL certificates warnings
    soup1 = BeautifulSoup(page1.content,"html.parser")  #parses the HTML page content using BeautifulSoup 
    find_anchor = soup1.find_all('a', attrs={"data-qs": True})  #finds all <a> tag with with 'data-qs' attributes
    final_data = []
    for projects in find_anchor[:6]:  
        query_string = projects["data-qs"]  #extracts the value of the 'data-qs' attribute from the current <a> tag and stores it in the variable query_string

        payload = {
        "qs": query_string,
        "UpdatedChangeDets": "N"  
        }
        page2=requests.get(child_url,verify=False,params=payload)
        soup2=BeautifulSoup(page2.content,"html.parser")
        find_tr=(soup2.find_all('tr'))
        dic_element = {}
        for element in find_tr:
            # print(i)
            gst_element = element.find('td', string='GSTIN No.')
            if gst_element:
                tag_data = gst_element.find_next_sibling('td').find('span', class_='text-orange font-xs')
                if tag_data:
                    dic_element['GST NO'] = tag_data.string
                

            pan_element = element.find('td', string='PAN No.')
            if pan_element:
                tag_data = pan_element.find_next_sibling('td').find('span', class_='mr-1 fw-600')
                if tag_data:
                    dic_element['PAN No.'] = tag_data.string

            name_element = element.find('td', string='Name')
            if name_element:
                tag_data = name_element.find_next_sibling('td')
                if tag_data:
                    dic_element['Name'] = tag_data.string

            address_element= element.find('td', string='Permanent Address')
            if address_element:
                tag_data = address_element.find_next_sibling('td').find('span', class_='fw-600')
                if tag_data:
                    dic_element['Permanent Address.'] = tag_data.string
        final_data.append(dic_element)
    
    return (final_data)


    

    

