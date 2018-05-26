from bs4 import BeautifulSoup
import urllib, bs4, re
import googlesearch
import whois
import datetime
import time
import phishtank
import socket


#if url contains ip addresses instead of name
def have_ip_address(url):
    match=re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  #IPv4
                    '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  #IPv4 in hexadecimal
                    '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',url)     #Ipv6
    if match:
        return -1
    else:
        return 1

#length of urls
def url_length(url):
    if len(url)<54:
        return 1
    elif len(url)>=54|len(url)<=75:
        return 0
    else:
        return -1

#if url contains shortening services
def url_shortener(url):
    match=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)

    if match:
        return -1
    else:
        return 1

#url having @ symbol
def have_atrate_symbol(url):
    match = re.search('@',url)

    if match:
        return -1
    else:
        return 1

#double slash redirecting
def double_slash_redirect(url):
    list = [x.start(0) for x in re.finditer('\\.',url)]
    if list[len(list)-1]>6:
        return -1
    else:
        return 1


#having hyphen in urls
def prefix_suffix(url):
    match = re.search('-',url)
    if match:
        return -1
    else:
        return 1

#finding subdomains in a domain
def have_subdomain(url):
    if(have_ip_address(url)==-1):
        match = re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5]))|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',url)
        pos = match.end(0)
        url = url[pos:]
    list = [x.start(0) for x in re.finditer('\.',url)]
    if len(list)<=3:
        return 1
    elif len(list) == 4:
        return 0
    else:
        return -1

#SSHFinal

#Domain_registration_length
def domain_registration_length(domain):
    expiry_date = domain.expiration_date
    today = time.strftime("%Y-%m-%d")
    today_date = datetime.datetime.strptime(today,"%Y-%m-%d")
    registration_length = abs((expiry_date - today_date).days)

    if registration_length / 365 <= 1:
        return -1
    else:
        return 1

#website has favicon

def favicon(wiki,soup,domain):
    for head in soup.find_all('link'):
        for head.link in soup.find_all('link',href=True):
            dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
            if wiki in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                return 1
            else:
                return -1
    return 1

#Checking Ports
status_port = []
import socket
def isOpen(url,port_numbers):
    for port in port_numbers:
        ip = socket.gethostbyname(url)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            s.shutdown(2)
            status_port.append(0)
        except:
            status_port.append(1)
    if(status_port[3] == 0 & status_port[4] == 0):
        if(status_port[0] == 1 & status_port[1] == 1 & status_port[2] == 1):
            return -1
        else:
            return -1
    else:
        return 1

#http tokens
def https_token(url):
    match = [(x.start(0), x.end(0)) for x in re.finditer('https:// | http:// | http | https', url)]

    if len(match)!= 1:
        return -1
    else:
        return 1


#Request URLs
def request_url(wiki, soup, domain):
    i = 0
    success = 0
    for img in soup.find_all('img',src=True):
        dots = [x.start(0) for x in re.finditer('\.',img['src'])]
        if wiki in img['src'] or domain in img['src'] or len(dots)==1:
         success = success + 1
        i=i+1

    for audio in soup.find_all('audio', src= True):
      dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
      if wiki in audio['src'] or domain in audio['src'] or len(dots)==1:
         success = success + 1
      i=i+1

    for embed in soup.find_all('embed', src= True):
      dots=[x.start(0) for x in re.finditer('\.',embed['src'])]
      if wiki in embed['src'] or domain in embed['src'] or len(dots)==1:
         success = success + 1
      i=i+1

    for iframe in soup.find_all('iframe', src= True):
      dots=[x.start(0) for x in re.finditer('\.',iframe['src'])]
      if wiki in iframe['src'] or domain in iframe['src'] or len(dots)==1:
         success = success + 1
      i=i+1

    try:
       percentage = success/float(i) * 100
    except:
        return 1

    if percentage < 22.0 :
       return 1
    elif((percentage >= 22.0) and (percentage < 61.0)) :
       return 0
    else :
       return -1


#url anchor tags
def url_of_anchor(wiki, soup, domain):
    i = 0
    unsafe=0
    for a in soup.find_all('a', href=True):
        if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (wiki in a['href'] or domain in a['href']):
            unsafe = unsafe + 1
        i = i + 1
    try:
        percentage = unsafe / float(i) * 100
    except:
        return 1
    if percentage < 31.0:
        return 1
    elif ((percentage >= 31.0) and (percentage < 67.0)):
        return 0
    else:
        return -1


# Links in <Script> and <Link> tags
def links_in_tags(wiki, soup, domain):
   i=0
   success =0
   for link in soup.find_all('link', href= True):
      dots=[x.start(0) for x in re.finditer('\.',link['href'])]
      if wiki in link['href'] or domain in link['href'] or len(dots)==1:
         success = success + 1
      i=i+1

   for script in soup.find_all('script', src= True):
      dots=[x.start(0) for x in re.finditer('\.',script['src'])]
      if wiki in script['src'] or domain in script['src'] or len(dots)==1 :
         success = success + 1
      i=i+1
   try:
       percentage = success / float(i) * 100
   except:
       return 1

   if percentage < 17.0 :
      return 1
   elif((percentage >= 17.0) and (percentage < 81.0)) :
      return 0
   else :
      return -1


