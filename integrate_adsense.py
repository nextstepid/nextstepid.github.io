import os
import re

adsense_script = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3079804302150146" crossorigin="anonymous"></script>'

def get_ad_unit(position, slot_id="GANTI_DENGAN_SLOT_ID"):
    return f"""
        <!-- Google AdSense - {position} -->
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-3079804302150146"
             data-ad-slot="{slot_id}"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
    """

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r') as f:
            content = f.read()
        
        # 1. Add to <head> if not exists
        if adsense_script not in content:
            content = content.replace('</head>', f'    {adsense_script}\n</head>')
        
        # 2. Replace existing placeholders
        content = content.replace('Place your AdSense code here (Home Banner Top)', get_ad_unit("Banner Atas"))
        content = content.replace('Place your AdSense code here (Home Banner Bottom Large)', get_ad_unit("Banner Bawah Besar"))
        content = content.replace('Place your AdSense code here (Contact Footer)', get_ad_unit("Contact Footer"))
        content = content.replace('Place your AdSense code here (Privacy Slot)', get_ad_unit("Privacy Slot"))
        content = content.replace('Place your AdSense code here (About Banner)', get_ad_unit("About Banner"))
        content = content.replace('Place your AdSense code here (Mulai Dari Sini Banner)', get_ad_unit("Mulai Dari Sini Banner"))
        content = content.replace('Place your AdSense code here (Bottom)', get_ad_unit("Bottom Artikel"))

        # 3. Middle of Article (for artikel*.html)
        if 'artikel' in filename and '<article class="article-body">' in content:
            # Find the second paragraph closing tag </p>
            paragraphs = re.findall(r'<p>.*?</p>', content, re.DOTALL)
            if len(paragraphs) >= 2:
                second_p = paragraphs[1]
                ad_middle = get_ad_unit("Tengah Artikel")
                content = content.replace(second_p, second_p + ad_middle)

        with open(filename, 'w') as f:
            f.write(content)
        print(f"Updated {filename}")
