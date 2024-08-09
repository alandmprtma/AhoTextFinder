# 🔍 Aho-Corasick Text Finder
Implementasikan algoritma Aho-Corasick untuk mencari suatu set string dari query teks tertentu
## 📝 Application Description
### Overview
This application leverages the Aho-Corasick algorithm to efficiently search for and match multiple string patterns within a given text. Ideal for handling large datasets, such as DNA sequences or malware code signatures, this tool builds a trie-based automaton offline. Once constructed, this automaton facilitates rapid, online text searches without the need for tedious index-by-index comparisons.

### Features
#### Core Functionality
- <b>Pattern Matching:</b> Quickly find multiple patterns within texts using a pre-built automaton.
- <b>Case-Insensitive Search:</b> Perform searches that ignore case differences.
- <b>Efficiency:</b> Reduce search times significantly compared to naive text searching algorithms.

#### Input/Output
- Input: Accepts JSON formatted input containing the text to be searched and an array of patterns.
- Output: Displays the count of each pattern found in the text and the indices of their occurrences.

#### GUI
The application features a user-friendly graphical interface that allows users to easily input their data and view results.

#### Bonus Features
- <b>Pattern Highlighting:</b> Visual indicators show where each pattern is found within the text.
- <b>Automaton Visualization:</b> Provides a graphical representation of the constructed automaton, offering insight into the algorithm's matching process.

## 💻 Tech Stacks
### Programming Language
- Python (version 3.11.9 or above)

### Dependencies
- flet (https://flet.dev/)
- graphviz (https://graphviz.org/)

## 🗂️ Program Structure
```bash

```

## 🧙 Algorithms 
### Aho-Corasick
The Aho-Corasick algorithm is an efficient method for searching multiple patterns simultaneously within a text. It’s particularly useful when you need to find many patterns in a large text quickly.

### Key Steps
1. <b>Build the Automaton:</b> The algorithm starts by constructing an automaton based on a trie (prefix tree) of the patterns you want to search for. This trie is augmented with transition tables for fast matching and failure links that indicate fallback points when a direct match isn’t found.
2. <b>Add Failure Transitions:</b> In addition to normal transitions, failure transitions are added. These allow the search to continue efficiently by falling back to relevant nodes in the trie when a mismatch occurs, rather than restarting the search.
3. <b>Process the Text:</b> The algorithm then processes the input text sequentially. Using the constructed automaton, it efficiently matches patterns against the text. The failure transitions help avoid re-checking parts of the text unnecessarily.
4. <b>Identify Matches:</b> As patterns match, the algorithm records the matches and continues searching for other patterns using the automaton.

### Advantages
- <b>Time Efficiency:</b> The algorithm is very efficient with a time complexity of O(n + m + z), where n is the length of the text, m is the total length of the patterns, and z is the number of matches.
- <b>Multi-Pattern Matching:</b> It’s well-suited for cases where multiple patterns need to be matched simultaneously.

## 🛠️ Configuration Guide

## 🏃‍♂️ How To Run

## 📸 Screenshots

