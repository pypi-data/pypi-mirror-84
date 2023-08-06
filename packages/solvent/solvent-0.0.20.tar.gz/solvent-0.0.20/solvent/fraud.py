import time

import pomace
import phonenumbers


URL = "https://defendyourballot.formstack.com/forms/voter_fraud"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        person = pomace.fake.person

        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)

        page.fill_phone(
            phonenumbers.format_number(
                phonenumbers.parse(person.phone, "US"),
                phonenumbers.PhoneNumberFormat.NATIONAL,
            )
        )

        page.fill_address(person.address)
        page.fill_city(person.city)
        page.select_state(person.state)
        page.fill_zip_code(person.zip_code)

        page.fill_email(person.email)
        page.fill_email_confirmation(person.email)

        page.select_state_of_the_incident(pomace.fake.state)
        page.fill_county_of_the_incident(person.county)

        page.fill_name_of_the_polling_place("")
        page.fill_description_of_the_incident("More people voted for Biden than Trump.")

        result = page.click_submit_form()

        if "<strong>Your Phone" in result:
            errors += 1
            print(f"Error count: {errors}")
            continue

        if pomace.shared.browser.url == URL:
            print("Complete CAPTCHA manually...")
        while pomace.shared.browser.url == URL:
            time.sleep(1)  # CAPTCHA visible

        if "Please provide as much information as possible." in result:
            errors += 1
            print(f"Error count: {errors}")
            continue

        submits += 1
        errors = 0
        print(f"Submission count: {submits}")
