import nltk
from nltk.tokenize import word_tokenize
from nltk.util import trigrams
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer,LancasterStemmer,SnowballStemmer
from nltk.stem import wordnet, WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.probability import FreqDist
import pandas as pd 
import numpy as np

#smaller
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

#copy pasta-ed
def binary_search(item_list,item):
    first = 0
    last = len(item_list)-1
    found = False
    while( first<=last and not found):
        mid = (first + last)//2
        #print(item)
        #print("YO U MID",mid)
        #print(type(item_list[mid]))
        if item_list[mid] == item :
            found = True
        else:
            if item < item_list[mid]:
                last = mid - 1
            else:
                first = mid + 1	
    return found


samplestring = "My stomach hurts "



def returnMeSymps():
	#tokenize the usersentence
	samplestring_tokens = word_tokenize(samplestring)
	#Filter stop words
	stopWords = set(stopwords.words('english'))
	samplestring_tokens_filtered = []

	for w in samplestring_tokens:
	    if w.lower() not in stopWords:
	        samplestring_tokens_filtered.append(w)
	#Filter punctuation
	samplestring_tokens_filtered_postpunctuation = []
	punctuation = re.compile(r'[-.?!,:;()|]')
	for w in samplestring_tokens_filtered:
	    word = punctuation.sub("",w)
	    if len(word) > 0:
	        samplestring_tokens_filtered_postpunctuation.append(word)

	#List of symtoms all sorted for binary search
	symptoms = pd.read_csv('diagnosis_analysis/sym_t.csv')
	symptoms = symptoms.dropna()
	symstr = ' '.join(symptoms["symptom"])
	#List of key words vs occurences in symptoms, sorted
	rawsymtoken = nltk.word_tokenize(symstr)
	symptokens = [x.lower() for x in rawsymtoken]
	symptokens
	symfdist = FreqDist(symptokens)
	symvocab = sorted(symfdist.keys())
	symoccurences = {}
	for key in symvocab:
	    symoccurences[key] = []
	    for s in symptoms["symptom"]:
	        if key in s.lower():
	            symoccurences[key].append(s)

	SYMPTOMS_LIST = []
	#Let's filter the verbs before we lemma and stem 
	#Not sure if we need to chunk. Depends on possible user language symptoms
	word_lem = WordNetLemmatizer()
	samplestring_verbs = []
	for tkn in samplestring_tokens_filtered_postpunctuation:
	    synonyms = []
	    POStype = nltk.pos_tag([tkn])
	    print(POStype)
	    result = binary_search(symvocab,POStype[0][0].lower())
	    if result == True:
	        print(POStype[0][0].upper(),"EXISTS1") #the word user type exists as it is in list of symptoms
	        print(symoccurences[POStype[0][0].lower()])
	        SYMPTOMS_LIST.append(symoccurences[POStype[0][0].lower()])
	        #no need to go and find all these synonyms as we can go find the symptoms
	    syns1 = wordnet.synsets(POStype[0][0])
	    print("From the original",syns1)
	    for x in syns1:
	        #this loop only looks through the 1st level synonym
	        syns1type = re.search('^(.*?)\..*',x.name()).group(0)
	        if not (syns1type == "n" and POStype[0][1][0].lower() == "v") or (syns1type == "v" and POStype[0][1][0].lower() == "n"):
	            #at least no unnecessary search bet noun and verb
	            keyword = x.name().lower().split(".")[0]
	            print("KEYWORD",keyword)
	            if keyword != POStype[0][0].lower() and keyword not in synonyms:
	                synonyms.append(keyword)
	                print("SEARCHING FOR...",keyword)
	                result = binary_search(symvocab,keyword)
	                if result == True:
	                    print(keyword.upper(),"EXISTS2") #a direct synonym of the user word exist in the list
	                    print(symoccurences[keyword])
	                    SYMPTOMS_LIST.append(symoccurences[keyword])
	            #let's look at the other nyms
	            others = []
	            hypernyms = [others.append(y.name().lower().split(".")[0]) for y in x.hypernyms()]
	            for i,j in enumerate(x.hypernyms()):
	                #print("HYPONYM",x.hypernyms()[i].hyponyms())
	                for z in x.hypernyms()[i].hyponyms():
	                    others.append(z.name().lower().split(".")[0])
	            lemmas = [others.append(l.lower()) for l in x.lemma_names()]
	            print("OTHERS",others)
	            for word in others:
	                if word not in synonyms:
	                    synonyms.append(word)
	                    print("SEARCHING FOR...",word)
	                    result = binary_search(symvocab,word)
	                    if result == True:
	                        print(word,"EXISTS3")
	                        print(symoccurences[word])
	                        SYMPTOMS_LIST.append(symoccurences[word])
	return SYMPTOMS_LIST
	                

