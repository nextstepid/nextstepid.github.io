import os
import re

# The new script block
new_script = """
        var _mt = document.getElementById('mobile-menu-toggle');
        var _nl = document.querySelector('.nav-links');
        if (_mt && _nl) {
            _mt.addEventListener('click', function() { 
                _nl.classList.toggle('active'); 
                _mt.classList.toggle('active'); 
            });
            
            // Handle Dropdown Toggles
            document.querySelectorAll('.nav-dropdown-toggle').forEach(function(toggle) {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    var parent = toggle.parentElement;
                    
                    // Close other dropdowns
                    document.querySelectorAll('.nav-dropdown').forEach(function(d) {
                        if (d !== parent) d.classList.remove('active');
                    });
                    
                    parent.classList.toggle('active');
                });
            });

            // Handle All Link Clicks
            document.querySelectorAll('.nav-links a').forEach(function(link) {
                link.addEventListener('click', function(e) {
                    // Only close if it's NOT a dropdown toggle
                    if (!link.classList.contains('nav-dropdown-toggle')) {
                        _nl.classList.remove('active');
                        _mt.classList.remove('active');
                        document.querySelectorAll('.nav-dropdown').forEach(function(d) {
                            d.classList.remove('active');
                        });
                    }
                });
            });

            // Close when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.nav-dropdown')) {
                    document.querySelectorAll('.nav-dropdown').forEach(function(d) {
                        d.classList.remove('active');
                    });
                }
            });
        }
"""

# Pattern to find the old script block
# This is a bit tricky because of variations, but usually it starts with var _mt = ... and ends with the article search logic or similar.
# I will target the navigation part only.

old_nav_pattern = re.compile(r'var _mt = document\.getElementById\(\'mobile-menu-toggle\'\);.*?if \(_mt && _nl\) \{.*?\}\s*(?=var _cat|var _si)', re.DOTALL)

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r') as f:
            content = f.read()
        
        new_content = old_nav_pattern.sub(new_script.strip() + '\n        ', content)
        
        if new_content != content:
            with open(filename, 'w') as f:
                f.write(new_content)
            print(f"Updated {filename}")
