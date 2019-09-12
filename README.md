# English-Hindi-Digital-Document-Translater
This repository contains the code to convert English Digital Documents(pdf) into Hindi. 

Below are the two components present :

### 1. **Machine-Translation**

We have used [opennmt](https://github.com/OpenNMT/OpenNMT-py) to train
and serve the model trained on our own custom dataset along with this
[open source](http://www.cfilt.iitb.ac.in/iitb_parallel/) dataset. Follow below instructions to start this
component server:

1. **Installing Dependencies**
    ```bash
    cd OpenNMT-py && pip install -r requirements.txt --no-cache-dir
    ```
2. **Model Download**: 

    Download model from [here](https://drive.google.com/open?id=1IT-rxl4oUog036sGdvoRAsLebGlhOyRo) and copy inside the
    ./OpenNMT-py/available_models folder
   
3. **Start Server**(Will start a server at default port **5000**)
    ```bash
    python server.py
    ```
    Below is a sample curl request to test the results:
    
    ```bash
     curl --header "Content-Type: application/json"   --request POST   --data '[{"id":100,"src":"You should refrain from doing this."}]' http://localhost:5000/translator/translate
    ```
    Tools like postman etc can also be used to test the api.

### 2. **PDF to Converted Text**

1. **Installing Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
2. **Start Server** (will start a server on port 5001)
    ```bash
    export PYTHONPATH=$PWD && python src/app.py
    ```
3. Go to http://localhost:5001/home
    <center style="padding: 40px"><img width="100%" height="50%" src="./static/images/server_demo.png" /></center>

    **Note: Having too many pages in the pdf might take a bit of time for
the API to return the results. On successfull processing, a text file
with the converted hindi text will be generated.**
