import souputils


if __name__ == "__main__":
    uri2 = "https://www.pagina12.com.ar/16889-el-poder-de-la-memoria"
    pagina = souputils.SoupHelper(souputils.getURL(uri2))
    pagina.getBlock("^article-date$", 1)
    print(pagina.findAttrs("time","datetime"))
    

