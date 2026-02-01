N-Gram Language Model using Streamlit

This project is a Natural Language Processing (NLP) web application that implements Unigram, Bigram, and Trigram Language Models with Laplace (Add-One) Smoothing.
The app is built using Python and Streamlit and uses the Brown Corpus from NLTK for training.

🚀 Features

📊 Sentence Probability Calculation

📈 Perplexity Computation

🧠 Best Model Selection based on minimum perplexity

✍️ Text Generation using:

Unigram Model

Bigram Model

Trigram Model

🌐 Web-based interactive UI using Streamlit

🛠️ Technologies Used

Python

Streamlit

NLTK (Brown Corpus)

Collections (Counter)

Mathematics & Probability Concepts

📖 How It Works

The Brown Corpus is preprocessed by adding:

<s> → Start token

</s> → End token

The application computes:

Unigram counts

Bigram counts

Trigram counts

Laplace Smoothing is applied to avoid zero probability problems.

For a given input sentence:

Probability is calculated

Perplexity is computed

Best N-gram model is selected

The app can also generate new text based on the selected N-gram model.
