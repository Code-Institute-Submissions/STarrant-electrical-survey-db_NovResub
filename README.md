# Electrical Survey DB : Switchroom Safety Database

* A data-driven web application for tracking electrical safety issues across your site(s).

## Contents

---

* UX
  * Project Goals
    * User Goals
    * User Stories
    * Site Owner Goals
    * User Requirements and Expectations
    * Design Choices
      * Fonts
        * Icons
        * Colours
* Technologies
* Features
  * Features that have been developed
    * Features that will be implemented in the future
* Testing
* Bugs
* Deployment
* Credits

## UX (User Experience)

---

### Project Goals

* The goal of this project is to create a simple to use data-driven site to track electrical safety issues.

### User Goals

* User registration available to sign up as a site-user.
* View, add, modify and delete electrical rooms from the survey.
* View, add, modify and delete survey questions from the site.
* Create individual issue notifications.
* Get an overview of the status of all the surveyed rooms.

### User Stories

* As a **user**, I want to see a simple, intuitive interface that requires zero learning to use.
* As a **user**, I want to be able to use a mobile device to carry out a survey. (e.g. A tablet or mobile phone)
* As a **user**, I want to be able to view a list of the electrical rooms.
* As a **user**, I want to be able to add a new electrical room to the survey.
* As a **user**, I want to be able to modify an electrical room's details.
* As a **user**, I want to be able to delete an electrical room from the survey.
* As a **user**, I want to be able to carry out an electrical survey of a room and save the data to the site.
* As a **user**, I want to be able view the results of surveys carried out.
* As a **user**, I want to be able see an overview of current issues.

### Site Owner Goals

* As a **site-owner**, I want to be able to see a list of users for the site.
* As a **site-owner**, I want to have user authentication to ensure malicious activity is avoided.
* As a **site-owner**, I want to be able to manage the electrical data for the site in a simple, effective and secure way.

### User Requirements and Expectations

#### Requirements

* Simple, responsive, data-driven site.
* Fast loading times are imperative.
* No frills, high-contrast layout for maximum legibity since this site will primarily be used on mobile devices in the field.
* Intuitive navigation and site operation with flash messages for good UX.

#### Expectations

* Content is visually minimalist and clear to look at.
* The design is responsive and will work across a wide variety of screen sizes.
* No frills to ensure fast loading times.

### Design Choices

---

In terms of design, the standard materialize fonts and color schemes were used for the sake of simplicity. An amber-yellow color scheme was chosen to reflect the relevance of this site to safety with these colors being synonymous with ISO7010 warning signage.

#### Fonts

