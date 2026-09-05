from importlib.resources import files
import qure.assets
from PIL import Image, ImageDraw, ImageFont


def template5(gen, card_template: str, MprimaryColor: int,
    MsecondarColor: int, school_logo: str, school_stamp: str, school_name: str, school_slogan: str,
    academic_year: str, expiration_date: str, student_photo: str, school_phone: str, school_email: str,
    location: str, website: str, principal_name: str, principal_phone: str, principal_mail: str, principal_signature: str, cards_path: str) -> str:
    """Designs a student ID card with a modern, professional layout with curved header."""
    print("Designing card with template 4...")

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

    # School logo (right side of header)
    print("adding school logo...")
    try:
        logo = Image.open(school_logo).resize((130, 130), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (card_width - logo.width - 45, 25)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # School name and slogan (left side of header)
    draw.text((60, 40), school_name, fill="white", font=font_title)
    draw.text((60, 90), school_slogan, fill="white", font=font_slogan_regular)

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
    back_side = template5_back(gen, card_template, MprimaryColor, MsecondarColor,
                school_logo, school_stamp, school_name, school_slogan, school_phone, school_email,
                location, website, principal_name, principal_phone,
                principal_mail, principal_signature)
    return gen.save_double_sided_card(card, back_side, cards_path, school_name, academic_year, card_template)


def template5_back(gen, card_template: str, MprimaryColor: int, MsecondarColor: int,
                  school_logo: str, school_stamp: str, school_name: str, school_slogan: str, school_phone: str, school_email: str,
                  location: str, website: str, principal_name: str, principal_phone: str,
                  principal_mail: str, principal_signature: str) -> Image:
    """Designs the back side of template 4 with terms and conditions."""
    print("Designing card back side with template 4...")

    # Load fonts and assign them to variables
    font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_new_fonts()

    # Card dimensions
    card_width, card_height = 1012, 638
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Add subtle pattern to background
    print("Adding background pattern...")
    # Create a pattern of small dots/shapes
    pattern_spacing = 32
    pattern_size = 8
    pattern_color = gen.lighten_color(primaryColor, 0.9)

    for x in range(0, card_width, pattern_spacing):
        for y in range(0, card_height, pattern_spacing):
            # Add small circle or square for pattern
            draw.ellipse([(x, y), (x + pattern_size, y + pattern_size)], fill=pattern_color)

    # Create curved header (approx 40% of card height)
    header_height = int(card_height * 0.3)

    # Draw a curved bottom edge for the header using a polygon
    # Create points for the curved bottom edge
    curve_points = []
    for x in range(0, card_width + 1, 10):
        # Create a sine wave effect for the bottom edge
        y_offset = 20 * (1 - abs((x - card_width/2) / (card_width/2)))
        curve_points.append((x, header_height + y_offset))

    # Complete the polygon by adding corners
    header_points = [(0, 0), (card_width, 0)]
    header_points.extend(curve_points)
    header_points.append((0, header_height))

    # Create gradient colors for header
    gradient_start = gen.lighten_color(primaryColor, 0.2)
    gradient_end = gen.darken_color(primaryColor, 0.2)

    # Draw rectangular header with gradient
    for y in range(header_height):
        # Calculate gradient color for current y position
        r = gradient_start[0] + (gradient_end[0] - gradient_start[0]) * y // header_height
        g = gradient_start[1] + (gradient_end[1] - gradient_start[1]) * y // header_height
        b = gradient_start[2] + (gradient_end[2] - gradient_start[2]) * y // header_height
        current_color = (r, g, b)

        # Draw horizontal line for gradient
        draw.line([(0, y), (card_width, y)], fill=current_color)

    # Add horizontal gold line with dots
    line_y = header_height + 20
    dot_radius = 10
    dot_positions = [60, 238, 510, 782, 952]  # Positions for the dots

    # Draw the line
    draw.line([(20, line_y), (card_width - 20, line_y)], fill=secondaryColor, width=5)

    # Draw the dots
    for x_pos in dot_positions:
        draw.ellipse([(x_pos - dot_radius, line_y - dot_radius),
                      (x_pos + dot_radius, line_y + dot_radius)],
                     fill=secondaryColor)

    # School logo (right side of header)
    try:
        logo = Image.open(school_logo).resize((130, 130), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (card_width - logo.width - 45, 25)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # School name and slogan (left side of header)
    school_name_width = draw.textlength(school_name, font=font_title)
    school_slogan_width = draw.textlength(school_slogan, font=font_slogan_regular)
    draw.text(((card_width - school_name_width) // 2, 40), school_name, fill="white", font=font_title)
    draw.text(((card_width - school_slogan_width) // 2, 90), school_slogan, fill="white", font=font_slogan_regular)

    # Add QR code with student ID and name on the left side
    print("Adding QR code...")
    try:
        import qrcode
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.colormasks import RadialGradiantColorMask

        #Create QR code data with student ID and name
        student_id = gen.data.get('student_id', '00000000-0000-0000-0000-000000000000')
        student_name = f"{gen.data.get('Surname', 'N/A')} {gen.data.get('Firstname', 'N/A')}"
        qr_data = f"{student_id}"


        # Generate QR code with colors
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create a colored QR code with gradient
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask(
                back_color=(255, 255, 255),
                center_color=secondaryColor,
                edge_color=primaryColor,
            )
        )

        # Resize QR code to fit nicely on the left side
        qr_size = (260, 260)
        qr_img = qr_img.resize(qr_size, Image.LANCZOS)

        # Position QR code on the left side
        qr_position = (120, header_height + 120)

        # Add a white background behind QR code for better visibility
        draw.rounded_rectangle(
            [qr_position[0]-10, qr_position[1]-10,
             qr_position[0]+qr_size[0]+10, qr_position[1]+qr_size[1]+10],
            radius=15, fill=(255, 255, 255, 220)
        )

        # Paste QR code
        card.paste(qr_img, qr_position)

        # Add "Scan Me" text above QR code
        scan_text = "SCAN ME"
        scan_width = draw.textlength(scan_text, font=font_medium_bold)
        scan_x = qr_position[0] + (qr_size[0] - scan_width) // 2
        draw.text((scan_x, qr_position[1] - 50), scan_text, fill=secondaryColor, font=font_medium_bold)

    except ImportError:
        print("QR code libraries not installed; skipping QR code generation")
        # Draw a placeholder rectangle instead
        qr_position = (60, header_height + 80)
        qr_size = (200, 200)
        draw.rounded_rectangle(
            [qr_position[0], qr_position[1],
             qr_position[0]+qr_size[0], qr_position[1]+qr_size[1]],
            radius=15, fill="white", outline=secondaryColor, width=3
        )
        draw.text((qr_position[0]+50, qr_position[1]+80), "QR CODE", fill=primaryColor, font=font_medium_bold)
    except Exception as e:
        print(f"Error generating QR code: {e}")

    # Terms and conditions content
    terms_x = card_width - 450
    terms_y = header_height + 50
    terms_text = [
        f"1. This card is the property of {school_name}.",
        f"2. If found, please return to the school office or kaascan office.",
        "3. This card must be carried at all times.",
        "4. This card is not transferable.",
        "5. Replacement fee applies for lost cards."
    ]

    for line in terms_text:
        draw.text((terms_x, terms_y), line, fill="black", font=font_small)
        terms_y += 25

    # Contact information
    contact_y = terms_y + 20
    draw.text((terms_x, contact_y), "CONTACT INFORMATION:", fill=secondaryColor, font=font_small_bold)
    contact_y += 25

    contact_info = [
        f"Phone:  {school_phone}",
        f"Email:  {school_email} ",
        f"Website: {website}",
        f"Address: {location}"
    ]

    for line in contact_info:
        draw.text((terms_x, contact_y), line, fill="black", font=font_small)
        contact_y += 20

    # Principal signature section (right side)
    print("Adding principal signature box...")
    sig_box_x = card_width - 650
    sig_box_y = card_height - 130
    sig_box_width = 420
    sig_box_height = 140

    # Add signature line and text
    sig_line_start = sig_box_x + 50
    sig_line_end = sig_box_x + 210
    sig_line_width = sig_line_end - sig_line_start

    # Draw the signature line
    draw.line([(sig_line_start, sig_box_y + 70), (sig_line_end, sig_box_y + 70)], fill="black", width=1)

    #add sugnature
    print("Adding principal signature...")
    try:
        signature = Image.open(principal_signature).resize((130, 90), Image.LANCZOS)
        if signature.mode != 'RGBA':
            signature = signature.convert('RGBA')
        signature_x = sig_line_start + (sig_line_width - 130) // 2
        signature_y = sig_box_y - 25
        signature_position = (signature_x, signature_y)
        card.paste(signature, signature_position, signature)
    except IOError:
        print("Principal signature not found; skipping signature placement.")

    # Center the principal name
    name_width = draw.textlength(principal_name, font=font_small)
    name_x = sig_line_start + (sig_line_width - name_width) // 2
    draw.text((name_x, sig_box_y + 80), principal_name, fill="black", font=font_small)

    #add stamp
    print("Adding school stamp...")
    try:
        stamp = Image.open(school_stamp).resize((120, 120), Image.LANCZOS)
        if stamp.mode != 'RGBA':
            stamp = stamp.convert('RGBA')

        # Create a white circular background
        background = Image.new('RGBA', (130, 130), (0, 0, 0, 0))
        draw_bg = ImageDraw.Draw(background)
        draw_bg.ellipse([0, 0, 130, 130], fill=(255, 255, 255, 230))

        # Calculate position to center stamp on background
        stamp_x = sig_box_x + 240
        stamp_y = sig_box_y - 20
        bg_x = stamp_x - 5
        bg_y = stamp_y - 5

        # Paste background first
        card.paste(background, (bg_x, bg_y), background)

        # Then paste stamp
        card.paste(stamp, (stamp_x, stamp_y), stamp)

    except IOError:
        print("School stamp not found; skipping stamp placement.")

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

    except IOError:
        pass


    # Add "SECURE DOCUMENT - DO NOT COPY" text at very bottom with professional styling
    secure_text = "SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY"
    draw.text((-10, card_height - 20), secure_text, fill=secure_color, font=font_smallest)

    return card
