# Testing

1. [HTML Validation](#html-validation)
2. [CSS Validation](#css-validation)
3. [JavaScript Validation](#javascript-validation)
4. [Python Validation](#python-validation)
5. [Lighthouse](#lighthouse)
6. [Manual Testing](#manual-testing)
7. [Seat Allocation Algorithm](#seat-allocation-algorithm)
   
## HTML Validation
This was performed using [W3C HTML Validator](https://validator.w3.org/nu/)

* There were conflicts with the validator and Django Template Language, for example

* Spaces following % produced "Non-space characters found without seeing a doctype first."

* Besides these conflicts I changed all my \<article\>'s and \<section\>'s to \<div\>'s

* *Warning: The type attribute is unnecessary for JavaScript resources.*

## CSS Validation

This was performed using [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)

 - No issues flagged during CSS validation

## JavaScript Validation

This was performed using [JSHint](https://jshint.com/)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a9008930-a53c-4785-a23c-656f3a89931a)

- **infantsCheck is *not unused*** since it is needed in ...[templates/booking/create-booking-form.html](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/templates/booking/create-booking-form.html)

 ## Python Validation

This was performed using Code Institute's [PEP8 Linter](https://pep8ci.herokuapp.com/)

- No issues flagged during Python validation

## Lighthouse

I used Lighthouse within the Chrome Developer Tools to test the performance, accessibility and SEO of the website.
This test was performed before the authentication profile was added.

<details>
  <summary>Lighthouse Report</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/09b1697c-a33e-42ee-b9f4-9dcf1fa07283)

</details>

## Additional Testing Comments
+ Carried out tests of the program on both the local terminal and the Code Institute Heroku terminal.
+ Chrome DevTools was used throughout the development process for testing purposes.
+ Added Custom [404](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/templates/includes/404_not_found.html) and [500](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/templates/includes/500_error.html) pages just in case such errors occur.
  
## Manual Testing 

Begin with a **Mock Employer App**

### Epic: *Set up a mock-up system to begin with that demonstrates CRUD functionality*

This is broken down into the following

<details>
  <summary>User Stories</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/51c2cb43-0f4e-4bcf-b6b1-756f8f259578)

</details>

**User Tasks:**
1. Right at the onset, deploy the App on Heroku to ensure that it runs correctly on Heroku
2. Demonstrate that records can be created
3. Demonstrate that records can be searched for by a reference or by names
4. Demonstrate that records can be edited and updated.
5. Demonstrate that records can be deleted


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T01 | Install Django  | Install Django, psycopg2. Create requirements.txt. Name the Project **manxairlines**. Create the App and name it **booking**. Deploy locally. | Expected to see the webpage showing the following message: *The install worked successfully!* | PASS |

<details>
<summary>Screenshot</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9fab1caa-a916-4c8e-a733-0e420a65d671)
  
</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T02 | Heroku Deployment  | Create App on Heroku. Call it **manx-airlines-bookings**. Setup a Database Instance on [ElephantSQL](https://www.elephantsql.com/). Set up the following Heroku Config Vars: <br>1) Copy the generated URL into **DATABASE_URL**; <br>2) Copy Secret Key into **SECRET_KEY**; <br>3) Set **PORT to 8000**; <br>4) Set **DISABLE_COLLECTSTATIC to 1**. <br>Connect Heroku App to GitHub. Deploy. | Expected to see the webpage showing the following message: *The install worked successfully!* As in the above screenshot. | PASS |

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T03 | Display Home Page  | Set up the relevant Django directories, views and urls to display **index.html**. | Expect to see the home page with the ubiquitous **Hello World** message. | PASS |

<details>
<summary>Screenshot</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5e82ae15-1dfd-4424-8fef-71d027c6dc3f)

</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T04 | Include 'base.html' | Update index.html to use **base.html**.<br>It contains H1 Tagged: *HELLO WORLD*. Whilst **index.html** contains  *{% block content %}* of H3 tagged: *GOODBYE!* | Expect to see both sentences:<br>**Hello World** followed by **GOODBYE!** | PASS |

<details>
<summary>Screenshot</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fba9f7f3-008d-48c9-aea0-4dca6f7312a4)

</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T05 | Create | Create a template and update views.py in order to be able to Create a Record. | In Admin, expect to see a created record. | PASS |

<details>
<summary>Form used to Create a Mock Record</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0e2e9151-74af-401b-a791-bb95c8b220bc)

<summary>Admin Views showing that the Record had been created</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/526f16b7-c657-4a5e-914f-ca5bfd9ec438)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d510ad5b-ccca-4788-b653-2b99a1c660c4)

</details>

----

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T06 | Search Record | Create a Search Bar in order to be able to Search for created records. Searches are *case insensitive*. | Expect to see matching records or a message showing that no matching criteria found. | PASS |

<details>
<summary>Search Bar - Demonstrate when no matching records found</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bee4f3f5-abcc-4959-b767-cd5067f5294f)

</details>

<details>
<summary>Demonstrate when search text "wa" is entered - case insensitive - three matches found</summary>
  
  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2bc24dc8-5c36-41b8-b98a-d94af6e71cf8)

