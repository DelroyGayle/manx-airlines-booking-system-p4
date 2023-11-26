from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, OuterRef, Subquery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Booking, Passenger
from .models import Flight

from .forms import BookingForm, CreateBookingForm
from .forms import AdultsForm, MinorsForm
from .forms import HiddenForm
from .forms import BagsRemarks

from . import morecode
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import random  # TODO
import re

from .common import Common

# TODO
# from .constants import FIRSTNAME_BLANK
# KEEP THIS - TODO
# import constants

# Constants

NULLPAX = "Enter the details for this passenger."
BAD_NAME = ("Names must begin and end with a letter. "
            "Names must consist of only alphabetical characters, "
            "apostrophes and hyphens.")
FIRSTNAME_BLANK = (f"Passenger Name required. "
                   f"Enter the First Name as on the passport.")
LASTNAME_BLANK = (f"Passenger Name required. "
                  f"Enter the Last Name as on the passport.")
CONTACTS_BLANK = ("Adult 1 is the Principal Passenger. "
                  "Contact Details are "
                  "mandatory for this Passenger. "
                  "Enter passenger's phone number and/or email.")
BAD_TELNO = "Enter a phone number of at least six digits."
BAD_EMAIL = "Enter a valid email address."
BAD_DATE = "Enter a valid date of birth."
FUTURE_DATE = "Your date of birth must be in the past."
TOO_YOUNG = ("Newly born infants younger than 14 days "
             " on the {0} will not be accepted for travel.")

ADULT_PRICE = 100   # Age > 15
CHILD_PRICE = 60 # Age 2-15
INFANT_PRICE = 30   # Age < 2
BAG_PRICE = 30

def display_formset_errors(request, prefix, errors_list):
    """
    Instead of showing form errors within the form
    This routine will display any errors via the Django Messaging facility

    Sample 'errors_list'
    [{'last_name': ['This field is required.'],
      'last_name': ['This field is required.'],
      'contact_number': ['This field is required.'],
      'contact_email': ['This field is required.'],
      'wheelchair_ssr': ['This field is required.'],
      'wheelchair_type': ['This field is required.']}, {}]
    """

    number_of_forms = len(errors_list)
    for form_number in range(number_of_forms):
        prefix_number = form_number + 1
        fields_dict = errors_list[form_number]
        if not fields_dict:  # i.e. empty {}
            continue
        list_of_errors = fields_dict.items()
        for (field, field_errors) in list_of_errors:
            for item in field_errors:
                begin = f"{prefix} {prefix_number}:"
                formatted = Common.format_error(f"{field}")
                message_string = f"{begin} {formatted} - {item}"
                messages.add_message(request, messages.ERROR,
                                     message_string)


def append_to_dict(dict, key, item):
    """
    This dictionary should be of the form
    {item: [ ... , ... , ...]}
    Create a list if one does not exist before appending item
    """

    if item not in dict:
        dict[key] = [item]
    else:
        dict[key] = dict[key] + [item]
    return dict


def name_validation(fields_dict, accum_dict, errors_found):
    """ Handle the Formsets' Validation of First and Last Names """
# def adults_formset_validated(cleaned_data, request):  # TODO

    # First Name Validation
    temp_field = fields_dict.get("first_name", "").replace(" ", "")
    if temp_field == "":
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "first_name",
                                    FIRSTNAME_BLANK)
    elif not re.search("^[A-Z]$|^[A-Z][A-Za-z'-]*[A-Z]$",
                       temp_field, re.IGNORECASE):
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "first_name", BAD_NAME)

    # Last Name Validation
    temp_field = fields_dict.get("last_name", "").replace(" ", "")
    if temp_field == "":
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "last_name",
                                    LASTNAME_BLANK)
    elif not re.search("^[A-Z]$|^[A-Z][A-Za-z'-]*[A-Z]$",
                       temp_field, re.IGNORECASE):
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "last_name", BAD_NAME)

    return (accum_dict, errors_found)


