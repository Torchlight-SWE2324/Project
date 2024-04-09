# ChatSQL MVP (Minimum Viable Product)

## How to run the program with the Docker Image

First of all, you need to have Docker installed on your computer. You can download it from the following link: <https://www.docker.com/products/docker-desktop>.

you can check if Docker is installed by running the following command in the terminal:

```shell
docker --version
```

### Download the Docker image

To download the Docker image, you need to run the following command in the terminal:

```shell
docker pull ghcr.io/torchlight-swe2324/chatsql-docker:latest
```

### Run the Docker container

In the terminal, run the following command:

```shell
docker run -p 8501:8501 ghcr.io/torchlight-swe2324/chatsql-docker:latest
```

The container will be built and started. Now you can open the browser and go to the ```localhost:8501``` address to access the program.

> [!WARNING]
> Thw terminal will say that the progarm is running on ```0.0.0.0:8501```, but you need to go to ```localhost:8501``` in the browser to access it.

## How to run the program locally withouth Docker

To run the program, you need to follow these steps:

### Step One

Ensure that you have Python 3.11 installed on your computer. You can download it from the following link: <https://www.python.org/downloads/>.

> [!NOTE]
> The program has been tested with python 3.11. Versions lower than that may not be compatible.
> Tests w'ere also conducted with Python 3.9 and 3.10, but the program did not work properly, due to cross-compatibility issues with the libraries used.
> The latest version of Python, 3.12, has been tested but is not recommended for use with the current version of *txtai*, as it is not yet compatible with the library.

### Step Two

To download the project, just click the ```Code``` button on the GitHub project page and select ```Download ZIP```. Unzip the archive into any folder.

Alternatively, you can use *git* from the terminal by running the following command:

```shell
git clone https://github.com/Torchlight-SWE2324/ChatSQL.git
```

### Step Three

Now you need to install the necessary libraries. To do this, go to the ```ChatSQL``` folder and run the following command in the terminal:

```shell
pip install -r requirements.txt
```

Alternatively, you can specify the path to the ```requirements.txt``` file:

```shell
pip install -r \path\to\ChatSQL\requirements.txt
```

### Step Four

Finally, you can run the program. To do this, you need to be inside the ```ChatSQL``` folder and run the ```main.py``` file from the terminal by typing:

```shell
streamlit run main.py
```

The program will start and the browser will open automatically. If this does not happened, you can open the browser yourself and go to the ```localhost``` address and specify the port printed in the terminal.

> [!WARNING]
> In order to avoid issues, you ***NEED*** to run the ```main.py``` file from the ```ChatSQL``` folder.
>
> The path should look something like this (in Windows):
>
> ```shell
> C:\path\to\the\folder\ChatSQL
> ```
>
> Then to run the ```main.py``` file:
>
> ```shell
> C:\path\to\the\folder\ChatSQL> streamlit run main.py
> ```
>
> Beaware that, if you run the ```main.py``` file from another folder, the program will not work.
