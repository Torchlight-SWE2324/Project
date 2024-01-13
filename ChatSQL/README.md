# ChatSQL Proof of Concept (POC)

## Instructions for testing the PoC locally

### Step One

You need to have Python 3.9 or higher installed on your computer. You can download it from the following link: <https://www.python.org/downloads/>

>[!NOTE]
The program has been tested with version of python ranging from 3.9 to 3.11.6, versions lower than 3.9 may not work.
Also, the latest version of python, 3.12, has been tested, but it does not work with the current version of txtai, so it is not recommended to use it.

Once you have installed Python, you need to install the necessary libraries. To do this, you can use the following command in a terminal:

```pip install -r requirements.txt```

Alternatively, you can specify the path to the ```requirements.txt``` file, for example:

```pip install -r /path/to/requirements.txt```

### Step Two

Clone the repository to your computer. You can do this by typing the following command in a terminal:

```git clone https://github.com/Torchlight-SWE2324/ChatSQL.git```

### Step Three

Go to the ```ChatSQL``` folder and run the ```guiUser.py``` file. You can do this by typing the following command in a terminal:

```streamlit run guiUser.py```

The program will start and the browser will be opened automatically. If this does not happen, you can open the browser yourself and go to the ```localhost``` address specified in the terminal.
