# ChatSQL Proof of Concept (POC)

## Instructions for testing the PoC locally

### Step One

Ensure that you have Python 3.11 installed on your computer. You can download it from the following link: <https://www.python.org/downloads/>.

> [!NOTE]
> The program has been tested with python 3.11. Versions lower than that may not be compatible.
> Tests w'ere also conducted with Python 3.9 and 3.10, but the program did not work properly, due to problems with the libraries.
> The latest version of Python, 3.12, has been tested but is not recommended for use with the current version of *txtai*, as it is not yet compatible with the library.

### Step Two

To download the project, click on the green button labeled ```Code``` on the GitHub project page and select ```Download ZIP```. Unzip the archive into any folder.

Alternatively, use *git* from the terminal by running the following command:

```shell
git clone https://github.com/Torchlight-SWE2324/ChatSQL.git
```

### Step Three

Now you need to install the necessary libraries. To do this, go to the ```ChatSQL`` folder and run the following command in a terminal

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