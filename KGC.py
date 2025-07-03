# KGC_Smart.py — Improved Knowledge Graph with spaCy Matcher

import spacy
import networkx as nx
import matplotlib.pyplot as plt
from spacy.matcher import Matcher

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Sample text (replace with your MOSDAC data later)
text = """
INSAT-3D carries a sounder for weather monitoring.
It was launched by ISRO in 2013.
MOSDAC provides satellite data to IMD and researchers.
INSAT-3DR is an advanced meteorological satellite that enhances observations.
INSAT-3D and INSAT-3DR work together to improve forecasting.
"""

# Process text
doc = nlp(text)

# Smarter triplet extractor using spaCy Matcher
def extract_triplets_smart(doc):
    matcher = Matcher(nlp.vocab)
    triplets = []

    # Pattern: subject + verb + object
    pattern = [
        {"DEP": "nsubj"},                 # subject
        {"POS": "VERB"},                  # verb
        {"DEP": {"IN": ["dobj", "pobj", "attr", "prep"]}}  # object types
    ]
    matcher.add("SVO", [pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if len(span) == 3:
            subject = span[0].text
            verb = span[1].lemma_  # use base form: carries → carry
            obj = span[2].text
            triplets.append((subject, verb, obj))
    return triplets

# Build the graph
G = nx.DiGraph()

triplets = extract_triplets_smart(doc)

for sub, rel, obj in triplets:
    G.add_node(sub)
    G.add_node(obj)
    G.add_edge(sub, obj, label=rel)

# Draw graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5)

nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=10)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title("Smarter MOSDAC Knowledge Graph", fontsize=15)
plt.tight_layout()
plt.show()
