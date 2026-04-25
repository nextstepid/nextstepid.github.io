import os

script_block = """    <script>
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

        var _cat = new URLSearchParams(window.location.search).get('cat');
        if (_cat) {
            document.querySelectorAll('.article-card').forEach(function(c) {
                if (c.getAttribute('data-cat') !== _cat) c.style.display = 'none';
            });
            var btn = document.querySelector('.picker-btn[data-cat="' + _cat + '"]');
            if (btn) btn.classList.add('active-filter');
        }
        var _si = document.getElementById('articleSearch');
        if (_si) {
            _si.addEventListener('input', function(e) {
                var t = e.target.value.toLowerCase();
                document.querySelectorAll('.article-card').forEach(function(c) {
                    c.style.display = (c.getAttribute('data-title') || '').toLowerCase().includes(t) ? '' : 'none';
                });
            });
        }
    </script>"""

for i in range(1, 20):
    filename = f"artikel{i}.html"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        
        # Find the start and end of the script block
        start_idx = -1
        end_idx = -1
        for idx, line in enumerate(lines):
            if "<script>" in line:
                start_idx = idx
            if "</script>" in line:
                end_idx = idx
        
        if start_idx != -1 and end_idx != -1:
            new_lines = lines[:start_idx] + [script_block + "\n"] + lines[end_idx+1:]
            with open(filename, "w") as f:
                f.writelines(new_lines)
            print(f"Updated {filename}")