# Server Form Handler (SFH)
###### Have written consitions directly from word file..as there are no sites to test ######
def sfh(wiki, soup, domain):
   for form in soup.find_all('form', action= True):
      if form['action'] =="" or form['action'] == "about:blank" :
         return -1
      elif wiki not in form['action'] and domain not in form['action']:
          return 0
      else:
            return 1
   return 1

#Mail Function
###### PHP mail() function is difficult to retreive, hence the following function is based on mailto ######
def submitting_to_email(soup):
   for form in soup.find_all('form', action= True):
      if "mailto:" in form['action'] :
         return -1
      else:
          return 1
   return 1



#Abnormal URLs
def abnormal_url(domain,url):
    hostname=domain.name
    match=re.search(hostname,url)
    if match:
        return 1
    else:
        return -1


#IFrame Redirection
###### Checking remaining on some site######
def iframe(soup):
    for iframe in soup.find_all('iframe', width=True, height=True, frameBorder=True):
        if iframe['width']=="0" and iframe['height']=="0" and iframe['frameBorder']=="0":
            return -1
        else:
            return 1
    return 1

#Age of Domain
def age_of_domain(domain):
    creation_date = domain.creation_date
    expiration_date = domain.expiration_date
    ageofdomain = abs((expiration_date - creation_date).days)
    if ageofdomain / 30 < 6:
        return -1
    else:
        return 1

#Traffic on website using Alexa
def web_traffic(url):
    try:
        rank = bs4.BeautifulSoup(urllib.request("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
    except TypeError:
        return -1
    rank= int(rank)
    if (rank<100000):
        return 1
    else:
        return 0


#Google Index
def google_index(url):
    site=googlesearch.search(url, 5)
    if site:
        return 1
    else:
        return -1


def statistical_report(url,hostname):
    url_match=re.search('esy\.es | hol\.es | 	000webhostapp\.com | 16mb\.com | bit\.ly | for-our\.info | beget\.tech | blogspot\.com | weebly\.com |raymannag\.ch',url)
    try:
        ip_address=socket.gethostbyname(hostname)
    except:
        print ('Connection problem. Please check your internet connection!')
##### 1st line is phishtank top 10 domain ips and 2nd, 3rd, 4th, 5th, 6th lines are top 50 domain ips from stopbadware #####
    ip_match=re.search('146\.112\.61\.108 | 31\.170\.160\.61 | 67\.199\.248\.11 | 67\.199\.248\.10 | 69\.50\.209\.78 | 192\.254\.172\.78 | 	216\.58\.193\.65 | 23\.234\.229\.68 | 173\.212\.223\.160 | 60\.249\.179\.122',ip_address)
    if url_match:
        return -1
    elif ip_match:
        return -1
    else:
        return 1


def main(url):
    with open('markup.txt', 'r', encoding='utf-8') as file:
        soup_string=file.read()

    soup = BeautifulSoup(soup_string, 'html.parser')

    status=[]

    hostname = url
    h = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
    z = int(len(h))
    if z != 0:
        y = h[0][1]
        hostname = hostname[y:]
        h = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
        z = int(len(h))
        if z != 0:
            hostname = hostname[:h[0][0]]

    status.append(have_ip_address(url))
    status.append(url_length(url))
    status.append(url_shortener(url))
    status.append(have_atrate_symbol(url))
    status.append(double_slash_redirect(url))
    status.append(prefix_suffix(hostname))
    status.append(have_subdomain(url))
    # status.append(sslfinal_state(url))

    dns=1
    try:
        domain = whois.query(hostname)
    except:
        dns=-1

    if dns==-1:
        status.append(-1)
    else:
        status.append(domain_registration_length(domain))

    status.append(favicon(url,soup, hostname))

    port_numbers = [21,22,23, 80,443]
    status.append(isOpen(url,port_numbers))
    status.append(https_token(url))
    status.append(request_url(url, soup, hostname))
    status.append(url_of_anchor(url, soup, hostname))
    status.append(links_in_tags(url,soup, hostname))
    status.append(sfh(url,soup, hostname))
    status.append(submitting_to_email(soup))

    if dns == -1:
        status.append(-1)
    else:
        status.append(abnormal_url(domain,url))

    # status.append(redirect(url))
    status.append(iframe(soup))

    if dns == -1:
        status.append(-1)
    else:
        status.append(age_of_domain(domain))

    status.append(dns)

    status.append(web_traffic(soup))
    status.append(google_index(url))
    status.append(statistical_report(url,hostname))

    print ('\n1. Having IP address\n2. URL Length\n3. URL Shortening service\n4. Having @ symbol\n5. Having double slash\n' \
          '6. Having dash symbol(Prefix Suffix)\n7. Having multiple subdomains\n8888. SSL Final State\n8. Domain Registration Length\n9. Favicon\n' \
          '10. HTTP or HTTPS token in domain name\n11. Request URL\n12. URL of Anchor\n13. Links in tags\n' \
          '14. SFH\n15. Submitting to email\n16. Abnormal URL\n(removed temporarily)11117. Redirect\n17. IFrame\n18. Age of Domain\n19. DNS Record\n20. Web Traffic\n' \
          '21. Google Index\n22. Statistical Reports\n')
    print (status)
    return status

if __name__ == "__main__":
    main()
