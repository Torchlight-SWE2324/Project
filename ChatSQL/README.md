# ChatSQL Proof of Concept (POC)

## Instructions for testing the PoC locally

### Step One

Let's start with python.

You need to have Python 3.9 or higher installed on your computer. You can download it from the following link: <https://www.python.org/downloads/>

>[!NOTE]
The program has been tested with version of python ranging from 3.9 to 3.11.6, versions lower than 3.9 may not work.
Also, the latest version of python, 3.12, has been tested, but it does not work with the current version of txtai, so it is not recommended to use it.

### Step Two

Now you need to download the project. You can do this by clicking on the green button ```Code``` and selecting ```Download ZIP```. After that, you need to unzip the archive and go to the ```ChatSQL``` folder.

Alternatively, you can use *git* right from the terminal. To do this, you need to run the following command in a terminal:

```shell
git clone https://github.com/Torchlight-SWE2324/ChatSQL.git
```

### Step Three

After installing python, you need to install the required packages. To do this, you need to go to the ```ChatSQL``` folder and run the following command in a terminal:

```shell
pip install -r requirements.txt
```

Alternatively, you can specify the path to the ```requirements.txt``` file, for example:

```shell
pip install -r /path/to/requirements.txt
```

### Step Four

Finally, you can run the program. To do this, you need to go into the ```ChatSQL``` folder and run the ```guiUser.py``` file from the terminal by typing:

```shell
streamlit run guiUser.py
```

The program will start and the browser will be opened automatically. If this does not happen, you can open the browser yourself and go to the ```localhost``` address specified in the terminal.

>[!WARNING]
In order to run the program properly, you need to open the ChatSQL folder in the terminal and run the ```guiUser.py``` file from there.

It should look something like this:

```shell
C:\path\to\the\folder\ChatSQL>
```

Then you need to run the ```guiUser.py``` file:

```shell
C:\path\to\the\folder\ChatSQL> streamlit run guiUser.py
```

Beaware that, if you run the ```guiUser.py``` file from another folder, the program will not work properly.