def adults_formset_validated(cleaned_data, request):
    """ Carry out Custom Validation of the Adults Formset """
    formset_errors = []  # Hopefully this will remain empty
    errors_found = False
    number_of_forms = len(cleaned_data)
    for form_number in range(number_of_forms):
        accum_dict = {}
        prefix_number = form_number + 1
        fields_dict = cleaned_data[form_number]

        # Blank Form?
        if not fields_dict:  # i.e. empty {} which indicates a blank form
            errors_found = True
            accum_dict = append_to_dict(accum_dict, "first_name", NULLPAX)
            formset_errors.append(accum_dict)
            continue

        accum_dict, errors_found = name_validation(fields_dict,
                                                   accum_dict, errors_found)

        # Contact Number/Email Validation can be null except for Adult 1
        telephone = fields_dict.get("contact_number", "").replace(" ", "")
        email = fields_dict.get("contact_email", "").replace(" ", "")
        # These can be null except for Adult 1
        both_blank = telephone == "" and email == ""
        if both_blank and prefix_number == 1:
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "contact_number", CONTACTS_BLANK)

        if not both_blank:
            if telephone != "" and not re.search("^[0-9]{6,}$", telephone):
                errors_found = True
                accum_dict = append_to_dict(accum_dict,
                                            "contact_number", BAD_TELNO)

        # This solution found at
        # https://stackoverflow.com/questions/3217682/
        # how-to-validate-an-email-address-in-django

            if email:
                try:
                    validate_email(email)
                except ValidationError as e:
                    errors_found = True
                    accum_dict = append_to_dict(accum_dict,
                                                "contact_email", BAD_EMAIL)

        formset_errors.append(accum_dict)

    if errors_found:
        # Send as 'Django Messages' the errors that were found
        display_formset_errors(request, "Adult", formset_errors)
        return False

    print(500) # TODO
    return True


