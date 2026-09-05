from PIL import Image, ImageDraw, ImageFont

from .template6 import template6_back


def template7(gen, card_template: str, MprimaryColor: int, MsecondarColor: int,
             school_logo: str, school_name: str, school_slogan: str,
             academic_year: str, expiration_date: str, student_photo: str,
             school_phone: str, school_email: str, location: str, website: str, cards_path: str) -> str:
    """Designs a professional student ID card with navy blue accents and clean layout."""
    print("Designing card with template 6...")

    # Load fonts and assign them to variables
    font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_fonts()

    # Card dimensions (3.375 × 2.125 inches at 300 DPI)
    card_width, card_height = 1012, 638  # 3.375*300, 2.125*300
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor  # Navy blue
    secondaryColor = MsecondarColor  # White or accent color

    # Add a thin white border around the entire card
    border_width = 2
    draw.rectangle([0, 0, card_width, card_height], outline="white", width=border_width)

    # Header bar (15% of card height)
    header_height = int(card_height * 0.15)
    draw.rectangle([0, 0, card_width, header_height], fill=primaryColor)

    # Lightning bolt/zigzag accent on left side of header
    zigzag_points = [
        (20, 10), (40, 25), (20, 40), (40, 55), (20, 70)
    ]
    draw.line(zigzag_points, fill="white", width=3)

    # School logo on left side of header
    try:
        logo = Image.open(school_logo).resize((70, 70), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (60, (header_height - 70) // 2)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; using placeholder text")
        draw.text((60, (header_height - 20) // 2), "LOGO HERE", fill="white", font=font_medium_bold)

    # School name centered in header
    school_name_width = draw.textlength(school_name, font=font_title)
    school_name_x = (card_width - school_name_width) // 2
    draw.text((school_name_x, 15), school_name, fill="white", font=font_title)

    # School slogan below school name
    slogan_text = school_slogan if school_slogan else "SLOGAN HERE"
    slogan_width = draw.textlength(slogan_text, font=font_small)
    slogan_x = (card_width - slogan_width) // 2
    draw.text((slogan_x, 50), slogan_text, fill="white", font=font_small)

    # Student photo placeholder
    photo_size = (180, 200)
    photo_position = (40, header_height + 30)
    try:
        with Image.open(student_photo) as photo:
            photo = photo.resize(photo_size, Image.LANCZOS)
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rectangle([0, 0, *photo_size], fill=255)
            card.paste(photo, photo_position, mask)

            # Add border around photo
            draw.rectangle([photo_position[0]-1, photo_position[1]-1,
                           photo_position[0]+photo_size[0]+1, photo_position[1]+photo_size[1]+1],
                           outline=primaryColor, width=2)
    except IOError:
        print("Student photo not found; using placeholder")
        draw.rectangle([*photo_position, photo_position[0]+photo_size[0], photo_position[1]+photo_size[1]],
                      fill="lightgray", outline=primaryColor, width=2)

    # Student information fields
    details_x = 260
    details_y = header_height + 40
    spacing = 35
    fields = [
        ("Reg. No", gen.data.get('RegNo', '123456')),
        ("Student ID", gen.data.get('StudentID', '1234')),
        ("Student Name", f"{gen.data.get('Surname', 'Name')} {gen.data.get('Firstname', 'Here')}"),
        ("Father/Guardian", gen.data.get('Guardian', 'Name Here')),
        ("Class", gen.data.get('Class', 'Class Here')),
        ("Emergency Call", gen.data.get('EmergencyContact', '123-456-7890'))
    ]

    for label, value in fields:
        # Draw label with colon
        draw.text((details_x, details_y), f"{label}:", fill=primaryColor, font=font_small_bold)

        # Draw value after colon
        label_width = draw.textlength(f"{label}:", font=font_small_bold)
        draw.text((details_x + label_width + 10, details_y), value, fill="black", font=font_small)
        details_y += spacing

    # Footer with geometric accent in bottom-left corner
    footer_y = card_height - 80

    # Geometric accent (angular shapes)
    draw.polygon([(0, footer_y), (150, footer_y), (0, card_height)], fill=primaryColor)
    draw.polygon([(0, footer_y+30), (80, footer_y+30), (0, footer_y+60)], fill=secondaryColor)

    # School address
    address_text = location if location else "School address, Street, State, 1234"
    draw.text((170, footer_y + 10), address_text, fill=primaryColor, font=font_small)

    # Telephone information
    phone_text = f"Telephone: {school_phone}" if school_phone else "Telephone: 123-456-7890"
    draw.text((170, footer_y + 40), phone_text, fill=primaryColor, font=font_small)

    # Add hole punch indicator at top center
    draw.ellipse([(card_width//2 - 15, 0), (card_width//2 + 15, 30)], outline="lightgray")

    # Save both sides
    # NOTE: this preserves a pre-existing bug - template7's front has always called
    # template6's back method (wrong name/wrong argument list) instead of its own
    # template7_back below. It raises a TypeError if ever invoked, exactly as before;
    # this template is not wired into create_student_card's dispatcher either way.
    back_side = template6_back(gen, card_template, MprimaryColor, MsecondarColor,
                                   school_logo, school_name, school_slogan,
                                   academic_year, expiration_date, school_phone,
                                   school_email, website)
    return gen.save_double_sided_card(card, back_side, cards_path, school_name, academic_year, card_template)


def template7_back(gen, card_template: str, MprimaryColor: int, MsecondarColor: int,
                  school_logo: str, school_name: str, school_slogan: str,
                  academic_year: str, expiration_date: str, school_phone: str,
                  school_email: str, website: str) -> Image:
    """Designs the back side of template 6 with terms and conditions."""
    print("Designing card back side with template 6...")

    # Load fonts and assign them to variables
    font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_fonts()

    # Card dimensions (3.375 × 2.125 inches at 300 DPI)
    card_width, card_height = 1012, 638
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Add a thin white border around the entire card
    border_width = 2
    draw.rectangle([0, 0, card_width, card_height], outline="white", width=border_width)

    # Header bar (matching front)
    header_height = int(card_height * 0.15)
    draw.rectangle([0, 0, card_width, header_height], fill=primaryColor)

    # "TERMS AND CONDITIONS" text on left side
    draw.text((20, (header_height - 20) // 2), "TERMS AND CONDITIONS", fill="white", font=font_medium_bold)

    # School logo on right side of header
    try:
        logo = Image.open(school_logo).resize((70, 70), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (card_width - 90, (header_height - 70) // 2)
        card.paste(logo, logo_position, logo)

        # Tag line below logo
        tag_line = school_slogan if school_slogan else "TAG LINE HERE"
        tag_width = draw.textlength(tag_line, font=font_smallest)
        tag_x = card_width - 90 + (70 - tag_width) // 2
        draw.text((tag_x, header_height - 25), tag_line, fill="white", font=font_smallest)
    except IOError:
        print("School logo not found; using placeholder text")
        draw.text((card_width - 150, (header_height - 20) // 2), "LOGO HERE", fill="white", font=font_medium_bold)

        # Tag line below logo placeholder
        tag_line = school_slogan if school_slogan else "TAG LINE HERE"
        draw.text((card_width - 150, header_height - 25), tag_line, fill="white", font=font_smallest)

    # Terms and conditions content
    terms_x = 40
    terms_y = header_height + 30
    terms_text = [
        "• Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "• Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "• Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
        "• Laboris nisi ut aliquip ex ea commodo consequat.",
        "• Duis aute irure dolor in reprehenderit in voluptate velit.",
        "• Excepteur sint occaecat cupidatat non proident.",
        "• Sunt in culpa qui officia deserunt mollit anim id est laborum."
    ]

    for line in terms_text:
        draw.text((terms_x, terms_y), line, fill="black", font=font_small)
        terms_y += 30

    # Generate QR code on right side
    qr_size = 150
    qr_data = f"School: {school_name}, Website: {website}"
    try:
        qr_img = gen.generate_qr_code(qr_data, qr_size)
        qr_position = (card_width - qr_size - 40, header_height + 40)
        card.paste(qr_img, qr_position)
    except Exception as e:
        print(f"Error generating QR code: {e}")
        # Draw placeholder for QR code
        draw.rectangle([card_width - qr_size - 40, header_height + 40,
                       card_width - 40, header_height + 40 + qr_size],
                      outline=primaryColor, width=2)

    # Contact information
    contact_x = card_width - qr_size - 40
    contact_y = header_height + qr_size + 60
    contact_info = [
        ("Phone", school_phone if school_phone else "123-456-7890"),
        ("Mail", school_email if school_email else "Lorem@email.com"),
        ("Website", website if website else "your-website-here")
    ]

    for label, value in contact_info:
        draw.text((contact_x, contact_y), f"{label}: {value}", fill=primaryColor, font=font_small)
        contact_y += 25

    # Signature area
    sig_y = card_height - 120
    sig_x = card_width // 2 - 100

    # Signature line
    draw.line([(sig_x, sig_y), (sig_x + 200, sig_y)], fill=primaryColor, width=1)

    # "Principal" text below signature line
    principal_text = "Principal"
    principal_width = draw.textlength(principal_text, font=font_small)
    principal_x = sig_x + (200 - principal_width) // 2
    draw.text((principal_x, sig_y + 10), principal_text, fill=primaryColor, font=font_small)

    # Date information
    date_y = card_height - 70

    # Joined date
    joined_text = f"Joined Date: {academic_year}"
    draw.text((40, date_y), joined_text, fill=primaryColor, font=font_small)

    # Expiry date
    expiry_text = f"Expiry Date: {expiration_date}"
    draw.text((card_width - 200, date_y), expiry_text, fill=primaryColor, font=font_small)

    # Add hole punch indicator at top center (matching front)
    draw.ellipse([(card_width//2 - 15, 0), (card_width//2 + 15, 30)], outline="lightgray")

    return card
