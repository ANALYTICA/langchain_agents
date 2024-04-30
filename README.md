# Using agents in Langchain
This is a repo for using agents with an LLM to carry out specific tasks. This repo uses langchain for prompt writing, fastapi for api functionality, and llama-cpp-python as the model interface.

## Build the image
Docker must be installed on your computer. When using an Analytica computer, you might have to call R3 and get added to the Docker users list, even if docker desktop is installed. 

With the docker engine running, from the root directory of this repo, run:

```
 docker build -t agent:0 .
```

You can name/tag the image however you'd like. Building might take around 10 minutes. 

## Prior to running the built image
Required folder structure of the repo, create whatever folders are needed prior to building:

repo
  |---Dockerfile, README.md, llama.py, etc. 
  |---bind
      |---model
          put your model here
      |---documents
          not used but might throw error if not present
      |---vectorstore
          not used but might throw error if not present

Prior to running the image, you need a model to use which is llama-cpp compliant. This must be stored in the bind/model folder relative to this repo. Create this folder if it does not exist. This repo was tested with this model:

https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF/blob/main/capybarahermes-2.5-mistral-7b.Q5_K_M.gguf 

You can download it from this url. It is around 5 GB. 
 

## Run
The following command will create a container from the built image: 

```
docker run --mount type=bind,source=/absolute/path/to/folder/bind,target=/app/persist -p 8000:8000  agent:0
```

You must include the absolute path to your "bind" directory that contains the model and documents for the mount option, relative paths will not work. This can be obtained with the pwd command while in the bind directory. 

An api will be set up running on the container at port 8000 and forwarded to the host port localhost:8000.  

A container printout with "INFO: Application startup complete." indicates the api is running. It may take two or three minutes for the container to execute the startup code.  

## Chat
Send requests to the api in JSON form with a "text" field, i.e.:

```
{
	"text": "What is today's date?"
}
```

Make sure you are sending the correct request (e.g., "PUT") to the correct route (e.g. localhost:8000/chat/tools). Routes can be found in main.py. A dedicated API tool like Insomnia is recommended. 

## Notes
The behavior of the LLM can be changed in the llama.py file (e.g., temperature, etc.). A rebuild (that should only take a few seconds) will be needed to implement the changes.

Restarting a stopped container has not been tested, but should be feasible. You can always delete the old, stopped container and run a new one from the built image. 

 