def date_validation_part2(accum_dict, errors_found,
                          date_of_birth, is_child):
    """ Handles the date validation for children and infants """

    todays_date = datetime.now().date()
    # datediff = date_of_birth - todays_date

    departing_date = Common.save_context["booking"]["departing_date"]
    print(9881, Common.save_context["booking"]["departing_date"], "DEP")
    print(9882, Common.save_context["booking"]["returning_date"], "RET")
    output_departing_date = departing_date.strftime("%d/%m/%Y")
    datediff = date_of_birth - todays_date
    days = datediff.days

    # days > 0 caters for hours/minutes/seconds!
    if date_of_birth > todays_date and days > 0:
        errors_found = True
        accum_dict = append_to_dict(accum_dict,
                                    "date_of_birth", FUTURE_DATE)
        return (accum_dict, errors_found)

    # if date_of_birth > todays_date then that means
    # days == 0 i.e. identical to Today's Date
    if days == 0:
        errors_found = True
        accum_dict = append_to_dict(accum_dict,
                                    "date_of_birth",
                                    TOO_YOUNG.format(output_departing_date))

        return (accum_dict, errors_found)

    datediff = departing_date - date_of_birth
    days = datediff.days
    if days < 14:
        errors_found = True
        accum_dict = append_to_dict(accum_dict,
                                    "date_of_birth",
                                    TOO_YOUNG.format(output_departing_date))
        return (accum_dict, errors_found)

    # Calculate the difference in years as shown here
    # https://stackoverflow.com/questions/3278999/how-can-i-compare-a-date-and-a-datetime-in-python
    difference_in_years = relativedelta(departing_date, date_of_birth).years

    if is_child:
        # CHILD
        if difference_in_years > 15:
            error_message = (
                "A child should be at least 2 "
                "and under 16 "
                f"on the Date of Departure: {output_departing_date} "
                f"But this passenger will be {difference_in_years}.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
            return (accum_dict, errors_found)

    if not is_child:
        # INFANT
        if difference_in_years >= 2:
            error_message = (
                "An infant should be under 2 "
                f"on the Date of Departure: {output_departing_date} "
                f"But this passenger will be {difference_in_years}.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
            return (accum_dict, errors_found)

    # Does this Booking have a Return Journey?
    if Common.save_context["booking"]["return_option"] == "N":
        # No!
        return (accum_dict, errors_found)

    # Yes! - Check the D.O.B. against the Return Date
    returning_date = Common.save_context["booking"]["returning_date"]
    output_returning_date = returning_date.strftime("%d/%m/%Y")
    # Method to determine the years was found at
    # https://stackoverflow.com/questions/4436957/pythonic-difference-between-two-dates-in-years
    difference_in_years = relativedelta(returning_date, date_of_birth).years
    paxtype = "an Adult" if difference_in_years > 15 else "a Child"

    if is_child:
        # CHILD
        if difference_in_years > 15:
            error_message = (
                "A child should be at least 2 "
                "and under 16 "
                f"on the Returning Date: {output_returning_date} "
                f"But this passenger will be {difference_in_years}. "
                f"Please enter {paxtype} Booking for this passenger.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
    if not is_child:
        # INFANT
        if difference_in_years >= 2:
            error_message = (
                "An infant should be under 2 "
                f"on the Returning Date: {output_returning_date} "
                f"But this passenger will be {difference_in_years}. "
                f"Please enter {paxtype} Booking for this passenger.")

            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)

    return (accum_dict, errors_found)


def minors_formset_validated(cleaned_data, is_child_formset, request,):
    """
    Formsets have been 'cleaned' at this point
    Carry out Custom Validation of the Children Formset
    and the Infants Formset
    """
    formset_errors = []  # Hopefully this will remain empty
    errors_found = False
    number_of_forms = len(cleaned_data)
    todays_date = datetime.now().date()
    for form_number in range(number_of_forms):
        accum_dict = {}
        prefix_number = form_number + 1
        fields_dict = cleaned_data[form_number]

        # Blank Form?
        if not fields_dict:  # i.e. empty {} which indicates a blank form
            errors_found = True
            accum_dict = append_to_dict(accum_dict, "first_name", NULLPAX)
            formset_errors.append(accum_dict)
            continue

        accum_dict, errors_found = name_validation(fields_dict, accum_dict,
                                                   errors_found)

        # Date of Birth Validation
        # Children must be between 2 and 15
        # Infants must be between at least  14 days old and under 2 years old

        date_of_birth = fields_dict.get("date_of_birth", todays_date)
        # This field SHOULD BE <class 'datetime.date'>
        # Defensive Programming - because the 'cleaned' version
        # ought to be a valid date
        if not isinstance(date_of_birth, date):
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", BAD_DATE)

        else:
            accum_dict, errors_found = date_validation_part2(accum_dict,
                                                             errors_found,
                                                             date_of_birth,
                                                             is_child_formset)

        formset_errors.append(accum_dict)

    if errors_found:
        # Send as 'Django Messages' the errors that were found
        paxtype = "Child" if is_child_formset else "Infant"
        display_formset_errors(request, paxtype, formset_errors)
        return False

    return True


def all_formsets_valid(request, adults_formset,
                       children_included, children_formset,
                       infants_included, infants_formset,
                       bags_remarks_form):
    """
    Carry out validation on up to three formsets
    1) Adults
    2) Children
    3) Infants

    They differ slightly:
    Adults have contact telephone/email
    Children/Infants have the Date of Birth - no contact details

    4) If the above are all valid, then valid the BagsRemarks Form
    """

    # Are there any Django Validations Errors to begin with?

    errors_found = False
    if adults_formset.is_valid():
        print(400) #TODO
        pass
    else:
        # The Adults Formset is Invalid - Report the Errors
        errors_found = True
        display_formset_errors(request, "Adult", adults_formset.errors)
        # Are there any 'non-form errors' in the Adults Formset?
        formset_non_form_errors = adults_formset.non_form_errors()
        if formset_non_form_errors:
            display_formset_errors(request,
                                   "Adult", formset_non_form_errors)

    if children_included:
        if children_formset.is_valid():
            pass
        else:
            # The Children Formset is Invalid - Report the Errors
            errors_found = True
            display_formset_errors(request, "Child", children_formset.errors)
            # Are there any 'non-form errors' in the Children Formset?
            formset_non_form_errors = children_formset.non_form_errors()
            if formset_non_form_errors:
                display_formset_errors(request,
                                       "Child", formset_non_form_errors)

    if infants_included:
        if infants_formset.is_valid():
            pass
        else:
            # The Infants Formset is Invalid - Report the Errors
            errors_found = True
            display_formset_errors(request, "Infant", infants_formset.errors)
            # Are there any 'non-form errors' in the Infants Formset?
            formset_non_form_errors = infants_formset.non_form_errors()
            if formset_non_form_errors:
                display_formset_errors(request,
                                       "Infant", formset_non_form_errors)

    if errors_found:
        # Proceed no further because errors have been discovered
        return (False, None)

    # Are the forms blank?
    is_empty = False

    # ADULTS
    print(401) # TODO
    cleaned_data = adults_formset.cleaned_data
    if not any(cleaned_data):
        print(402) # TODO
        is_empty = True
        messages.add_message(request, messages.ERROR,
                             "Enter the Adult's Passenger Details "
                             "for this booking.")
    else:
        Common.save_context["adults_data"] = cleaned_data

    # CHILDREN
    if children_included:
        cleaned_data = children_formset.cleaned_data
        if not any(children_formset.cleaned_data):
            is_empty = True
            messages.add_message(request, messages.ERROR,
                                 "Enter the Child's Passenger Details "
                                 "for this booking.")
        else:
            Common.save_context["children_data"] = cleaned_data

    if is_empty:
        return (False, None)

    # INFANTS
    if infants_included:
        cleaned_data = infants_formset.cleaned_data
        if not any(infants_formset.cleaned_data):
            is_empty = True
            messages.add_message(request, messages.ERROR,
                                 "Enter the Infant's Passenger Details "
                                 "for this booking.")
        else:
            Common.save_context["infants_data"] = cleaned_data

    print(403) # TODO
    if is_empty:
        return (False, None)

    # Validate all three formsets
    if not adults_formset_validated(adults_formset.cleaned_data, request):
        return (False, None)

    if (children_included and
        not minors_formset_validated(children_formset.cleaned_data,
                                     True, request)):
        return (False, None)
    
    if (infants_included and
        not minors_formset_validated(infants_formset.cleaned_data,
                                     False, request)):
        return (False, None)

    print(860, type(bags_remarks_form), bags_remarks_form) # TODO
    # Validate BagsRemarks Form
    if not bags_remarks_form.is_valid:
        print(865) # TODO
        display_formset_errors(request, "Bag/Remarks", bags_remarks_form.errors)
        return (False, None)

    print(870, bags_remarks_form.cleaned_data) # TODO
    return (True, bags_remarks_form.cleaned_data)

# Create your views here.

# Display the Home Page


def homepage(request):
    # On the first display of the Home Page
    # Initialise various settings
    if not Common.initialised:
        Common.initialisation()

    return render(request, "booking/index.html")


def message_error(message_string, request):
    messages.add_message(request, messages.ERROR, message_string)


def is_booking_form_valid(form, request):
    if not form.is_valid():
        for field in form.errors:
            for item in form.errors[field]:
                message_string = Common.format_error(f"{field} - {item}")
                message_error(message_string, request)

        return (False, None)

    # FURTHER VALIDATION NEEDED
    # Check Dates and Flight Availability
    cleaned_data = form.cleaned_data
    print("CD", cleaned_data)
    if (cleaned_data["return_option"] == "Y" and
            cleaned_data["returning_date"] == cleaned_data["departing_date"]):
        # Same Day Travel - Is there enough time between journey times?
        depart_time = cleaned_data["departing_time"]
        return_time = cleaned_data["returning_time"]
        time_diff = morecode.calc_time_difference(return_time, depart_time)
        if time_diff < 0:
            message_error("Returning Time - The time of the return flight "
                          "cannot be in the past.",
                          request)
            return (False, None)

        if time_diff < 90:
            message_error(
                "Returning Time - The interval between flights cannot be "
                "less than 90 minutes.", request)
            return (False, None)

    # The Form's contents has passed all validation checks!
    # Save the information for later processing
    print("CD2", cleaned_data)
    print("CO", Common.save_context)
    # TODO
    save_data = {"return_option": cleaned_data["return_option"]}
    if cleaned_data["return_option"] == "Y":
        # Return Flight - Determine both flight numbers
        thetime = cleaned_data["departing_time"]
        depart_pos = Common.OUTBOUND_TIME_OPTIONS1.index(thetime)
        save_data["depart_pos"] = depart_pos
        outbound_flightno = Common.outbound_listof_flights[depart_pos]            
        thetime = cleaned_data["returning_time"]
        return_pos = Common.INBOUND_TIME_OPTIONS1.index(thetime)
        save_data["return_pos"] = return_pos

    else:

        # One-way: Note the position of the departure flight
        thetime = cleaned_data["departing_time"]
        depart_pos = Common.OUTBOUND_TIME_OPTIONS1.index(thetime)
        save_data["depart_pos"] = depart_pos
        outbound_flightno = Common.outbound_listof_flights[depart_pos]            

    # Check Availability regarding the Selected Journeys
    # Outbound Flight
    outbound_date = cleaned_data["departing_date"]
    outbound_time = cleaned_data["departing_time"]
    
    return_option = cleaned_data["return_option"]
    if return_option == "Y":
        # Return Flight - Check Availability
        inbound_time = cleaned_data["returning_time"]
        return_pos = Common.INBOUND_TIME_OPTIONS1.index(inbound_time)
        inbound_flightno = Common.inbound_listof_flights[return_pos]            
        inbound_date = cleaned_data["returning_date"]
    else:
        inbound_time = None
        inbound_flightno = None
        inbound_date = None

    check_avail = morecode.check_availability(request,
                                              "Departing Flight",
                                              outbound_date, 
                                              outbound_flightno,
                                              outbound_time,
                                              "Returning Flight",
                                              inbound_date, 
                                              inbound_flightno,
                                              inbound_time,
                                              cleaned_data)

    print("CV", check_avail)
    if not check_avail:
        # Insufficient Availability for Selected Flight(s)
        return (False, None)
    
    # Successful Validation
    return (True, save_data)


# TODO
def create_booking_form(request):
    """ The Handling of the Create Bookings Form """

    if not Common.initialised:
        Common.initialisation()

    form = CreateBookingForm(request.POST or None)

    if request.method == "POST":
        #  create a form instance and populate it with data from the request:
        # check whether it is valid:
        # TODO
        is_form_valid, saved_data = is_booking_form_valid(form, request)
        if is_form_valid:
            context = {"booking": form.cleaned_data}
            # Update dict 'context' with the contents of dict 'saved_data'
            context |= saved_data 

            # ADULTS
            number_of_adults = form.cleaned_data["adults"]
            print("N/A", number_of_adults) # TODO
            AdultsFormSet = formset_factory(AdultsForm,
                                            extra=number_of_adults)
            adults_formset = AdultsFormSet(prefix="adult")

            # CHILDREN
            number_of_children = form.cleaned_data["children"]
            if number_of_children > 0:
                children_included = True
                ChildrenFormSet = formset_factory(MinorsForm,
                                                  extra=number_of_children)
                children_formset = ChildrenFormSet(prefix="child")
            else:
                children_included = False
                children_formset = []

            # INFANTS
            number_of_infants = form.cleaned_data["infants"]
            if number_of_infants > 0:
                infants_included = True
                InfantsFormSet = formset_factory(MinorsForm,
                                                 extra=number_of_infants)
                infants_formset = InfantsFormSet(prefix="infant")
            else:
                infants_included = False
                infants_formset = []

            # Create the 'context'
            hiddenForm = HiddenForm(form.cleaned_data)
            bags_remarks_form = BagsRemarks(prefix="bagrem")
            context["adults_formset"] = adults_formset
            context["children_formset"] = children_formset
            context["children_included"] = children_included
            context["infants_formset"] = infants_formset
            context["infants_included"] = infants_included
            context["hidden_form"] = hiddenForm
            context["bags_remarks_form"] = bags_remarks_form

            # Save a copy in order to fetch any values as and when needed
            Common.save_context = context
            print("SAVED/1", Common.save_context) # TODO
            # TODO
            print("NOW", context)
            return render(request, "booking/passenger-details-form.html",
                          context)

            # CREATE SUCCESS MESSAGE TODO

        else:
            # The Booking Form has failed validation
            form = CreateBookingForm(request.POST)

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)

def initialise_formset_context(request):
    """
    Create the 'context' to be used by the Passenger Details Template
    Necessary preset values have been saved in 'Common.save_context'
    """
    context = {}

    # ADULTS
    number_of_adults = Common.save_context["booking"]["adults"]
    AdultsFormSet = formset_factory(AdultsForm,
                                    extra=number_of_adults)
    adults_formset = AdultsFormSet(request.POST or None, prefix="adult")
    context["adults_formset"] = adults_formset

    # CHILDREN
    children_included = Common.save_context["children_included"]
    context["children_included"] = children_included
    if children_included:
        number_of_children = Common.save_context["booking"]["children"]
        ChildrenFormSet = formset_factory(MinorsForm,
                                          extra=number_of_children)
        children_formset = ChildrenFormSet(request.POST or None,
                                           prefix="child")
        context["children_formset"] = children_formset

    # INFANTS

    infants_included = Common.save_context["infants_included"]
    context["infants_included"] = infants_included
    if infants_included:
        number_of_infants = Common.save_context["booking"]["infants"]
        InfantsFormSet = formset_factory(MinorsForm,
                                         extra=number_of_infants)
        infants_formset = InfantsFormSet(request.POST or None,
                                         prefix="infant")
        context["infants_formset"] = infants_formset

    #context["bags_remarks_form"] = Common.save_context["bags_remarks_form"]
    bags_remarks_form = BagsRemarks(request.POST or None, prefix="bagrem")
    context["bags_remarks_form"] = bags_remarks_form
    context["hidden_form"] = Common.save_context["hidden_form"]
    # TODO
    print("CON", context)
    print("SAVED_CONTEXT", Common.save_context)

    return context

def compute_total_price(children_included, infants_included):
    """ 
    Compute the Total Price of the Booking 

    Adults   - £100     Age > 15
    Children -  £60     Age 2-15
    Infants  -  £30     Age < 2
    Bags     -  £30 

    Then store the values in 'the_fees_template_values'
    in order that they can be rendered on the Confirmation Form
    """

    the_fees_template_values = {}
    number_of_adults = Common.save_context["booking"]["adults"]
    print("N/A2", number_of_adults)
    total = number_of_adults * ADULT_PRICE
    the_fees_template_values["adults_total"] = (
            f"{number_of_adults} x GBP{ADULT_PRICE:3.2f} = GBP{total:5.2f}")

    if children_included:
        number_of_children = Common.save_context["booking"]["children"]
        product = number_of_children * CHILD_PRICE 
        total += product
        the_fees_template_values["children_total"] = (
                    f"{number_of_children} x GBP{CHILD_PRICE:3.2f} = "
                    f"GBP{product:5.2f}")

    if infants_included:
        number_of_infants = Common.save_context["booking"]["infants"]
        product = number_of_infants * INFANT_PRICE
        total += product
        the_fees_template_values["infants_total"] = (
                    f"{number_of_infants} x GBP{INFANT_PRICE:3.2f} = "
                    f"GBP{product:5.2f}")
    
    print("BAGS",Common.save_context["bags"] ) # TODO
    number_of_bags = Common.save_context["bags"]
    if number_of_bags > 0:
        product = number_of_bags * BAG_PRICE
        total += product
        the_fees_template_values["bags_total"] = (
                f"{number_of_bags} x GBP{BAG_PRICE:3.2f} = "
                f"GBP{product:5.2f}")

    the_fees_template_values["total_price_string"] = f"GBP{total:5.2f}"
    # The Actual Total Price
    the_fees_template_values["total_price"] = total
    Common.save_context["total_price"] = total
    print("TYPE/C1", the_fees_template_values) # TODO
    return the_fees_template_values

def add_fees_to_context(the_fees_template_values):
    """
    The fees for the selected journey need to be added to
    the Context which in turn will be rendered on the Confirmation Form
    """ 
    # print(702, type(context)) # TODO
    context = {}
    for var in the_fees_template_values:
        context[var] = the_fees_template_values[var]
    print(703, type(context)) # TODO
    return context
    
def generate_pnr():
    """ 
    Generate a Random Unique 6-character PNR
    PNR - Passenger Name Record
    """

    # For now use a random number - TODO
    # For testing purposes use this naive approach:
    # a 3-character string prefixed with SMI
    # However ensure it is unique!
    matches = 1
    while matches > 0:
        random_string = str(random.randrange(100, 1000))  # 3 digits TODO
        newpnr = "SMI" + random_string
        matches = Booking.objects.filter(pnr=newpnr)[:1].count()
    # Unique PNR
    print(newpnr, "TYPE", type(newpnr)) # TODO
    return newpnr

def setup_confirm_booking_context(request,
                                  children_included,
                                  infants_included,
                                  context):
    # TODO
    """
    Calculate the Fees and Total Price
    Then add the results to the 'context' in order
    to be displayed on the Confirmation Form
    """

    print("CONTEXTIN", context)
    print(701, type(context))
    the_fees = compute_total_price(children_included, infants_included)
    print(the_fees)
    context = add_fees_to_context(the_fees)

    # TODO
    # Update the 'context' with the fees and total price
    context |= the_fees
    print("900DONE", context)


    # Generate a Random Unique 6-character PNR
    # PNR - Passenger Name Record
    context["pnr"] = generate_pnr()
    print("type pnr", 1001, context["pnr"], type(context["pnr"]))

    #print("CONTEXTIN2", context)
    # context = booking_total_price(context, 
    #                               children_included, infants_included)

    # Render the Booking Confirmation Form
    print("CONFIRM BOOKING FORM", context) # TODO
    print(type(context))
    # TODO
    return context


# TODO
def passenger_details_form(request):
    """
    The Handling of the Passenger Details Form
    This form consists of three formsets:
    1) AdultsForm - class AdultsForm
    2) ChildrenFormSet - Class MinorsForm
    2) InfantsFormSet - Class MinorsForm
    followed by the BagsRemarks Form
    Therefore, this method processes the validation
    of all 3 form types.

    # TODO
    Calculate the Fees and Total Price
    Then add the results to the 'context' in order
    to be displayed on the Confirmation Form
    Display result for the Customer to confirm payment
    If Yes, Create the Record
    If No, Continue viewing the Passengers' Details

    """

    print(800, "REQ", request.method)  # TODO
    context = {}

    # ADULTS
    AdultsFormSet = formset_factory(AdultsForm, extra=0)
    adults_formset = AdultsFormSet(request.POST or None, prefix="adult")

    # CHILDREN
    children_included = Common.save_context["children_included"]
    if children_included:
        ChildrenFormSet = formset_factory(MinorsForm, extra=0)
        children_formset = ChildrenFormSet(request.POST or None,
                                           prefix="child")
    else:
        children_formset = []

    # INFANTS
    infants_included = Common.save_context["infants_included"]
    if infants_included:
        InfantsFormSet = formset_factory(MinorsForm, extra=0)
        infants_formset = InfantsFormSet(request.POST or None, prefix="infant")
    else:
        infants_formset = []

    bags_remarks_form = BagsRemarks(request.POST or None, prefix="bagrem")
    print(802, request.method, "CONTEXT FETCH",
          children_included, request.POST)  # TODO
    print(803, context)

    if request.method == "POST":
        context = request.POST
        print(804, "A POST")
        are_all_forms_valid = all_formsets_valid(request,
                                                 adults_formset,
                                                 children_included,
                                                 children_formset,
                                                 infants_included,
                                                 infants_formset,
                                                 bags_remarks_form)
        print(880, are_all_forms_valid)
        if are_all_forms_valid[0]:
            print(881)

            depart_pos = Common.save_context["depart_pos"]
            outbound_date = Common.save_context["booking"]["departing_date"]
            outbound_flightno = Common.outbound_listof_flights[depart_pos]            
            print(882)

            print(Common.save_context["booking"]["departing_date"], "DEP")
            print(Common.save_context["booking"]["returning_date"], "RET")

            cleaned_data = are_all_forms_valid[1]
            Common.save_context["bags"] = cleaned_data.get("bags")
            Common.save_context["remarks"] = cleaned_data.get("remarks")
            print(100) # TODO
            context_copy = request.POST.copy()
            print(200) # TODO
            new_context = setup_confirm_booking_context(request,
                                                        children_included,
                                                        infants_included,
                                                        context_copy)
            print(300, new_context) # TODO
            Common.save_context["pnr"] = new_context["pnr"]
            # TODO: CREATE THE RECORD!!
            print(810, "C1", Common.save_context["bags"], new_context["pnr"])
            print("C2", Common.save_context["remarks"])
            print(type(new_context))
            print(new_context)
            print("C3", context_copy)
            Common.save_context["confirm-booking-context"] = context_copy
            print(2000, Common.save_context["confirm-booking-context"])
#           return render(request, "booking/confirm-booking-form.html", context)  TODO
            return render(request, "booking/confirm-booking-form.html", new_context)

        else:
            context = initialise_formset_context(request)
            #  TODO
            print(820, type(Common.save_context))
            print("TT", Common.save_context)
            print("CON", context)
            print("SAVED_CONTEXT", Common.save_context)

    else:
        # request.method is "GET"
        number_of_adults = Common.save_context["booking"]["adults"]
        context = initialise_formset_context(request)

    return render(request, "booking/passenger-details-form.html", context)

def confirm_booking_form(request):
    
    print(request.method, "RQ")
    if request.method == "POST":
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse("home"))
        # TODO
        else:
            # Create new record Booking/Passenger Records
            # Create new Transaction Record
            # Update Schedule Database
                        # TODO
            morecode.create_new_records(request)
            # Then show home page
            return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/confirm-booking-form.html", context)