</details>

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T07 | View Records | Once a Matching Record has been found, view the Record. | Click the View Button to see the matched record. | PASS |

<details>
  <summary>View Waterstons record by clicking the View button. Showing the Edit and Delete options</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a4a584fd-6e97-4fa7-8294-297a28fd8c6f)

</details>


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T08 | Delete Records | Implement the functionality to delete a record. Give the user the option to cancel the 'Delete' command. | Click the Yes Button to delete the record. | PASS |

<details>
  <summary>Showing Yes/Cancel options</summary> 

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8e9b2c0c-4789-47a8-a075-adff7f57fd51)

  <summary>Record deleted - originally three records, now two</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5a5a41e4-026d-41aa-8111-230e4239f7e7)

  <summary>Delete the other two - confirm that there are no further records that match "wa"</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/c357e514-2256-48f9-9101-083a353c51f4)

</details>

----

## Manual Testing of the Manx Airlines Travel Agency Booking System

### Epic: *Create and View Bookings*

This is broken down into the following
<details>
  <summary>User Stories</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/08800e14-83ad-45aa-b78d-8542215de0f9)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/21afde94-51af-4a89-80db-b600a24e7431) 

</details>

User Tasks:
1. Implement Navbar with Isle of Man Logo
2. Demonstrate the forms used to Create a Booking
3. Show each stage of a Booking being created
4. Demonstrate the validation of the fields entered
5. Once Bookings have been made, demonstrate that the user can Search for Bookings and see the List of Bookings found
6. Demonstrate that the user can View Bookings

<details>
  <summary>Navbar</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/94f86cd6-17c0-4488-8ca5-39fbb4525f7c)

</details>

#### Create Booking

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T09 | Create Booking | Create a Booking with 3 PAX, bags and remarks. | Confirmation Form regarding Booking. | PASS |

<details>
 
  <summary>Creating a Booking - First Page - Flight Details and Number of PAX</summary>
  
  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9f48c63f-af8e-4134-8791-52535c96d320)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/16b90e4e-9128-4a74-824f-16038e4b5006)

<summary>Creating a Booking - Second Page - Enter Passenger Details - Adult, Child, Infant, Bags and Remarks</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fad66edc-fc39-44dd-b4fe-0e45d6057dbc)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/27d2220d-4974-4d98-8fdc-a1eb34321906)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ae233a53-3a3e-4060-b47b-8f3f8eea0dd5)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/daa38270-6e9a-4718-a774-8fcc08bc95cb)

</details>


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T10 | Confirm Booking | Make a Booking then Click *Agree and pay now*. | Booking created. In Admin, expect to see all the records created by this action. | PASS |

<details>

<summary>Confirmation Form of the Booking being made - Display the generated PNR</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f8d0031a-dd58-42f6-9584-e402022d3a85)

<summary>Success Message showing that the Booking has been made</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a79e7ee2-c7c5-4b34-935b-bb81e9c3d80c)

</details>

Admin View of the Booking and Passengers Records

<details>
<summary>Admin view of the Booking record</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/564be75a-8a37-40e2-8a91-d8e4635dee82)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6878835d-b191-4fad-b0b0-e9b02b349b1e)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/74d78d46-02bc-4d7c-86ce-2793b3cf3693)

