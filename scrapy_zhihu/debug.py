from scrapy import cmdline



def main():
    cmdline.execute(['scrapy', 'crawl', 'login'])

if __name__ == '__main__':
    main()

