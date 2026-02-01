import streamlit as st
import nltk
nltk.download('brown')
from nltk.corpus import brown
from collections import Counter
import random
import math

sentences=brown.sents()

processed=[]
for s in sentences:
    processed.append(['<s>']+[w.lower() for w in s]+['</s>'])

unigram_counts=Counter()
bigram_counts=Counter()
trigram_counts=Counter()
total_words=0

for s in processed:
    unigram_counts.update(s)
    total_words+=len(s)
    for i in range(len(s)-1):
        bigram_counts[(s[i],s[i+1])]+=1
    for i in range(len(s)-2):
        trigram_counts[(s[i],s[i+1],s[i+2])]+=1

vocab_size=len(unigram_counts)

def unigram_prob(w):
    return (unigram_counts[w]+1)/(total_words+vocab_size)

def bigram_prob(w1,w2):
    return (bigram_counts[(w1,w2)]+1)/(unigram_counts[w1]+vocab_size)

def trigram_prob(w1,w2,w3):
    return (trigram_counts[(w1,w2,w3)]+1)/(bigram_counts[(w1,w2)]+vocab_size)

def sentence_probability(sentence,model):
    words=['<s>']+sentence.lower().split()+['</s>']
    prob=1
    if model=="Unigram":
        for w in words:
            prob*=unigram_prob(w)
    elif model=="Bigram":
        for i in range(len(words)-1):
            prob*=bigram_prob(words[i],words[i+1])
    else:
        for i in range(len(words)-2):
            prob*=trigram_prob(words[i],words[i+1],words[i+2])
    return prob

def perplexity(prob,n):
    return math.exp(-math.log(prob)/n)

# ✅ FIXED TEXT GENERATION
def generate_text(model,max_len):
    if model=="Unigram":
        words=[w for w in unigram_counts if w not in ['<s>','</s>']]
        return " ".join(random.choice(words) for _ in range(max_len))

    if model=="Bigram":
        w=random.choice([w for w in unigram_counts if w not in ['<s>','</s>']])
        result=[w]
        for _ in range(max_len-1):
            candidates=[k[1] for k in bigram_counts if k[0]==w and k[1] not in ['<s>','</s>']]
            if not candidates:
                break
            w=random.choice(candidates)
            result.append(w)
        return " ".join(result)

    w1,w2=random.choice(list(bigram_counts.keys()))
    result=[w1,w2]
    for _ in range(max_len-2):
        candidates=[k[2] for k in trigram_counts if k[0]==w1 and k[1]==w2 and k[2] not in ['<s>','</s>']]
        if not candidates:
            break
        w3=random.choice(candidates)
        result.append(w3)
        w1,w2=w2,w3
    return " ".join(result)

def best_model(sentence):
    p1=sentence_probability(sentence,"Unigram")
    p2=sentence_probability(sentence,"Bigram")
    p3=sentence_probability(sentence,"Trigram")

    perp1=perplexity(p1,len(sentence.split())+2)
    perp2=perplexity(p2,len(sentence.split())+2)
    perp3=perplexity(p3,len(sentence.split())+2)

    results={
        "Unigram":perp1,
        "Bigram":perp2,
        "Trigram":perp3
    }

    best=min(results,key=results.get)
    return best,results

st.title("N-Gram Language Model with Laplace Smoothing")

model=st.selectbox("Select N-Gram Model",["Unigram","Bigram","Trigram"])

sentence=st.text_input("Enter a sentence")

if st.button("Calculate Probability & Perplexity"):
    if sentence.strip()!="":
        p=sentence_probability(sentence,model)
        perp=perplexity(p,len(sentence.split())+2)
        st.write("Sentence Probability:",p)
        st.write("Perplexity:",perp)
    else:
        st.warning("Please enter a sentence")

st.subheader("Best Model Selection")

if st.button("Best Model Based on Perplexity"):
    if sentence.strip()=="":
        st.warning("Please enter a sentence first")
    else:
        best,results=best_model(sentence)
        st.write("Unigram Perplexity:",results["Unigram"])
        st.write("Bigram Perplexity:",results["Bigram"])
        st.write("Trigram Perplexity:",results["Trigram"])
        st.success(f"Best Model is: {best}")

st.subheader("Text Generation")

length=st.slider("Generated Sentence Length",5,20,10)

if st.button("Generate Text"):
    text=generate_text(model,length)
    st.success(text)