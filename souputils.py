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

class SoupHelper:
    
    def __init__(self, strHtml):
        # setting up the soup object
        self.baseStrHtml= str(strHtml)
        self.soupbase=BeautifulSoup(self.baseStrHtml, "lxml")
        
    def getBlock(self, strTag, l): 
        """ A diferencia de getAllBlocks, puedo es un wrapper de
        find_all para setear el limite de la cantidad de resultados. """
        result = self.soupbase.find_all(class_=re.compile(strTag), limit=l)
        print (type(result))
        print (len(result))
        self.block = result[0]
        
    def getAllBlocks (self, strTag): 
        """ Se le pasa un tag especifico para que busque
        todos los elementos que existan en el html. """
        result = self.soupbase.find_all(class_=re.compile(strTag))
        print (type(result))
        print (len(result))
        self.allBlocks = result
    #def extractLink(self):
    def findAttrs (self, strTag, strAttrs):
        """ Busca el atributo un objeto del tipo soup, y devuelve el valor. """ 
        #print (self.block.attrs)
        #print (strTag)
        try:
            r = str(self.block.find(strTag).attrs[strAttrs]) 
        except AttributeError as e:
            r = "Error with tag: " + strTag 
            #r = "Error with tag: " + strTag + str(e)
        except KeyError as e: 
            r = "Error with attribute: " + str(e)
        return r 
        
    def linksInBlocks(self, strTag):
        """ Recorre self.allBlocks buscando el link y el texto.
        Recibe un string con el tag a buscar. 
        Setea dictLinks, un diccionario con el par link / text. """
        
        self.dictLinks = {}
        for b in self.allBlocks:
            print ("strTag: " + strTag)
            print (b)
            element = b.find(class_=re.compile(strTag))
            link = element.find("a").attrs['href']
            text = element.text
            self.dictLinks[link] = text
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
    
    def getTextDivBlock(self, strTag):
        # Agregar excepcion en caso de NoneType
        return str(self.allBlocks[0].find(class_=re.compile(strTag)))

if __name__ == '__main__':
    
    
    ### LEYENDO BLOQUE general ###
    uri = "http://pagina12.com.ar"
    #print (getURL(uri)) 
    """ Al wrapper yo le paso el codigo html, significa que no hace 
    falta que le pase todo el sitio, sino la porcion de codigo con la que 
    quiero trabajar. """
    paginaEntera = SoupHelper(getURL(uri)) 
    paginaEntera.getAllBlocks("^block-articles$")  
    #paginaEntera.printAllBlocks()
    print ("!!!!!!!! COMENZANDO NOTICIA")
    noticias = SoupHelper(str(paginaEntera.allBlocks[0]))
    print (noticias.soupbase.prettify())
    noticias.getAllBlocks("^article-body$")
    print ("Imprimiendo bloque entero")
    noticias.printAllBlocks()
    print ("Imprimiendo titulo y link")
    # No todos los bloques tienen suffix, 
    # agregar un metodo que verifique la existencia del  bloque
    # agregar un handler para la excepcion de que no exista un tag
    #noticias.linksInBlocks("^article-title-suffix$")
    noticias.linksInBlocks("^article-title")
    #for (link, text) in noticias.dictLinks.items():
    #    print ("links is: " + link + "text is: " + text)
        #newUrl = uri + link 
        #paginaEntera = SoupHelper(get
        
    ####### Trabajando con una noticia #####
    uri2 = "https://www.pagina12.com.ar/16889-el-poder-de-la-memoria"
    pagina = SoupHelper(getURL(uri2))
    pagina.getAllBlocks("^article-text$")
    
    
    #print (type(pagina.allBlocks[0]))
    print (pagina.allBlocks[0].text)
    pagina.getBlock("^article-date$", 1)
    print(pagina.findAttrs("time","datetime"))
    
        
        
