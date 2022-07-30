import spacy
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/MAD_I_BDAD')
table = client['MAD_I_BDAD']['OLTP_SpeechData']
table2 = client['MAD_I_BDAD']['users']

nlp = spacy.load("en_core_web_sm")

def textProcessing(doc):
    Nouns = []
    Noun_set = []
    trimmed_noun_set = []
    removing_duplicates = []
    arr = []
    vocab = []
    vocab_dict = {}
    
    doc = nlp(doc.upper())

    for possible_nouns in doc:
        if possible_nouns.pos_ in ["NOUN","PROPN"] :
            Nouns.append([possible_nouns , [child for child in possible_nouns.children]])
       
    
    for i,j in Nouns:
        for k in j:
            Noun_set.append([k,i])

    
    for i , j in Noun_set:
        if i.pos_ in ['PROPN','NOUN','ADJ']:
            trimmed_noun_set.append([i ,j])
            
    
    for word in trimmed_noun_set:
        if word not in removing_duplicates:
            removing_duplicates.append(word)
    
    
    for i in removing_duplicates:
        strs = ''
        for j in i:
            strs += str(j)+" "
        arr.append(strs.strip())

    
    for word in Noun_set:
        string = ''
        for j in word:
            string+= str(j)+ " "
        vocab.append(string.strip())

    
    for word in vocab:
        vocab_dict[word]= 0
        
    for word in arr:
        vocab_dict[word]+= 1

    return vocab_dict , arr

def computeTF(wordDict,bow):
    '''Computing TF(Term Frequency of the vocab) '''
    try:
        tfDict = {}
        bowCount = len(bow)
        for word, count in wordDict.items():
            tfDict[word] = count/float(bowCount)
        return tfDict
    except ZeroDivisionError:
        print('No recognisable nouns detected please try again.')
        return False

def computeIDF(doclist):
    '''Computing IDF for the vocab '''
    import math 
    count = 0
    idfDict = {}
    for element in doclist:
        for j in element:
            count+=1
    N = count
    
    idfDict = dict.fromkeys(doclist[0].keys(),0)

    for doc in doclist:
        for word,val in doc.items():
            if val>0:
                idfDict[word]+= 1

    for word,val in idfDict.items():
        if val == 0:
            idfDict[word] = 0.0
        else:
            idfDict[word] = math.log(N / float(val))

    return idfDict

def computeTfidf(tf,idf):

    tfidf = {}
    sorted_list = []
    for word , val in tf.items():
        tfidf[word] = val * idf[word]

    ranking_list  = sorted(tfidf.items(),reverse=True, key = lambda kv:(kv[1], kv[0]))[:10]
    for i, _ in ranking_list:
        sorted_list.append(i)

    return sorted_list

def topic_ext(text):
    vocab_dict , arr = textProcessing(text)
    tf = computeTF(vocab_dict,arr)
    if(tf != False):
        idf = computeIDF([vocab_dict])
        tfidf = computeTfidf(tf,idf)
        return tfidf

def extract():
    data = table.find()
    return data

def transform(data):
    transformed_data = {}
    for i in data:
        transformed_data[i['user_id']] = topic_ext(i['string'])
        deli = table.delete_one({'user_id': i['user_id']})
        print(deli)
    return transformed_data

def load(t):
    for i in t:
        print(i)
        temp = table2.find_one(ObjectId(i))
        if len(temp['tags']) >= 100:
            s = table2.update_many(
                { "_id": ObjectId(i) },
                { "$push": { "tags": { "$each": [], "$slice": len(temp['tags']) } }
             }
            )
            for j in t[i]:
                table2.update_many(
                    { "_id": ObjectId(i) },
                    {'$push': {'tags': j}}
                )
        else:
            for j in t[i]:
                table2.update_many(
                    { "_id": ObjectId(i) },
                    {'$push': {'tags': j}}
                )   
    return 0

d = extract()
print(d)
t = transform(d)
for i in t:
    print(i, ":", t[i])
l = load(t)
print(l)
