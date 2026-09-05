import os
import logging
import random
from importlib.resources import files
import qure.assets
import qure.fonts
from PIL import Image, ImageDraw, ImageFont

from .templates import (
    TEMPLATES,
    templates,
    template1,
    template2,
    template3,
    template4,
    template5,
    template6,
    template9,
    template_kaascan_only,
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CGenerator:
    def __init__(self, data: dict):
        if data is None:
            raise ValueError("Data cannot be None")
        self.data = data
        self.student_id = (data.get('student_id', 'Unknown'))
        self.student_name = (data.get('Firstname', 'Unknown') + " " + data.get('Surname', 'Unknown'))
        logging.debug(f"Initialized CardGenerator for student: {self.student_name}, and ID: {self.student_id}")

        # Get assets path from environment variable or use default
        self.assets_path = os.environ.get('QURE_ASSETS_PATH', None)
        if not self.assets_path:
            # Fallback to relative path
            self.assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")

        logging.debug(f"Using assets path: {self.assets_path}")

        self.fonts_path = os.environ.get('QURE_FONTS_PATH', None)
        if not self.fonts_path:
            # Fallback to relative path
            self.fonts_path = os.path.join(os.path.dirname(__file__), "..", "fonts")

        logging.debug(f"Using fonts path: {self.fonts_path}")

    def create_student_card(
        self,
        template: str,
        primaryColor: int,
        secondarColor: int,
        student_photo: str,
        school_logo: str,
        school_stamp: str,
        school_name: str,
        school_slogan: str,
        academic_year: str,
        expiration_date: str,
        school_phone: str,
        school_email: str,
        location: str,
        website: str,
        principal_name: str,
        principal_phone: str,
        principal_mail: str,
        principal_signature: str,
        cards_path: str = None
        ) -> str:

        print(f'Starting request to create_student_card....')

        # Templates registered with `templates` (see generation/templates/registry.py)
        # are dispatched generically - no elif branch needed to add one. Only
        # "Template 1" and "Kaascan Only" have been migrated so far; the rest
        # still fall through to the hardcoded chain below.
        if template in templates.list():
            config = {
                "primaryColor": primaryColor,
                "secondarColor": secondarColor,
                "student_photo": student_photo,
                "school_logo": school_logo,
                "school_stamp": school_stamp,
                "school_name": school_name,
                "school_slogan": school_slogan,
                "academic_year": academic_year,
                "expiration_date": expiration_date,
                "school_phone": school_phone,
                "school_email": school_email,
                "location": location,
                "website": website,
                "principal_name": principal_name,
                "principal_phone": principal_phone,
                "principal_mail": principal_mail,
                "principal_signature": principal_signature,
            }
            return templates.get(template).render(self, config, cards_path)

        if template == "Template 2":
            return template2(
                self, template, primaryColor, secondarColor,
                school_logo, school_stamp, school_name, school_slogan, academic_year,
                expiration_date, student_photo, school_phone, school_email, location, website, principal_name,
                principal_phone, principal_mail, principal_signature, cards_path
            )
        elif template == "Template 3":
            return template3(self, template, primaryColor, secondarColor, school_logo, school_name, school_slogan, academic_year, expiration_date, student_photo, cards_path)
        elif template == "Template 4":
            return template4(
                self, template, primaryColor, secondarColor,
                school_logo, school_stamp, school_name, school_slogan,
                academic_year, expiration_date, student_photo,
                school_phone, school_email, location, website,
                principal_name, principal_phone, principal_mail, principal_signature,
                cards_path
            )
        elif template == "Template 5":
            return template5(
                self, template, primaryColor, secondarColor,
                school_logo, school_stamp, school_name, school_slogan,
                academic_year, expiration_date, student_photo,
                school_phone, school_email, location, website,
                principal_name, principal_phone, principal_mail, principal_signature,
                cards_path
            )
        elif template == "Template 6":
            return template6(
                self, template, primaryColor, secondarColor,
                school_logo, school_stamp, school_name, school_slogan,
                academic_year, expiration_date, student_photo,
                school_phone, school_email, location, website,
                principal_name, principal_phone, principal_mail, principal_signature,
                cards_path
            )
        elif template == "Template 9":
            return template9(
                self, template, primaryColor, secondarColor,
                school_logo, school_stamp, school_name, school_slogan,
                academic_year, expiration_date, student_photo,
                school_phone, school_email, location, website,
                principal_name, principal_phone, principal_mail, principal_signature,
                cards_path
            )
        # For non-partnered schools
        # card_path = self.template_kaascan_only(
        #     card_template="kaascan_only",
        #     MprimaryColor=(45, 104, 196),  # Your brand color
        #     MsecondarColor=(255, 215, 0),   # Gold accent
        #     academic_year="2024-2025",
        #     expiration_date="Dec 31, 2025",
        #     student_photo="path/to/photo.jpg",
        #     cards_path="output/path/"
        # )
        else:
            raise ValueError("Invalid template name")

    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> list:
        """Helper function to wrap text."""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = font.getlength(word + " ")
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def generate_qr_code(self, data: str, size: int) -> Image:
        """Generate QR code image."""
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image = qr_image.resize((size, size), Image.LANCZOS)
        return qr_image

    def load_fonts(self):
        # Get the absolute path to the fonts directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fonts_dir = self.fonts_path
        print("Fonts directory:", fonts_dir)

        # Define font paths using importlib.resources
        try:
            font_paths = {
                "Montserrat-Bold": files(qure.fonts).joinpath("Montserrat/static/Montserrat-Bold.ttf"),
                "Roboto-Bold": files(qure.fonts).joinpath("Roboto/static/Roboto-Bold.ttf"),
                "Roboto-Regular": files(qure.fonts).joinpath("Roboto/static/Roboto-Regular.ttf"),
                "OpenSans-Regular": files(qure.fonts).joinpath("OpenSans/static/OpenSans-Regular.ttf"),
                "OpenSans-Bold": files(qure.fonts).joinpath("OpenSans/static/OpenSans-Bold.ttf"),
                "Montserrat-Medium": files(qure.fonts).joinpath("Montserrat/static/Montserrat-Medium.ttf"),
                "Pacifico-Medium": files(qure.fonts).joinpath("Pacifico/Pacifico-Regular.ttf"),
            }

            # Convert Path objects to strings for compatibility with PIL
            font_paths = {name: str(path) for name, path in font_paths.items()}
        except Exception as e:
            print(f"Error accessing font resources: {e}. Falling back to file paths...")
            # Fallback to traditional path joining if importlib approach fails
            font_paths = {
                "Montserrat-Bold": os.path.join(fonts_dir, "Montserrat", "static", "Montserrat-Bold.ttf"),
                "Roboto-Bold": os.path.join(fonts_dir, "Roboto", "static", "Roboto-Bold.ttf"),
                "Roboto-Regular": os.path.join(fonts_dir, "Roboto", "static", "Roboto-Regular.ttf"),
                "OpenSans-Regular": os.path.join(fonts_dir, "OpenSans", "static", "OpenSans-Regular.ttf"),
                "OpenSans-Bold": os.path.join(fonts_dir, "OpenSans", "static", "OpenSans-Bold.ttf"),
                "Montserrat-Medium": os.path.join(fonts_dir, "Montserrat", "static", "Montserrat-Medium.ttf"),
                "Pacifico-Medium": os.path.join(fonts_dir, "Pacifico", "Pacifico-Regular.ttf"),
            }

        # Print the paths for debugging
        for font_name, font_path in font_paths.items():
            print(f"Looking for {font_name} at: {font_path}")
            if not os.path.exists(font_path):
                print(f"WARNING: Font file not found: {font_path}")

        # Load fonts with error handling
        print("Loading fonts...")
        try:
            font_title_big = ImageFont.truetype(font_paths["Montserrat-Bold"], 32)
            font_title = ImageFont.truetype(font_paths["Montserrat-Bold"], 24)
            font_min_title = ImageFont.truetype(font_paths["OpenSans-Bold"], 18)
            font_bold = ImageFont.truetype(font_paths["Roboto-Bold"], 24)
            font_regular = ImageFont.truetype(font_paths["OpenSans-Regular"], 16)
            font_regular_bold = ImageFont.truetype(font_paths["OpenSans-Bold"], 16)
            font_small = ImageFont.truetype(font_paths["Roboto-Regular"], 11)
            font_small_bold = ImageFont.truetype(font_paths["Roboto-Bold"], 13)
            font_smallest = ImageFont.truetype(font_paths["Roboto-Bold"], 6)
            font_large = ImageFont.truetype(font_paths["Montserrat-Medium"], 28)
            font_medium = ImageFont.truetype(font_paths["Montserrat-Medium"], 13)
            font_medium_bold = ImageFont.truetype(font_paths["Montserrat-Bold"], 13)
            font_slogan_regular = ImageFont.truetype(font_paths["Pacifico-Medium"], 13)
            font_slogan_small = ImageFont.truetype(font_paths["Pacifico-Medium"], 11)
        except IOError as e:
            print(f"Error loading fonts: {e}. Using default fonts...")
            font_title = font_title_big = font_min_title = font_bold = font_regular = font_regular_bold = font_small = font_smallest = font_slogan_regular = font_small_bold = font_large = font_slogan_small = font_medium = font_medium_bold = ImageFont.load_default()

        return font_title_big, font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold

    def load_new_fonts(self):
        # Get the absolute path to the fonts directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fonts_dir = self.fonts_path
        print("Fonts directory:", fonts_dir)

        try:
            font_paths = {
                "Montserrat-Bold": files(qure.fonts).joinpath("Montserrat/static/Montserrat-Bold.ttf"),
                "Roboto-Bold": files(qure.fonts).joinpath("Roboto/static/Roboto-Bold.ttf"),
                "Roboto-Regular": files(qure.fonts).joinpath("Roboto/static/Roboto-Regular.ttf"),
                "Roboto-Italic": files(qure.fonts).joinpath("Roboto/static/Roboto-Italic.ttf"),
                "OpenSans-Regular": files(qure.fonts).joinpath("OpenSans/static/OpenSans-Regular.ttf"),
                "OpenSans-Bold": files(qure.fonts).joinpath("OpenSans/static/OpenSans-Bold.ttf"),
                "Montserrat-Medium": files(qure.fonts).joinpath("Montserrat/static/Montserrat-Medium.ttf"),
                "Pacifico-Medium": files(qure.fonts).joinpath("Pacifico/Pacifico-Regular.ttf"),
            }

            # Convert Path objects to strings for compatibility with PIL
            font_paths = {name: str(path) for name, path in font_paths.items()}
        except Exception as e:
            print(f"Error accessing font resources: {e}. Falling back to file paths...")
            font_paths = {
                "Montserrat-Bold": os.path.join(fonts_dir, "Montserrat", "static", "Montserrat-Bold.ttf"),
                "Roboto-Bold": os.path.join(fonts_dir, "Roboto", "static", "Roboto-Bold.ttf"),
                "Roboto-Regular": os.path.join(fonts_dir, "Roboto", "static", "Roboto-Regular.ttf"),
                "Roboto-Italic": os.path.join(fonts_dir, "Roboto", "static", "Roboto-Italic.ttf"),
                "OpenSans-Regular": os.path.join(fonts_dir, "OpenSans", "static", "OpenSans-Regular.ttf"),
                "OpenSans-Bold": os.path.join(fonts_dir, "OpenSans", "static", "OpenSans-Bold.ttf"),
                "Montserrat-Medium": os.path.join(fonts_dir, "Montserrat", "static", "Montserrat-Medium.ttf"),
                "Pacifico-Medium": os.path.join(fonts_dir, "Pacifico", "Pacifico-Regular.ttf"),
            }

        # Print the paths for debugging
        for font_name, font_path in font_paths.items():
            print(f"Looking for {font_name} at: {font_path}")
            if not os.path.exists(font_path):
                print(f"WARNING: Font file not found: {font_path}")


        # Load fonts with error handling
        print("Loading fonts...")
        try:
            font_title_big = ImageFont.truetype(font_paths["Montserrat-Bold"], 54)
            font_title = ImageFont.truetype(font_paths["Montserrat-Bold"], 46)
            font_min_title = ImageFont.truetype(font_paths["OpenSans-Bold"], 36)
            font_bold = ImageFont.truetype(font_paths["Roboto-Bold"], 28)
            font_regular = ImageFont.truetype(font_paths["OpenSans-Regular"], 21)
            font_regular_bold = ImageFont.truetype(font_paths["OpenSans-Bold"], 21)
            font_small = ImageFont.truetype(font_paths["Roboto-Italic"], 16)
            font_smallest = ImageFont.truetype(font_paths["Roboto-Bold"], 14)
            font_small_bold = ImageFont.truetype(font_paths["Roboto-Bold"], 16)
            font_large = ImageFont.truetype(font_paths["Montserrat-Medium"], 32)
            font_medium = ImageFont.truetype(font_paths["Montserrat-Medium"], 24)
            font_medium_bold = ImageFont.truetype(font_paths["Montserrat-Bold"], 24)
            font_slogan_regular = ImageFont.truetype(font_paths["Pacifico-Medium"], 28)
            font_slogan_small = ImageFont.truetype(font_paths["Pacifico-Medium"], 18)
        except IOError as e:
            print(f"Error loading fonts: {e}. Using default fonts...")
            font_title_big = font_title = font_min_title = font_bold = font_regular = font_regular_bold = font_small = font_smallest = font_slogan_regular = font_small_bold = font_large = font_slogan_small = font_medium = font_medium_bold = ImageFont.load_default()

        return font_title_big, font_title, font_min_title, font_bold, font_regular, font_regular_bold, font_small, font_smallest, font_small_bold, font_large, font_slogan_regular, font_slogan_small, font_medium, font_medium_bold

    def place_student_photo(self, card: Image.Image, student_photo: str, school_logo: str, size: tuple, position: tuple):
        """Place student photo on the card."""
        try:
            with Image.open(student_photo) as photo:
                # Create white background image
                bg = Image.new('RGBA', size, 'white')

                # Resize photo maintaining transparency
                photo = photo.resize(size, Image.LANCZOS)

                # Paste photo onto white background
                if photo.mode == 'RGBA':
                    bg.paste(photo, (0,0), photo)
                else:
                    bg.paste(photo, (0,0))

                # Create mask for rounded corners
                mask = Image.new("L", size, 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.rounded_rectangle([0, 0, *size], radius=10, fill=255)

                # Paste final image with mask
                card.paste(bg, position, mask)
        except IOError:
            print("Student photo not found; using school logo as placeholder")
            with Image.open(school_logo) as logo:
                # Create white background image
                bg = Image.new('RGBA', size, 'white')

                # Resize logo maintaining transparency
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')
                logo = logo.resize(size, Image.LANCZOS)

                # Paste logo onto white background
                bg.paste(logo, (0,0), logo)

                # Create mask for rounded corners
                mask = Image.new("L", size, 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.rounded_rectangle([0, 0, *size], radius=10, fill=255)

                # Paste final image with mask
                card.paste(bg, position, mask)

    def lighten_color(self, color, factor=0.1):
        """Lighten a color by the given factor."""
        if isinstance(color, tuple) and len(color) >= 3:
            r, g, b = color[:3]
            r = min(255, int(r + (255 - r) * factor))
            g = min(255, int(g + (255 - g) * factor))
            b = min(255, int(b + (255 - b) * factor))
            return (r, g, b) if len(color) == 3 else (r, g, b, color[3] if len(color) > 3 else 255)
        return color

    def darken_color(self, color, factor=0.1):
        """Darken a color by the given factor."""
        if isinstance(color, tuple) and len(color) >= 3:
            r, g, b = color[:3]
            r = max(0, int(r * (1 - factor)))
            g = max(0, int(g * (1 - factor)))
            b = max(0, int(b * (1 - factor)))
            return (r, g, b) if len(color) == 3 else (r, g, b, color[3] if len(color) > 3 else 255)
        return color

    def load_background():
        print("Adding background...")
        background_path = files(qure.assets).joinpath("background.jpg")
        with background_path.open('rb') as img_file:
            background_img = Image.open(img_file).convert("RGBA")

        return background_img

    def add_watermark(self, card, watermark_path=None, opacity=40, rotation=15):
        """Add a watermark to the card with optimized processing."""
        try:
            if not watermark_path:
                try:
                    watermark_path = files(qure.assets).joinpath("avatar1.png")
                    watermark_path = str(watermark_path)
                except Exception as e:
                    print(f"Error accessing watermark resource: {e}. Falling back to file path...")
                    watermark_path = os.path.join(self.assets_path, "avatar1.png")

            # Check if watermark exists in cache
            watermark_cache_key = f"{watermark_path}_{opacity}_{rotation}"
            if hasattr(self, '_watermark_cache') and watermark_cache_key in self._watermark_cache:
                watermark = self._watermark_cache[watermark_cache_key]
            else:
                # Load and process watermark
                watermark = Image.open(watermark_path)
                if watermark.mode != 'RGBA':
                    watermark = watermark.convert('RGBA')

                # Apply opacity
                watermark.putalpha(opacity)
                watermark = watermark.rotate(rotation)

                # Cache the processed watermark
                if not hasattr(self, '_watermark_cache'):
                    self._watermark_cache = {}
                self._watermark_cache[watermark_cache_key] = watermark

            # Calculate position
            wx = (card.width - watermark.width) // 2
            wy = (card.height - watermark.height) // 2

            # Paste the watermark
            card.paste(watermark, (wx, wy), watermark)
            return True
        except Exception as e:
            print(f"Error adding watermark: {e}")
            return False

    def add_holographic_effect(self, card, region=None, intensity=0.7):
        """Add a premium holographic effect to a region of the card."""
        try:
            # If no region specified, use a default region
            if region is None:
                region = (card.width // 4, card.height // 4,
                          3 * card.width // 4, 3 * card.height // 4)

            # Create a holographic pattern
            holo_overlay = Image.new('RGBA', card.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(holo_overlay)

            # Generate rainbow gradient lines
            for i in range(region[1], region[3], 2):
                # Calculate rainbow color
                hue = (i % 100) / 100.0
                r, g, b = [int(255 * x) for x in self._hsv_to_rgb(hue, 0.5, 1.0)]

                # Draw thin diagonal line with rainbow color
                draw.line([(region[0], i), (region[2], i - 20)],
                          fill=(r, g, b, int(40 * intensity)), width=1)

            # Apply the holographic effect
            card = Image.alpha_composite(card.convert('RGBA'), holo_overlay)
            return card.convert('RGB') if card.mode != 'RGB' else card
        except Exception as e:
            print(f"Error adding holographic effect: {e}")
            return card

    def _hsv_to_rgb(self, h, s, v):
        """Convert HSV color to RGB."""
        if s == 0.0:
            return (v, v, v)

        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i %= 6

        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    def generate_verification_code(self, student_id, school_name, expiration_date):
        """Generate a unique verification code for the card."""
        import hashlib
        import base64

        # Create a unique string from student data
        unique_string = f"{student_id}:{school_name}:{expiration_date}:{random.randint(1000, 9999)}"

        # Generate a hash
        hash_object = hashlib.sha256(unique_string.encode())
        hash_digest = hash_object.digest()

        # Convert to a shorter, readable code
        verification_code = base64.b32encode(hash_digest[:5]).decode().strip('=')

        # Format in groups for readability
        formatted_code = '-'.join([verification_code[i:i+4] for i in range(0, len(verification_code), 4)])

        return formatted_code

    def export_card(self, card, format_type, output_path=None, quality=95, dpi=(300, 300)):
        """Export card in various formats for different use cases."""
        if output_path is None:
            # Generate default output path based on format
            directory_root = os.path.expanduser("~")
            base_name = f"{self.student_name}_card"
            output_path = os.path.join(directory_root, "Documents", "kaascan", "Exports",
                                      f"{base_name}.{format_type.lower()}")

            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            if format_type.upper() == 'PDF':
                # For PDF export
                from PIL import PdfWriter
                pdf = PdfWriter()
                pdf.add_page(card)
                pdf.save(output_path)

            elif format_type.upper() == 'SVG':
                # For SVG export (vector format)
                card.save(output_path, format='SVG')

            elif format_type.upper() in ['PNG', 'JPEG', 'JPG', 'WEBP']:
                # For raster formats with quality and DPI settings
                card.save(output_path, format=format_type.upper(),
                         quality=quality, dpi=dpi)
            else:
                # Default fallback
                card.save(output_path)

            print(f"Card exported as {format_type.upper()} to: {output_path}")
            return output_path
        except Exception as e:
            print(f"Error exporting card as {format_type}: {e}")
            return None

    def log_card_generation(self, school_name, template, success=True):
        """Log card generation for analytics (enterprise feature)."""
        try:
            log_dir = os.path.join(os.path.expanduser("~"), "Documents", "kaascan", "Analytics")
            os.makedirs(log_dir, exist_ok=True)

            log_file = os.path.join(log_dir, "card_generation_log.csv")

            # Create file with headers if it doesn't exist
            if not os.path.exists(log_file):
                with open(log_file, 'w') as f:
                    f.write("timestamp,school,template,student_id,success\n")

            # Append log entry
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            student_id = str(self.data.get('id', 'unknown'))

            with open(log_file, 'a') as f:
                f.write(f"{timestamp},{school_name},{template},{student_id},{success}\n")

            return True
        except Exception as e:
            print(f"Error logging analytics: {e}")
            return False

    def save_double_sided_card(self, front_card: Image, back_card: Image, cards_path: str, school_name: str, academic_year: str, template: str) -> tuple:
        """Save both sides of the card."""
        directory_root = os.path.expanduser("~")
        base_path = os.path.join(directory_root, "Documents", "kaascan", "Cards")
        school_folder = str(school_name)

        # Create school folder
        school_path = os.path.join(base_path, school_folder)
        os.makedirs(school_path, exist_ok=True)

        # Create front side and back side subfolders
        front_side_folder = os.path.join(school_path, "front side")
        back_side_folder = os.path.join(school_path, "back side")
        os.makedirs(front_side_folder, exist_ok=True)
        os.makedirs(back_side_folder, exist_ok=True)

        # Get student details for folder structure
        department_folder = str(self.data.get('Department', 'Unknown Department'))
        trade_folder = str(self.data.get('Trade', 'Unknown Trade'))
        level_of_study_folder = str(self.data.get('Class', 'Unknown Level'))

        # Create folder structure for front side
        front_student_path = os.path.join(front_side_folder, department_folder, trade_folder, level_of_study_folder)
        os.makedirs(front_student_path, exist_ok=True)

        # Create folder structure for back side
        back_student_path = os.path.join(back_side_folder, department_folder, trade_folder, level_of_study_folder)
        os.makedirs(back_student_path, exist_ok=True)

        # Save front side in student-specific folder
        front_file = f"{self.student_name}.png"
        front_path = os.path.join(front_student_path, front_file)
        front_card.save(front_path)

        # Save back side with the same name as front side
        back_file = f"{self.student_name}.png"
        back_path = os.path.join(back_student_path, back_file)
        back_card.save(back_path)

        return front_path, back_path

    def save_card(self, card: Image.Image, cards_path: str, school_name: str, academic_year: str, template: str) -> str:
        """Save the card to a specified file path."""
        directory_root = os.path.expanduser("~")
        base_path = f"{directory_root}\\Documents\\kaascan\\Cards"
        print(base_path)
        school_folder = school_name.replace(" ", " ")
        department_folder = self.data.get('Department', 'Unknown Department')
        trade_folder = self.data.get('Trade', 'Unknown Trade')
        level_of_study_folder = self.data.get('Class', 'Unknown Trade')

        full_path = os.path.join(base_path, school_folder, department_folder, trade_folder, level_of_study_folder)
        os.makedirs(full_path, exist_ok=True)

        # Determine the file name
        file_name = f"{self.student_name}_student_card.png"
        full_file_path = os.path.join(full_path, file_name)
        card.save(full_file_path)
        return full_file_path

    def add_gradient_background(self, card: Image.Image, start_color: tuple, end_color: tuple):
        """Adds a gradient background to the card."""
        for y in range(card.height):
            r = start_color[0] + (end_color[0] - start_color[0]) * y // card.height
            g = start_color[1] + (end_color[1] - start_color[1]) * y // card.height
            b = start_color[2] + (end_color[2] - start_color[2]) * y // card.height
            draw = ImageDraw.Draw(card)
            draw.line((0, y, card.width, y), fill=(r, g, b))
