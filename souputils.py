import requests, re
from bs4 import BeautifulSoup

def getURL(strUri):
    """ Abre la url pasada como parametro, 
        devuelve un string con el codigo html del sitio. """
    
    headers= {'User-Agent': 'Mozilla/5.0'}
    try:
        strHtml = requests.get(strUri, headers=headers)
        # If a http error related, this will rise a exception (such as 404, 403 etc)
        # http://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
        strHtml.raise_for_status()
    except requests.exceptions.HTTPError as err: 
        print (err)
    except requests.exceptions.Timeout as t:
        print (t)
    except requests.exceptions.RequestException as e: #general exception 
        print (e)
        sys.exit(1)
    # print(html_doc.text) # debug
    #print (html_doc.status_code) # debug
    return strHtml.text

class SoupWrapper:
    
    def __init__(self, strHtml):
        # setting up the soup object
        self.baseStrHtml= str(strHtml)
        self.soupbase=BeautifulSoup(self.baseStrHtml, "lxml")
        
        
    def getAllBlocks (self, strTag): 
        """ Se le pasa un tag especifico para que busque
        todos los elementos que existan en el html. """
        result = self.soupbase.find_all(class_=re.compile(strTag))
        print (type(result))
        print (len(result))
        self.allBlocks = result
    #def extractLink(self):
    def iterator(self, strTag):
        for b in self.allBlocks:
            element = b.find(class_=re.compile(strTag))
            link = element.find("a").attrs['href']
            text = element.text
            print (link)
            print (text)
            print ("----")
        
    def printAllBlocks(self):
        """ va a imprimir el vector.
        if i use the print for result, it is NoneType object. """
        
        for b in self.allBlocks:
            #print (b.prettify()) # debug
            print (b)
            print (type(str(b)))
            print ("--------------------------------")
        
        #return text

if __name__ == '__main__':
    
    uri = "http://pagina12.com.ar"
    #print (getURL(uri)) 
    """ Al wrapper yo le paso el codigo html, significa que no hace 
    falta que le pase todo el sitio, sino la porcion de codigo con la que 
    quiero trabajar. """
    paginaEntera = SoupWrapper(getURL(uri)) 
    paginaEntera.getAllBlocks("^block-articles$")  
    #paginaEntera.printAllBlocks()
    print ("!!!!!!!! COMENZANDO NOTICIA")
    noticias = SoupWrapper(str(paginaEntera.allBlocks[0]))
    print (noticias.soupbase.prettify())
    noticias.getAllBlocks("^article-body$")
    print ("Imprimiendo bloque entero")
    noticias.printAllBlocks()
    print ("Imprimiendo titulo y link")
    noticias.iterator("^article-title-suffix$")
