
# peaking for Pets - Pet Adoption App

This is a pet adoption app aiming to provide a smooth user experience and give easy acceess to the Petfinder API

## Technologies

Project is created with:

* JS/jquery
* Python3
* Html/Css/Fontawesome
* Boostrap
* SQL
* Flask
* RESTFUL API
* Bcrypt
* SCSS
* Less

## Features

* Login/ Registration validation with flash
* Users can choose to "Keep me signed in"
* After registration, a verification email with a confirmation link will be sent to the user's inbox
* On the dashboard page, users can choose to view the information of listed animals and start an adoption application
* If the pet has been adopted by the other users, the application would not go through
* There are validations set to the application form, edit from, and pet search functions
* Users can also check out the "About" page to get more information regarding the site
* Users can search for local pets available for adoption from the Petfinder API
* Users can either check out the pet's profile, start an application or add certain pets into their watchlise
* In the users account, they can see their pet adoption history and their Pet's watchlist
* In the users account, there is an alert indicating whether the account has been verified. Clicking "close" will make the alert disappear
* The verfication URL expires after an hour. To resend the confirmation link, the user has to click the expired link and input the email again
* The user can modify their pet adoption application and their pet watchlist

## Usage

```python
pip install petpy

pip install beautifulsoup4

pip install Flask-Mail

pipenv install python-dotenv

pipenv shell

python3 server.py
```


	
