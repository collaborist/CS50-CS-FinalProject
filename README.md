# Translit & Convert
#### Video Demo: https://youtu.be/5wegp5yQ-1k
#### Description:
My project is designed to solve two tasks:

1. Transliterate any Russian text to English according to the standards of the Federal Migration Service of Russia, issuing international passports.
2. Have the ability to conveniently choose a time for an online call with friends in different time zones. I can easily see what time it will be for me if they specify their local time. Also, knowing my time, I can tell what time will it be in their time zone.

The project utilizes technologies such as Flask, SQL, HTML, CSS, and JavaScript.

The project consists of the following files:
* app.py - the main Flask file that brings together the entire project and contains all the internal logic of my website project.
* helpers.py - an auxiliary Python file taken from the Finance problem set for the purpose of using the apology and login_required functions to generate an error page and indicate the need to log in to the account, respectively.
* In the _templates_ folder, there are HTML pages of the project:
    - apology.html - a page for displaying error code and error text. I use it in such cases as:
        - user didn't provide username or password during Sigh In process;
        - user didn't provide correct password during Sigh In process;
        - user didn't provide correct username, password or password confirmation during Sigh Up process.
    - index.html - the home page of the site, which contains:
        - online form to input Russian text (non-Russian symbols are allowed);
        - textarea to show the results of transliteration procedure (non-Russian symbols stay as they are);
        - _Clear_ button to erase all results;
        - _Copy to Clipboard_ button to copy the results.
        - _Don't have an account_ hyperlink to get to the registration page in case you don't have an account.
    - layout.html - a template page based on which all other HTML pages of the project are generated. It contains Navigational bar and CDN inserts of _bootstrap_, _jQuery_, _clipboard.js_, _luxon.js_, _select2.js_.
    - login.html - a page with a login forms:
        - username input form;
        - password input form;
        - _Sign In_ button to get access to the web-site.
    - register.html - a page to create a new account using such forms as:
        - username input form;
        - password input form;
        - password confirmation input form;
        - _Sign Up_ button to create an account.
    - roman.html - an auxiliary page for generating transliteration;
    - timezone.html - a page where the conversion of time from one time zone to another is implemented. Contains following elements:
        - _Choose your Timezone_ selector with options gathered from _timezone_ table. Default options is selected by parsing your local timezone name;
        - _Choose your friend's Timezone_ selector with options gathered from _timezone_ table. You supposed to choose one option. There is a search field to find proper timezone faster.
        - Your local time input form. You may change it.
        - Your friend's loca time input form. You may change it too.
* In the _static_ folder, there is a styles.css file responsible for styling and visually displaying elements of the site. I utilized _Bootstrap_'s styling capabilities, but there is an opportunity to make adjustments using _CSS_ features.
* In the root folder, there is the _time_zone.db_ database, which contains the following tables:
    - users - a table with usernames and hashes of their passwords;
    - letters - a table mapping English letters to Russian ones according to transliteration rules;
    - timezones - a table with the names of existing time zones;
    - sqlite_sequence - a table tracking the last sequence element for each of the tables above.