<summary>Admin view of the Passenger records</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/dd51e2ec-69a8-4180-ac45-24d54ea32fdf)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3cccbf1a-ea40-4707-a9d4-52fea8efa175)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/81fbecbe-2bdb-4a83-8468-d4e8d9720fd6)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/69ce8b19-454c-489d-95e5-4fc5e5c99f9d)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/49d3efc2-f1ad-429c-a5e0-aa56a49a02ef)

</details>

Admin View of the Transaction and Schedule Records
<details>
<summary>Admin view of the Transaction record</summary>

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a5779787-cbfc-4a00-9918-9c93c3dea426)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f423230d-be3f-4ae3-b110-896e01373d22)

<summary>Admin view of the Schedule records and Seatmaps</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/82969fd2-b940-44c4-b06d-b38cecd698f7)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a0d21ac1-e688-41e4-9ceb-31400fba1ab4)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ecd0b996-860a-4ac2-81a6-b73302a7881c)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/cb95778e-79b2-4b14-be24-c71f7b2e124c)

</details>

Using [RapidTables](https://www.rapidtables.com/convert/number/hex-to-binary.html) the Hex String C000 reading from the left indeed shows that two seats have been allocated.<br>*24 Hex Characters represents 96 Binary Bits which represents 96 seats* - see [below](#seat-allocation-algorithm) for further details.

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/64064f51-7e10-4641-9bdd-d318efc90cb1)

----

#### Validation

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T11 | Validate All Input | Enter various erroneous and invalid values. | Suitable Messages should be displayed indicating that validation has been performed. | PASS |

<details>

##### Flight Detail Validation

<summary>Entering Past Dates</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/895384ff-32e5-4e5b-9956-d9f686ce9241)

<br/> 

Note: The same validation is applied to the *Returning Date*

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/c5ba3fe4-94bf-42db-b9ad-9210310dad08)


<summary>Illegal Dates</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/cfd46e5f-c44c-4d59-833a-b9087dbe2be2)

<summary>Same Day Return Journey - entering an earlier Return Time than the Departure Time e.g. 13:30pm and 11:00am</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fa80a9d7-0a96-475f-8a5f-e74f56810113)

   
<summary>Attempt to make a Booking with an interval of more than 180 days</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/10d838cf-a5c6-4069-aeb1-dac28771edce)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0fa112c4-b722-44ca-b3a1-3f809c6b0e76)

<summary>Attempt to make a Booking too far into the future</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/4fde0e59-0cea-49c3-9737-a607c88ffe46)

<br/> 

<summary>Same Day Return Journey - The Return Time cannot be less than 90 minutes from the Departure Time e.g. 09:45am and 11:00am</summary>
<br/>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/39d819b1-895e-4e27-97ec-0ef187d0b8e8)

</details>

##### Passenger Detail Validation

<details>

   <summary>Attempt to add more infants than the number of adults</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/82522b91-5583-49c4-ad98-806712e280b0)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ef338adb-c6cc-4eb7-90e8-13e390864a07)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/eed0ff1d-c609-431c-afd2-644bd056f042)

   <summary>Zero number of Adults</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b3ae4c55-a2a8-45c6-bdff-969d1def16b3)

   <summary>Attempt to make a Child Booking with Zero Adults</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8a552933-547d-4b97-84c8-5c858848404e)

   <summary>Attempt to enter more than 20 passengers in a booking </summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/dc5d8842-0fb0-42cf-8f1a-fba229ed6a02)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/317f579f-3749-4121-9348-7478a7e27dfb)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/31ce0552-ee93-438a-9ec4-e963c8833b5a)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2b2f222e-b654-455f-b471-6918b012992d)


 <summary>Entering a Blank Form or Blank Passenger Details</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/80992d59-a8a6-4527-88f2-5b9382359725)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2aa78b99-9b8f-453d-9cb9-c07751b32f50)

<summary>Blank First Name</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9e137e6c-c89e-49a3-bc9c-a5cf29a4355e)

<summary>Blank Last Name</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/832b9aa2-d680-40d9-aff9-4c6f4842dce9)

<summary>Names must consist only of Letters, Apostrophes and Hyphens</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/e0f1fa9d-ca8a-4c9e-97ca-d6c85087f3e7)

<br/> 
<summary>Email Validation</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5900ed07-693b-4fa9-9af1-82cc71285d7c)

   <summary>Principal Passenger (Adult 1) Contact Details must be entered</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1f6dcea1-e58d-4b35-bde6-aa0e1214659f)

   

   <summary>Erroneous Telephone Numbers</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b25fb09e-1d56-4dc0-99d0-3b3aaa3e72fb)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9e894431-939b-47be-a836-b520d02b48f8)


