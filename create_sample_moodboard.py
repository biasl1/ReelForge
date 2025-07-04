#!/usr/bin/env python3
"""
Create a sample moodboard image for testing
"""

from PIL import Image, ImageDraw, ImageFont
import colorsys

def create_sample_moodboard():
    """Create a sample moodboard image for testing"""
    
    # Create a gradient background
    width, height = 800, 600
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create a gradient from purple to blue
    for y in range(height):
        # Calculate color based on position
        ratio = y / height
        
        # Purple to blue gradient
        r1, g1, b1 = 75, 0, 130    # Purple
        r2, g2, b2 = 0, 100, 200   # Blue
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add some artistic elements
    # Draw some circles for visual interest
    for i in range(15):
        x = (i * 60) % width
        y = (i * 40) % height
        radius = 20 + (i * 3)
        
        # Semi-transparent circles
        overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        circle_color = (255, 255, 255, 30 + (i * 5))
        overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=circle_color)
        
        image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
    
    # Add text overlay
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        font = ImageFont.load_default()
    
    text_overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_overlay)
    
    text = "SAMPLE MOODBOARD"
    text_bbox = text_draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (width - text_width) // 2
    text_y = height // 2 - 50
    
    # Draw text with shadow
    text_draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 100), font=font)
    text_draw.text((text_x, text_y), text, fill=(255, 255, 255, 200), font=font)
    
    # Add subtitle
    subtitle = "Professional Audio Plugin Vibes"
    try:
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        subtitle_font = ImageFont.load_default()
    
    sub_bbox = text_draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (width - sub_width) // 2
    sub_y = text_y + text_height + 20
    
    text_draw.text((sub_x + 1, sub_y + 1), subtitle, fill=(0, 0, 0, 80), font=subtitle_font)
    text_draw.text((sub_x, sub_y), subtitle, fill=(255, 255, 255, 150), font=subtitle_font)
    
    # Composite the text
    image = Image.alpha_composite(image.convert('RGBA'), text_overlay).convert('RGB')
    
    # Save the image
    output_path = "sample_moodboard.jpg"
    image.save(output_path, "JPEG", quality=90)
    print(f"Sample moodboard created: {output_path}")
    
    return output_path

if __name__ == "__main__":
    try:
        create_sample_moodboard()
    except ImportError:
        print("PIL (Pillow) not available. Please install with: pip install Pillow")
        print("Or use any image file as a moodboard for testing.")
