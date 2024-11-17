# ResearchNexus

## How to run ?

### Creating virtualenv
```
conda create --name venv python=3.10 -y
conda activate venv
pip install -r requirements.txt
```

### To run Data Ingestion Pipeline
- Update `LLAMAINDEX_API_KEY` in .env file
- Run:
    ```
    python3 prepare_data.py </path/to/pdf>
    ```
- Cited research papers are fetched from the input pdf and stored in *pdf_papers*
- PDF's are parfed into .txt format using llamaIndex efficiently and stored in *txt_papers* papers

### To retreive most relevant papers for 
- Implemented __BM25__ and __BERT__ based retreival methods in *retreive_docs.ipynb* file
- We Qualitatively found __ColBERT__ results to be better.
- Update `PAPER_NAME = *.txt` in .env file
- Run 
    ```
    sudo apt install jupyter-nbconvert
    jupyter nbconvert --execute --inplace colbert.ipynb
    ```
- Retrives the most relevant papers from *txt_papers* using __ColBERT__ model.
- Stores most relevant papers in *final_input* directory in .txt format
- *final_input* dir is used for running on __Microsoft Graph RAG__.

### To run Knowledge GraphRAG
- cp final_input/* `/path/to/input`
- `/path/to/input` directory refers to input directory of `MS KG-RAG` implementation
- Run `KG-RAG`, CLI app with QnA session