</details>

 #### Date of Birth Validation

<details>
   
 <summary>Future Date</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0fb63bf6-0349-42ee-b48d-e3752e0dc507)

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/e5e0ddad-05f1-485f-8e17-c641bd8aa264)


 <summary>Date of Birth cannot be Today's Date e.g.</summary>
<br/> 

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ef65f84a-1db9-4639-875d-64dce3916c1b)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a35b78ad-de90-4a91-9008-42fbe152668a)

   <summary>An Infant Passenger must be at least 14 days old to travel e.g. for the 19/11/2023</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/59ecaf0a-3049-4307-b37f-bb06134dbe03)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d60aa11b-6784-4996-88aa-4c4ef33f85e4)

   <summary>An Infant Passenger must be under 2 years of age at the time of the Departure Date of Travel e.g. for the 04/12/2023</summary>
<br/> 

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/ad52263e-4074-4b12-9c33-00629f67822e)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/944fb559-bdb2-4ea3-8674-97df103b955d)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b2743b4d-36bb-4772-ab05-c19847e7b5dc)


<summary>An Infant Passenger must be under 2 years of age at the time of the Return Date of Travel e.g. for the 16/12/2023</summary>
<br/> 
   
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/685a043b-f4b2-4343-8482-151ecc8bf46e)

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/88c86db2-8764-4d9a-9601-35dff073b536)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a7e2cc9a-121a-4559-a4e7-f7a8003237d5)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/109dabe6-428e-40e4-ac2d-897178663591)

<summary>A Child Passenger must be under 16 years of age  at the time of the Departure Date of Travel e.g. for the 04/12/2023</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/7f0d29ca-8c32-4ec3-a87e-f75a54397c6e)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/15ba523d-ea89-4f27-9647-3d858e0edf8f)

<summary>A Child Passenger must be under 16 years at the time of the Return Date of Travel e.g. for the 24/11/2023</summary>
<br/> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b7ce3e44-db40-4e8b-9a38-37194b7026d5)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9bd59f1b-39b0-400d-8ee5-1edd4f917d8b)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6bc4a6d7-f0bc-4bb8-b043-bb0cfe3b2798)


   </details>


---

#### PRM SSRs - Wheelchair Details

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T12 | Enter Wheelchair SSRs | Implement a Drop Down Menu whereby the user can enter PRM SSRs. | Show Drop Down Menu. | PASS |

<details>

 <summary>PRM SSRs</summary>
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f6f58dea-918e-4483-943f-7734ec500824)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2b80632b-712b-42c4-8da8-200ca8c30a70)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5cad4431-b47a-42ce-82ee-2d3bfd36c298)

</details>

#### Search Booking

| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T13 | Search Bookings | Implement a Search Bar where case-insensitive searches of Bookings can be performed. | Demonstrate Search Functionality and Pagination. | PASS |

<details>
<summary>Search Bar - Demonstrate when no matching records found</summary>
  
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/7a73f6b0-0afa-4e7d-92b3-bee30dcfcff9)

</details>

For testing purposes, initially all PNRs were prefixed with 'SMI'
<details>
 <summary>Search for 'smi'</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/30da195f-6c25-4fe1-9244-7b23363f9d75)

<summary>Pagination</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/689a2afa-0e26-4b2a-81da-dea3a677c734)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f9366a2d-0e77-4f6b-b04e-8d542a1eae0a)

<summary>User can search by PNR</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/478f722d-a0e9-441d-a6c8-0b64aa45e845)

<summary>User can search by Adult 1's First Name</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a2057aac-09e7-41af-818f-38b3d5be0bc6)

<summary>User can search by Adult 1's Last Name</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/f7328591-b4c9-4bd0-833b-59e2e69e31a5)

</details>

- Now that the Search Functionality has passed all tests - PNRs no longer have a 'SMI' prefix
- Instead, **a unique 6 character PNR is generated beginning with a letter**
  
#### View Booking

When a Booking is Viewed, the user has the option to *Edit or Delete a Booking*

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1b4188d2-d07a-40c2-a7a4-33f161a41d80)


