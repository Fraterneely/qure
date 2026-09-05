from importlib.resources import files
import qure.assets
import qure.fonts
from PIL import Image, ImageDraw, ImageFont


def _nfc_icon(fg, bg=None, size=240, supersample=4):
    """Draws a small NFC / contactless glyph - a wifi-style radio-wave icon
    turned on its side. With `bg` set, it sits on an opaque circular backing
    plate (used inside the QR code, so it reads cleanly against the modules);
    with `bg=None` it's just the glyph on a transparent background."""
    hi = size * supersample
    img = Image.new("RGBA", (hi, hi), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if bg is not None:
        d.ellipse([0, 0, hi, hi], fill=(*bg, 255))

    cx, cy = hi * 0.36, hi * 0.5
    dot_r = hi * 0.07
    d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=(*fg, 255))

    stroke = max(1, int(hi * 0.055))
    for r in (hi * 0.20, hi * 0.315, hi * 0.43):
        bbox = [cx - r, cy - r, cx + r, cy + r]
        d.arc(bbox, start=-42, end=42, fill=(*fg, 255), width=stroke)

    return img.resize((size, size), Image.LANCZOS)


def template9(gen, card_template: str, MprimaryColor: int,
    MsecondarColor: int, school_logo: str, school_stamp: str, school_name: str, school_slogan: str,
    academic_year: str, expiration_date: str, student_photo: str, school_phone: str, school_email: str,
    location: str, website: str, principal_name: str, principal_phone: str, principal_mail: str, principal_signature: str, cards_path: str) -> str:
    """Designs a student ID card with the QR code on the front, sized for reliable
    phone-camera scanning. The photo and detail fields stack in one left column so the
    QR gets a full-height column of its own on the right; the back carries nothing
    student-specific, so it comes out identical for every card this school prints."""
    print("Designing card with template 9...")

    # Load fonts and assign them to variables
    font_title_big, font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_new_fonts()

    # Card dimensions (3.375 x 2.125 inches at 300 DPI - ISO 7810 ID-1)
    card_width, card_height = 1012, 638
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Background pattern - identical to Template 6
    print("Adding background pattern...")
    pattern_spacing = 32
    pattern_size = 8
    pattern_color = gen.lighten_color(primaryColor, 0.9)
    for x in range(0, card_width, pattern_spacing):
        for y in range(0, card_height, pattern_spacing):
            draw.ellipse([(x, y), (x + pattern_size, y + pattern_size)], fill=pattern_color)

    # Header - identical to Template 6
    header_height = int(card_height * 0.3)
    gradient_start = gen.lighten_color(primaryColor, 0.2)
    gradient_end = gen.darken_color(primaryColor, 0.2)
    for y in range(header_height):
        r = gradient_start[0] + (gradient_end[0] - gradient_start[0]) * y // header_height
        g = gradient_start[1] + (gradient_end[1] - gradient_start[1]) * y // header_height
        b = gradient_start[2] + (gradient_end[2] - gradient_start[2]) * y // header_height
        draw.line([(0, y), (card_width, y)], fill=(r, g, b))

    # Divider line with dots
    line_y = header_height + 20
    dot_radius = 10
    dot_positions = [60, 238, 510, 782, 952]
    draw.line([(20, line_y), (card_width - 20, line_y)], fill=secondaryColor, width=5)
    for x_pos in dot_positions:
        draw.ellipse([(x_pos - dot_radius, line_y - dot_radius),
                      (x_pos + dot_radius, line_y + dot_radius)], fill=secondaryColor)

    # School name and slogan (centered in header)
    print("Adding school name and slogan...")
    school_name_width = draw.textlength(school_name, font=font_title)
    school_slogan_width = draw.textlength(school_slogan, font=font_slogan_regular)
    draw.text(((card_width - school_name_width) // 2, 40), school_name, fill="white", font=font_title)
    draw.text(((card_width - school_slogan_width) // 2, 90), school_slogan, fill="white", font=font_slogan_regular)

    # School logo (right side of header)
    print("Adding school logo...")
    try:
        logo = Image.open(school_logo).resize((140, 140), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (45, 25)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    body_top = 250
    body_bottom = card_height - 75

    # Left column: student photo stacked above the detail fields
    print("Adding student photo...")
    left_x, left_width = 60, 480
    photo_size = (160, 180)
    photo_position = (left_x, body_top)
    try:
        with Image.open(student_photo) as photo:
            bg = Image.new('RGBA', photo_size, 'white')
            photo = photo.resize(photo_size, Image.LANCZOS)
            if photo.mode == 'RGBA':
                bg.paste(photo, (0, 0), photo)
            else:
                bg.paste(photo, (0, 0))
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=18, fill=255)
            card.paste(bg, photo_position, mask)
    except IOError:
        print("Student photo not found; skipping photo placement.")
        with Image.open(school_logo) as photo:
            bg = Image.new('RGBA', photo_size, 'white')
            if photo.mode != 'RGBA':
                photo = photo.convert('RGBA')
            photo = photo.resize(photo_size, Image.LANCZOS)
            bg.paste(photo, (0, 0), photo)
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=18, fill=255)
            card.paste(bg, photo_position, mask)

    # Student details, stacked below the photo - the same gradient/glow/shadow
    # treatment as the details box in Template 6 (only the font size is smaller,
    # to fit this narrower column)
    print("Adding student details...")
    try:
        detail_font = ImageFont.truetype(str(files(qure.fonts).joinpath("Montserrat/static/Montserrat-Medium.ttf")), 15)
        detail_font_bold = ImageFont.truetype(str(files(qure.fonts).joinpath("Montserrat/static/Montserrat-Bold.ttf")), 15)
    except Exception:
        detail_font, detail_font_bold = font_small, font_small_bold

    details_x = left_x + 30
    details_y = photo_position[1] + photo_size[1] + 15

    if card.mode != 'RGBA':
        card = card.convert('RGBA')

    details_overlay = Image.new('RGBA', card.size, (0, 0, 0, 0))
    details_draw = ImageDraw.Draw(details_overlay)

    details_rect = [left_x, details_y, left_x + left_width, body_bottom]
    for y in range(details_rect[1], details_rect[3]):
        opacity = int(40 + (y - details_rect[1]) * 0.1)
        opacity = min(opacity, 80)
        r, g, b = secondaryColor
        details_draw.line([(details_rect[0], y), (details_rect[2], y)], fill=(r, g, b, opacity))

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
    spacing = (body_bottom - details_y - 10) / 5

    fields = [
        ("Student ID: ", "KAA" + str(gen.data.get('id', '001'))),
        ("Name: ", f"{gen.data.get('Surname', 'N/A')} {gen.data.get('Firstname', 'N/A')}"),
        ("Trade:", f"{gen.data.get('Trade', 'N/A')}"),
        ("Level:", f"{gen.data.get('Class', 'N/A')}"),
        ("Valid Until:", expiration_date),
    ]
    for label, value in fields:
        shadow_offset = 1
        draw.text((details_x + shadow_offset, details_y + shadow_offset), label, fill=(0, 0, 0, 100), font=detail_font)
        draw.text((details_x, details_y), label, fill="black", font=detail_font)
        draw.text((details_x + 130, details_y), value, fill="black", font=detail_font_bold)
        details_y += spacing

    # Right column: the QR code, sized to fill the available height, framed by a
    # thin border that sits just off the code (not touching it), with an NFC
    # glyph embedded in the QR's own center (ERROR_CORRECT_H leaves enough
    # redundancy for that without hurting scannability)
    print("Adding QR code...")
    right_x = left_x + left_width + 40
    right_width = card_width - right_x - 60
    border_gap = 5
    border_width = 10
    qr_target = min(right_width - 20, body_bottom - body_top - 20) - 2 * (border_gap + border_width)
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
            ),
        )
        qr_img = qr_img.resize((qr_target, qr_target), Image.LANCZOS)

        qr_x = right_x + (right_width - qr_target) // 2
        qr_y = body_top + (body_bottom - body_top - qr_target) // 2
        card.paste(qr_img, (qr_x, qr_y))

        # border framing the QR, offset just enough that it never touches it
        draw.rounded_rectangle(
            [qr_x - border_gap, qr_y - border_gap, qr_x + qr_target + border_gap, qr_y + qr_target + border_gap],
            radius=10, outline=primaryColor, width=border_width
        )
    except ImportError:
        print("QR code libraries not installed; skipping QR code generation")
        qr_x = right_x + (right_width - qr_target) // 2
        qr_y = body_top + (body_bottom - body_top - qr_target) // 2
        draw.rounded_rectangle(
            [qr_x, qr_y, qr_x + qr_target, qr_y + qr_target],
            radius=16, fill="white", outline=primaryColor, width=3
        )
        draw.text((qr_x + qr_target // 2 - 40, qr_y + qr_target // 2), "QR CODE", fill=primaryColor, font=font_medium_bold)
    except Exception as e:
        print(f"Error generating QR code: {e}")

    # NFC glyph
    try:
        qr_left_edge = qr_x - border_gap - border_width
    except NameError:
        qr_left_edge = right_x
    photo_right = photo_position[0] + photo_size[0]
    mid_icon_size = max(60, min(120, (qr_left_edge - photo_right) - 40))
    mid_icon = _nfc_icon(fg=primaryColor, size=mid_icon_size)
    mid_x = (photo_right + qr_left_edge) // 2
    mid_y = photo_position[1] + photo_size[1] // 2
    card.paste(mid_icon, (mid_x - mid_icon_size // 2, mid_y - mid_icon_size // 2), mid_icon)

    # Footer branding
    # Add small watermark icons at bottom corners
    secure_color = (150, 150, 150)
    try:
        watermark_path = files(qure.assets).joinpath("avatar1.png")
        with watermark_path.open("rb") as f:
            watermark_logo = Image.open(f).convert("RGBA")

        small_logo = watermark_logo.resize((60, 60), Image.LANCZOS)
        if small_logo.mode != 'RGBA':
            small_logo = small_logo.convert('RGBA')

        # Text position/width is computed first so the logo above it can be
        # centered on the text's actual rendered width, not a fixed offset
        powered_text = "© Powered by Kaascan"
        powered_width = draw.textlength(powered_text, font=font_smallest)
        powered_x = card_width - powered_width - 30
        powered_y = card_height - 40

        logo_x = int(powered_x + (powered_width - small_logo.width) / 2)
        logo_y = card_height - 90
        card.paste(small_logo, (logo_x, logo_y), small_logo)

        draw.text((powered_x, powered_y), powered_text, fill=(0, 34, 255), font=font_smallest)

    except IOError as e:
        print(f"Watermark load failed: {e}")

    secure_text = "SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY"
    draw.text((-10, card_height - 20), secure_text, fill=secure_color, font=font_smallest)

    # Save both sides - the back carries nothing student-specific, so it is identical
    # for every card this school prints
    back_side = template9_back(gen, card_template, MprimaryColor, MsecondarColor,
                school_logo, school_stamp, school_name, school_slogan, school_phone, school_email,
                location, website, principal_name, principal_phone,
                principal_mail, principal_signature)
    return gen.save_double_sided_card(card, back_side, cards_path, school_name, academic_year, card_template)


def template9_back(gen, card_template: str, MprimaryColor: int, MsecondarColor: int,
                  school_logo: str, school_stamp: str, school_name: str, school_slogan: str, school_phone: str, school_email: str,
                  location: str, website: str, principal_name: str, principal_phone: str,
                  principal_mail: str, principal_signature: str) -> Image:
    """Designs the back side of template 9. Nothing here is student-specific, so this
    image comes out identical for every card printed for this school."""
    print("Designing card back side with template 9...")

    font_title_big, font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_new_fonts()

    card_width, card_height = 1012, 638
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Background pattern - identical to Template 6
    print("Adding background pattern...")
    pattern_spacing = 32
    pattern_size = 8
    pattern_color = gen.lighten_color(primaryColor, 0.9)
    for x in range(0, card_width, pattern_spacing):
        for y in range(0, card_height, pattern_spacing):
            draw.ellipse([(x, y), (x + pattern_size, y + pattern_size)], fill=pattern_color)

    # Header - identical to Template 6's back
    header_height = int(card_height * 0.3)
    gradient_start = gen.lighten_color(primaryColor, 0.2)
    gradient_end = gen.darken_color(primaryColor, 0.2)
    for y in range(header_height):
        r = gradient_start[0] + (gradient_end[0] - gradient_start[0]) * y // header_height
        g = gradient_start[1] + (gradient_end[1] - gradient_start[1]) * y // header_height
        b = gradient_start[2] + (gradient_end[2] - gradient_start[2]) * y // header_height
        draw.line([(0, y), (card_width, y)], fill=(r, g, b))

    line_y = header_height + 20
    dot_radius = 10
    dot_positions = [60, 238, 510, 782, 952]
    draw.line([(20, line_y), (card_width - 20, line_y)], fill=secondaryColor, width=5)
    for x_pos in dot_positions:
        draw.ellipse([(x_pos - dot_radius, line_y - dot_radius),
                      (x_pos + dot_radius, line_y + dot_radius)], fill=secondaryColor)

    school_name_width = draw.textlength(school_name, font=font_title)
    school_slogan_width = draw.textlength(school_slogan, font=font_slogan_regular)
    draw.text(((card_width - school_name_width) // 2, 40), school_name, fill="white", font=font_title)
    draw.text(((card_width - school_slogan_width) // 2, 90), school_slogan, fill="white", font=font_slogan_regular)

    try:
        logo = Image.open(school_logo).resize((140, 140), Image.LANCZOS)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_position = (45, 25)
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    body_top = line_y + 40
    body_bottom = card_height - 60

    # Left zone: a school-monogram watermark fills the space the QR used to take on
    # the back. This is the only thing that replaces it, so the zone stays identical
    # across every card for this school.
    print("Adding watermark...")
    left_x, left_width = 60, 400
    watermark_area = [left_x, body_top, left_x + left_width, body_bottom]
    draw.rounded_rectangle(watermark_area, fill=gen.lighten_color(primaryColor, 0.92), radius=14)

    dot_spacing = 22
    dot_col = gen.lighten_color(primaryColor, 0.8)
    for x in range(left_x + 10, left_x + left_width - 10, dot_spacing):
        for y in range(body_top + 10, body_bottom - 10, dot_spacing):
            draw.ellipse([x, y, x + 2, y + 2], fill=dot_col)

    try:
        name_words = school_name.split()
        initials = (name_words[0][0] + name_words[-1][0]).upper() if len(name_words) > 1 else (name_words[0][:2].upper() if name_words else "ID")
        watermark_font = ImageFont.truetype(str(files(qure.fonts).joinpath("Montserrat/static/Montserrat-Bold.ttf")), 190)
        wm_color = gen.lighten_color(primaryColor, 0.55)
        wm_layer = Image.new('RGBA', (left_width, body_bottom - body_top), (0, 0, 0, 0))
        wm_draw = ImageDraw.Draw(wm_layer)
        wm_width = wm_draw.textlength(initials, font=watermark_font)
        wm_draw.text(((left_width - wm_width) // 2, (wm_layer.height - 190) // 2), initials, fill=(*wm_color, 255), font=watermark_font)
        wm_layer = wm_layer.rotate(8, resample=Image.BICUBIC)
        card.paste(wm_layer, (left_x, body_top), wm_layer)
    except Exception as e:
        print(f"Error drawing watermark monogram: {e}")

    # Right zone: rules and contact information - the same for every card
    print("Adding terms and contact information...")
    terms_x = left_x + left_width + 40
    terms_y = body_top
    terms_text = [
        f"1. This card is the property of {school_name}.",
        "2. If found, please return to the school office or kaascan office.",
        "3. This card must be carried at all times.",
        "4. This card is not transferable.",
        "5. Replacement fee applies for lost cards.",
    ]
    for line in terms_text:
        draw.text((terms_x, terms_y), line, fill="black", font=font_small)
        terms_y += 25

    contact_y = terms_y + 20
    draw.text((terms_x, contact_y), "CONTACT INFORMATION:", fill=primaryColor, font=font_small_bold)
    contact_y += 25
    contact_info = [
        f"Phone:  {school_phone}",
        f"Email:  {school_email}",
        f"Website: {website}",
        f"Address: {location}",
    ]
    for line in contact_info:
        draw.text((terms_x, contact_y), line, fill="black", font=font_small)
        contact_y += 20

    # Signature and stamp
    print("Adding principal signature and school stamp...")
    sig_line_start = terms_x
    sig_line_end = terms_x + 160
    # Anchored off contact_y (where the contact block actually finished) rather
    # than a fixed offset from the bottom, so this never overlaps the text above
    # it regardless of how long the contact details run.
    sig_y = contact_y + 55
    draw.line([(sig_line_start, sig_y), (sig_line_end, sig_y)], fill=primaryColor, width=2)
    try:
        signature = Image.open(principal_signature).resize((110, 35), Image.LANCZOS)
        if signature.mode != 'RGBA':
            signature = signature.convert('RGBA')
        card.paste(signature, (sig_line_start, sig_y - 38), signature)
    except IOError:
        print("Principal signature not found; skipping signature placement.")

    name_width = draw.textlength(principal_name, font=font_small_bold)
    draw.text((sig_line_start + (sig_line_end - sig_line_start - name_width) // 2, sig_y + 8), principal_name, fill="black", font=font_small_bold)

    try:
        stamp = Image.open(school_stamp).resize((60, 60), Image.LANCZOS)
        if stamp.mode != 'RGBA':
            stamp = stamp.convert('RGBA')
        card.paste(stamp, (sig_line_end + 40, sig_y - 28), stamp)
    except IOError:
        print("School stamp not found; skipping stamp placement.")

    # Footer branding
    # Add small watermark icons at bottom corners
    secure_color = (150, 150, 150)
    try:
        watermark_path = files(qure.assets).joinpath("avatar1.png")
        with watermark_path.open("rb") as f:
            watermark_logo = Image.open(f).convert("RGBA")

        small_logo = watermark_logo.resize((60, 60), Image.LANCZOS)
        if small_logo.mode != 'RGBA':
            small_logo = small_logo.convert('RGBA')

        # Text position/width is computed first so the logo above it can be
        # centered on the text's actual rendered width, not a fixed offset
        powered_text = "© Powered by Kaascan"
        powered_width = draw.textlength(powered_text, font=font_smallest)
        powered_x = card_width - powered_width - 30
        powered_y = card_height - 40

        logo_x = int(powered_x + (powered_width - small_logo.width) / 2)
        logo_y = card_height - 90
        card.paste(small_logo, (logo_x, logo_y), small_logo)

        draw.text((powered_x, powered_y), powered_text, fill=(0, 34, 255), font=font_smallest)

    except IOError as e:
        print(f"Watermark load failed: {e}")

    secure_text = "SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY • SECURE DOCUMENT • DO NOT COPY"
    draw.text((-10, card_height - 20), secure_text, fill=secure_color, font=font_smallest)

    return card
