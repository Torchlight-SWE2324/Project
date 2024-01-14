# ChatSQL Proof of Concept (POC)

## Instructions for testing the PoC locally

### Step One

Let's start with python.

You need to have Python 3.9 or higher installed on your computer. You can download it from the following link: <https://www.python.org/downloads/>

> [!NOTE]
> The program has been tested with version of python ranging from 3.9 to 3.11.6, versions lower than 3.9 may not work.
> Also, the latest version of python, 3.12, has been tested, but it does not work with the current version of txtai, so it is not recommended to use it.

### Step Two

Now you need to download the project. You can do this by clicking on the green button ```Code``` and selecting ```Download ZIP``` on the page of the project on GitHub. After that, you need to unzip the archive into any folder.

Alternatively, you can use *git* right from the terminal. To do this, you need to run the following command in a terminal:

```shell
git clone https://github.com/Torchlight-SWE2324/ChatSQL.git
```

### Step Three

Now you need to install the necessary libraries. To do this, you need to go into the ```ChatSQL\code``` folder and run the following command in the terminal:

```shell
pip install -r requirements.txt
```

Alternatively, you can specify the path to the ```requirements.txt``` file, for example:

```shell
pip install -r \path\to\ChatSQL\code\requirements.txt
```

### Step Four

Finally, you can run the program. To do this, you need to go into the ```ChatSQL\code``` folder and run the ```guiUser.py``` file from the terminal by typing:

```shell
streamlit run guiUser.py
```

The program will start and the browser will be opened automatically. If this does not happen, you can open the browser yourself and go to the ```localhost``` address specified in the terminal.

> [!WARNING]
> In order to run the program properly, you ***NEED*** to run the ```guiUser.py``` file from the ```shellChatSQL\code``` folder.
>
> It should look something like this:
>
> ```shell
> C:\path\to\the\folder\ChatSQL\code
> ```
>
> Then you need to run the ```guiUser.py``` file:
>
> ```shell
> C:\path\to\the\folder\ChatSQL\code> streamlit run guiUser.py
> ```
>
> Beaware that, if you run the ```guiUser.py``` file from another folder, the program may not work properly.
