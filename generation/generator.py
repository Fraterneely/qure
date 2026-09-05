"""Backward-compatible entry point.

The card-drawing code that used to live entirely in this file has been split up:
CGenerator itself (plus its shared drawing helpers) now lives in `core.py`, and
each template's front/back methods live in their own module under `templates/`.
This module re-exports the same names it always has - `CGenerator`,
`generate_cards`, `load_json` - so existing imports like
`from qure.generation.generator import generate_cards` keep working unchanged.
"""
import json
import logging

from .core import CGenerator

__all__ = ["CGenerator", "generate_cards", "load_json"]


def load_json(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None


def generate_cards(
    is_single: str, json_file: str, card_template: str,
    card_template_primaryColor: int, card_template_secondaryColor: int,
    school_logo: str, school_stamp: str, school_name: str, school_slogan: str,
    academic_year: str, expiration_date: str, school_phone: str, school_email: str, location: str,
    website: str, principal_name: str, principal_phone: str, principal_mail: str, principal_signature: str):
    """Generate cards for all students in the JSON file."""
    try:
        # Track generated cards information
        generated_cards = []

        logging.debug('Starting request to create_student_card....')

        if is_single == 'yes':
            logging.debug('Sending request for single student card....')
            data = json_file
            if data and "students" in data:
                for student in data["students"]:
                    card_generator = CGenerator(student)
                    logging.debug('Sending request to create_student_card....')
                    logging.debug(f'Student Record: {student}')
                    logging.debug(f'Student Firstname: {student.get("Firstname")}')
                    logging.debug(f'We will be using this photot path: {student.get("Photo")}')
                    card_front_path, card_back_path = card_generator.create_student_card(
                        template=card_template,
                        primaryColor=card_template_primaryColor,
                        secondarColor=card_template_secondaryColor,
                        student_photo=student['Photo'],
                        school_logo=school_logo,
                        school_stamp=school_stamp,
                        school_name=school_name,
                        school_slogan=school_slogan,
                        academic_year=academic_year,
                        expiration_date=expiration_date,
                        school_phone=school_phone,
                        school_email=school_email,
                        location=location,
                        website=website,
                        principal_name=principal_name,
                        principal_phone=principal_phone,
                        principal_mail=principal_mail,
                        principal_signature=principal_signature,
                    )
                    logging.debug(f"Student Card generated for {student['Firstname']} at: (Front) {card_front_path}; (Back) {card_back_path}")

                    generated_cards.append({
                        'student_name': student['Firstname'],
                        'department': student['Department'],
                        'trade': student['Trade'],
                        'level': student['Class'],
                        'front_path': card_front_path,
                        'back_path': card_back_path
                    })

                return card_front_path, card_back_path, student['Firstname'], student['Department'], student['Trade'], student['Class'], generated_cards
            else:
                print("Invalid or empty JSON file")

        else:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if data and "students" in data:
                    for student in data["students"]:
                        card_generator = CGenerator(student)
                        logging.debug('Sending request to create_student_card....')
                        card_front_path, card_back_path = card_generator.create_student_card(
                            template=card_template,
                            primaryColor=card_template_primaryColor,
                            secondarColor=card_template_secondaryColor,
                            student_photo=student['Photo'],
                            school_logo=school_logo,
                            school_stamp=school_stamp,
                            school_name=school_name,
                            school_slogan=school_slogan,
                            academic_year=academic_year,
                            expiration_date=expiration_date,
                            school_phone=school_phone,
                            school_email=school_email,
                            location=location,
                            website=website,
                            principal_name=principal_name,
                            principal_phone=principal_phone,
                            principal_mail=principal_mail,
                            principal_signature=principal_signature,
                        )
                        logging.debug(f"Student Card generated for {student['Firstname']} at: (Front) {card_front_path}; (Back) {card_back_path}")

                        generated_cards.append({
                            'student_name': student['Firstname'],
                            'department': student['Department'],
                            'trade': student['Trade'],
                            'level': student['Class'],
                            'front_path': card_front_path,
                            'back_path': card_back_path
                        })

                    return card_front_path, card_back_path, student['Firstname'], student['Department'], student['Trade'], student['Class'], generated_cards
                else:
                    print("Invalid or empty JSON file")


    except Exception as e:
        print(f"Error generating cards on Library section: {e}")
        return None
