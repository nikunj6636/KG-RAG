# GraphRAG Setup and Usage Guide

## Pre-requirements:
Python latest version is giving some errors in installing Gensim and another library, so python 3.10 version installation is recommended.

### Steps:

1. **Set Up Virtual Environment:**

    ```sh
    mkdir Graphrag
    conda create -p ./graphragvenv python=3.10
    conda activate ./graphragvenv
    python -m pip install --upgrade pip
    python -m pip install --upgrade setuptools
    ```

2. **Install GraphRAG:**

    ```sh
    pip install graphrag
    python -m pip install --no-cache-dir --force-reinstall gensim
    pip install graphrag
    ```

3. **Initialize GraphRAG:**

    ```sh
    python -m graphrag.index --init --root .
    ```

    Running the above command, GraphRAG is initiated.

4. **Creating the Deployments of LLM Model and Embedding Model in Azure OpenAI:**

    - For embedding, the model is `text-embedding-ada-002`
    - For LLM model, recommended is `gpt-4o-mini`.
    After creating the deployments, following changes need to be made in the `settings.yaml` file.


5. **Configure OPENAI_API_KEY:**
    Update OpenAI Key and Base API Endpoint in the `.env` file.


6. **Changes required in `settings.yaml` File:**

    In the `llm` section:

    - Change `model` to the model name that you deployed in Azure OpenAI. Here `gpt-4o-mini` is used by us.
    - Uncomment the `deployment_name`, and replace that with the deployment you have given to the model while creating the deployment.
        - We have taken `<deployment_name_of_model>`

    In the same `settings.yaml` file, go to the `embeddings` section and make some changes:

    - Change `model` to the model name that you deployed in Azure OpenAI. Here `text-embedding-ada-002` is used by us.
    - Uncomment the `deployment_name`, and replace that with the deployment you have given to the model while creating the deployment.
        - We have taken `<deployment_name_of_model>`


7. **Add Input File:**

    Copy the Dataset(.txt file format) on which you want to run GraphRAG model.

8. **Run GraphRAG to Create Graphs on the Data:**

    ```sh
    python -m graphrag.index --root .
    ```

    This command will run the GraphRAG and create the parquet files. This will convert all your text data into entities and relationships graphs. You can check that in `output > last folder > artifacts folder` (you have parquet files, which are converted data into graphs).

9. **Evaluate Our RAG Model:**

    Run  Command Line Interface (CLI):
    ```
    python cli_app.py
    ```
    and provide the Question as input to the App.