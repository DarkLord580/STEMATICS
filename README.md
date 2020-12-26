**Getting Started**


for this you will need everything except the db.sqlite3 and other files that are related to db. After that you will need to make migrations using the command "python3 manage.py makemigrations" and then migrating it with "python3 manage.py migrate". Then make a super user(admin) for the website with the code "python3 manage.py makesuperuser". I made a code for putting texts for typing and you can run that by "python3 test_populate.py"


**website**


this website allows the user to take a typing speed test which after you take it will show how many words you got wrong, how many you got right and how many characters you got right. To start this, you will have to click the typing test. Then you will be lead to a page with some text, a start button, and a input box. After you type in some string for the program, the program will change the color to blue if you got the word correctly and red if you got it incorrectly. After taking the test, you will be able to go again with the button saying Go Again. Finally there is a tab with scores. That will show you the correct words that you got, and the date ordered in chorological order.
