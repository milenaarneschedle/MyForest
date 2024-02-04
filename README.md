# MyForest
#### Video Demo:  https://youtu.be/RMBicI5cxws
#### Description:
In a world full of hustle culture and self optimization, it can be hard not to compare yourself and value small actions and thoughts as actual achievements. MyForest is a browser based web application based on the Finance PSET using Flask, Python, SQL, HTML, CSS and JavaScript where the user grows their own forest by noting personal achievements of all kind.

## Design
### Colors
The design of the application is limited to three colors, using green and brown for the background and orange for the font and the interactive elements. The same colors can be found in the images for the rewards (further explained at the myforest function).
While aiming for a forest and fox inspired optic, these three colors happen to have very interesting meanings in color psychology.
**Green** stands for growth, regeneration, balance, harmony and security
**Brown** stands for stability, structure, being grounded and and calm
**Orange** is adding an appealing contrast, standing for extravagance, positivity and optimism

### Structure/Philosophy
Thea aforementioned meanings of colors are exactly the feeling MyForest wants its users to experience. It is supposed to be a place isolated form a world constantlz demanding of ud to be stronger, better, smarter, faster or richer, to achieve crazier and crazier goals and push ourselves to higher and higher limits. While not all of this is necessarily bad or toxic, not all people have the same oppotunities to reach limits of the same kind. Social media is overflooding us with the outstanding accomplishments of others and rarely making us see their breakdowns, failures and other lows. We not only tend to compare ourselves to others and taling ourselves down, we also have such high expectations of what a real accoplishment is, it become very hard to accomplish something without is being overshone by something bigger, harder and better, done by someone younger, smarter and more successful.

It was a concious decision to disable any kind of interaction between the users. A MyForest account should be a safe space where you, if you really must, can only compare yourself to you. Despite creting a functioning delete function first, I have decided against it, for the following reason (also displayed on the "My Achievements" page):

> _Sometimes, our view on what is or is not an achievement, changes. You might have a moment where some achievements you wrote down in the past, seem embarassing or not productive enough. It could also happen that we did something that made us feel good an proud of ourselves and at some point we notice we have actually ignored our needs to meet an outside expectation of what should be productive and achieveable. Or we noticed we have hurt somebody with a bahavior that felt good but was not justified. In this case it could become attractive to delete those memories and start fresh. But just like in life, we cannot make those actions undone. And they made us feel good about ourselves in the moment we wrote them down after all. If this happens, think about it this way: You noticed the "mistake", thought it through, forgave yourself for it and decided to do it differently next time. Congratulations, you got yourself another achievement!_

### Foxes/Accordion Elements
Since foxes are known for being smart an often depicted as such in stories, certain hints, advices on how to use MyForest and what could be considered an achievement, are placed within Bootstrap Accordions labeled "What does the fox say?" - named after the 2013 hit song by Ylvis.


## Functions
### Register.
For the registration, the user will not only be asked to choose a username and password, but also a security question and answer. Password and answer will be hashed in a SQL table called users

### Login/Forgot Password/Change Password
Below the login form, which asks for username and password, is a link labeled "forgot password?". Once the user provided an existing username, they will be asked the security question and have to provide the correct answer. After, they will be directed to a page where they can choose a new password and log in again.
A similar version is provided for already logged in users, where they can change their password by providing their old password and selecting a new one.

### New Achievement
The newachievement function asks the user to note a personal achievement. All achievements must be stored in a folder. The user can either choose an existing folder from a select menu or create a new folder. The name of the new folder is limited to a maximum of 40 characters and cannot have a name identical to an existing folder.

### My Folders
Here, the user will be provided with their folder they can click on to access the achievements saved in them.

### Openfolder
Inside of the folder, the foldername can be changed using the rename function. Each achievement can be selected through a checkbox typed input and moved to either an existing folder or a directly created new folder. If all achievements are moved to a different folder, the old folder gets automatically deleted. The user gets redirected to the My Folders page and is provided with the updated number and names of Folders.

### My Achievements/Edit
The complete list of a user's achievements can be seen at My Achievements, including the name of the folder they are stored in, the date they were created, the reward the user received for it (further explained at the MyForest function), as well as a Button directing the user to a form where the selected achievement can be edited. Despite writing a working delete function, I conceptionally decided against a feature of deleting achievements, since something you would not consider an achievement anymore after some time still felt like one in the Moment of its creation. If something did not make someone feel good on second thought, the new achievement is bla

### My Forest
For every achievement the user notes, they receive a tree as a reward. for every tenth achievement, they receive a bird and for every hundreth a fox. The idea is to grow a forest out of your own achievements, creating your own breathing ecosystem by simply investing in yourself - not in the sense of productivity, but in the sense of kindness and patience towards yourself and being good as you are. The forest will be displayed on the page. Counters inside the users table as well as the new achievement function keep track of when to provide which reward.

### Flash messages
Flashed danger messages will appear for
-required inputs not given by the users
-password and confirmation not matching
-already existing user and folder names
-folder names longer than 40 characters
-incorrect password or answer to security question
-unknown username in the forgotpassword function

## SQL tables
I have used two SQL tables, accessible via final.db.
The **users** table stores the user's ID, username, password (hashed), the security question, it's answer (hashed) and keeps track of the different kinds of rewards, using a tree counter, a bird counter and a fox counter. They are being managed within the newachievement function.

The **achievements** table stores every achievement a user writes down, together with the user's ID, the folder it is saved in, the date it was created and the type of reward

## Future Improvements
Creating a version for mobile devices

## Sources
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

https://flask.palletsprojects.com/en/2.0.x/quickstart/

https://htmlcolorcodes.com/

https://stackoverflow.com/questions/44913155/using-multiple-vendor-specific-css-selectors-at-once/45045464

https://pixabay.com/

https://getbootstrap.com/docs/5.3/getting-started/introduction/

login_required/after_request/logout/parts of login: CS50 PSET "Finance"