### Epic: *Delete and Edit Bookings*

This is broken down into the following
<details>
  <summary>User Stories</summary>

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6976ec42-6552-49a8-97f9-0fbebf88bc3a)
     
  
</details>

User Tasks:
1. Demonstrate that the user can Delete Bookings
2. Demonstrate the forms used to Edit a Booking
3. Show each stage of a Booking being Edited

#### Delete a Booking

##### Before Deletion

<detail>
 
<summary>This flight shows 5 passengers</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/7f6b3d46-def4-4594-bf45-74ba3639afc2)

<summary>Seatmap - 5 bits set showing 5 allocated seats</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/fa59c5c3-11cc-494a-8f30-fbfbf374dc1a)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1f60d893-0df5-44de-82c7-d9a9cb081544)

<summary>These 3 passengers are on this flight - Booking QPJXWV</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/51ac79a8-3edf-44ee-918d-75832b5a5667)

<summary>View the Booking</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/a21e6494-d495-4819-a00e-3b6bdddcdd2a)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/55f71352-a784-4862-960f-b35f5b7ed747)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8b8ab4bc-c3c2-447a-ab6e-a7424dbb54ee)

<summary>Click Delete</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b17f5aec-a773-4ea8-8f62-3b0caeba6300)

<summary>Click Yes - Booking Deleted Successfully</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3913d007-b6e2-4be6-a9e3-9a9d47fb2f7a)

</details>


##### After Deletion

<detail>
 
<summary>This flight now shows 5-3 = 2 passengers</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/e0272621-15f8-437d-967c-344a4d17f26f)

<summary>Seatmap - 2 bits set showing 2 allocated seats</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/336013ae-aa82-4e74-b1d5-04b4240ad0fc)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6c2e039c-d871-49da-8b4a-d7a5f0d4e15b)

<summary>The two remaining 'seated' passengers belong to Booking EVZM6K</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/88e3fbb7-599c-4efe-9a3c-f9b8ccace553)

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9bded516-d37c-41f5-a5f1-fbee65ee21ed)

</details>

Note: Infants are **not** allocated seats - hence Booking EVZM6K rightfully shows 2 seated passengers.
The Booking consists of two adults (who are allocated seats) and two infants!

Demonstrated that Booking QPJXWV has been deleted including all the passengers associated with this booking! 

#### Edit A Booking


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T14 | Edit Bookings | View a Booking and Click the *Edit* Button | Demonstrate that PAX details can be edited/updated. | PASS |

##### Edit Booking - Scenario 1

- Create a Booking of 1 Adult, 1 Child, 1 Infant
- When that is done, Edit the Booking - that is, make some changes to the Booking and update it.

<details>
  <summary>Create the Booking</summary>

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d9468430-96ac-46a0-a75c-dd0287d5d640)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/dae66823-22ff-4f94-a832-627dc6b838e7)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5e8d730d-d2c2-4677-8b00-b558f1490ad9)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8d866adb-ed0b-4adf-b6e5-ee58ac5ccdfc)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/4291e437-87e0-4217-87fe-ff642cd47ca5)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/d02de58e-d12e-4644-913a-bbd58a788b30)

  <summary>Confirm the Booking</summary>

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/17f3b2dd-98e5-4e73-bd43-97a3cd0eb568)

  ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/0b20237f-4f6f-4638-9562-b49154ce3e37)

  </details>

  - Mr Jack Jones made a mistake when he initially requested this booking.
  - Jimmy Jones' name is wrong. It ought to be *James*! Change the name.
  - Also Mr Jones requests two more bags to be added.

    <details>
     <summary>Search for the Booking LWQ9Q2</summary>

     ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5f89d6e0-8360-4568-ae07-5b67e19b47ac)

    ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/809d361c-9654-4c42-bdee-afe24a17e712)

    <summary>View the Booking</summary>

    ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/1f212573-3404-4827-ad52-6f858dbeeae3)

    <summary>Change the Name and Add two bags</summary>

    ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/2c22548f-1a0a-4d65-b42f-086d82fc16d7)

    <summary>Confirm the Changes to the Booking by clicking Agree and pay now</summary>

    ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/66ae7aeb-5fda-4fd6-b358-371ec179bf4c)

    <summary>Message confirming that the Update has been done</summary>
    
    ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3ed89cde-efa0-494b-bf5a-f34a757d2c65)

    <summary>View Booking to confirm the Update</summary>

    ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3a19cde6-a95e-43ab-9433-53529b923748)

    </details>

