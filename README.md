# MAD-I-adsense-for-audio-data
 * Python Flask webapp, collects audio data of users through a vanilla JS frontend.
 * Shows advertisement recommendations for user personalization. 
 * Semi structured data stored in MongoDB cluster, Transaction of data using ETL Pipelines developed in python. Extraction of keywords done by TF IDF

### System Overview.
![System flowchart](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/ProgressModel2.drawio.png)

### Project Walkthrough.
Here, We have used HTML5 and CSS3 with Bootstrap5 framework to design good looking and responsive webpages. Here for development of this frontend of the web application. The first and the default page was of the login page.

![System flowchart](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/Picture1.jpg)

User can use their provided username and password to login to the web application. This details has been stored in the users table. In the backend, using flask framework and python we are verifying a valid and authenticate user login.

![](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/carbon.png)

After verifying a successful user login, we will implement a best search algorithm and based on that we will find a best fit advertisement for that particular user and get’s total of that three tags and passes it to the further route of index.

![System flowchart](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/Picture3.jpg)

As we can see here at max total of 3 best fit advertisement recommendation will be passed to the further. And the audio data of a user also will be provided on the index page.

### Index Page.
The index page is the primary page of the web application here lies the code of fetching the audio data of user and sending it to the backend to store it in the OLTP_SpeechData database. Here also we shows some recommendation that has been provided us by the login page so let’s first see about index page. Also built using BootStrap5 and HTML5, basic JavaScript for animations.

![](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/Picture2.jpg)

This recommendation has been generated based on the best fit of the advertisement tags and tags associated with user. These associated tags are based on the user’s speech data.
Now to fetch this audio data we need some mechanism to extract data from frontend convert that into speech data and some how send it to the backend. To extract speech data and convert into the text we are using basic JavaScript modules and their inbuilt functions to achieve our goals.

![](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/carbon2.png)

From the login route we have been provided with three advertisement recommendations. First of all we are using speech recognition module and it’s SpeechRecognition function which we will use to recognize user’s speech from the raw audio data.


### Key-word extraction.
TF-IDF is a measure of originality of a word by comparing the number of times a word appears in a doc with the number of docs the word appears in.
TF-IDF = TF(t,d) * IDF(t)
Terminology – 
t – term/word
d – document
N -  Number of documents
corpus – the set of documents

Since we are only taking one continuous speech number of documents will be 1.

![ComputeTF](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/computeTF.png)

TF(t,d) = count of t in d/ number of words in d
In simple words, we are getting the ratio of count of a particular word upon the total number of words. For example in the sentence – “Data science is the analysis of data to get insights“, 
TF(‘data’) = 2/10

![ComputeIDF](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/computeIDF.png)

IDF(t) = log(N/ df(t))
Here, df(t) = occurrence of t in documents
In simple words, it measures informativeness of term t, IDF is will be very low for common words such as stop words is,the,A,etc. Hence, they will be unimportant for overall data extraction allowing us to focus more on topic words.

![ComputeTFIDF](https://github.com/AdityaLakkad/MAD-I-adsense-for-audio-data/blob/main/Project%20Docs/computetfidf%20and%20topic%20extraction.png/)

We have to get key words from a single sentence; hence we have to do extra filtering to get accurate output. For this, we have applied filter that will only return nouns and proper nouns. We accomplish that through POS tagging. We convert all words from the sentence to upper case so as to avoid problems with upper- and lower-case words, next we add all words that are classified as nouns or proper nouns and also their child nodes if any, to a list. Later if there are any duplicates, we remove those as well.

The output we got from the above function is passed on to TF function, we get the ratio as output. If in an unusual case, there are no nouns or proper nouns identified in the sentence it will give us an ‘No recognisable nouns detected please try again.’ Message and not carry out the remaining function

After that we calculate the output of IDF function, and save it. And finally, we multiply both outputs to get our TF-IDF output. An additional step is we sort the output value for each term in descending way so it gives us the most relevant term first and least relevant term last, and then match those values with their terms to give us the aforementioned terms in descending order of their TF-IDF values. And this is how we get keyword extraction from a sentence

