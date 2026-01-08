import streamlit as st 
import random 
from collections import defaultdict


# Sample Corpus Training

corpus = """
Hello how are you 
Tell me some facts about world poitics 
Give a brief note on revolution of artificial intelligence 
What are you doing? 
I was wondering if we could hangout tomorrow 
I would like to have a cup of black coffee 
Let's watch an anime together 
You are really pretty 
I like to go out on cafe's 
""".strip().lower().split("\n")

# Building Trigram Model 
model = defaultdict(list)

for sentence in corpus:
    words = sentence.split()
    for i in range(len(words) - 2):
        key = (words[i], words[i+1])
        next_word = words[i+2]
        model[key].append(next_word)
    
def predict_next_word(w1, w2):
    if key in model:
        suggestions = random.choices(model[key], k=3)
    else:
        # Pick a random word
        all_words = [word for sent in corpus for word in sent.split()]
        suggestions = random.choices(all_words, k=3)
    return suggestions

# Streamlit UI 
st.title('Predict---Key:  AI Predictive Keybord')

if "text" not in st.session_state:
    st.session_state.text = ""
    
input_text = st.text_input('Type here:', st.session_state.text)

if input_text:
    st.session_state.text = input_text
    
# get last 2 words 
words = input_text.strip().strip()

st.subheader("Suggestions:")

if len(words) >= 2:
    s1, s2 = words[-2], words[-1]
    suggestions = predict_next_word(s1, s2)
else:
    suggestions = ['corpus']
    
# displaying clickable buttons 
cols = st.columns(3)
for i, suggestion in enumerate(suggestions):
    with cols[i]:
        if st.button(suggestion, key=f"suggestion_{i}"):
            st.session_state.text = input_text + " " + suggestion
            st.rerun()

st.write("Current text:")
st.code(st.session_state.text)