##### Edit Booking - Scenario 2

- The children are no longer flying
- Edit the Booking - that is, remove the Child and Infant PAX from the Booking
- Click *Edit* on the Viewed Booking and proceed with the editing

<details>

 <summary>Click Child 1</summary>

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/255eeb95-0be3-48f9-ab6b-586e42f43857)

 Note the **red strike-through** indicating that this passenger will be removed.

<summary>Click Infant 1</summary>

 ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/350cc3a5-84c9-41f5-8762-831854d90951)

 Note the **red strike-through** indicating that this passenger will be removed.

<summary>Click Continue to view the Confirmation Form</summary> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/5be3434c-a247-4979-8da7-6238d1f26c0e)


<summary><summary>Click Agree and pay now - Message confirming that the Update has been done</summary>
    
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3ed89cde-efa0-494b-bf5a-f34a757d2c65)

<summary>View Booking to confirm the Update</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/8781bbc3-d03e-4833-a7c2-2c39099a2aff)

</details>

In a Booking, each Infant PAX is assigned to an Adult PAX. If the Adult PAX is selected for Removal, the Infant PAX assigned to that Adult *will automatically be selected for removal* as well! Demonstrate and Test this scenario.

----

##### Edit Booking - Scenario 3


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T15 | Remove Adult and Infant | Click Remove Pax? on an Adult PAX. | Both the Adult and Infant PAX are removed. | PASS |

<details>

<summary>View Booking EVZM6K</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/9bded516-d37c-41f5-a5f1-fbee65ee21ed)

<summary>Click Edit and Select Adult 2</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b86a7d0a-e15b-496f-8bdc-73cb80c1e267)

When one scrolls down the page one will see that Infant 2 has been automatically selected.

<summary>Infant 2</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/7a7fdcc9-f427-455f-bee6-baeb4614bf68)

<summary>Click Continue to view the Confirmation Form</summary> 

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/6c9487b5-e588-41a5-a25f-ffd40786de07)

<summary><summary>Click Agree and pay now - Message confirming that the Update has been done</summary>
    
![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/bf043c4e-ac80-4fc3-aa06-cc55e4b03eae)

<summary>View Booking to confirm the Update</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/3b388acc-409f-41bc-aee6-7e631b0f1d0d)

Also before the Edit there were **two allocated seats on Flight MX0465 29DEC**

<summary>View the Schedule Now</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/94c0a88d-01f2-4682-ae7a-3f7b9a36a957)

<summary>View Flight Now</summary>

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/85492883-50a5-4180-9d03-6542bf7c94ef)

</details>

- Please note: Infants can be removed just as well as any other PAX (*except for Adult 1 - the Principal PAX*)
- By clicking *Remove Pax?* and proceeding with the Update.
- That is, the assigned Adult does **not** have to be removed!
- **All PAX** (*except for Adult 1 - the Principal PAX*) can be removed from the Booking individually.
- Adult 1 - the Principal PAX can be edited however e.g. Name Change
- If the user wants to make a Booking without the assigned Adult 1 PAX then the Booking has to be deleted and a new Booking created.

---


### Epic: *Register, Login and Logout*

This is broken down into the following
<details>
  <summary>User Story</summary>

   ![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/b42f0e62-f10e-446a-aa65-7719f9f40775)
   
  
</details>

User Tasks:
1. Demonstrate that the user can Register in order to use the site
2. Demonstrate that the user can Login to the site
3. Demonstrate that the user can Logout from the site
4. That the endpoints are protected - that only logged-in users can use the site


| Test No. | Feature        | Steps        | Expected Outcome  | Actual Outcome |
| ------------- | ------------- | -------------    | ------------- | ------------- |
| T16 | Register, Login, Logout | Using Django's authentication system setup Register/Login?logout functionality. | That the above User Tasks are accomplished. | PASS |

----

## Conclusion

CRUD functionality has been demonstrated.

## Seat Allocation Algorithm

I proposed the following algorithm to seat passengers on a 96-seat aircraft.
- Each seat would be represented by a *binary digit - 1 for allocated, 0 for free* (base 2)
- 96 bits are represented by 24 Hex Characters (base 16: 0-9, A-F)
- Therefore, in the Schedule Model, the seatmap is a 24 character Charfield


