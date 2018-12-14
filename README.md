# Online Cookbook

A fully resposive web application where users can access cooking recipes easily through a number of search and navigation options,
as well as share their own recipes with others. Users can also favourite others' recipes in order to show their support/like of 
that recipe and to quickly access it later on without having to search for it all over again.


## UX

The design is based around the [Materialize](https://materializecss.com/) library and was achieved by customizing it. 
Its minimalistic in order to be easy to use and not confuse users unnecessarily.

* Upon entering the web application, a user is presented with a login form and an option to register in order
  to start sharing recipes. A carousel is positioned below that showing off the ten most
  popular recipes in order to let the user know which are popular at the moment. A user can
  choose to switch the carousel to show either the ten most recent recipes or the ten least popular recipes.

* In order to give the user a way to quickly get a feel for what recipes there are, the navigation
  bar contains dropdoww menus with links to browse recipes based on major criteria grouping such as category,
  cuisine or allergen. The resulting list of recipes can be sorted by popularity or date and it includes the number
  of matching recipes.

* If a user wants to search through all the recipes in the databse, they can select the 'All recipes' link
  which will redirect the user to a list of all the recipes and options to fiter and search through them.
  A user can either choose to search by title or ingredient, or filter by category, cuisine or allergen or a combination
  of all of them. Whenever a user uses the search and filter options, their chosen search criteria are
  displayed below in case the user forgets what they searched for.
  Recipes matching the search criteria can be sorted by popularity and date.

* In order to not overwhelm the user and to make it easier to search through recipes, the number of recipes
  displayed per page is limited to 9, with subsequent 9 recipes appearing on the next page and so on. Pagination
  navigation is only visible if there is at least 1 recipe returned for the search criteria.

* Clicking on a recipe's image or title will take the user to a page displaying all the information for that recipe.
  Here initially all the information is visible but if for example the user is only interested in the ingredients, they can
  collapse the other information for better readability. The details of a recipe can also be printed
  in order to allow a user to have a physical copy of the recipe.

* Once a user creates an account or logs in, they are greeted with a welcome message and can begin sharing and favouriting
  recipes. Each recipe card has a favourite button in the shape of a star which can only be clicked
  if a user is logged in and hasn't favourited the recipe yet(if they have, the star will be solid rather than an outline).
  Once a recipe is favourited, its vote/like score will increase by 1 to reflect that. That recipe will be then added
  to that user's favourite recipes list which can be access by navigating to the user's profile.
  Recipes in the favourite recipes list can be removed from the list if a user chooses to do so, this will remove their 1 vote
  from that recipe's vote score. A removed recipe can be favourited again at any time.

* Navigating to a user's profile allows that user to add a new recipe of their own. This takes them to a page where they have to
  fill out all the neccessary information. The user's username is automatically set as the author of the recipe.
  In case a user doesn't have a picture of the recipe to link to or the link is not a valid url, the recipe will be supplied with a default image so as not to have
  recipes with blank space for an image.
  Once a recipe has been added by a user, it will show up in their 'my recipes' list. This list can be sorted by
  popularity and date and the total number of recipes it contains is displayed as well for the user's convenience.
  All the information of a user's own recipes can be edited and an own recipe can be deleted(permanently) from the databse.
  
* When a user is adding or editing a recipe, nutritional and allergen information is not required nor is cooking time, the rest of non-required
  fields will be set to default values. This means that when searching for recipes by criteria such as an allergen, recipes
  containing that allergen might be displayed simply due to the author not specifying that allergen.

Mockups in a pdf format and user stories can be found here [UX assets](static/assets/ux)

The final version of the project differs from the mockups. 
As I developed the project I would realize that some of the design decisions weren't 
the right solutions and I would update them on the go.


## Database Schema

Details on the finalized database schema can be found here [Schema](static/assets/databse_schema)

## Features 

* Basic user registration and authentication 
* Persistent databse of recipes
* Quick navigation options to recipes grouped by major criteria such as category, cuisine or allergen
* Modified Materialize carousels showing off ten recipes each for popular, recent and least popular recipes
* Ability to add, edit and delete a recipe by a registered user
* Ability to favourite and unfavourite a recipe by a registered user
* Ability to search through recipes by title, ingredient, allergen, category, cuisine or a combination of any of those
* Ability to sort the displayed recipes by popularity or date
* Simple statistics showing how many recipes match search criteria, how many recipes a user added or favourited
* If number of returned recipes is too large, they are split into separate pages each displaying 9 recipes(pagination)
* Can print the detailed information of a recipe
 
## Technologies

* [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
  * Used for structuring content
* [SCSS](https://sass-lang.com/)
  * Used for the presentation of the page
* [Materialize](https://materializecss.com/) and [Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox)
  * Used for the layout of the page, with materialize also used for it's UI components
* [JavaScript](https://www.javascript.com/)
  * Used for interactive functionality
* [JQuery](https://jquery.com/)
  * Used to simplify DOM manipulation
* [Flask](http://flask.pocoo.org/)
  * Used for structuring the back-end
* [Jinja](http://jinja.pocoo.org/)
  * Used for generating web pages
* [Python](https://www.python.org/)
  * Used for logic of the game
* [MongoDB](https://www.mongodb.com/)
  * Used for the database
* [mLab](https://mlab.com/home)
  * Used for hosting the databse
* [python-dotenv](https://github.com/theskumar/python-dotenv)
  * Used for hiding environment variables
* [validators](https://validators.readthedocs.io/en/latest/)
  * Used for validating image urls 
* [PyMongo](https://api.mongodb.com/python/current/)
  * MongoDB driver for python used to access the MongoDB database
* [BSON](http://bsonspec.org/)
  * Used for manipulating the "_id" value of a document
* [Markdown](https://en.wikipedia.org/wiki/Markdown)
  * Used for formatting user_stories.md and README.md

## Testing 

### Manual Tests

1. **Index:**
   
    i. Attempt to log in with an unregistered username and password, verify that a message appears stating 'Account with this username does not exist'
   
    ii. Attempt to log in with a registered username but wrong password, verify a message is displayed stating 'incorrect password, try again'

    iii. Attempt to log in with a registered username and correct password, verify page is refreshed and the login form is replaced with a welcome message
    
    iv. Attempt to close the page and open it again, verify a user is still logged in
    
    v. Attempt to select the 'Recent' carousel by clicking on the heading, verify the carousel changes to display the ten most recent recipes
    
    vi. Attempt to select the 'Oldest' carousel by clicking on the heading, verify the carousel changes to display the ten oldest recipes
    
    vii. Attempt to select the 'Most Popular' carousel by clicking on the heading, verify the carousel changes to display the ten most popular recipes
    
    viii. Attempt to click on the favourite button of a recipe inside one of the carousels, verify page refreshes, the button is now filled in and the number of times
    the recipe has been favourited has increased by 1.
    
    ix. Attempt to click the favourite button of that same recipe again, verify it cannot be clicked
    
    x. Attempt to log out, verify page refreshes and instead of a welcome message, the login form is displayed again.
    
    xi. Attempt to click on the favourite button of a recipe inside one of the carousels, verify it cannot be clicked
    
    xii. Attempt to either click the link inside the login form to register or the navigation link on the navbar, verify being redirected
    to a registration page
    
2. **Registration:**
    i. Attempt to register with a username already being used, verify a message is displayed stating 'This username is already taken'

    ii. Attempt to register with a unique username and a password shorter than 8 characters, verify being informed the password has to be at least
    8 characters long
    
    iii. Attempt to register with a unique username and password at least 8 characters long, verify being redirected to the index
    page where the login form has been replaced by a welcome message reflecting being logged in
    
3. **Summary/Groups navigation and page:**

    i. Attempt to hover over one of the summary navigation links, verify a dropdown appears containing relevant links
    
    ii. Attempt to click on one of the links inside the dropdown, verify being redirected to a page showing a list of recipes
    limited to that criteria
    
    iii. Attempt to sort the recipes on this page by most popular, verify recipes are listed in descending order by number of times favourited
    
4. **All recipes page:**

    i. From the index page, attempt to activate the 'All recipes' navigation link, verify being redirected to a page containing
    a list of all the recipes, options to search and filter through them as well as sort the list of recipes and pagination links are displayed 
    at the bottom of the page if the number of recipes is greater than 9 while showing only 9 recipes per page
    
    ii. Attempt to search recipes by chosen title, verify a recipe of that title is displayed, that the field 'Search:' displays
    your chosen title as text and that the 'Results' field shows '1 out of (total number of recipes) recipes'. 
    
    iii. Attempt to search by chosen ingredient, verify recipes containing that ingredient are displayed and that the field 'Search:' now
    displays the chosen ingredient
    
    iv. Attempt to filter by chosen category, verify recipes in that category are displayed and the 'Search:' field displays
    chosen category
    
    v. Attempt to filter by chosen cuisine, verify recipes of that cuisine are display and the 'Search:' field displays 
    chosen cuisine
    
    vi. Attempt to filter by chosen allergen, verify recipes displayed do not contain that allergen(in allergen section) and 
    the 'Search:' field displays chosen allergen
    
    vii. Attempt to search and filter through a combination of all of the above, verify only recipes matching all criteria are
    displayed and the 'Search:' field displays all the search criteria
    
    viii. While recipes matching some criteria are displayed, sort the recipes by least popular, verify recipes displayed are still
    only those that match the criteria and that they are now ordered in ascending order by number of times favourited
    
5. **Recipe details page:**

    i. Click on any recipes image or title and verify being redirected to a page containing detailes about that recipe with none of
    the elements showing collapsed
    
    ii. Attempt to collapse one of the section, e.g. Instructions, verify the Instructions section collapses and only the heading is visible
    
    iii. Attempt to expand the Instructions section by clicking on the heading, verify the Instructions section expands to reveal the instructions
    
    iv. Attempt to print the recipe information by clicking on the 'Print this recipe' link, verify being taken to a new window where
    the information about the recipe is the only thing displated a it is styled differently than on the recipe details page. Verify a print window
    opens to allow for printing the recipe. Verify that once printed, the window closes.
    
6. **Account:**
    
    i. Navigate to the account page, verify there are 2 headings for my recipes and favourite recipes with 'My recipes'
    having an orange background to signify it's the current page and a button to add new recipe

    ii. Navigate to the favourits page by clicking the 'Favourites' heading on the account page, verify being redirected
    to a page containing a list of favourited recipes which can be sorted.
    
    iii. On the my recipes page, attempt to add a new recipe, verify being redirected to a page where all the recipe
    information can be entered.
    
    iv. Attempt to add a recipe without filling out any information, verify that title, description, image, preparation time
    and two of each, ingredients and instructions have to be filled out in order to create the recipe.
    
    v. Attempt to add another ingredient or instruction, verify a new input field appears
    
    vi. Attempt to remove all the ingredient or instruction input fields, verify that the first 2 input fields for each cannot be removed
    
    vii. Attempt to fill out the details of the recipe and to create a new recipe, verify being redirected back to the account page where
    in 'My recipes', the new recipe appears.
    
    viii. Attempt to edit this recipe, verify being redirected to a page where all that recipe's information can be edited
    
    ix. Attempt to update the recipe with a wrong image url, verify that upon being redirected to the account page, the recipe
    now has a default image
    
    x. Attempt to delete the recipe, verify that the recipe has been removed and is not longer being displayed
    
    xi. After favouriting a recipe, attempt to navigate to the 'Favourites' page, verify the favourited recipe appears on the page
    
    xii. Attempt to remove the favourited recipe, verify it is gone from the list, it's number of times favourited has decreased by
    1 and it can be favourited again.
    
7. **Pagination:**

    i. Attempt to navigate to the 'All recipes' page and verify the number of recipes displayed on the first page is 9 and verify
    that being on the first page, the arrow for previous page is disabled
    
    ii. Attempt to navigate to the next page either using arrows or selecting the page number itself, verify being redirected
    to a page where the next 9 recipes are shown. On the last page, verify the arrow for the next page is disabled.
    
### Automated Tests

* [W3C Markup Validation Service](https://validator.w3.org/)
  * Used for testing html
* [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
  * Used for testing css
* [Mobile Friendly Test](https://search.google.com/test/mobile-friendly)
  * Used for testing mobile layout
* [JSHint](https://jshint.com/)
  * Used for testing JavaScript
 
### Bugs

* When expanding a window on the index page from mobile resolution, the carousel items on either side of the current one will become visible
* until the page is refreshed or another carousel is activated or another recipe on that carousel is navigated to. Haven't found the solution to this yet.

## Deployment 

Deployed on Heroku at [Guess The Flag](https://guess-the-country-by-flag.herokuapp.com/).

* Clone the repository by copying the clone url
* In the terminal type `git clone` followed by the copied url
* `cd` into `guess-the-flag`
* In the terminal type `pip3 install -r requirements.txt` to install all the dependencies 
* Create an account on Heroku if you don't have one yet and create a new app
* In the terminal, type `echo "web: python main.py" > Procfile`
* Create a new folder inside the apps directory called secret_settings and in it a .env file
* In the .env file set DBNAME, URI and SECRET_KEY
* In the terminal, `heroku login`
* `git init` to create a new repository
* `heroku git:remote -a (name of your heroku app, no brackets)`
* `git add .`
* `git commit -m "Initial commit"`
* `git push heroku master`
* `heroku ps:scale web=1`
* In your heroku app navigate to settings and reveal config vars, set IP = 0.0.0.0, PORT = 5000, DBNAME, URI and SECRET_KEY
* `restart all dynos and open your heroku app`

## Credits

### Content 

* Recipes - [BBC Good Food](https://www.bbcgoodfood.com)

### Images 

* Background image - [PAVBCA](http://pavbca.com/walls/spice-wallpapers)
* Recipe images - [BBC Good Food](https://www.bbcgoodfood.com)

### CSS 

* Hover effects - [Hover.css](http://ianlunn.github.io/Hover/)

#### Fonts

* Roboto - [Google Fonts](https://fonts.google.com/)
* Font Awesome - [Font Awesome](https://fontawesome.com/?from=io)


## License

MIT
