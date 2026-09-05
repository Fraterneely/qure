from importlib.resources import files
import qure.assets
from PIL import Image, ImageDraw, ImageFont


def template8(gen, card_template: str, MprimaryColor: int,
    MsecondarColor: int, school_logo: str, school_stamp: str, school_name: str, school_slogan: str,
    academic_year: str, expiration_date: str, student_photo: str, school_phone: str, school_email: str,
    location: str, website: str, principal_name: str, principal_phone: str, principal_mail: str, principal_signature: str, cards_path: str) -> str:
    """Designs a student ID card with a modern, professional layout with curved header."""
    print("Designing card with template 6...")

    # Load fonts and assign them to variables
    font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_new_fonts()

    # Card dimensions
    card_width, card_height = 1012, 638
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    # Set colors - using deep purple as primary color
    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Add subtle pattern to background
    print("Adding background pattern...")
    pattern_spacing = 32
    pattern_size = 8
    pattern_color = gen.lighten_color(primaryColor, 0.9)

    for x in range(0, card_width, pattern_spacing):
        for y in range(0, card_height, pattern_spacing):
            # Add small circle or square for pattern
            draw.ellipse([(x, y), (x + pattern_size, y + pattern_size)], fill=pattern_color)

    # Create curved header (approx 40% of card height)
    header_height = int(card_height * 0.3)

    gradient_start = gen.lighten_color(primaryColor, 0.2)
    gradient_end = gen.darken_color(primaryColor, 0.2)

    # Draw rectangular header with gradient
    print("Drawing rectangular with gradient...")
    for y in range(header_height):
        # Calculate gradient color for current y position
        r = gradient_start[0] + (gradient_end[0] - gradient_start[0]) * y // header_height
        g = gradient_start[1] + (gradient_end[1] - gradient_start[1]) * y // header_height
        b = gradient_start[2] + (gradient_end[2] - gradient_start[2]) * y // header_height
        current_color = (r, g, b)

        # Draw horizontal line for gradient
        draw.line([(0, y), (card_width, y)], fill=current_color)

    # Student card text
    text_y = header_height + 15
    text = "Student Card"
    text_width = draw.textlength(text, font=font_min_title)
    draw.text(((card_width - text_width) // 2, text_y), text, fill=primaryColor, font=font_min_title)

    # Add horizontal line with dots
    line_y = header_height + 80
    dot_radius = 10
    dot_positions = [60, 238, 510, 782, 952]  # Positions for the dots

    # Draw the line
    draw.line([(20, line_y), (card_width - 20, line_y)], fill=secondaryColor, width=5)

    # Draw the dots
    for x_pos in dot_positions:
        draw.ellipse([(x_pos - dot_radius, line_y - dot_radius),
                      (x_pos + dot_radius, line_y + dot_radius)],
                     fill=secondaryColor)

    # RTB logo (left side of header)
    print("adding RTB logo...")
    rtb_logo = files(qure.assets).joinpath("RTB_logo.png")
    try:
        logo = Image.open(rtb_logo).resize((130, 130), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')

        # Create rounded background
        bg_size = (140, 140)
        background = Image.new('RGBA', bg_size, (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(background)
        bg_draw.rounded_rectangle([(0, 0), bg_size], radius=20, fill=(255, 255, 255, 255))

        # Paste logo on background
        background.paste(logo, (5, 5), logo)
        card.paste(background, (45, 25), background)

    except IOError:
        print("RTB logo not found; skipping logo placement.")

    # School name and slogan (in the middle of header)
    print("adding school name and slogan...")
    school_name_width = draw.textlength(school_name, font=font_title)
    school_slogan_width = draw.textlength(school_slogan, font=font_slogan_regular)
    draw.text(((card_width - school_name_width) // 2, 40), school_name, fill="white", font=font_title)
    draw.text(((card_width - school_slogan_width) // 2, 90), school_slogan, fill="white", font=font_slogan_regular)

    # School logo (right side of header)
    print("adding school logo...")
    try:
        logo = Image.open(school_logo).resize((140, 140), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (card_width - logo.width - 45, 25)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # Student photo
    print("Adding student photo...")
    photo_size = (240, 280)
    photo_position = (60, 290)
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
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=30, fill=255)

            # Create slightly larger mask for the border with rounded corners
            border_size = (photo_size[0] + 3, photo_size[1] + 3)
            border_mask = Image.new("L", border_size, 0)
            border_draw = ImageDraw.Draw(border_mask)
            border_draw.rounded_rectangle([0, 0, *border_size], radius=30, fill=255)

            # Paste the photo with rounded corners
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
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=30, fill=255)

            # Paste final image with mask
            card.paste(bg, photo_position, mask)

    # Student details (right side)
    print("Adding student details...")
    details_x = 360
    details_y = 330

    if card.mode != 'RGBA':
        card = card.convert('RGBA')

    # Create a new transparent overlay for the details section
    details_overlay = Image.new('RGBA', card.size, (0, 0, 0, 0))
    details_draw = ImageDraw.Draw(details_overlay)

    # Draw a semi-transparent rounded rectangle with gradient
    details_rect = [details_x - 30, details_y, card_width - 40, card_height - 100]

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
            radius=20,
            outline=(*secondaryColor, border_opacity),
            width=1
        )

    # Composite the details overlay onto the card
    card = Image.alpha_composite(card, details_overlay)
    draw = ImageDraw.Draw(card)  # Recreate the draw object for the updated card

    # Adjust starting position for fields after header and line
    details_y += 10
    spacing = 40

    # Enhanced fields with icons/symbols
    print("Adding student details info...")
    fields = [
        ("Student ID: ", "KAA" + str(gen.data.get('id', '001'))),
        ("Name: ", f"{gen.data.get('Surname', 'N/A')} {gen.data.get('Firstname', 'N/A')}"),
        ("Trade:", f"{gen.data.get('Trade', 'Computer Science')}"),
        ("Level:", f"{gen.data.get('Class', 'Level 1')}"),
        ("Valid Until:", expiration_date)
    ]

    # Draw fields with enhanced styling
    print("Adding enhanced styling on details...")
    for i, (label, value) in enumerate(fields):
        # Label with subtle shadow for depth
        shadow_offset = 1
        draw.text((details_x + shadow_offset, details_y + shadow_offset),
                 label, fill=(0, 0, 0, 100), font=font_medium)
        draw.text((details_x, details_y), label,
                 fill="black", font=font_medium)

        # Value with professional styling
        # Create a subtle highlight effect for the value text
        draw.text((details_x + 200, details_y), value,
                 fill="black", font=font_medium_bold)

        details_y += spacing

    # Add small watermark icons at bottom corners
    secure_color = (150, 150, 150)
    try:
        watermark_path = files(qure.assets).joinpath("avatar1.png")
        with watermark_path.open("rb") as f:
            watermark_logo = Image.open(f).convert("RGBA")

        small_logo = watermark_logo.resize((40, 47), Image.LANCZOS)
        if small_logo.mode != 'RGBA':
            small_logo = small_logo.convert('RGBA')

        # Bottom right corner
        card.paste(small_logo, (card_width - 120, card_height - 90), small_logo)

        # Add "Powered by Kaascan" text at bottom
        powered_text = "© Powered by Kaascan"
        powered_width = draw.textlength(powered_text, font=font_smallest)
        draw.text((card_width - powered_width - 30, card_height - 40),
                powered_text, fill=(45, 104, 196), font=font_smallest)

    except IOError as e:
        print(f"Watermark load failed: {e}")


    # Add "SECURE DOCUMENT - DO NOT COPY" text at very bottom
    secure_text = "SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY"
    draw.text((-10, card_height - 20), secure_text, fill=secure_color, font=font_smallest)

    # Save both sides
    # NOTE: this preserves a pre-existing bug - `template8_back` has never existed
    # anywhere in this codebase. This call raises a NameError if template8 is ever
    # invoked, exactly mirroring the original's AttributeError. template8 is not
    # wired into create_student_card's dispatcher, so this is unreachable today.
    back_side = template8_back(gen, card_template, MprimaryColor, MsecondarColor,
                school_logo, school_stamp, school_name, school_slogan, school_phone, school_email,
                location, website, principal_name, principal_phone,
                principal_mail, principal_signature)
    return gen.save_double_sided_card(card, back_side, cards_path, school_name, academic_year, card_template)
