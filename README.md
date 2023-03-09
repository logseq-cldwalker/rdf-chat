## Description

This repo demonstrates we can use a Logseq graph's [RDF
export](https://github.com/logseq/rdf-export) to intelligently query our graph.
We use the [LLamaIndex](https://github.com/jerryjliu/gpt_index) python library
because it has third party RDF integration and can import knowledge to
LLMs that exceed current token constraints e.g. ~4k tokens.

## Initial experiment

The example graph used is https://github.com/logseq/docs since it's public,
exports valid RDF and has a variety of practical knowledge. The experiment
uses the `rdf_chat.py` script and the included [docs.ttl](docs.ttl), a Mar 9
RDF export of the docs graph. To generate your own rdf export, [see
below](#build-rdf-export).

I ran a couple of queries and saved the interactions in [examples](examples).
Each file contains output from one or more uses of the script. Each use of the script
has an Analysis section in which I describe how accurate the data is.

Overall, I'm pretty happy with the initial results. Using llama-index's
defaults, I was able to get fairly accurate results on questions about the docs
graph. I was able to list, search and even do some relational querying with
varying levels of accuracy. It is annoying that the default LLM makes up stuff
when it doesn't know an answer. Results varied depending on how questions were
worded and whether meaningful words had quotes and the correct capitalization.

## Setup

You'll need to have an https://openai.com/ account. Once you have an api key,
set it in your terminal:

```bash
export OPENAI_API_KEY="MY-API-KEY"
```

Be sure to have python installed, preferably python3. Install llama-index with
`pip3 install llama-index`.

## Usage

```bash
# Do a live query
$ python3 rdf_chat.py live list platforms
ENV: text-davinci
INFO:root:> [build_index_from_documents] Total LLM token usage: 0 tokens
INFO:root:> [build_index_from_documents] Total embedding token usage: 2135 tokens
PROMPT: list platforms
INFO:root:> [query] Total LLM token usage: 2181 tokens
INFO:root:> [query] Total embedding token usage: 2 tokens
RESPONSE:

All Platforms, Desktop, Publish Web, Web, Android, iOS


# Generate an index for cheaper embedded querying
$ python3 rdf_chat.py save-index
...

# Do a cached query
$ python3 rdf_chat.py list whiteboard only ui elements
ENV: text-embedding-ada-002-v2
PROMPT: list whiteboard only ui elements
INFO:root:> [query] Total LLM token usage: 2212 tokens
INFO:root:> [query] Total embedding token usage: 7 tokens
RESPONSE:

- Whiteboard/Toolbar
- Whiteboard/Action Bar
- Whiteboard/Quick Add
- Whiteboard/Dashboard
- Whiteboard/Context Menu
- Whiteboard___Canvas
```

## Development

### Build RDF Export

To build a fresh rdf export of the docs graph, first install the [rdf-export
CLI](https://github.com/logseq/rdf-export#cli). Then simply:

```bash
# From docs directory
$ logseq-rdf-export docs.ttl -a -c '{:exclude-properties [:initial-version :description]}'
Parsing 303 files...
Writing 272 triples to file docs.ttl
```

## TODO

* Try chatgpt model e.g. gpt-3.5-turbo for better accuracy
* Try a [custom prompt](https://gpt-index.readthedocs.io/en/latest/how_to/custom_prompts.html) for better accuracy
* Try a different LLM. Is it possible to use one that we control?
* Build a RDF file that includes more data including descriptions of entities
* Try a graph that includes subclasses to see how useful that is. rdf-qa repo is promising


## Additional Links
* https://github.com/mommi84/rdf-qa - The repo which inspired this experiment. Recommend trying it
* [RDF Loader](https://github.com/emptycrown/llama-hub/tree/main/loader_hub/file/rdf) - The RDF loader for llama-index
* [LLama Index docs](https://gpt-index.readthedocs.io/en/latest/)
