# Holy-bible-2-Tokyo-Drift-2-Electric-Boogaloo
## Dog Eat Dog
Ryan Aday, Jiajie Mai, Theodore Peters

## What is this game?
This is a game about selling stocks and being a dog while battling other dogs.

## RESTful APIs Used
This game uses 2 APIs
- Dog API
[This API] (https://dog.ceo/dog-api/) is used for dogs, allowing us to have pictures of dogs at our will. This does not require an API key. 
- IEXtrading API
[This API] (https://iextrading.com/developer/) is used to retrive stock information and stock price. These are the fundemental parts of our project, allowing us to actually work the game's components and have it actually function.

## Dependencies
You don't need much to operate as you do not need any API keys. You only really need to install the things inside [requirements.txt] (https://github.com/Jiajie-Mai/Holy-bible-2-Tokyo-Drift-2-Electric-Boogaloo/blob/master/requirements.txt) via pip install.

## What's the deal with the packages? (The ones that matter)
- urllib
Keeps your data safe, allows for accounts to be made without somebody being able to easily find the login information.
- pip
Pretty importatn for installing other things on this list. Most likely already comes when you have downloaded Python.
- venv
Stops damage if you do run into an error. Creates a seperate, isolated environment to keep your computer safe. Using Python 3.0.0 or higher already has this. However, if you do need it as you have a version older than Python 3.0.0, use this:
> pip install virtualenv
- Jinja2/Flask
Both of these applications are useful for the actual functionality of the website from creating them to making them actually appear on your browser.

## How to run our masterpiece
1. Open a terminal
2. Create a virtual environment:
> $ python3 -m venv virtual_env_name
3. Activate the virtual environment:
Mac OS/Linux:
> $ source virtual_env_name/bin/activate
Windows:
> $ virtual_env_name\Scripts\activate
After activating you should see (virtual_env_name) in front.
4. Download the packages in the [requirements.txt] (https://github.com/Jiajie-Mai/Holy-bible-2-Tokyo-Drift-2-Electric-Boogaloo/blob/master/requirements.txt) via pip install
5. Clone this baby using SSH
> $ git clone git@github.com:Jiajie-Mai/Holy-bible-2-Tokyo-Drift-2-Electric-Boogaloo.git
6. Change to the correct directory:
> $ cd Holy-bible-2-Tokyo-Drift-2-Electric-Boogaloo/
7. Run this application by typing:
> (virtual_env_name)$ python app.py
8. This should appear: 
>  * Debug mode: on
>  * Restarting with stat
>  * Debugger is active!
>  * Debugger PIN: 209-234-496
>  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
9. Open your web browser of choice and go to [http://localhost:5000/] (http://localhost:5000/).