def view_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    print("BOOKING:", booking)  # PK/ID   TODO
    print("ID", id)
    print("PNR", booking.pnr)
    queryset = Passenger.objects.filter(pnr_id=id).order_by("pax_number")
    #morecode.handle_view_booking(request, booking, queryset)
    #return #TODO
    # TODO REMOVE
    print(queryset)  # TODO
    print(len(queryset))
    # passenger_list = []
    # for pax_record in queryset:  # TODO
    #     print(type(pax_record))
    #     print(pax_record.pax_type, pax_record.pax_number, pax_record.date_of_birth,
    #           pax_record.first_name, pax_record.last_name)
    #     passenger_list.append(pax_record)

    display = dict(created_at=booking.created_at.strftime("%d%b%y").upper(),
                   # EG 17NOV23
                   outbound_date=booking.outbound_date.strftime("%d%b%y").upper())
    if booking.return_flight:
        display["inbound_date"] = booking.inbound_date.strftime("%d%b%y").upper()

    passenger_list = queryset.values()
    count = 0
    for each_record in passenger_list:
        for each_field in each_record:
            if (each_field == "pax_type" 
                    and passenger_list[count]["pax_type"] in "CI"):
                passenger_list[count]["date_of_birth"] = (
                    passenger_list[count]["date_of_birth"]
                             .strftime("%d%b%y").upper())
        count+=1

    context = {"booking": booking, "passengers": passenger_list, "display": display}
    return render(request, "booking/view-booking.html", context)