Here is an example showing that seats 24BCD are allocated.

| 95 | 94 | 93 | 92 | ... | 3 | 2 | 1 | 0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bit 95 | Bit 94 | Bit 93 | Bit 92 | ... | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
| 24D | 24C | 24B | 24A | ... |  1D | 1C | 1B | 1A |
| 1 | 1 | 1 | 0 | ... |  0 | 0 | 0 | 0 |
  
- I chose to use a recursive solution where N is the number of seats needed
- It would first search for a **row** of N *0's* in the Schedule's seatmap
- If such a row is found, invert the 0's to 1's and return  [**True**, allocated seats, the updated seatmap]

- If N=1 at this stage, then there are no available seats, return [**False**, ...]

- Otherwise, from the range *M = N-1 to 2*,
-  - **Loop**
-  - First see if a **row** of *M seats* can be allocated
   - If Yes, then allocate the other *(N - M) seats by recursively calling this algorithm* - **return the result**
   - If No, then subtract 1 from M; if it is **M != 1** then repeat the Loop
   - Otherwise **M == 1** so there is not enough seats available for the Booking being made - return [**False**, ...]
 
If enough seats cannot be allocated then the following sample message would be displayed:

![image](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/assets/91061592/e6a30082-7b89-4d2d-aa56-0149ceecfca5)

The user would have to choose an alternative flight date/time.


I used the Python module [bitstring](https://pypi.org/project/bitstring/) to do the *bit searching and manipulations*.

[binary.py](https://github.com/DelroyGayle/manx-airlines-booking-system-p4/blob/main/booking/misctests/binary.py) demonstrates the seven tests that I conducted.

Here is my Python code of the algorithm

```
"""
    Airlines generally seat passengers from the back of the aircraft
    So interpret the leftmost bit as position 95
    95 94 93 ... 2 1 0
     0  0  0 ... 0 0 0
"""

# CAPACITY is 96 - Number of seats in the aircraft
CAPACITY = 96  # Number of seats in the aircraft
LEFT_BIT_POS = CAPACITY - 1  # I.E. 95


def row_of_N_seats(number_needed, allocated, available):
    """ Find a 'row' of 'number_needed' seats """
    zeros = "0b" + "0"*number_needed
    result = available.find(zeros)
    if not result:
        return (False, allocated, available)

    # Set the bits to 1 to represent 'taken' seats
    bitrange = range(result[0], result[0] + number_needed)
    available.invert(bitrange)

    """
    Determine the range of seat positions
    e.g. 6 seats at position 77
    77-6+1 = 72
    so range(72, 78) = 72, 73, 74, 75, 76, 77
    Then add that range of seats to the 'allocated' list
    """
    end = LEFT_BIT_POS - result[0]
    start = end - number_needed + 1
    seat_range = range(start, end + 1)
    allocated += [*seat_range]
    return (True, allocated, available)


def find_N_seats(number_needed, allocated, available):
    """
    Find 'N' number of seats
    N being 'number_needed'
    'allocated' are all the seats found so far
    'available' is a bitstring depicting what is available
    This is a recursive algorithm
    """

    result = row_of_N_seats(number_needed, allocated, available)
    if result[0]:
        # Successfully found a row of N seats - so allocation is done!
        return result

    # if N = 1 then no available seats i.e. the flight is full
    if number_needed == 1:
        return (False, allocated, available)

    # Otherwise, starting with M=N-1,
    # see if it is possible to find a row of M seats
    # if so, allocate that row of seats
    # then see if the remainder can be allocated
    minus1 = number_needed - 1
    count = number_needed - 1
    while count != 1:
        result = row_of_N_seats(count, allocated, available)
        if not result[0]:
            # Try a smaller row allocation
            count -= 1
            continue

        remainder_needed = number_needed - count
        remainder = find_N_seats(remainder_needed,
                                 allocated + result[1], result[2])
        if remainder[0]:
            # Found all the seats!
            return remainder

    # Not successful in finding any 'row' > 1
    # Therefore, allocate one seat
    # Then repeat 'find_N_seats' for the remainder

    result = row_of_N_seats(1, allocated, available)

    return find_N_seats(minus1,
                        allocated + result[1], result[2])
```








