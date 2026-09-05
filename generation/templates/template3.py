from PIL import Image, ImageDraw, ImageFont


def template3(gen, card_template: str, MprimaryColor: int, MsecondarColor: int, school_logo: str, school_name: str, school_slogan: str, academic_year: str, expiration_date: str, student_photo: str, cards_path: str) -> str:
    """Designs a landscape-oriented student ID card with a modern, asymmetrical layout."""
    print("Designing card with template 3 (landscape)...")

    # # Load fonts and assign them to variables
    # font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold = gen.load_fonts()

    # Card dimensions (landscape)
    card_width, card_height = 800, 500
    card = Image.new("RGB", (card_width, card_height), "white")
    draw = ImageDraw.Draw(card)

    primaryColor = MprimaryColor
    secondaryColor = MsecondarColor

    # Add a diagonal accent (modern design element)
    print("Adding diagonal accent...")
    draw.polygon([(0, 0), (card_width // 2, 0), (0, card_height // 2)], fill=primaryColor)
    draw.polygon([(card_width, card_height), (card_width // 2, card_height), (card_width, card_height // 2)], fill=secondaryColor)

    # Load perfect fonts
    print("Loading fonts...")
    try:
        # Debug: Print the font paths
        font_paths = {
            "Montserrat-Bold": "fonts/Montserrat/static/Montserrat-Bold.ttf",
            "Montserrat-Regular": "fonts/Montserrat/static/Montserrat-Regular.ttf",
            "OpenSans-Regular": "fonts/OpenSans/static/OpenSans-Regular.ttf",
            "OpenSans-Bold": "fonts/OpenSans/static/OpenSans-Bold.ttf",
            "Raleway-Medium": "fonts/Raleway/static/Raleway-Medium.ttf",
            "SourceCodePro-Regular": "fonts/Source_Code_Pro/static/SourceCodePro-Regular.ttf",
            "Grechen-Fuemen": "fonts/Grechen_Fuemen/GrechenFuemen-Regular.ttf",
        }

        for font_name, font_path in font_paths.items():
            print(f"Loading {font_name} from: {font_path}")

        # Load fonts
        font_header = ImageFont.truetype(font_paths["Montserrat-Bold"], 28)
        font_body = ImageFont.truetype(font_paths["OpenSans-Regular"], 21)
        font_Regular = ImageFont.truetype(font_paths["Montserrat-Regular"], 21)
        font_body_bold = ImageFont.truetype(font_paths["OpenSans-Bold"], 21)
        font_accent = ImageFont.truetype(font_paths["Raleway-Medium"], 18)
        font_mono = ImageFont.truetype(font_paths["SourceCodePro-Regular"], 18)
        font_stylish = ImageFont.truetype(font_paths["Grechen-Fuemen"], 18)
        font_stylish_regular = ImageFont.truetype(font_paths["Grechen-Fuemen"], 25)
    except IOError as e:
        print(f"Error loading fonts: {e}. Using default fonts...")
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_body_bold = ImageFont.load_default()
        font_accent = ImageFont.load_default()
        font_mono = ImageFont.load_default()
        font_stylish = ImageFont.load_default()
        font_stylish_regular = ImageFont.load_default()

    # School logo
    print("Adding school logo...")
    logo = Image.open(school_logo).resize((100, 100), Image.LANCZOS)
    logo_position = (30, 30)

    # Add school logo to the top-left corner
    try:
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        card.paste(logo, logo_position, logo)
    except IOError:
        print("School logo not found; skipping logo placement.")

    # School name and academic year
    print("Adding school name and academic year...")
    school_name_position = (150, 40)
    draw.text(school_name_position, school_name, fill=secondaryColor, font=font_header)

    academic_year_position = (150, 80)
    draw.text(academic_year_position, academic_year, fill=secondaryColor, font=font_body_bold)

    # Student photo
    print("Adding student photo...")
    photo_position = (card_width - 250, 20)
    try:
        photo_size = (200, 250)
        with Image.open(student_photo) as photo:
            photo = photo.resize(photo_size, Image.LANCZOS)
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=30, fill=255)
            card.paste(photo, photo_position, mask)
    except IOError:
        print("Student photo not found; skipping photo placement.")
        photo_size = (200, 200)
        with Image.open(school_logo) as photo:
            if photo.mode != 'RGBA':
                photo = logo.convert('RGBA')
            photo = photo.resize(photo_size, Image.LANCZOS)
            mask = Image.new("L", photo_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle([0, 0, *photo_size], radius=30, fill=255)
            card.paste(photo, photo_position, photo)

    # Student details (icon-style layout)
    print("Adding student details...")
    details_x = 50
    details_y = 250
    spacing = 35
    fields = [
        ("Name", gen.data.get('Surname', 'N/A') + " " + gen.data.get('Firstname', 'N/A')),
        ("Sex", gen.data.get('Gender', 'N/A')),
        ("Age", gen.data.get('Age', 'N/A')),
        ("Option", gen.data.get('Trade', 'N/A')),
        ("Valid up to", expiration_date),
    ]

    # Add student details text
    for label, value in fields:
        draw.text((details_x, details_y), label + ":", fill=primaryColor, font=font_body_bold)
        draw.text((details_x + draw.textlength(label + ":", font=font_body_bold) + 10, details_y), value, fill=primaryColor, font=font_Regular)
        details_y += spacing

    # Slogan area (minimalist, bottom-right corner)
    print("Adding slogan area...")
    slogan_text = school_slogan if school_slogan else "Your School Slogan Here"
    slogan_x = card_width - 400  # Right-aligned
    slogan_y = card_height - 60
    draw.text((slogan_x, slogan_y), slogan_text, fill=primaryColor, font=font_stylish_regular)

    # Add a decorative line above the slogan
    draw.line([(slogan_x, slogan_y + 10), (slogan_x + (draw.textlength(slogan_text, font=font_stylish_regular) + 10), slogan_y + 10)], fill=primaryColor, width=3,)

    # Save the card
    print("Saving card...")
    return gen.save_card(card, cards_path, school_name, academic_year, card_template)