def search_bookings(request):
    query = request.GET.get("query")
    # Blank Search
    if not query:
        return HttpResponseRedirect(reverse("home"))

    # TODO

    # Each Booking must has one Principal Passenger
    # That Passenger must be the first mentioned (pax_number=1)
    # and an Adult (pax_type="A")

    # Every Booking has 'one' Principal Passenger
    # Adult 1 - query that Passenger i.e.
    # pax_type == "A" and pax_number == 1
    adult1_qs = Passenger.objects.filter(pnr=OuterRef("id"),
                                         
                                         pax_number=1)

    # Case Insensitive Search - in 3 parts

    queryset = (Booking.objects.filter(
                # 1) Matching PNR
                Q(pnr__icontains=query) | (

                 # 2) Or Matching Principal Passenger's First Name
                 Q(passenger__first_name__icontains=query) &
                 #Q(passenger__pax_type__exact="A") &
                 Q(passenger__pax_number=1)) | (

                 # 3) Or Matching Principal Passenger's Last Name
                 Q(passenger__last_name__icontains=query) &
                 #Q(passenger__pax_type__exact="A") &
                 Q(passenger__pax_number=1)))

                # Sort the Query Result by the PNR
                .distinct().order_by("pnr")

                # Include the name of the Principal Passenger
                .annotate(first_name=Subquery(
                         adult1_qs.values("first_name")[:1]),
                          last_name=Subquery(
                         adult1_qs.values("last_name")[:1])))

    if queryset.count() == 0:
        # No Matching Bookings Found
        message_string = f"No Bookings found that matched '{query }'"
        messages.add_message(request, messages.ERROR,
                             message_string)
        return HttpResponseRedirect(reverse("home"))

    print("QS1", queryset)  # TODO
    for element in queryset:
        print("PNR1", element.pnr)  # TODO
        qs = Passenger.objects.filter(pnr=element.id,
                                      #pax_type="A",
                                      pax_number=1)
        print("SUBQ", qs)  # TODO
        for elem2 in qs:
            print(elem2.first_name, elem2.last_name)

    # Pagination as demonstrated in
    # https://testdriven.io/blog/django-pagination/

    # 3 records per page
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get("page", 1)

    try:
        page_object = paginator.page(page_number)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_object = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_object = paginator.page(paginator.num_pages)

    context = {"queryset": queryset, "query": query,
               "page_object": page_object}
    return render(request, "booking/search-bookings.html", context)


def delete_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    context = {"booking": booking}

    if request.method == "POST":
        morecode.realloc_seats_first(request, id, booking)
        return HttpResponseRedirect(reverse("home"))
        return
        booking.delete()
        messages.add_message(request, messages.SUCCESS,
                             "Booking Deleted Successfully")
        return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/delete-booking.html", context)


def edit_booking(request, id):
    booking = get_object_or_404(Employer, pk=id)
    form = BookingForm(instance=booking)
    context = {"booking": booking, "form": form}
    if request.method == "POST":

        # Update Booking() with the new values
        # TODO

        booking.company_name = request.POST.get("company_name")
        booking.number_of_employees = request.POST.get("number_of_employees")
        # employer_test_flag will either be set to "on" or None
        # Handle it so that it is either "on" or False
        new_employer_test_flag = request.POST.get("employer_test_flag", False)
        # "employer_test_flag" -  convert "on" value to either True or False."]
        booking.employer_test_flag = (True if new_employer_test_flag == "on"
                                      else False)

        booking.save()
        return HttpResponseRedirect(reverse("view-booking",
                                            kwargs={"id": booking.pk}))
        # CREATE SUCCESS MESSAGE TODO

    return render(request, "booking/edit-booking.html", context)
