# CS50 Final Project - Typing Test

This is a website which allows the user to take a typing test. After the test, the website will show how many words he misspelled, how many words he spelled correctly, and how many correct characters he typed.

Here is some of the Technologies used: 

- Django
- Sqlite3
- Bootstrap
- jquery
- Ajax

## How the webpage works?

When the user presses the space bar, the program will get the value inside of the input and compare it to the word that is being typed. If it is correct, it will make the current word into blue by adding a class called correct and move the current word into the next word
. It will also add 1 to the corrent word count and add the length of the current word to correct character count. If it is incorrect it will make the current word into red by adding a class caleed wrong and move the current word into the next word and adding 1 to error count. When the timer hits to 0, the input box becomes hidden and the error count, correct word count, and the correct character count becomes shown. Then correct word count will be then stored in the db so that the user can see them again in score.

### Database

Database stores all users, the scores they got for each test and the sample texts for the typing test.

## Possible improvements

As all applications this one can also be improved. Possible improvements:

- Make it so that the timer starts when a person types something.
- Make the sample text more random.


## How to launch application

1. Get the code and delete the db files.
2. Run command `python3 manage.py makemigrations` to make migrations.
3. Run command `python3 manage.py migrate` to migrate.
4. Run command `python3 manage.py createsuperuser` to make an admin.
5. Run command `python3 manage.py runserver` to make the server run.
6. Go to your web browser and type in `http://127.0.0.1:8000/` for the website.
7. You are ready to go!
