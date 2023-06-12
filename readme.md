## Project Description: Company Information Retrieval System

### User Features:

1. User can sign up and log in to the system.
2. Each user is granted 10 free searches.
3. Admins have the ability to increase the search limits for users.
4. Searches are focused on retrieving information about companies.

### Search Results:
1. Search results will include products from Amazon.
2. Company information will be gathered from LinkedIn or the company's website.
3. For each company, the system will provide information about 10 employees along with their Twitter feeds.

### Historic Searches:
1. Users can retrieve their past search history.

### Admin Access:
1. Admins have the privilege to view all searches performed by all users.
2. The goal of the project is to develop a production-grade application using the Django/Python framework. 
3. The application should support multiple concurrent users and fulfill the requirements mentioned above.


## Postman Document
[ClickMe](https://documenter.getpostman.com/view/17690645/UVREkQgW)


## Follow the steps
1. clone the repository on your local system

```commandline
git clone https://github.com/krisskad/CIRS.git
```
```commandline
cd CIRS
```

2. create virtual env in python3.10

```commandline
python -m pip install --user virtualenv
```
```commandline
virtualenv -p /usr/bin/python3 virtualenv_name
```
```commandline
source virtualenv_name/bin/activate
```

3. Install dependencies packages from requirements.txt
```commandline
pip install -r requirements.txt
```

4. Requirement to setup pyvirtual display
```commandline
sudo apt-get install python3-tk python3-dev
sudo apt-get install xvfb
pip install xlib pyvirtualdisplay pyautogui
pip install python-xlib
```

5. Start the server
```commandline
python manage.py runserver
```

## Testing API's
#### Go to the postman documentation which given above and if you are familier with django api view you can directly hit the api url in the browser to get api view interface to test the app.
All API's and its description are given sequencially and Your sequence should be
   1. user registration api (please enter valid email address to get the activation email)
   3. user activation api (enter the uid and token from your email to activate the user and once you activated your user successfully you will be notified on your email)
   4. jwt create token api -> (once you got the access token then use access token in request header as bearer token)
   5. list registered user api -> (need access token)
   6. list packages -> (need access token)
   7. update package -> (need access token where only superuser can update packages)
   8. get scrapped data -> (need access token and if you are admin youll be able to see all user history and if you are normal user you'll be able to see your history only)
   9. extract api -> (need access token if you are admin you can scrape unlimited searches and if you are normal user you can scrape trial limit only)
      10. Extract api will give you all the extracted information and amazon product file link which you can download by opening in browser


## What are we scrapping
1. amazon product
2. linkedin company profile
3. google answer

## Issues
1. Linkedin platform is not permitting to get user name or user url form the people section of the company page. We need to follow some other flow to scrape employees data and get their twitter handle if possible.
2. Once you give company name to scrape for - we search that keyword in linkedin search box to get all the result but the issue is each company own multiple pages and sometimes irrelevant searches appears, in that case we are using cosine similarity between given search term and list of company names from search result which gives us the most relevant company name to search the appropriate linkedin profile for further scrapping.
3. Amazon might give some irrelevant products in that case we have to implement brand name similarity metrix to match the product brand which could be added as a features.