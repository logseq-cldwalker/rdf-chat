from pathlib import Path
from llama_index import GPTSimpleVectorIndex, download_loader
import sys

def load_document(file):
    RDFReader = download_loader("RDFReader")
    loader = RDFReader()
    return loader.load_data(file=Path(file))

def query(index, prompt):
    print("PROMPT:", prompt)
    result = index.query(prompt)
    print("RESPONSE:")
    print(result.response)

if __name__ == '__main__':
    RDF_FILE = 'docs.ttl'
    INDEX_FILE = 'docs.json'

    # live query - more expensive
    if sys.argv[1] == 'live':
        print("ENV: text-davinci")
        document = load_document(RDF_FILE)
        index = GPTSimpleVectorIndex(document)
        prompt = " ".join(sys.argv[2:])
        query(index, prompt)

    elif sys.argv[1] == 'save-index':
        print("Saving index to docs.json...")
        document = load_document(RDF_FILE)
        index = GPTSimpleVectorIndex(document)
        index.save_to_disk(INDEX_FILE)
    # query from ada embeddings - cheaper
    else:
        print("ENV: text-embedding-ada-002-v2")
        index = GPTSimpleVectorIndex.load_from_disk(INDEX_FILE)
        prompt = " ".join(sys.argv[1:])
        query(index, prompt)
