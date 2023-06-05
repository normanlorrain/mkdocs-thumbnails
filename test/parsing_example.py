# import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


html = """
<a class="pdf" href="appendix%20one.pdf"><img class="pdf" src="appendix%20one.pdf-thumb.png" style=""/>Appendix one</a>
"""
if __name__ == "__main__":
    soup = BeautifulSoup(html, "html.parser")
    # pdf links
    links = soup.find_all("a")
    for link in links:
        pass
