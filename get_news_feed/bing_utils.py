import requests, re, string

def fetch_page(url,filename):
    try:
        rsp = requests.get(url)
        with open(filename,'wb') as file:
            for block in rsp.iter_content(1024):
                file.write(block)
                
    except:
        pass

def remove_tag(word,html):
    start_tag = '<{}>'.format(word)
    end_tag = '</{}>'.format(word)
    html = html.replace(start_tag,'')
    html = html.replace(end_tag,'')
    return html

def remove_nonprintable(text):
    text = ''.join(filter(lambda x: x in string.printable, text))
    return text