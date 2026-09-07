"""Generate self-contained profile SVGs using only Python's standard library."""
from pathlib import Path
from html import escape

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
THEMES = {
    '': ('#0d1117', '#e6edf3', '#00ff99', '#243b40'),
    '-light': ('#f6f8fa', '#1f2328', '#087f5b', '#cbd5e1'),
}
BADGES = {
    'profile': 'DX4GREY / OPEN SOURCE', 'followers': 'FOLLOW ON GITHUB',
    'sponsor': 'SUPPORT OPEN SOURCE', 'cpp': 'C++ / 20',
    'linux': 'LINUX / NATIVE', 'esp32': 'ESP32-S3',
    'embedded': 'EMBEDDED / C++', 'support': 'BECOME A GITHUB SPONSOR',
    'github': 'GITHUB / DX4GREY', 'repositories': 'EXPLORE REPOSITORIES',
}

def write(name, suffix, title, body, width, height):
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / f'{name}{suffix}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">\n<title>{escape(title)}</title>\n'
        '<style>.still { display: none; } @media (prefers-reduced-motion: reduce) '
        '{ .motion { display: none; } .still { display: inline; } }</style>\n'
        + body + '\n</svg>\n', encoding='utf-8')

for suffix, (bg, fg, accent, border) in THEMES.items():
    for name, label in BADGES.items():
        width = len(label) * 8 + 40
        write(name, suffix, label,
              f'<rect x=".5" y=".5" width="{width-1}" height="33" rx="8" fill="{bg}" stroke="{border}"/>'
              f'<circle cx="16" cy="17" r="3" fill="{accent}"/>'
              f'<text x="29" y="22" fill="{fg}" font-family="monospace" font-size="12">{escape(label)}</text>', width, 34)
    roles = ['Software Developer', 'Linux Enthusiast', 'Kernel Explorer',
             'Embedded Systems Builder', 'Security Research Learner']
    body = f'<text class="still" x="350" y="35" text-anchor="middle" fill="{accent}" font-family="monospace" font-size="21">Software Developer</text>'
    for i, role in enumerate(roles):
        values = ['0'] * 6
        values[i] = '1'
        values[5] = values[0]
        body += (f'<text class="motion" x="350" y="35" text-anchor="middle" fill="{accent}" '
                 f'font-family="monospace" font-size="21" opacity="{1 if i == 0 else 0}">{role}'
                 f'<animate attributeName="opacity" values="{";".join(values)}" keyTimes="0;.2;.4;.6;.8;1" '
                 'calcMode="discrete" dur="15s" repeatCount="indefinite"/></text>')
    write('roles', suffix, 'Developer interests: systems, Linux, embedded hardware and security research', body, 700, 56)
    tech = [('C++', 'Systems'), ('Python', 'Scripting'), ('CMake', 'Build'), ('Linux', 'Platform'),
            ('Bash', 'Shell'), ('Git', 'Versioning'), ('GitHub', 'Open source'),
            ('Arduino', 'Hardware'), ('Android', 'Mobile'), ('VS Code', 'Editor')]
    body = ''
    for i, (name, label) in enumerate(tech):
        x, y = (i % 5) * 192, (i // 5) * 92
        body += (f'<g transform="translate({x} {y})"><rect x="4" y="4" width="180" height="80" rx="12" fill="{bg}" stroke="{border}"/>'
                 f'<path d="M20 25h16" stroke="{accent}" stroke-width="3"/>'
                 f'<text x="20" y="49" fill="{fg}" font-family="monospace" font-size="18">{name}</text>'
                 f'<text x="20" y="69" fill="{accent}" font-family="monospace" font-size="12">{label}</text></g>')
    write('tech-stack', suffix, ', '.join(name for name, _ in tech), body, 960, 184)
    body = f'<rect width="960" height="150" rx="16" fill="{bg}"/>'
    for row in range(3):
        for col in range(38):
            body += f'<rect x="{26+col*24}" y="{24+row*24}" width="15" height="15" rx="3" fill="{accent}" opacity="{.08+((col+row)%4)*.05:.2f}"/>'
    body += (f'<path class="motion" d="M32 55H920" fill="none" stroke="{accent}" stroke-width="10" stroke-linecap="round" stroke-dasharray="48 888">'
             '<animate attributeName="stroke-dashoffset" from="48" to="-888" dur="9s" repeatCount="indefinite"/></path>'
             f'<text x="480" y="126" text-anchor="middle" fill="{fg}" font-family="monospace" font-size="14">EXPLORE → BUILD → SHARE → REPEAT</text>')
    write('playground', suffix, 'Decorative animated code grid — not contribution data', body, 960, 150)

# Shared drawing primitives keep every surface and both palettes consistent.
def text(x, y, label, color, size=16, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}" {extra}>{escape(label)}</text>'


def tracer(path, color, duration=12):
    return (f'<path class="motion" d="{path}" fill="none" stroke="{color}" stroke-width="2" '
            'stroke-linecap="round" stroke-dasharray="24 1100">'
            f'<animate attributeName="stroke-dashoffset" from="1124" to="0" dur="{duration}s" repeatCount="indefinite"/></path>')


for suffix, (bg, fg, accent, border) in THEMES.items():
    muted = '#91a6b7' if not suffix else '#526477'
    secondary = '#73bfff' if not suffix else '#2563a6'
    surface = '#10252a' if not suffix else '#e4f4ed'
    defs = (f'<defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="{bg}"/>'
            f'<stop offset="1" stop-color="{surface}"/></linearGradient>'
            f'<radialGradient id="halo"><stop stop-color="{accent}" stop-opacity=".14"/>'
            '<stop offset="1" stop-opacity="0"/></radialGradient></defs>')

    def panel(w, h):
        return defs + f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="url(#surface)" stroke="{border}"/>'

    body = panel(960, 340)
    body += '<ellipse cx="760" cy="165" rx="200" ry="165" fill="url(#halo)"/>'
    for y in range(32, 320, 32):
        for x in range(32, 940, 32):
            body += f'<circle cx="{x}" cy="{y}" r="1" fill="{muted}" opacity=".14"/>'
    body += text(48, 51, 'DX / LAB', accent, 13, 'letter-spacing="3"')
    body += text(48, 101, 'SYSTEMS ENGINEERING · CREATIVE CURIOSITY', muted, 12)
    body += text(43, 178, 'DX4GREY', fg, 76, 'font-weight="700" letter-spacing="-4"')
    body += text(377, 178, '.', accent, 76)
    body += text(48, 218, 'Close to the metal. Open to discovery.', muted, 17)
    body += f'<path d="M48 249H490" stroke="{border}"/>'
    body += text(48, 282, 'INDONESIA', accent, 12, 'letter-spacing="2"')
    body += text(194, 282, 'SOFTWARE / HARDWARE / OPEN SOURCE', muted, 11)
    for r in (49, 84, 120):
        body += f'<circle cx="775" cy="169" r="{r}" fill="none" stroke="{accent}" stroke-opacity=".18"/>'
    for r, dur, direction in ((120, 28, 360), (84, 20, -360)):
        body += (f'<g class="motion"><circle cx="775" cy="169" r="{r}" fill="none" stroke="{secondary}" stroke-width="2" stroke-dasharray="32 18 4 700"/>'
                 f'<animateTransform attributeName="transform" type="rotate" from="0 775 169" to="{direction} 775 169" dur="{dur}s" repeatCount="indefinite"/></g>')
    body += f'<rect x="742" y="136" width="66" height="66" rx="18" fill="{bg}" stroke="{border}"/>'
    body += text(754, 177, '</>', accent, 23)
    body += (f'<circle class="motion" cx="775" cy="169" r="49" fill="none" stroke="{accent}">'
             '<animate attributeName="r" values="49;118" dur="6s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values=".35;0" dur="6s" repeatCount="indefinite"/></circle>')
    body += tracer('M48 313H912', accent, 16)
    write('hero', suffix, 'DX4GREY — Software, hardware and open source', body, 960, 340)

    body = panel(960, 250)
    for i, color in enumerate((muted, secondary, accent)):
        body += f'<circle cx="{26+i*18}" cy="25" r="4" fill="{color}" opacity=".7"/>'
    body += text(92, 30, 'dx4grey@lab / exploration.log', muted, 12)
    body += f'<path d="M1 48H959" stroke="{border}"/>'
    body += text(30, 85, '❯ ./explore --from-kernel-to-hardware', fg, 18)
    rows = [('01', 'INSPECT', 'Understand the internals'), ('02', 'BUILD', 'Turn curiosity into code'), ('03', 'SHARE', 'Document, test, improve')]
    for i, (n, title, desc) in enumerate(rows):
        y=123+i*34
        body += text(30, y, n, muted, 12) + text(70, y, title, accent, 13) + text(190, y, desc, fg, 16)
    body += f'<rect class="motion" x="16" y="108" width="3" height="18" rx="1.5" fill="{accent}"><animate attributeName="y" values="108;142;176;108" calcMode="discrete" dur="9s" repeatCount="indefinite"/></rect>'
    body += text(30, 230, '❯', accent, 18)
    body += f'<rect class="motion" x="51" y="216" width="9" height="17" fill="{accent}"><animate attributeName="opacity" values="1;0;1" dur="1.8s" repeatCount="indefinite"/></rect>'
    body += tracer('M90 228H918', accent, 14)
    write('terminal', suffix, 'Inspect systems, build tools, share findings', body, 960, 250)

    body = f'<path d="M0 24H960" stroke="{border}"/>'
    body += f'<path d="M430 24H448L460 14L472 34L484 14L496 24H530" fill="none" stroke="{accent}" opacity=".6"/>'
    body += tracer('M0 24H960', secondary, 12)
    write('signal', suffix, 'Flowing circuit signal', body, 960, 48)

    for name, title, label, motif in [('project-nizaw', 'Nizaw', '01 / SYSTEMS EXPLORATION', 'system'), ('project-rf', 'ESP32 RF Suite', '02 / EMBEDDED EXPERIMENTS', 'radio')]:
        body = panel(460, 164) + text(24, 35, label, accent, 11, 'letter-spacing="1"') + text(24, 83, title, fg, 28, 'font-weight="700"')
        body += text(24, 115, 'LINUX / C++20' if motif=='system' else 'ESP32-S3 / RADIO', muted, 12)
        if motif=='system':
            for i in range(4):
                body += f'<rect x="{330+i*23}" y="{87-i*12}" width="12" height="{22+i*12}" rx="4" fill="{accent}" opacity=".2"/>'
                body += f'<rect class="motion" x="{330+i*23}" y="{87-i*12}" width="12" height="{22+i*12}" rx="4" fill="{accent}" opacity=".5"><animate attributeName="opacity" values=".2;.8;.2" dur="4s" begin="-{i}s" repeatCount="indefinite"/></rect>'
        else:
            for i in range(3):
                body += f'<circle cx="385" cy="81" r="{15+i*13}" fill="none" stroke="{accent}" opacity=".22"/>'
            body += f'<circle class="motion" cx="385" cy="81" r="10" fill="none" stroke="{accent}"><animate attributeName="r" values="10;45" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="4s" repeatCount="indefinite"/></circle>'
        body += tracer('M24 143H436', secondary, 10)
        write(name, suffix, title+' — '+label, body, 460, 164)

    body = panel(960, 164) + text(480, 52, 'ALWAYS CURIOUS. ALWAYS BUILDING.', accent, 12, 'text-anchor="middle" letter-spacing="3"')
    body += text(480, 88, 'Build low-level. Learn deeply. Ship something useful.', fg, 17, 'text-anchor="middle"')
    for i in range(3):
        body += f'<path class="motion" d="M-240 {125+i*9}Q-120 {105+i*9} 0 {125+i*9}T240 {125+i*9}T480 {125+i*9}T720 {125+i*9}T960 {125+i*9}T1200 {125+i*9}" fill="none" stroke="{accent}" opacity="{.1+i*.06}"><animateTransform attributeName="transform" type="translate" from="0 0" to="240 0" dur="{12+i*5}s" repeatCount="indefinite"/></path>'
    write('footer', suffix, 'Build low-level. Learn deeply. Ship something useful.', body, 960, 164)

    # Give compact controls and technology tiles a restrained moving accent.
    for name in (*BADGES, 'tech-stack'):
        path = ASSETS / f'{name}{suffix}.svg'
        svg = path.read_text()
        if name in BADGES:
            width = len(BADGES[name])*8+40
            effect = tracer(f'M12 31H{width-12}', accent, 10)
        else:
            effect=''
            for i in range(10):
                x,y=(i%5)*192,(i//5)*92
                effect += (f'<rect class="motion" x="{x+20}" y="{y+23}" width="16" height="3" rx="1.5" fill="{accent}">'
                           f'<animate attributeName="width" values="16;72;16" dur="{5+i%3}s" begin="-{i*.6}s" repeatCount="indefinite"/></rect>')
        path.write_text(svg.replace('</svg>', effect+'\n</svg>'))

# Compact artwork keeps lettering legible when the README is viewed on phones.
for suffix, (bg, fg, accent, border) in THEMES.items():
    muted = '#91a6b7' if not suffix else '#526477'
    def compact(body, h):
        return f'<rect x="1" y="1" width="358" height="{h-2}" rx="18" fill="{bg}" stroke="{border}"/>'+body
    body = text(24, 38, 'SOFTWARE / HARDWARE', accent, 12)
    body += text(22, 105, 'DX4GREY', fg, 48, 'font-weight="700"')
    body += text(24, 140, 'Close to the metal.', muted, 16)+text(24, 165, 'Open to discovery.', muted, 16)
    body += text(24, 207, 'INDONESIA · OPEN SOURCE', accent, 12)
    body += tracer('M24 233H336',accent,12)
    write('hero-mobile',suffix,'DX4GREY — software, hardware, open source',compact(body,256),360,256)
    body=text(24,35,'dx4grey@lab / exploration',muted,12)
    for i,(heading,detail) in enumerate([('01 / INSPECT','Understand the internals'),('02 / BUILD','Turn curiosity into code'),('03 / SHARE','Document, test, improve')]):
        y=78+i*65
        body+=text(24,y,heading,accent,13)+text(24,y+25,detail,fg,16)
    body+=tracer('M24 254H336',accent,10)
    write('terminal-mobile',suffix,'Inspect, build, share — illustrative workflow',compact(body,280),360,280)
    body=text(180,43,'ALWAYS CURIOUS.',accent,13,'text-anchor="middle"')+text(180,71,'ALWAYS BUILDING.',accent,13,'text-anchor="middle"')
    for i,line in enumerate(['Build low-level.','Learn deeply.','Ship something useful.']):
        body+=text(180,111+i*25,line,fg,17,'text-anchor="middle"')
    body+=tracer('M24 192H336',accent,13)
    write('footer-mobile',suffix,'Build low-level. Learn deeply. Ship something useful.',compact(body,216),360,216)
    body=text(180,33,'CODE PLAYGROUND',accent,12,'text-anchor="middle"')
    for i in range(12):
        body+=f'<circle cx="{26+i*28}" cy="66" r="4" fill="{accent}" opacity=".2"/>'
    body+=tracer('M26 66H334',accent,7)
    body+=text(180,108,'EXPLORE → BUILD → SHARE',fg,14,'text-anchor="middle"')
    write('playground-mobile',suffix,'Decorative signal animation, not contribution data',compact(body,132),360,132)
    body=text(180,31,'Backend development',accent,17,'text-anchor="middle"')
    body+=tracer('M74 47H286',accent,9)
    write('roles-mobile',suffix,'Backend development',body,360,58)
    for name,label in [('tech-cpp','C++20'),('tech-linux','Linux'),('tech-esp32','ESP32-S3'),('tech-nrf','nRF24L01+'),('tech-arduino','Arduino')]:
        body=f'<rect x="1" y="1" width="158" height="58" rx="12" fill="{bg}" stroke="{border}"/>'+text(16,33,label,fg,17)+tracer('M16 47H144',accent,11)
        write(name,suffix,label,body,160,60)
    for name,title,lines in [
        ('focus-systems','SYSTEMS',['Linux customization','Kernel experiments']),
        ('focus-embedded','EMBEDDED',['Arduino / ESP projects','Hardware experiments']),
        ('focus-security','SECURITY LEARNING',['Network analysis','Defensive practices'])]:
        body=text(24,39,title,accent,14)
        for i,line in enumerate(lines): body+=text(24,78+i*27,line,fg,16)
        body+=tracer('M24 129H336',accent,12)
        write(name,suffix,title+' — '+', '.join(lines),compact(body,150),360,150)
