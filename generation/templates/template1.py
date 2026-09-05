from PIL import Image, ImageDraw, ImageFont


def template1(gen, card_template: str, MprimaryColor: int, MsecondarColor: int, school_logo: str, school_name: str, school_slogan: str, academic_year: str, expiration_date: str, student_photo: str, cards_path: str) -> str:
    print("Designing card with template 1...")

    # Load fonts and assign them to variables
    font_title_big, font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_fonts()

    # Card dimensions
    card_width, card_height = 500, 300
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondarColor = MsecondarColor

    # School logo
    print("Adding school logo...")
    logo = Image.open(school_logo).resize((70, 70), Image.LANCZOS)
    logo_position = (30, 15)

    # Header area for school name (centered with rounded rectangle)
    print("Drawing header...")
    header_height = 60
    header_fill = primaryColor
    border_radius = 10  # Rounded corners

    # Calculate header width and position
    header_width = card_width - 60  # Leave some margin on both sides
    header_x_start = (card_width - header_width) // 2  # Center the header
    header_y_start = 15
    header_area = [header_x_start, header_y_start, header_x_start + header_width, header_y_start + header_height]

    # Draw rounded rectangle for header
    draw.rounded_rectangle(header_area, fill=header_fill, radius=border_radius)

    # Add school logo to the left of the header
    try:
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        card.paste(logo, (header_x_start + 10, header_y_start + (header_height - logo.size[1]) // 2), logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # Add school name in the center of the header
    school_name_position = (header_x_start + 90, header_y_start + (header_height - 35) // 2)
    draw.text(school_name_position, school_name, fill=secondarColor, font=font_title)

    # Academic year in its own rounded rectangle (smaller, on the right)
    print("Adding academic year...")
    academic_year_width = 120
    academic_year_height = 40
    academic_year_x_start = header_x_start + 90
    academic_year_y_start = header_y_start + (header_height) - 25
    draw.text((academic_year_x_start, academic_year_y_start), academic_year, fill=secondarColor, font=font_small_bold)

    # Add "Student Card" below the header
    print("Adding 'Student Card' text...")
    student_card_text = "Student Card"
    student_card_x = (card_width - draw.textlength(student_card_text, font=font_bold)) // 2  # Center the text
    student_card_y = header_y_start + header_height + 10
    draw.text((student_card_x, student_card_y), student_card_text, fill=primaryColor, font=font_bold)

    # Student photo
    print("Adding student photo...")
    photo_position = (30, student_card_y + 50)  # Adjusted position to fit below "Student Card"
    photo_size = (100, 120)
    try:
        with Image.open(student_photo) as photo:
            # Create white background image
            bg = Image.new('RGBA', photo_size, 'white')

            # Resize photo maintaining transparency
            photo = photo.resize(photo_size, Image.LANCZOS)

            # Paste photo onto white background
            if photo.mode == 'RGBA':
                bg.paste(photo, (0,0), photo)
            else:
                bg.paste(photo, (0,0))

            # Create mask for rounded corners
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=20, fill=255)

            # Paste final image with mask
            card.paste(bg, photo_position, mask)
    except IOError:
        print("Student photo not found; skipping photo placement.")
        with Image.open(school_logo) as photo:
            # Create white background image
            bg = Image.new('RGBA', photo_size, 'white')

            if photo.mode != 'RGBA':
                photo = logo.convert('RGBA')
            photo = photo.resize(photo_size, Image.LANCZOS)

            # Paste photo onto white background
            bg.paste(photo, (0,0), photo)

            # Create mask for rounded corners
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=20, fill=255)

            # Paste final image with mask
            card.paste(bg, photo_position, mask)


    # Student details with rounded rectangle background
    print("Adding student details...")
    details_x = 150
    details_y = photo_position[1]  # Align with the top of the photo
    spacing = 20
    fields = [
        ("Fullname", gen.data.get('Surname', 'N/A') + " " + gen.data.get('Firstname', 'N/A')),
        ("Sex", gen.data.get('Gender', 'N/A')),
        ("Age", gen.data.get('Age', 'N/A')),
        ("Course", gen.data.get('Trade', 'N/A')),
        ("Exp. Date", expiration_date),
    ]

    # Calculate the size of the details area
    details_width = card_width - details_x - 30  # Leave some margin on the right
    details_height = len(fields) * spacing + 20  # Add padding
    details_area = [details_x - 10, details_y - 10, details_x + details_width, details_y + details_height]

    # Draw rounded rectangle for student details
    draw.rounded_rectangle(details_area, fill=primaryColor, radius=border_radius)

    # Add student details text
    for label, value in fields:
        draw.text((details_x, details_y), f"{label}:", fill=secondarColor, font=font_small_bold)
        draw.text((details_x + draw.textlength(label, font=font_small_bold) + 10, details_y), f"{value}", fill=secondarColor, font=font_small)
        details_y += spacing

    # Slogan area with rounded rectangle background
    print("Adding slogan area...")
    slogan_area_height = 20
    slogan_area_y = card_height - slogan_area_height - 20
    slogan_area = [20, slogan_area_y, card_width - 20, card_height - 10]

    # Draw rounded rectangle for slogan area
    draw.rounded_rectangle(slogan_area, fill=primaryColor, radius=border_radius)

    # Add slogan text (centered)
    slogan_text = school_slogan if school_slogan else "Your School Slogan Here"
    slogan_x = (card_width - draw.textlength(slogan_text, font=font_small)) // 2
    slogan_y = slogan_area_y + (slogan_area_height - 10) // 2
    draw.text((slogan_x, slogan_y), slogan_text, fill=primaryColor, font=font_slogan_regular, stroke_width=2, stroke_fill=secondarColor)

    # Save the card
    print("Saving card...")
    back_side = template1_back(gen, card_template, MprimaryColor, MsecondarColor, school_logo, school_name)
    return gen.save_double_sided_card(card, back_side, cards_path, school_name, academic_year, card_template)


def template1_back(gen, card_template: str, MprimaryColor: int, MsecondarColor: int, school_logo: str, school_name: str, qr_data: str = None) -> Image:
    print("Designing card back side with template 1...")

    # Card dimensions (same as front)
    card_width, card_height = 500, 300
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondarColor = MsecondarColor

    # Load fonts
    font_paths = {
        "Montserrat-Bold": "fonts/Montserrat/static/Montserrat-Bold.ttf",
        "OpenSans-Regular": "fonts/OpenSans/static/OpenSans-Regular.ttf",
        "OpenSans-Bold": "fonts/OpenSans/static/OpenSans-Bold.ttf",
    }

    try:
        font_title = ImageFont.truetype(font_paths["Montserrat-Bold"], 16)
        font_regular = ImageFont.truetype(font_paths["OpenSans-Regular"], 12)
        font_bold = ImageFont.truetype(font_paths["OpenSans-Bold"], 12)
    except IOError as e:
        print(f"Error loading fonts: {e}. Using default fonts...")
        font_title = font_regular = font_bold = ImageFont.load_default()

    # Add decorative border
    border_width = 5
    draw.rectangle([0, 0, card_width, card_height], outline=primaryColor, width=border_width)

    # QR Code section (centered, top)
    qr_size = 150
    qr_position = ((card_width - qr_size) // 2, 30)

    # Generate and add QR code
    if qr_data:
        qr_img = gen.generate_qr_code(qr_data, qr_size)
        card.paste(qr_img, qr_position)

    # Add school logo (small, bottom right)
    try:
        logo = Image.open(school_logo).resize((50, 50), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (card_width - 70, card_height - 70)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # Add terms and conditions
    terms_text = [
        "Terms and Conditions:",
        "1. This card is the property of " + school_name,
        "2. If found, please return to the school administration",
        "3. This card is not transferable",
        "4. Report lost card immediately",
        "5. Replacement fee applies for lost cards"
    ]

    # Add terms text
    text_y = qr_position[1] + qr_size + 20
    for term in terms_text:
        font = font_bold if term.startswith("Terms") else font_regular
        text_width = draw.textlength(term, font=font)
        x = (card_width - text_width) // 2
        draw.text((x, text_y), term, fill=primaryColor, font=font)
        text_y += 20

    return card