* [Materialize Typography](https://materializecss.com/typography.html) has been used throughout the site. With legibilty and ease of eye strain being a key focus for site users, the standard Materialize fonts are excellent.

#### Icons

* [FontAwesome](https://fontawesome.com/) free icons were used throughout this project.

#### Colors

The website colors were chosen using [Materialize Colors](https://materializecss.com/color.html).

## Wireframing

<details>
  <summary>Wireframing was done using Balsamiq under full-functional trial provided by Code Institute.
Wireframes were developed for an add room screen as this was the only element of the project successfully implemented.
Other aspects of the design developed more organically.
NOTE TO CORRECTOR: OTHER WIREFRAMES SHOULD HAVE BEEN DEVELOPED FOR OTHER SCREENS.
</summary>

### Project Wireframes

* Add a room screen
* ![Add a room screen wireframe](/wireframes/wf_add_room_screen.png)

</details>

---

## Features

---
**Features** that have been **implemented:**

* User authentication with log in and logout functions available.
* User profile page with username, First Name, Surname and Company name available.
* List of DB rooms is available with each of the details available in collapsible elements.
* Create, update and delete possible to rooms and their details.


**Features** that will be **implemented** in the **future:**

* List of survey questions will be available with each of the details available in collapsible elements.
* Create, update and delete possible to survey questions.
* Overview of status of electrical rooms with pass/fail point numbers.
* List of users on the site with edit and delete possible for admin users.
* Carry out an electrical survey and store the data.
* View completed surveys and edit results.
* Create a single inspection point.


## Technologies Used

---

### Languages

* HTML
* CSS
* JavaScript
* Python

### Tools & Libraries

* [Git](https://git-scm.com/)
* [Bootstrap](https://getbootstrap.com/)
* [Popper](https://popper.js.org/)
* [JQuery](https://jquery.com/)
* [Google fonts](https://fonts.google.com/)
* [Markdownlint](https://dlaa.me/markdownlint/)
* [W3C HTML Validator](https://validator.w3.org/)
* [W3C CSS Validator](https://jigsaw.w3.org/css-validator/validator)
* [JSHint](https://jshint.com/)
* [MongoDB](https://www.mongodb.com/)
* [Heroku](https://www.heroku.com/)
* [Jinja Templating for Python](https://jinja.palletsprojects.com/en/3.0.x/)
* [Random Key Generator](https://randomkeygen.com/)


## Testing

---

### HTML Test

HTML code has been tested using the [HTML Validator](https://validator.w3.org/) and gave the following error:

#### HTML Test Errors

* All errors related to illegal characters because of Jinja templating used.

#### HTML Test Fixes

* N/A

### CSS Test

CSS code has been tested using the [CSS validator](http://jigsaw.w3.org/css-validator/) and gave the following errors and warnings.

#### CSS Test Errors

* No errors.

#### CSS Test Warnings

* N/A

#### CSS Test Fixes

* N/A

### JavaScript Test

#### JavaScript Test Errors

* No errors.

#### JavaScript Test Warnings

* N/A

#### JavaScript Test Fixes

* N/A

### Python Test

#### Python Test Errors

* Python errors were fixed using Gitpods built in linter to reduce error down to the single remaining error relating to env.py.
* Most python issue were minor and relating to PEP8 complaince.

#### Python Test Warnings

* N/A

#### Python Test Fixes

* N/A

### Responsiveness

<details>
  <summary>Responsiveness of the design was not tested. It will be tested using Chrome's Developer Tools in future.</summary>

#### Summary of responsive design tests

* Site Responsiveness has not been tested.

</details>

### Design

* The idea for doing this project came from an Excel sheet that I had developed as part of my dayjob as an electrical engineer. I work in a very large industrial plant with over 80 electrical switchrooms so I developed a survey system to check for electrical issues across the site. A hard-copy survey sheet is filled out on paper and manually typed into Excel at the end of the survey run. The system works very well but is hugely labourious. The goal of this project is to use state-of-the-art web technology to make this a seamless process.

### User Stories

<details>
  <summary>User stories have not been tested.</summary>
  
#### Summary of user tests

* Test: NOT TESTED
* Result: NOT TESTED


</details>

## Bugs

---

Many bugs were encountered during the development of the project - all admittedly of my own making.

### Development Bugs

* Bug 1
* Bug 2
* Bug 3
* Bug 4
* Bug 5

### Testing Bugs

* A few bugs were thrown up during development and generally centered around getting .

## Deployment

---

The site has been deployed on [Heroku](https://www.heroku.com/) with under the following link [electrical-survey-db](http://electrical-survey-db.herokuapp.com/).

## Credits

---

* [JSHint.com](https://jshint.com/) was used to error check the JavaScript code.
* [Markdown guide basic syntax](https://www.markdownguide.org/basic-syntax/) was used as a reference in writing the README.md file.
* [Markdownlint](https://dlaa.me/markdownlint/) by [David Anson](https://github.com/DavidAnson) was used for correcting the errors in my markdown. It is an awesome resource and saved me hours of correction time.
* Code for box shadow on headers generated by [cssgenerator.org](https://cssgenerator.org/box-shadow-css-generator.html).

### Special Thanks

* My Code Institute mentor, [Simen Daehlin](https://github.com/Eventyret). 
* [Tim Nelson](https://github.com/TravelTimN) for his superb walk-through project on which this site is based. Without his tutorial videos, I would never have got Heroku, Github, Gitpod, Python, Jinja and Mongo all working together.

