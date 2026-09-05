import math
from importlib.resources import files
import qure.assets
from PIL import Image, ImageDraw, ImageFont


def template_kaascan_only(gen, card_template: str, MprimaryColor: int,
    MsecondarColor: int, academic_year: str, expiration_date: str,
    student_photo: str, school_name: str, cards_path: str) -> str:
    """Designs a Kaascan-branded student card without school branding."""
    print("Designing Kaascan-only branded card...")

    # Load fonts and assign them to variables
    font_title_big, font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_new_fonts()

    # Card dimensions
    card_width, card_height = 1012, 638
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    # Set colors - Kaascan brand colors
    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Add subtle pattern to background
    print("Adding background pattern...")
    pattern_spacing = 32
    pattern_size = 8
    pattern_color = gen.lighten_color(primaryColor, 0.9)

    for x in range(0, card_width, pattern_spacing):
        for y in range(0, card_height, pattern_spacing):
            draw.ellipse([(x, y), (x + pattern_size, y + pattern_size)], fill=pattern_color)

    # Create curved header (approx 35% of card height + curve)
    header_height = int(card_height * 0.20)
    curve_depth = 30

    gradient_start = gen.lighten_color(primaryColor, 0.15)
    gradient_end = gen.darken_color(primaryColor, 0.25)

    # Draw curved header with gradient
    print("Drawing curved header with gradient...")

    # Draw the header line by line with curve
    for y in range(header_height + curve_depth):
        # Calculate gradient color for current y position
        gradient_ratio = y / (header_height + curve_depth)
        r = int(gradient_start[0] + (gradient_end[0] - gradient_start[0]) * gradient_ratio)
        g = int(gradient_start[1] + (gradient_end[1] - gradient_start[1]) * gradient_ratio)
        b = int(gradient_start[2] + (gradient_end[2] - gradient_start[2]) * gradient_ratio)
        current_color = (r, g, b)

        # Create curved bottom edge using sine wave
        if y >= header_height:
            # Only draw the curve part
            curve_progress = (y - header_height) / curve_depth
            for x in range(card_width):
                # Create smooth wave curve
                x_normalized = (x / card_width) * math.pi
                wave_height = math.sin(x_normalized) * curve_depth
                y_threshold = header_height + wave_height

                if y <= y_threshold:
                    draw.point((x, y), fill=current_color)
        else:
            # Draw full width line for header body
            draw.line([(0, y), (card_width, y)], fill=current_color)

    # Add decorative wave overlay at the bottom of header
    wave_color = gen.lighten_color(primaryColor, 0.25)
    for x in range(0, card_width, 2):
        x_normalized = (x / card_width) * math.pi * 2
        wave_y = header_height + int(math.sin(x_normalized) * 15) - 10
        draw.ellipse([(x-3, wave_y-3), (x+3, wave_y+3)], fill=wave_color)

    # Kaascan logo (centered in header)
    print("Adding Kaascan logo...")
    kaascan_logo = files(qure.assets).joinpath("avatar.png")
    try:
        logo = Image.open(kaascan_logo).resize((100, 100), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')

        # Center the logo
        logo_x = 60
        logo_position = (logo_x, 15)
        card.paste(logo, logo_position, logo)

    except IOError:
        print("Kaascan logo not found; skipping logo placement.")

    # Kaascan branding with enhanced typography
    print("Adding Kaascan branding text...")

    # Main KAASCAN title with shadow effect for depth
    brand_text = "KAASCAN"
    brand_text_width = draw.textlength(brand_text, font=font_title_big)
    brand_x = (card_width - brand_text_width) // 2
    brand_y = 25

    # Add subtle shadow/glow effect
    shadow_color = (0, 0, 0, 100)
    for offset in range(3, 0, -1):
        shadow_alpha = int(50 * (offset / 3))
        draw.text((brand_x + offset, brand_y + offset), brand_text,
                fill=(*shadow_color[:3], shadow_alpha), font=font_title_big)

    # Main text
    draw.text((brand_x, brand_y), brand_text, fill="white", font=font_title_big)

    slogan_text = "Digital Student Wallet"
    slogan_width = draw.textlength(slogan_text, font=font_regular_bold)
    slogan_x = (card_width - slogan_width) // 2
    slogan_y = 100

    # Add subtle background rectangle for slogan
    padding = 15
    slogan_bg_color = gen.lighten_color(primaryColor, 0.3)
    draw.rounded_rectangle(
        [slogan_x - padding, slogan_y - 5,
        slogan_x + slogan_width + padding, slogan_y + 35],
        radius=15,
        fill=slogan_bg_color
    )

    draw.text((slogan_x, slogan_y), slogan_text, fill="white", font=font_regular_bold)

    # Student card text below header with icon
    text_y = header_height + 60
    text = "SmartCard Wallet"
    text_width = draw.textlength(text, font=font_bold)
    text_x = (card_width - text_width) // 2

    # Add subtle background bar
    bar_padding = 30
    draw.rounded_rectangle(
        [text_x - bar_padding, text_y - 4,
        text_x + text_width + bar_padding, text_y + 38],
        radius=20,
        fill=gen.lighten_color(primaryColor, 0.85),
        outline=primaryColor,
        width=2
    )

    draw.text((text_x, text_y), text, fill=primaryColor, font=font_bold)

    # Enhanced horizontal line with gradient dots
    line_y = header_height + 135
    dot_radius = 12
    dot_positions = [60, 238, 510, 782, 952]

    # Draw gradient line
    for x in range(20, card_width - 20):
        gradient_pos = (x - 20) / (card_width - 40)
        line_color = (
            int(primaryColor[0] * (1 - gradient_pos) + secondaryColor[0] * gradient_pos),
            int(primaryColor[1] * (1 - gradient_pos) + secondaryColor[1] * gradient_pos),
            int(primaryColor[2] * (1 - gradient_pos) + secondaryColor[2] * gradient_pos)
        )
        draw.line([(x, line_y), (x, line_y + 5)], fill=line_color)

    # Draw decorative dots with glow effect
    for x_pos in dot_positions:
        # Outer glow
        for r in range(dot_radius + 8, dot_radius, -2):
            glow_alpha = int(100 * (1 - (r - dot_radius) / 8))
            glow_color = (*primaryColor, glow_alpha)
            draw.ellipse([(x_pos - r, line_y - r + 2),
                        (x_pos + r, line_y + r + 2)],
                        fill=glow_color)

        # Main dot with gradient
        draw.ellipse([(x_pos - dot_radius, line_y - dot_radius + 2),
                    (x_pos + dot_radius, line_y + dot_radius + 2)],
                    fill=primaryColor)

        # Highlight for 3D effect
        highlight_color = gen.lighten_color(primaryColor, 0.4)
        draw.ellipse([(x_pos - dot_radius//2, line_y - dot_radius//2 + 2),
                    (x_pos + dot_radius//2, line_y + dot_radius//2 + 2)],
                    fill=highlight_color)

    # Student photo with border
    print("Adding student photo...")
    photo_size = (240, 240)
    photo_position = (60, 320)
    border_width = 2
    border_color = secondaryColor

    try:
        with Image.open(student_photo) as photo:
            # Create white background
            bg = Image.new('RGBA', photo_size, 'white')
            photo = photo.resize(photo_size, Image.LANCZOS)

            if photo.mode == 'RGBA':
                bg.paste(photo, (0,0), photo)
            else:
                bg.paste(photo, (0,0))

            # Create mask for rounded corners
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=30, fill=255)

            # Paste the photo with mask
            card.paste(bg, photo_position, mask)

            # Draw border around photo
            draw.rounded_rectangle(
                [photo_position[0] - border_width//2,
                photo_position[1] - border_width//2,
                photo_position[0] + photo_size[0] + border_width//2,
                photo_position[1] + photo_size[1] + border_width//2],
                radius=30,
                outline=border_color,
                width=border_width
            )

    except IOError:
        print("Student photo not found; using placeholder.")
        draw.rounded_rectangle(
            [photo_position[0], photo_position[1],
            photo_position[0] + photo_size[0], photo_position[1] + photo_size[1]],
            radius=30, fill=(240, 240, 240), outline=primaryColor, width=border_width
        )

    # Student details (right side)
    print("Adding student details...")
    details_x = 380
    details_y = 360

    if card.mode != 'RGBA':
        card = card.convert('RGBA')

    details_overlay = Image.new('RGBA', card.size, (0, 0, 0, 0))
    details_draw = ImageDraw.Draw(details_overlay)

    details_rect = [details_x - 35, details_y - 10, card_width - 40, card_height - 130]

    for y in range(details_rect[1], details_rect[3]):
        opacity = int(40 + (y - details_rect[1]) * 0.1)
        opacity = min(opacity, 80)

        r, g, b = secondaryColor
        gradient_color = (r, g, b, opacity)

        details_draw.line(
            [(details_rect[0], y), (details_rect[2], y)],
            fill=gradient_color
        )

    for i in range(3):
        border_opacity = 180 - (i * 50)
        details_draw.rounded_rectangle(
            [details_rect[0] - i, details_rect[1] - i,
            details_rect[2] + i, details_rect[3] + i],
            radius=20,
            outline=(*secondaryColor, border_opacity),
            width=1
        )

    card = Image.alpha_composite(card, details_overlay)
    draw = ImageDraw.Draw(card)

    details_y += 10
    spacing = 40

    # Enhanced fields with student info only
    print("Adding student details info...")
    fields = [
        ("Student ID: ", "KAA" + str(gen.data.get('id', '001'))),
        ("Name: ", f"{gen.data.get('Surname', 'N/A')} {gen.data.get('Firstname', 'N/A')}"),
        ("Trade:", f"{gen.data.get('Trade', 'Computer Science')}"),
    ]

    print("Adding enhanced styling on details...")
    for i, (label, value) in enumerate(fields):
        shadow_offset = 1
        draw.text((details_x + shadow_offset, details_y + shadow_offset),
                label, fill=(0, 0, 0, 100), font=font_medium)
        draw.text((details_x, details_y), label,
                fill="black", font=font_medium)

        draw.text((details_x + 200, details_y), value,
                fill="black", font=font_medium_bold)

        details_y += spacing

    # Add watermark and branding at bottom
    secure_color = (150, 150, 150)
    try:
        watermark_path = files(qure.assets).joinpath("avatar1.png")
        with watermark_path.open("rb") as f:
            watermark_logo = Image.open(f).convert("RGBA")

        small_logo = watermark_logo.resize((40, 47), Image.LANCZOS)
        if small_logo.mode != 'RGBA':
            small_logo = small_logo.convert('RGBA')

        card.paste(small_logo, (card_width - 120, card_height - 90), small_logo)

        powered_text = "© Powered by Kaascan"
        powered_width = draw.textlength(powered_text, font=font_smallest)
        draw.text((card_width - powered_width - 30, card_height - 40),
                powered_text, fill=(45, 104, 196), font=font_smallest)

    except IOError as e:
        print(f"Watermark load failed: {e}")

    # Add security text at bottom
    secure_text = "SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY"
    draw.text((-10, card_height - 20), secure_text, fill=secure_color, font=font_smallest)

    # Save both sides
    back_side = template_kaascan_only_back(gen, MprimaryColor, MsecondarColor)
    return gen.save_double_sided_card(card, back_side, cards_path, school_name, academic_year, card_template)


def template_kaascan_only_back(gen, MprimaryColor: int, MsecondarColor: int,) -> Image:
    """Designs the back side of Kaascan-only card."""
    print("Designing Kaascan-only card back side...")

    font_title_big, font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_new_fonts()

    card_width, card_height = 1012, 638
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Add subtle pattern to background
    print("Adding background pattern...")
    pattern_spacing = 32
    pattern_size = 8
    pattern_color = gen.lighten_color(primaryColor, 0.9)

    for x in range(0, card_width, pattern_spacing):
        for y in range(0, card_height, pattern_spacing):
            draw.ellipse([(x, y), (x + pattern_size, y + pattern_size)], fill=pattern_color)

    # Create curved header (approx 35% of card height + curve)
    header_height = int(card_height * 0.20)
    curve_depth = 30

    gradient_start = gen.lighten_color(primaryColor, 0.15)
    gradient_end = gen.darken_color(primaryColor, 0.25)

    # Draw curved header with gradient
    print("Drawing curved header with gradient...")

    # Draw the header line by line with curve
    for y in range(header_height + curve_depth):
        # Calculate gradient color for current y position
        gradient_ratio = y / (header_height + curve_depth)
        r = int(gradient_start[0] + (gradient_end[0] - gradient_start[0]) * gradient_ratio)
        g = int(gradient_start[1] + (gradient_end[1] - gradient_start[1]) * gradient_ratio)
        b = int(gradient_start[2] + (gradient_end[2] - gradient_start[2]) * gradient_ratio)
        current_color = (r, g, b)

        # Create curved bottom edge using sine wave
        if y >= header_height:
            # Only draw the curve part
            curve_progress = (y - header_height) / curve_depth
            for x in range(card_width):
                # Create smooth wave curve
                x_normalized = (x / card_width) * math.pi
                wave_height = math.sin(x_normalized) * curve_depth
                y_threshold = header_height + wave_height

                if y <= y_threshold:
                    draw.point((x, y), fill=current_color)
        else:
            # Draw full width line for header body
            draw.line([(0, y), (card_width, y)], fill=current_color)

    # Add decorative wave overlay at the bottom of header
    wave_color = gen.lighten_color(primaryColor, 0.25)
    for x in range(0, card_width, 2):
        x_normalized = (x / card_width) * math.pi * 2
        wave_y = header_height + int(math.sin(x_normalized) * 15) - 10
        draw.ellipse([(x-3, wave_y-3), (x+3, wave_y+3)], fill=wave_color)

    # Kaascan branding with enhanced typography
    print("Adding Kaascan branding text...")

    # Main KAASCAN title with shadow effect for depth
    brand_text = "KAASCAN"
    brand_text_width = draw.textlength(brand_text, font=font_title_big)
    brand_x = (card_width - brand_text_width) // 2
    brand_y = 30

    # Add subtle shadow/glow effect
    shadow_color = (0, 0, 0, 100)
    for offset in range(3, 0, -1):
        shadow_alpha = int(50 * (offset / 3))
        draw.text((brand_x + offset, brand_y + offset), brand_text,
                fill=(*shadow_color[:3], shadow_alpha), font=font_title_big)

    # Main text
    draw.text((brand_x, brand_y), brand_text, fill="white", font=font_title_big)

    slogan_text = "Digital Student Wallet"
    slogan_width = draw.textlength(slogan_text, font=font_regular_bold)
    slogan_x = (card_width - slogan_width) // 2
    slogan_y = 100

    # Add subtle background rectangle for slogan
    padding = 15
    slogan_bg_color = gen.lighten_color(primaryColor, 0.3)
    draw.rounded_rectangle(
        [slogan_x - padding, slogan_y - 5,
        slogan_x + slogan_width + padding, slogan_y + 35],
        radius=15,
        fill=slogan_bg_color
    )

    draw.text((slogan_x, slogan_y), slogan_text, fill="white", font=font_regular_bold)

    # Enhanced horizontal line with gradient dots
    line_y = header_height + 50
    dot_radius = 12
    dot_positions = [60, 238, 510, 782, 952]

    # Draw gradient line
    for x in range(20, card_width - 20):
        gradient_pos = (x - 20) / (card_width - 40)
        line_color = (
            int(primaryColor[0] * (1 - gradient_pos) + secondaryColor[0] * gradient_pos),
            int(primaryColor[1] * (1 - gradient_pos) + secondaryColor[1] * gradient_pos),
            int(primaryColor[2] * (1 - gradient_pos) + secondaryColor[2] * gradient_pos)
        )
        draw.line([(x, line_y), (x, line_y + 5)], fill=line_color)

    # Draw decorative dots with glow effect
    for x_pos in dot_positions:
        # Outer glow
        for r in range(dot_radius + 8, dot_radius, -2):
            glow_alpha = int(100 * (1 - (r - dot_radius) / 8))
            glow_color = (*primaryColor, glow_alpha)
            draw.ellipse([(x_pos - r, line_y - r + 2),
                        (x_pos + r, line_y + r + 2)],
                        fill=glow_color)

        # Main dot with gradient
        draw.ellipse([(x_pos - dot_radius, line_y - dot_radius + 2),
                    (x_pos + dot_radius, line_y + dot_radius + 2)],
                    fill=primaryColor)

        # Highlight for 3D effect
        highlight_color = gen.lighten_color(primaryColor, 0.4)
        draw.ellipse([(x_pos - dot_radius//2, line_y - dot_radius//2 + 2),
                    (x_pos + dot_radius//2, line_y + dot_radius//2 + 2)],
                    fill=highlight_color)

    # Add QR code on the left side
    print("Adding QR code...")
    try:
        import qrcode
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.colormasks import RadialGradiantColorMask

        student_id = gen.data.get('student_id', '00000000-0000-0000-0000-000000000000')
        qr_data = f"{student_id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask(
                back_color=(255, 255, 255),
                center_color=secondaryColor,
                edge_color=primaryColor,
            )
        )

        qr_size = (360, 360)
        qr_img = qr_img.resize(qr_size, Image.LANCZOS)

        qr_position = (120, header_height + 110)

        draw.rounded_rectangle(
            [qr_position[0]-10, qr_position[1]-10,
            qr_position[0]+qr_size[0]+10, qr_position[1]+qr_size[1]+10],
            radius=15, fill=(255, 255, 255, 220)
        )

        card.paste(qr_img, qr_position)

        scan_text = "SCAN ME"
        scan_width = draw.textlength(scan_text, font=font_medium_bold)
        scan_x = qr_position[0] + (qr_size[0] - scan_width) // 2
        draw.text((scan_x, qr_position[1] - 30), scan_text, fill=secondaryColor, font=font_medium_bold)

    except Exception as e:
        print(f"Error generating QR code: {e}")

    # Terms and conditions for Kaascan
    terms_x = card_width - 450
    terms_y = header_height + 100
    terms_text = [
        "TERMS & CONDITIONS:",
        "1. This card is property of Kaascan Ltd.",
        "2. If found, please contact Kaascan support.",
        "3. This card must be carried at all times.",
        "4. This card is not transferable.",
        "5. Replacement fee applies for lost cards.",
        "6. Valid for digital wallet transactions only."
    ]

    for i, line in enumerate(terms_text):
        if i == 0:
            draw.text((terms_x, terms_y), line, fill=secondaryColor, font=font_small_bold)
        else:
            draw.text((terms_x, terms_y), line, fill="black", font=font_small)
        terms_y += 25

    # Kaascan contact information
    contact_y = terms_y + 20
    draw.text((terms_x, contact_y), "CONTACT INFORMATION:", fill=secondaryColor, font=font_small_bold)
    contact_y += 25

    contact_info = [
        "Phone: +250 792 890 883",
        "Email: info@kaascan.com",
        "Website: www.kaascan.com",
        "Address: KK 15 Rd, Kicukiro, Kigali, Rwanda"
    ]

    for line in contact_info:
        draw.text((terms_x, contact_y), line, fill="black", font=font_small)
        contact_y += 20

    # Add watermark at bottom
    try:
        watermark_path = files(qure.assets).joinpath("avatar1.png")
        with watermark_path.open("rb") as f:
            watermark_logo = Image.open(f).convert("RGBA")

        small_logo = watermark_logo.resize((40, 47), Image.LANCZOS)
        if small_logo.mode != 'RGBA':
            small_logo = small_logo.convert('RGBA')

        card.paste(small_logo, (card_width - 120, card_height - 90), small_logo)

        powered_text = "© Powered by Kaascan"
        powered_width = draw.textlength(powered_text, font=font_smallest)
        draw.text((card_width - powered_width - 30, card_height - 40),
                powered_text, fill=(45, 104, 196), font=font_smallest)

    except IOError:
        pass

    # Security text
    secure_color = (150, 150, 150)
    secure_text = "SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY"
    draw.text((-10, card_height - 20), secure_text, fill=secure_color, font=font_smallest)

    return card
