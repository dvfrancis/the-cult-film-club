# DRAFT (NOT YET FINALISED)

[Return to the Cult Film Club README.md](https://github.com/dvfrancis/the-cult-film-club)

# Testing of The Cult Film Club

## Index

1. [Code Validation](#code-validation)
2. [Manual Validation](#manual-validation)
    1. [index.html]()
    2. [bad_request.html]()
    3. [permission_denied.html]()
    4. [page_not_found.html]()
    5. [server_error.html]()
    6. [releases.html]()
    7. [release_details.html]()
    8. [product_management.html]()
    9. [edit_release.html]()
    10. [delete_release.html]()
    11. [manage_images.html]()
    12. [edit_image.html]()
    13. [discount_codes.html]()
    14. [edit_discount_code.html]()
    15. [delete_discount_code.html]()
    16. [cart.html]()
    17. [checkout.html]()
    18. [checkout_success.html]()
    19. [order_details.html]()
    20. [account.html]()
    21. [about.html]()
    22. [contact_us.html]()
    23. [newsletter.html]()
    24. [edit_newsletter_preferences.html]()
    25. [unsubscribe.html]()
    26. [signup.html]()
    27. [login.html]()
    28. [password_reset.html]()
    29. [logout.html]()
3. [User Story Validation](#user-story-validation)
    1. [First Time Visitor Goals](#first-time-visitor-goals)
    2. [Returning Visitor Goals](#returning-visitor-goals)
    3. [Frequent Visitor Goals](#frequent-visitor-goals)
4. [User Personas](#user-personas)
5. [Browser Compatibility](#browser-compatibility)
6. [Accessibility](#accessibility)
7. [Responsiveness](#responsiveness)
8. [Performance](#performance)
9. [Bugs](#bugs)
    1. [Resolved](#resolved)
    2. [Unresolved](#unresolved)

## Code Validation

### HTML

- The [W3C Markup Validation Service](https://validator.w3.org) was used to check all HTML. The code for each page was validated by direct input of the code copied from each rendered page. Click to view the [HTML report](documentation/validation/html-report.pdf).

- I did not test base.html directly, as it is a part of all other pages.

### CSS

- The [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator) was used to check base.css. Click to view the [CSS report](documentation/validation/css-report.pdf).

### JavaScript

- [JSHint](https://jshint.com/) was used to check base.js. Click to view the [JavaScript report](documentation/validation/javascript-report.pdf).

### Python

- The [CI Python Linter](https://pep8ci.herokuapp.com/) was used to check all Python code. Click to view the [Python report](documentation/validation/python-report.pdf).

## Manual Validation

### index.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Button link for 'Explore' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Button link for 'Register' | Click to open register.html | The user is directed to register.html | The user is directed to register.html | WORKS AS EXPECTED |
| Featured class link for 'Introduction to Cricut - Cutting Machine Basics' | Click to open details.html for database item 4 | The user is directed to details.html for database item 4 | The user is directed to details.html for database item 4 | WORKS AS EXPECTED |
| Featured class link for '3D Modelling for Fabric Designs' | Click to open details.html for database item 4 | The user is directed to details.html for database item 4 | The user is directed to details.html for database item 4 | WORKS AS EXPECTED |
| Featured class link for 'DIY Leathercraft with Digital Cutting Techniques' | Click to open details.html for database item 17 | The user is directed to details.html for database item 17 | The user is directed to details.html for database item 17 | WORKS AS EXPECTED |
| Featured class link for 'Laser-Engraved Wood & Acrylic Jewellery' | Click to open details.html for database item 22 | The user is directed to details.html for database item 22 | The user is directed to details.html for database item 22 | WORKS AS EXPECTED |
| Featured class link for 'Custom Sticker & Decal Design' | Click to open details.html for database item 8 | The user is directed to details.html for database item 8 | The user is directed to details.html for database item 8 | WORKS AS EXPECTED |
| Featured class link for '3D Printing Basics for DIY Crafting' | Click to open details.html for database item 11 | The user is directed to details.html for database item 11 | The user is directed to details.html for database item 11 | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### diary.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Button link for 'Details' (for all 21 classes listed) | Click to open details for that class in the database | The user is directed to details for that class in the database | The user is directed to details for that class in the database | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### details.html

These results apply to all 21 classes:

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| For a logged in user - button link to 'Enrol' | Click to enrol on the class selected | The user is enrolled on the class selected | The user is enrolled on the class selected | WORKS AS EXPECTED |
| For a logged in user - button link to go 'Back to Diary' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| For a logged in user, who is enrolled on this class - button link to 'Withdraw' | Click to withdraw from the class enrolled on | The user is withdrawn from the class enrolled on | The user is withdrawn from the class enrolled on | WORKS AS EXPECTED |
| For a non-logged in user - button link to 'Login' | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| For a non-logged in user - button link to 'Register' | Click to open register.html | The user is directed to register.html | The user is directed to register.html | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### faq.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Accordion header for all 14 items | Click to expand / collapse the section | The section expands / collapses  | The section expands / collapses | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### contact.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Input field for 'First name' | Where all other fields are empty, enter first name and click 'Send' | The user is asked to complete their last name | The user is asked to complete their last name | WORKS AS EXPECTED |
| Input field for 'Last name' | Where other fields are empty (excluding 'First name') enter last name and click 'Send' | The user is asked to complete their email address | The user is asked to complete their email address | WORKS AS EXPECTED |
| Input field for a valid 'Email' | Where other fields are empty (excluding 'First name' and 'Last name'), enter email address and click 'Send' | The user is asked to enter their message | The user is asked to enter their message | WORKS AS EXPECTED |
| Input field for an invalid 'Email' | Where other fields are empty (excluding 'First name' and 'Last name'), enter email address and click 'Send' | The email is rejected, and the user is asked to enter a valid email address | The email is rejected, and the user is asked to enter a valid email address | WORKS AS EXPECTED |
| Input field for 'Message' | Where all other fields are completed correctly, enter message and click 'Send' | The form is accepted, the message is emailed to the organisers, and the user receives a Toast informing them 'Your message has been sent' | The form is accepted, the message is emailed to the organisers, and the user receives aToast informing them 'Your message has been sent' | WORKS AS EXPECTED |
| Button link to 'Send' | When all fields are completed correctly, click 'Send' | The form is accepted, the message is emailed to the organisers, and the user receives a Toast informing them 'Your message has been sent' | The form is accepted, the message is emailed to the organisers, and the user receives a Toast informing them 'Your message has been sent' | WORKS AS EXPECTED |
| Button link to 'Clear' | Enter any information into the field, click 'Clear' | The form is cleared of any input | The form is cleared of any input | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### register.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Input field for 'Username' | Where all other fields are empty, enter username and click 'Register' | The user is asked to complete their email address | The user is asked to complete their email address | WORKS AS EXPECTED |
| Input field for 'First name' | Where all other fields are empty (excluding 'Username') enter first name and click 'Register' | The user is asked to complete their email address | The user is asked to complete their email address | WORKS AS EXPECTED |
| Input field for 'Last name' | Where other fields are empty (excluding 'Username') enter last name and click 'Register' | The user is asked to complete their email address | The user is asked to complete their email address | WORKS AS EXPECTED |
| Input field for a valid 'Email' | Where other fields are empty (excluding 'Username'), enter email address and click 'Register' | The user is asked to enter their password | The user is asked to enter their password | WORKS AS EXPECTED |
| Input field for an invalid 'Email' | Where other fields are empty (excluding 'Username'), enter email address and click 'Register' | The email is rejected, and the user is asked to enter a valid email address | The email is rejected, and the user is asked to enter a valid email address | WORKS AS EXPECTED |
| Input field for a valid 'Location' | Where other fields are empty (excluding 'Username'), enter location and click 'Register' | The user is asked to enter their password | The user is asked to enter their password | WORKS AS EXPECTED |
| Input field for a valid 'Experience Level' | Where other fields are empty (excluding 'Username'), select experience level from drop-down list and click 'Register' | The user is asked to enter their password | The user is asked to enter their password | WORKS AS EXPECTED |
| Input field for a valid 'Profile Picture' | Where other fields are empty (excluding 'Username'), select a picture and click 'Register' | The user is asked to enter their password | The user is asked to enter their password | WORKS AS EXPECTED |
| Input field for a valid 'Password' | Where other fields are empty (excluding 'Username', 'Email', and 'Location'), enter password and click 'Register' | The user is asked to confirm their password | The email is asked to confirm their password | WORKS AS EXPECTED |
| Input field for a valid 'Password' and 'Confirm Password' | Where other fields are empty (excluding 'Username', 'Email', and 'Location'), enter matching valid passwords and click 'Register' | The user account is created and logged in. The user is redirected to account.html, and receives the Toast message "Account created, and logged in" | The user account is created and logged in. The user is redirected to account.html, and receives the Toast message "Account created, and logged in" | WORKS AS EXPECTED |
| Input field for an invalid non-matching 'Password' and 'Confirm Password' | Where other fields are empty (excluding 'Username' and 'Email'), enter invalid non-matching passwords and click 'Register' | The password fields are cleared and the user receives a Toast message saying "The passwords do not match, or have not been entered. Please enter them again" | The password fields are cleared and the user receives a Toast message saying "The passwords do not match, or have not been entered. Please enter them again" | WORKS AS EXPECTED |
| Button link to 'Register' | Do not complete any fields and click 'Register' | The form returns to the 'Username' field ready for completion | The form returns to the 'Username' field ready for completion | WORKS AS EXPECTED |
| Button link to 'Clear' | Enter any information into the field, click 'Clear' | The form is cleared of any input | The form is cleared of any input | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### login.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Input field for 'Username' | Where all other fields are empty, enter username and click 'Login' | The user is asked to complete their password | The user is asked to complete their password | WORKS AS EXPECTED |
| Input field for 'Password' | Where all other fields are empty, enter password and click 'Login' | The user is asked to complete their username | The user is asked to complete their username | WORKS AS EXPECTED |
| Input field for a valid 'Username' and 'Password' | Enter a valid username and password, and click 'Login' | The user is logged in, redirected to account.html, and receives the Toast "You have been logged in successfully!" | The user is logged in, redirected to account.html, and receives the Toast "You have been logged in successfully!" | WORKS AS EXPECTED |
| Input field for a valid 'Username' and invalid 'Password' | Enter a valid username but invalid password, and click 'Login' | The password field is cleared and the user receives a Toast message saying "Invalid username or password. Please try again." | The password field is cleared and the user receives a Toast message saying "Invalid username or password. Please try again." | WORKS AS EXPECTED |
| Input field for a invalid 'Username' and valid 'Password' | Enter an invalid username but valid password, and click 'Login' | The password field is cleared and the user receives a Toast message saying "Invalid username or password. Please try again." | The password field is cleared and the user receives a Toast message saying "Invalid username or password. Please try again." | WORKS AS EXPECTED |
| Button link to 'Login' | Do not complete any fields and click 'Login' | The form returns to 'Username' and prompts for it to completed | The form returns to 'Username' and prompts for it to completed | WORKS AS EXPECTED |
| Button link to 'Clear' | Whether or not the fields are completed, click 'Clear' | Both fields are cleared of any input | Both fields are cleared of any input | WORKS AS EXPECTED |
| Button link to 'Register' | Whether or not the fields are completed, click 'Register' | The user is directed to register.html | The user is directed to register.html | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### account.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Button link beneath any class enrolments to view 'Details' | Click 'Details' below any enrolled class | The user is directed to details for that class in the database | The user is directed to details for that class in the database | WORKS AS EXPECTED |
| Button link beneath any class enrolments to view 'Withdraw' | Click 'Withdraw' below any enrolled class | The user is withdrawn from the class and the page updates automatically to remove the class from the list of enrolled classes; the user receives a Toast message saying "Your enrolment has been withdrawn" | The user is withdrawn from the class and the page updates automatically to remove the class from the list of enrolled classes; the user receives a Toast message saying "Your enrolment has been withdrawn" | WORKS AS EXPECTED |
| Button link to 'Logout' | Click 'Logout' | The user is logged out and returned to login.html | The user is logged out and returned to login.html | WORKS AS EXPECTED |
| Button link to 'Edit' | Click 'Edit' | The user is directed to update_profile.html | The user is directed to update_profile.html | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### update_profile.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Button link to 'Save' | Click 'Save' | Whether or not changes have been made, the details are saved and the user is redirected to account.html; the user receives a Toast message saying "Profile updated" | Whether or not changes have been made, the details are saved and the user is redirected to account.html; the user receives a Toast message saying "Profile updated" | WORKS AS EXPECTED |
| Button link to 'Clear' | Click 'Clear' | If changes have been made, the values revert to what was stored. Otherwise, nothing happens. | If changes have been made, the values revert to what was stored. Otherwise, nothing happens. | WORKS AS EXPECTED |
| Button link to 'Cancel' | Click 'Cancel' | No changes are made and the user is directed to account.html | No changes are made and the user is directed to account.html | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### 404.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Button link to 'Home' | Click 'Home' | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Button link to 'Go Back' | Click 'Go Back' | The user is directed to the page they were previously viewing | The user is directed to the page they were previously viewing | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

### 500.html

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Navigation link for site logo | Click logo to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Home' | Click to open index.html | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Navigation link for 'Classes' | Click to open diary.html | The user is directed to diary.html | The user is directed to diary.html | WORKS AS EXPECTED |
| Navigation link for 'FAQ' | Click to open faq.html | The user is directed to faq.html | The user is directed to faq.html | WORKS AS EXPECTED |
| Navigation link for 'Contact' | Click to open contact.html | The user is directed to contact.html | The user is directed to contact.html | WORKS AS EXPECTED |
| Navigation link for 'Register / Login' (when a user is NOT logged in) | Click to open login.html | The user is directed to login.html | The user is directed to login.html | WORKS AS EXPECTED |
| Navigation link for 'Account' (when a user is logged in) | Click to open account.html | The user is directed to account.html | The user is directed to account.html | WORKS AS EXPECTED |
| Button link to 'Home' | Click 'Home' | The user is directed to index.html | The user is directed to index.html | WORKS AS EXPECTED |
| Button link to 'Go Back' | Click 'Go Back' | The user is directed to the page they were previously viewing | The user is directed to the page they were previously viewing | WORKS AS EXPECTED |
| Link in footer for '© 2025 Dominic Francis All Rights Reserved' | Click to open dominicfrancis.co.uk in a new tab | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Facebook | Click to open Facebook in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Instagram | Click to open Instagram in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for Bluesky | Click to open Threads in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |
| Social media link for GitHub | Click to open the Craftr project repository in a new tab  | The link opens in a new tab  | The link opens in a new tab | WORKS AS EXPECTED |

## User Story Validation

### First Time Visitor Goals

"What is Craftr about?” and “How do I sign up?”

<details>
<summary>Click here to see proof of first time visitor goal number 1 and 4</summary>

![First time visitor goal 1 and 4](documentation/validation/users-stories-personas/first-time-visitor-goal-1-4.webp)
</details>

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Home page | Scroll down to the hero section and below | View information about the event, and register | View information about register | WORKS AS EXPECTED |

“What training is being given?” and "When do the classes happen?"

<details>
<summary>Click here to see proof of first time visitor goals 2 and 3</summary>

![First time visitor goal 2 and 3](documentation/validation/users-stories-personas/first-time-visitor-goal-2-3.webp)
</details>

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Classes page | Scroll down to the complete list of classes | See what classes are running, and at the exact day and time | See what classes are running, and at the exact day and time | WORKS AS EXPECTED |

### Returning Visitor Goals

“What other classes am I interested in attending?” and "When is my class due to start?"

<details>
<summary>Click here to see proof of the returning visitor goals 1 and 2</summary>

![Returning visitor goals 1 and 2](documentation/validation/users-stories-personas/returning-visitor-goal-1-2.webp)
</details>

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Classes page | Scroll down to the complete list of classes | See what classes are running, and at the exact day and time | See what classes are running, and at the exact day and time | WORKS AS EXPECTED |

"Where can I keep track of the classes I've signed up for?"

<details>
<summary>Click here to see proof of the returning visitor goals 3</summary>

![Returning visitor goal 3](documentation/validation/users-stories-personas/returning-visitor-goal-3.webp)
</details>

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Account page | When logged in, scroll down to the complete list of enrolled classes | User can see the exact classes they are enrolled on | User can see the exact classes they are enrolled on | WORKS AS EXPECTED |

### Frequent Visitor Goals

“Who running my class?”

<details>
<summary>Click here to see proof of frequent visitor goal 1</summary>

![Frequent visitor goal 1](documentation/validation/users-stories-personas/frequent-visitor-goal-1.webp)
</details>

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Details page | Navigate to the details of a particular class | Details of the instructor can be seen on the class details page | Details of the instructor can be seen on the class details page | WORKS AS EXPECTED | 

"How do I cancel my class enrolment?"

<details>
<summary>Click here to see proof of frequent visitor goal 2</summary>

![Frequent visitor goal 2](documentation/validation/users-stories-personas/frequent-visitor-goal-2.webp)
</details>

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Account page or Class Details page | Navigate to the user account page or the details of an enrolled class, and click 'Withdraw' by the relevant class | The user is no longer enrolled on the class | The user is no longer enrolled on the class | WORKS AS EXPECTED | 

"How can I contact the organisers of this event?"

<details>
<summary>Click here to see proof of frequent visitor goal 3</summary>

![Frequent visitor goal 3](documentation/validation/users-stories-personas/frequent-visitor-goal-3.webp)
</details>

| ITEM | PROCESS | EXPECTED RESULT | ACTUAL RESULT | STATUS |
| --- | --- | --- | --- | --- |
| Contact page | Complete the fields of the contact form and click send | The message is sent to the event organisers | The message is sent to the event organisers | WORKS AS EXPECTED | 

## User Personas

### User 1

| ISSUE | ACCEPTANCE CRITERIA | TASKS | STATUS |
| --- | --- | --- | --- |
| [#55](https://github.com/dvfrancis/craftr/issues/55) | Ensure users of all skill levels (beginner to advanced) find suitable classes | Label each class with its appropriate skill level | COMPLETED SUCCESSFULLY |
| [#56](https://github.com/dvfrancis/craftr/issues/56) | Provide an intuitive way to navigate the site and discover content | Design an intuitive navigation menu for easy browsing | COMPLETED SUCCESSFULLY |
| [#59](https://github.com/dvfrancis/craftr/issues/59) | Enable users to create accounts and track enrolments | Develop a user-friendly account creation and class tracking system | COMPLETED SUCCESSFULLY |

### User 2

| ISSUE | ACCEPTANCE CRITERIA | TASKS | STATUS |
| --- | --- | --- | ---|
| [#57](https://github.com/dvfrancis/craftr/issues/57) | Make diverse craft types visible and engaging on the homepage | Design an engaging homepage that showcases various craft types | COMPLETED SUCCESSFULLY |
| [#58](https://github.com/dvfrancis/craftr/issues/58) | Ensure information is easily accessible for first-time visitors | Ensure class details are prominently displayed and easy to locate | COMPLETED SUCCESSFULLY |
| [#57](https://github.com/dvfrancis/craftr/issues/57) | Create an inviting and user-friendly interface | Develop a clean and welcoming website layout | COMPLETED SUCCESSFULLY |

### User 3

| ISSUE | ACCEPTANCE CRITERIA | TASKS | STATUS |
| --- | --- | --- | ---|
| [#60](https://github.com/dvfrancis/craftr/issues/60) | Ensure class information is detailed and easily accessible | Maintain a well-organized and searchable class directory | COMPLETED SUCCESSFULLY |
| [#60](https://github.com/dvfrancis/craftr/issues/60) | Clearly outline instructor details and course descriptions | Provide comprehensive course descriptions, including instructor details | COMPLETED SUCCESSFULLY |
| [#54](https://github.com/dvfrancis/craftr/issues/54) | Make sharing information simple and effective  | Implement easy-to-use social media sharing features | COMPLETED SUCCESSFULLY |

## Browser Compatibility

### Google Chrome

<details>
<summary>Click here to view the site in Google Chrome</summary>

![Website in Google Chrome](documentation/browsers/website-google-chrome.png)
</details>

### Microsoft Edge

<details>
<summary>Click here to view the site in Microsoft Edge</summary>

![Website in Microsoft Edge](documentation/browsers/website-microsoft-edge.png)
</details>

### Firefox

<details>
<summary>Click here to view the site in Mozilla Firefox</summary>

![Website in Mozilla Firefox](documentation/browsers/website-mozilla-firefox.png)
</details>

### Opera

<details>
<summary>Click here to view the site in Opera</summary>

![Website in Opera](documentation/browsers/website-opera.png)
</details>

### Safari

<details>
<summary>Click here to view the site in Safari</summary>

![Website in Safari](documentation/browsers/website-safari.png)
</details>

## Accessibility

The [Wave Accessibility Evaluation Tool (WAVE)](https://wave.webaim.org) was used to create an [accessibility report](documentation/accessibility/accessibility-report.pdf) for this project.

## Responsiveness

Pages were going to be assessed using the [Responsive Web Design Checker](https://responsivedesignchecker.com/) but, unfortunately, the site won't load there. Instead, they have been presented using the [Responsive Viewer](https://chromewebstore.google.com/detail/responsive-viewer/inmopeiepgfljkpkidclfgbgbmfcennb?hl=en-GB&utm_source=ext_sidebar) Google Chrome browser plugin.

Pages were tested for responsiveness on mobile (Apple iPhone 14 - 390px x 844px), tablet (Apple iPad Air 5 - 820px x 1180px), and desktop (MacBook Pro 16 - 1728px x 1117px).

Click here to see the [Responsiveness report](documentation/validation/responsiveness/responsiveness-report.pdf)

## Performance

Both mobile and desktop page performance was assessed with [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/).

Click here to see the [Performance report](documentation/validation/performance/performance-report.pdf)

## Bugs

### Resolved

Resolved bugs match the cases raised on the project board attached to the GitGub repository. They're named after their GitHub issue number (so are not sequential).

#### Bug 61

<details>
<summary>Click here to see a screenshot of bug #61</summary>

![Fixed Bug 61](documentation/bugs/bug-61-1.webp)
</details>

<details>
<summary>Click here to see folder structure</summary>

![Fixed Bug 61 folder structure](documentation/bugs/bug-61-2.webp)
</details>

<details>
<summary>Click here to see the local site working</summary>

![Fixed Bug 61 working local site](documentation/bugs/bug-61-3.webp)
</details>

<details>
<summary>Click here to see the deployed site working</summary>

![Fixed Bug 61 working deployed site](documentation/bugs/bug-61-4.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#61](https://github.com/dvfrancis/craftr/issues/61) | Heroku deployment keeps failing with the error shown above. Settings.py, Procfile, and requirements.txt all checked and confirmed as correctly configured | When I first created the project I used the following command but forgot to add the full stop at the end `django-admin startproject craftr.` This meant that the files were created in a directory called craftr, and not directly in the root. The folders and files highlighted in the above folder structure image should be in the root. This also had a knock-on effect as the local server no longer worked either. This is because manage.py and db.sqlite3 ended up in the craftr folder, and not in the root as expected. Once they were moved to the root, the local server also started working again |

#### Bug 63

<details>
<summary>Click here to see a screenshot of bug #63</summary>

![Fixed Bug 63](documentation/bugs/bug-63.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#63](https://github.com/dvfrancis/craftr/issues/63) | Unable to login as supervisor | After migrating some changes to the database I was unable to login as superuser (as shown in the screenshot above). Django is attempting to access the profile field of a User object, but a corresponding UserProfile does not exist for that user. This often happens because of a misalignment between the User model and the UserProfile model's one-to-one relationship. I ran the python shell using `python manage.py shell`, and in the shell ran the commands shown below to create a profile for each user that was missing one. This ensured that every User had a UserProfile, and allowed the superuser to login successfully (see code below this table).

```Python
from django.contrib.auth.models import User
from register.models import UserProfile

for user in User.objects.all():
    UserProfile.objects.get_or_create(user=user)
```

#### Bug 64

<details>
<summary>Click here to see a screenshot of bug #64</summary>

![Fixed Bug 64](documentation/bugs/bug-64-1.webp)
</details>

<details>
<summary>Click here to see a screenshot of the fixed issue</summary>

![Fixed Bug 64](documentation/bugs/bug-64-2.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#64](https://github.com/dvfrancis/craftr/issues/64) | Unable to see apps in Django admin portal - I am only able to see the event `Event days` app in the Django admin portal. | I had forgotten to add the apps to `INSTALLED_APPS` in `settings.py`. Once I did this, they appeared in the admin portal, as shown in the second screenshot above |

#### Bug 65

<details>
<summary>Click here to see a screenshot of bug #65</summary>

![Fixed Bug 65](documentation/bugs/bug-65.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#65](https://github.com/dvfrancis/craftr/issues/65) | I am able to create duplicate vent classes (a class with the same title as another)  | I changed the fields which were being compared so that no two events can be created for the same date and time, which fixed the issue (see code below this table).

```Python
# Enforce unique class titles regardless of case
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event_day', 'start_time'],
                name='unique_class_title_case_insensitive'
            )
        ]
```

#### Bug 67

<details>
<summary>Click here to see a screenshot of bug #67</summary>

![Fixed Bug 67](documentation/bugs/bug-67-1.webp)
</details>

<details>
<summary>Click here to see an example result of this error</summary>

![Fixed Bug 67](documentation/bugs/bug-67-2.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#67](https://github.com/dvfrancis/craftr/issues/67) | When registering a new user via the web form at "register/register.html", the error shown in the first screenshot above occurs. The user account and profile are still created, although the user profile is missing the supplied location and photograph (see second screenshot above of entry below for 'anparton') | It appears that the profile is being created twice - once by the UserProfile model and then again in the registration view. This was the original code for the registration view (see code below this table).

```Python
def register_user(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()
            # Create the associated profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Log in the user
            login(request, user)
            # Replace "home" with your desired redirect
            return redirect("account/account.html")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
```
and this is it updated so it doesn't attempt to create a duplicate user profile, and instead just updates the existing fields:
```Python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm

def register_user(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()
            profile = user.profile  # Access the profile created by the signal
            profile.location = profile_form.cleaned_data['location']
            profile.experience = profile_form.cleaned_data['experience']
            profile.photograph = profile_form.cleaned_data['photograph']
            profile.save()

            # Log in the user
            login(request, user)
            return redirect("account/account.html")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "app_name/register.html",
        {"user_form": user_form, "profile_form": profile_form}
    )
```

#### Bug 68

<details>
<summary>Click here to see a screenshot of bug #68</summary>

![Fixed Bug 68](documentation/bugs/bug-68.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#68](https://github.com/dvfrancis/craftr/issues/68) | SMTP authentication error - when sending a message via the contact form, it is unable to email the administrator due to the error shown in the screenshot above | I cannot use my main email account password directly as my email provider requires the use of app-specific passwords. Once I had generated one and updated `env.py`, the form was able to send the email as expected.|

#### Bug 69

| Issue | Bug | Fix |
| --- | --- | --- |
| [#69](https://github.com/dvfrancis/craftr/issues/69) | The contact form does not send an email notification to the admin of the site when deployed to Heroku (although it still creates the contact form in the database). | I have put all sensitive info (secret key, email addresses, passwords) into `env.py`, which is not synced to GitHub as it is in `.gitignore`. I needed to add the email address and email password variables to Heroku, after which the email functionality worked as expected |

#### Bug 70

<details>
<summary>Click here to see a screenshot of bug #70</summary>

![Fixed Bug 70](documentation/bugs/bug-70.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#70](https://github.com/dvfrancis/craftr/issues/70) | When attempting to register a new account from the login page, you are prompted to login first. When logged in, it redirects to the details page when the register button is clicked. | The 'Register' button was defined within the `<form>` HTML element, which was causing this bug. When moved outside of that element it behaves as expected. Buttons inside `<form>` elements often inherit functionality tied to the form itself |

#### Bug 75

<details>
<summary>Click here to see a screenshot of bug #75</summary>

![Fixed Bug 75](documentation/bugs/bug-75.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#75](https://github.com/dvfrancis/craftr/issues/75) | No feedback is given if non-matching passwords are entered | Conditional statement added to check for errors (error message delivered via Toast as shown in screenshot above). See code below this table.

```Python
else:
            # Show validation errors when passwords don't match or are missing
            if user_form.errors:
                messages.error(
                    request,
                    (
                        "Your passwords do not match, or are missing. "
                        "Please enter them again."
                    ))
```
#### Bug 83

<details>
<summary>Click here to see a screenshot of bug #83</summary>

![Fixed Bug 83](documentation/bugs/bug-83.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#83](https://github.com/dvfrancis/craftr/issues/83) | Images do not appear to work correctly when DEBUG is set to False; for example, the logo in the footer displays without problem when `DEBUG=True` but not when `DEBUG=False` | Apparently, this behaviour is by design (as detailed in [this article](https://www.geeksforgeeks.org/why-django-not-serve-your-static-files-in-debug-false-mode/)). Once I uploaded the images to Cloudinary, and used the correct URL, the images appeared as expected - even when `DEBUG=False` |

#### Bug 84

<details>
<summary>Click here to see a screenshot of bug #84, before clicking an accordion item</summary>

![Fixed Bug 84](documentation/bugs/bug-84-1.webp)
</details>

<details>
<summary>Click here to see a screenshot of bug #84, after clicking an accordion item</summary>

![Fixed Bug 84](documentation/bugs/bug-84-2.webp)
</details>

| Issue | Bug | Fix |
| --- | --- | --- |
| [#84](https://github.com/dvfrancis/craftr/issues/84) | On `faq.html`, when you expand an accordion item the background images appears to enlarge | I used `background-attachment: fixed;` to lock the background so it doesn't "expand" when an accordion item is clicked. The background no longer changes  (see code below this table).

```CSS
.faq-background {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: url("https://res.cloudinary.com/dvzs9gve0/image/upload/v1744652041/Depositphotos_356425758_XL_jsstrh.webp") no-repeat scroll center;
  background-size: cover;
  background-attachment: fixed;
}
```
#### Bug 87

| Issue | Bug | Fix |
| --- | --- | --- |
| [#87](https://github.com/dvfrancis/craftr/issues/87) | `Uncaught TypeError: Cannot read properties of null (reading 'defaultPrevented') toast.js:76` console error | It looks like this is related to the JavaScript that handles Toast messages. The original JavaScript is shown below this table.

```JavaScript
document.addEventListener("DOMContentLoaded", function () {
  var toastEl = document.getElementById("toastMessage");
  var toast = new bootstrap.Toast(toastEl);
  toast.show();
});
```
It is attempting to show `toastmessage` before the DOM element has been initialised. I've updated the code so that the element is created first before a Toast message is created:

```JavaScript
document.addEventListener('DOMContentLoaded', () => {
  let toastElement = document.getElementById('toastMessage');
  if (toastElement) {
    let toast = new bootstrap.Toast(toastElement);
    toast.show();
  }
});
```
I've also created an if statement to check a Toast message exists, before attempting to access the DOM element created and display the message.

The updated code removes the error from the console.

### Unresolved

There are no unresolved bugs in the project.