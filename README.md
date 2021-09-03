# p8-Pur_Beurre_nutella

Need to search another product for a better health condition ?  
Purbonheurre is your solution !  

#  Installation and requierement 

first of all, download [Python](https://www.python.org/) by going in the official website and choose the version you want ([Python download](https://www.python.org/downloads/)).

then, install [Pip](https://pypi.org/project/pip/) by entering in the terminal the following command line:
```bash
python3 -m pip --version  #for unix/mac
python get-pip.py         #for windows
```
after that, you have the choice to download the zip of the code or clone with the following command Line:
```bash
git clone https://github.com/ihsan-salman/p8-Pur_Beurre_nutella.git
```
Create an virtual environment with the following command line:
```bash
python3 -m venv <name of your environment>
```
then activate it with the following command line:
```bash
<name of your environment>\Scripts\activate.bat # for windows
source <name of your environment>/bin/activate # for unix/mac
```

finally, use the requirement document by entering the following command in the terminal:
```bash
pip install -r requirements.txt      # for unix
pip install -r requirements.txt       # for windows/mac
```

# How to use the program

To start the program, go to this website:
```bash
https://purbonheurre.herokuapp.com/
```

Or you can launch the website with Django command:
```bash
cd Pur_Beurre_Nutella        # place in the good file

manage.py runserver          # launch the local server

http://127.0.0.1:8000/       # local url
```