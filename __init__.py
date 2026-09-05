__version__ = "2.0.0"
__author__ = "INEZA Fraterne Ely HOZANA"

from .generation import CGenerator
from .encryption import encrypt_data, decrypt_data

def create_card(data: dict) -> str:
    print("Starting create card function...")
    """
    Create a student card using the provided data.
    
    Parameters:
    - data: Dictionary containing student and school information
    
    Returns:
    - Path to the generated card image
    """
    generator = CGenerator(data)
    return generator.create_student_card(
        template=data.get('template', 'Template 1'),
        primaryColor=data.get('primaryColor', 0x3498db),
        secondarColor=data.get('secondarColor', 0xffffff),
        student_photo=data.get('student_photo', ''),
        school_logo=data.get('school_logo', ''),
        school_stamp=data.get('school_stamp', ''),
        school_name=data.get('school_name', ''),
        school_slogan=data.get('school_slogan', ''),
        academic_year=data.get('academic_year', ''),
        expiration_date=data.get('expiration_date', ''),
        school_phone=data.get('school_phone', ''),
        school_email=data.get('school_email', ''),
        location=data.get('location', ''),
        website=data.get('website', ''),
        principal_name=data.get('principal_name', ''),
        principal_phone=data.get('principal_phone', ''),
        principal_mail=data.get('principal_mail', ''),
        principal_signature=data.get('principal_signature', ''),
        cards_path=data.get('cards_path', None)
    )
