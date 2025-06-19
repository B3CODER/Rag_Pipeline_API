import deepdoctection as dd
from matplotlib import pyplot as plt

# Initialize analyzer
analyzer = dd.get_dd_analyzer()

analyzer = dd.get_dd_analyzer()
df = analyzer.analyze(path="leac204.pdf")

for page in df:
    print(page.text)  # Extracted text with layout