from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt









#-------------------------------------------SENTIMENT ANALYSIS ----------------------------------------------------------











class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, query):
        # authenticating
        consumerKey = 'N7nYQv7iDQutsN0XOMTW47l1R'
        consumerSecret = 'rLZMF2wjShshiLkT5SO5dsA5XYCnklrVvZym3UuLbzrtewGT7J'
        accessToken = '1058371167482916866-MhtUsgycQYmf39uPFgYvPOgsbtjj4j'
        accessTokenSecret = 'Ld2Dnfqt96ClUgCXAj3psuDCTDxmKdR7LQSYk51o9GA4o'

        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm = query
        NoOfTerms = 150

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            # Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0):
                positive += 1
            elif (analysis.sentiment.polarity < 0):
                negative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)





        self.plotPieChart(positive, negative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, negative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['lightgreen', 'gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        #plt.show()
        plt.savefig('demo.png')









#--------------------------------------------INGREDIENT ANALYSIS----------------------------------------------------------









def fetch():

    # searching
    d = "+".join(l)

    # searching
    my_url = "https://www.goodguide.com/products?utf8=%E2%9C%93&filter="+d+"&button=#/"
    print(my_url)

    # calling the fn
    uClient = urlopen(my_url)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    name = page_soup.find_all("span", {"class": "auto-truncated"})
    try:
        for i in range(0, 8):
            print( i+1, ".", name[i].text),
            print("\n_________________\n")
        c = int(input("Enter the product no. you want to search - "))

    except:
        pass

    productDivs = page_soup.find_all('div', {'class': 'large-2 columns text-center'})
    j = 1
    for div in productDivs:
        if j == c :
          return div.find('a')['href']
          break
        else :
           j = j + 1


'''def details(link):
    my_url = "https://www.goodguide.com/products?utf8=%E2%9C%93&filter="+ d +"&button=#/"
    print(my_url)
    # calling the fn
    uClient = urlopen(my_url)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    name = page_soup.findAll("span", {"class": "auto-truncated"})'''



















#----------------------------------------------MAIN BEGINS--------------------------------------------------------------










if __name__== "__main__":
    a = input("Enter product name  -  ")
    sa = SentimentAnalysis()
    sa.DownloadData(a)
    i=0
    l=a.split(" ")
    k=fetch()
    print(k)
    print("\n\n")
    #if(i==0):
      #details()


