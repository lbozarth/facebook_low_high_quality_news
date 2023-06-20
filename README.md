# This repo contains code and data for the paper: "Bursts of contemporaneous publication among high and low credibility online information providers"

## scripts

### SRC folder
1. Code to scrape URLs: `src/fetch_url.py`
2. Code to extract body text from an html webpage: `src/parse_article.py`
3. Code for entity categorization: `gen_entcat_*.py`, and `torchProp.py`
4. Code to identify peaks: `gen_peaks.py`

### Third-party code+library
1. End to end entity linking: We used [Kolitsas, N., Ganea, O.-E. & Hofmann, T. End-to-end neural entity linking](https://aclanthology.org/K18-1050/).
2. Network analysis: We used [netinf](http://snap.stanford.edu/netinf/) (reconstructs a who-copies-from-whom network from these cascades), [networkx](https://networkx.org/)(bipartite, assortativity, etc.), [gephi](https://gephi.org/)(visualization), and [python-louvain](https://python-louvain.readthedocs.io/en/latest/api.html).
3. Text extraction: we relied on [trafilatura](https://trafilatura.readthedocs.io/en/latest/) and [newspaper3k](https://newspaper.readthedocs.io/en/latest/).


## Data
1. URLs: The 7 million URLs are located in this google driver folder: https://drive.google.com/file/d/10tw6m_qYQlaZB21Sw7NOcqUgjxHji6f3/view?usp=sharing
2. Domain-level quality: `data/domain_quality.csv`
3. Domain-level ideology: `data/domain_ideology.csv`
4. Domain-level popularity (viewer traffic): `data/domain_quality.csv`
5. Entity clustering final result: `data/clustering_results.csv`

### External data
1. Zimdars' list: https://docs.google.com/document/d/10eA5-mCZLSS4MQY5QGb5ewC3VAL6pLkT53V_81ZyitM/preview


## Contact
Please email cbudak@umich.edu or liafan@uw.edu if you have any questions about the code or script.