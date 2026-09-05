from importlib.resources import files
import qure.assets
from PIL import Image, ImageDraw, ImageFont


def template2(gen, card_template: str, MprimaryColor: int,
    MsecondarColor: int, school_logo: str, school_stamp: str, school_name: str, school_slogan: str,
    academic_year: str, expiration_date: str, student_photo: str, school_phone: str, school_email: str,
    location: str, website: str, principal_name: str, principal_phone: str, principal_mail: str, principal_signature: str, cards_path: str) -> str:
    """Designs a student ID card with a modern, professional layout."""
    print("Designing card with template 2...")

    # Load fonts and assign them to variables
    font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_fonts()

    # Card dimensions
    card_width, card_height = 500, 300
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Generate verification code for enhanced security
    verification_code = gen.generate_verification_code(
        gen.data.get('StudentID', 'unknown'),
        school_name,
        expiration_date
    )

    # Header area (full width, navy blue)
    header_height = 80
    draw.rectangle([0, 0, card_width, header_height], fill=primaryColor)

    # Add geometric accent
    draw.polygon([(card_width-80, 0), (card_width, 0), (card_width, 80)], fill=secondaryColor)

    # School logo
    try:
        logo = Image.open(school_logo).resize((60, 60), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (20, 10)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # School name and slogan
    draw.text((100, 15), school_name, fill="white", font=font_title)
    draw.text((100, 45), school_slogan, fill="white", font=font_slogan_regular)

    # Add academic year (top-right corner)
    academic_year_text = academic_year
    academic_year_width = draw.textlength(academic_year_text, font=font_medium_bold)
    academic_year_height = 20
    academic_year_x = card_width - academic_year_width - 20
    academic_year_y = (header_height // 2) - academic_year_height // 2
    draw.rounded_rectangle([academic_year_x, academic_year_y, academic_year_x + academic_year_width + 15, academic_year_y + academic_year_height], radius=10, fill=primaryColor)
    draw.text((academic_year_x + 10, academic_year_y + 2), academic_year_text, fill="white", font=font_medium_bold)

    #Add "Student card" text
    student_card_text = "Student Card"
    student_card_width = draw.textlength(student_card_text, font=font_min_title)
    draw.text(((card_width - student_card_width) // 2, header_height + 10), student_card_text, fill=primaryColor, font=font_min_title)

    # Add verification code with premium styling
    verify_text = f"Verification: {verification_code}"
    verify_width = draw.textlength(verify_text, font=font_small)
    verify_x = (card_width - verify_width) // 2
    draw.text((verify_x, card_height - 25), verify_text, fill=secondaryColor, font=font_small_bold)

    #adding background
    print("Adding background...")
    background_path = files(qure.assets).joinpath("background.jpg")
    with background_path.open("rb") as f:
        watermark_img = Image.open(f).convert("RGBA")

    gen.add_watermark(card, watermark_path=watermark_img, opacity=40, rotation=0)

    # Student photo with rounded corners
    print("Adding student photo...")
    photo_size = (120, 140)
    photo_position = (30, 120)
    gen.place_student_photo(card, student_photo, school_logo, photo_size, photo_position)

    # Student details (right side)
    print("Adding student details...")
    details_x = 180
    details_y = 150

    if card.mode != 'RGBA':
        card = card.convert('RGBA')

    # Create a new transparent overlay for the details section
    details_overlay = Image.new('RGBA', card.size, (0, 0, 0, 0))
    details_draw = ImageDraw.Draw(details_overlay)

    # Draw a semi-transparent rounded rectangle with gradient
    details_rect = [details_x - 12, details_y - 12, card_width - 20, card_height - 65]

    # Create gradient effect in the background
    for y in range(details_rect[1], details_rect[3]):
        # Calculate opacity based on position (more transparent at top, more solid at bottom)
        opacity = int(40 + (y - details_rect[1]) * 0.1)
        opacity = min(opacity, 80)  # Cap at 80 for semi-transparency

        # Get a slightly lighter version of secondary color for gradient
        r, g, b = secondaryColor
        gradient_color = (r, g, b, opacity)

        # Draw a horizontal line with calculated opacity
        details_draw.line(
            [(details_rect[0], y), (details_rect[2], y)],
            fill=gradient_color
        )

    # Add a subtle border with glow effect
    for i in range(3):
        # Decreasing opacity for outer borders (glow effect)
        border_opacity = 180 - (i * 50)
        details_draw.rounded_rectangle(
            [details_rect[0] - i, details_rect[1] - i,
             details_rect[2] + i, details_rect[3] + i],
            radius=10,
            outline=(*secondaryColor, border_opacity),
            width=1
        )

    # Composite the details overlay onto the card
    card = Image.alpha_composite(card, details_overlay)
    draw = ImageDraw.Draw(card)  # Recreate the draw object for the updated card

    # Adjust starting position for fields after header and line
    spacing = 20

    # Enhanced fields with icons/symbols
    print("Adding student details info...")
    fields = [
        ("Student ID: ", "KAA" + str(gen.data.get('id', '001'))),
        ("Name: ", f"{gen.data.get('Surname', 'N/A')} {gen.data.get('Firstname', 'N/A')}"),
        ("Trade:", f"{gen.data.get('Trade', 'Computer Science')}"),
        ("Valid Until:", expiration_date)
    ]

    for label, value in fields:
        draw.text((details_x, details_y), f"{label}:", fill=primaryColor, font=font_small_bold)
        draw.text((details_x + 80, details_y), value, fill="black", font=font_small_bold)
        details_y += spacing

    # Bottom bar
    draw.rectangle([0, card_height-30, card_width, card_height], fill=primaryColor)

    # Add location text (centered in bottom bar)
    location_text = location
    location_width = draw.textlength(location_text, font=font_slogan_small)
    location_x = (card_width - location_width) // 2
    draw.text((location_x, card_height-25), "."+location_text+".", fill=primaryColor, stroke_fill="white", stroke_width=2, font=font_slogan_small)


    # Log this card generation for analytics
    gen.log_card_generation(school_name, card_template)

    # Apply the holographic overlay
    # if card.mode != 'RGBA':
    #     card = card.convert('RGBA')
    # card = Image.alpha_composite(card, holo_overlay)

    # Create the back side of the card
    back_card = template2_back(
        gen, card_template, primaryColor, secondaryColor,
        school_logo, school_stamp, school_name,
        school_phone, school_email, location, website, principal_name,
        principal_phone, principal_mail, principal_signature
    )

    # Save both sides of the card
    front_path, back_path = gen.save_double_sided_card(
        card, back_card, cards_path, school_name, academic_year, card_template
    )

    # Export in high-quality PDF format for premium feel
    pdf_path = gen.export_card(card, 'PDF')

    return front_path, back_path


def template2_back(gen, card_template: str, MprimaryColor: int, MsecondarColor: int,
    school_logo: str, school_stamp: str, school_name: str,
    school_phone: str, school_email: str, school_location: str, website: str, principal_name: str,
    principal_phone: str, principal_mail: str, principal_signature: str,) -> Image:
    """Designs the back side of template 2 with terms and conditions."""
    print("Designing card back side with template 2...")

    # Update the font unpacking to match the number of fonts returned
    font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_fonts()

    # Card dimensions
    print("Card dimensions: 500x300")
    card_width, card_height = 500, 300
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    # Use optimized watermark function instead of direct implementation
    gen.add_watermark(card, opacity=30, rotation=15)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Header with "TERMS AND CONDITIONS" and logo
    header_height = 50
    draw.rectangle([0, 0, card_width, header_height], fill=primaryColor)

    # Terms and Conditions text (left-aligned)
    header_text = "TERMS AND CONDITIONS"
    draw.text((20, 15), header_text, fill="white", font=font_title)

    # School logo
    print("Adding school logo...")
    try:
        logo = Image.open(school_logo).resize((40, 40), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_x = card_width - 100
        logo_y = (header_height - logo.height) // 2
        logo_position = (logo_x, logo_y)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # Add geometric accent
    draw.polygon([(card_width-50, 0), (card_width, 0), (card_width, 50)], fill=secondaryColor)

    # Terms and conditions text (centered, smaller font)
    print("Adding terms and conditions...")
    terms_y = header_height + 30  # Adjusted starting position
    terms_text = [
        "This card is a property of " + school_name,
        "If found please return it to the office of " + school_name + " or nearest police station",
        "Whoever use this card contrary to the law will be punished.",
        " ",
        school_location,
    ]

    # Use smaller font size for terms
    terms_font = font_small

    for line in terms_text:
        # Calculate text width for centering
        text_width = draw.textlength(line, font=terms_font)
        x = (card_width - text_width) // 2  # Center the text
        draw.text((x, terms_y), line, fill=primaryColor, font=terms_font)  # Red color
        terms_y += 20  # Reduced spacing between lines

    # Contact information box (left side)
    print("Adding contact information...")
    contact_box = {
        "Phone": school_phone,
        "Mail": school_email,
        "Website": website
    }

    # Draw rounded rectangle for contact info
    contact_box_x = 30
    contact_box_y = card_height - 80
    contact_box_width = 200
    contact_box_height = 60

    # Add contact information
    y_offset = contact_box_y + 10
    for label, value in contact_box.items():
        draw.text((contact_box_x + 10, y_offset), f"{label} : ", fill=primaryColor, font=font_small_bold)
        label_width = draw.textlength(f"{label} : ", font=font_small_bold)
        draw.text((contact_box_x + 10 + label_width, y_offset), value, fill=primaryColor, font=font_small)
        y_offset += 15

    # Principal signature section (right side)
    print("Adding principal signature box...")
    sig_box_x = card_width - 230
    sig_box_y = card_height - 80
    sig_box_width = 200
    sig_box_height = 60

    # Add signature line and text
    sig_line_start = sig_box_x + 20
    sig_line_end = sig_box_x + 100
    sig_line_width = sig_line_end - sig_line_start

    # Draw the signature line
    draw.line([(sig_line_start, sig_box_y + 30), (sig_line_end, sig_box_y + 30)], fill=primaryColor, width=1)

    #add signature
    print("Adding principal signature...")
    try:
        signature = Image.open(principal_signature).resize((60, 40), Image.LANCZOS)
        if signature.mode != 'RGBA':
            signature = signature.convert('RGBA')
        signature_x = sig_line_start + (sig_line_width - 60) // 2
        signature_y = sig_box_y - 15
        signature_position = (signature_x, signature_y)
        card.paste(signature, signature_position, signature)
    except IOError:
        print("Principal signature not found; skipping signature placement.")

    # Center the principal name
    name_width = draw.textlength(principal_name, font=font_small_bold)
    name_x = sig_line_start + (sig_line_width - name_width) // 2
    draw.text((name_x, sig_box_y + 35), principal_name, fill=primaryColor, font=font_small_bold)

    #add stamp
    print("Adding school stamp...")
    try:
        stamp = Image.open(school_stamp).resize((50, 50), Image.LANCZOS)
        if stamp.mode != 'RGBA':
            stamp = stamp.convert('RGBA')
        stamp_x = sig_box_x + 120
        stamp_y = sig_box_y + 10
        stamp_position = (stamp_x, stamp_y)
        card.paste(stamp, stamp_position, stamp)
    except IOError:
        print("School stamp not found; skipping stamp placement.")

    # Add subtle holographic effect to the stamp area for authenticity
    stamp_region = (stamp_x-5, stamp_y-5, stamp_x+55, stamp_y+55)
    card = gen.add_holographic_effect(card, region=stamp_region, intensity=0.4)

    return card
