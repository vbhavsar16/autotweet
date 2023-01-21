import numpy as np

with open('tweets.txt',encoding='utf8') as tf:
    ########## Tweet generatoion using President Trump's tweets ##########
    #tweets = [line for line in tf.read().split('\n') if len(line)>0 and line.startswith('RealDonaldTrump') ]
    ########## Tweet generatoion using President Obama's tweets ##########
    tweets = [line for line in tf.read().split('\n') if len(line)>0 and line.startswith('BarackObama') ]
    
def join_string(list_string):
    string = ' '.join(list_string)
    return string

def next(pin):
    # pin might be a list not a numpy array
    p = np.array(pin)
    #print(p)
    csp = p.cumsum()
    #print(csp)
    r = np.random.rand()
    #print('r=',r)
    #print(r < csp)
    i = (r<csp).argmax()  # index of first True in r<csp
    return i

counts = {}
probability = {}
for tweet in tweets:
    #print(tweet)
    #words = tweet[2:].lower().split()
    
    words = tweet.lower().split()
    words = words[2:]
    words = [word for word in words if not word.startswith('http')]
    new_string = join_string(words)
    words = new_string.replace('#',' #').replace('.',' .').replace('!',' !').replace(',',' ,').replace(':',' :').replace(';',' ;').replace('...',' ...').replace('(',' (').replace(')',' )').split()
   
    wps = list(zip( words[:-1], words[1:] ))
    
    for wp in wps:
        #print(wp[0],wp[1])
        if wp[0] not in counts.keys():
            counts[wp[0]] = {} #has to use array
        if wp[1] not in counts[wp[0]].keys():
            counts[wp[0]][wp[1]] = 1
        else:
            counts[wp[0]][wp[1]] += 1
        #counts[wp[0]] += 1
    
    for f in counts.keys():
        probability[f] = {}
        for s in counts[f].keys():
            probability[f][s] = counts[f][s]/sum(counts[f].values())

initialword = 'a'
new_tweet = initialword
next_word = initialword
while len(new_tweet) < 280:
    lis = []
    for a in probability[next_word].keys():
        lis = lis + [probability[next_word][a]]
    i = next(lis)
    cond = list(probability[next_word].keys())[i]
    if cond == '.' or cond == ',' or cond == '!' or cond == ':' or cond == ';':
        new_tweet = new_tweet + cond
        next_word = cond
    else:
        new_tweet = new_tweet + ' ' + cond
        next_word = cond
print('new tweet = ',new_tweet + '.')
