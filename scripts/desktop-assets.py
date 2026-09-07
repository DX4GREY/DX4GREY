"""Desktop compositions, executed by generate-local-assets.py with shared helpers."""
for suffix, (bg, fg, accent, border) in THEMES.items():
    muted = '#91a6b7' if not suffix else '#526477'
    blue = '#73bfff' if not suffix else '#2563a6'
    surface = '#11252b' if not suffix else '#e7f3ee'
    defs = f'<defs><linearGradient id="wash" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{surface}"/></linearGradient><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{muted}" stroke-opacity=".07"/></pattern></defs>'
    def frame(w,h):
        return defs+f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#wash)" stroke="{border}"/>'
    def rule(x,y,w):
        return f'<path d="M{x} {y}h{w}" stroke="{border}"/>'
    def box(x,y,w,h,label,color=accent):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{bg}" stroke="{border}"/>'+text(x+w/2,y+h/2+4,label,color,12,'text-anchor="middle"')

    body=frame(960,400)+f'<rect x="590" y="64" width="340" height="270" fill="url(#grid)"/>'
    body+=text(32,34,'DX / LAB',accent,12,'letter-spacing="2"')+text(928,34,'PERSONAL ENGINEERING NOTEBOOK',muted,11,'text-anchor="end" letter-spacing="1"')+rule(32,52,896)
    body+=text(40,105,'BACKEND DEVELOPMENT / SYSTEM EXPLORATION',muted,12)
    body+=text(35,188,'DX4GREY',fg,78,'font-weight="700" letter-spacing="-4"')
    body+=text(40,229,'Close to the metal.',fg,22)+text(40,260,'Open to discovery.',muted,22)
    body+=box(40,291,115,30,'INDONESIA')+box(165,291,145,30,'OPEN SOURCE')
    # Layered orbital schematic: decorative, with no invented telemetry.
    for r in (48,83,119):
        body+=f'<circle cx="763" cy="204" r="{r}" fill="none" stroke="{border}"/>'
    for r,dur,angle in [(119,38,360),(83,26,-360)]:
        body+=f'<g class="motion"><circle cx="763" cy="204" r="{r}" fill="none" stroke="{accent}" stroke-dasharray="36 12 4 695"/><circle cx="{763+r}" cy="204" r="3" fill="{blue}"/><animateTransform attributeName="transform" type="rotate" from="0 763 204" to="{angle} 763 204" dur="{dur}s" repeatCount="indefinite"/></g>'
    body+=box(730,171,66,66,'</>')
    for x,y,label in [(610,92,'LINUX'),(837,278,'EMBEDDED')]:
        body+=box(x,y,90,28,label)
    body+=f'<path d="M655 120V147H730M808 232H882V278" fill="none" stroke="{border}"/>'+tracer('M655 120V147H730',accent,8)+tracer('M808 232H882V278',blue,10)
    body+=rule(32,348,896)
    for x,label in [(40,'01 / SYSTEMS'),(344,'02 / HARDWARE'),(648,'03 / SECURITY LEARNING')]:
        body+=text(x,378,label,muted,12)
    write('hero',suffix,'DX4GREY — backend development and system exploration',body,960,400)

    body=frame(960,246)
    sections=[('SYSTEMS','Linux customization','Kernel experiments'),('EMBEDDED','Arduino / ESP projects','Hardware experiments'),('SECURITY LEARNING','Network analysis','Defensive practices')]
    for i,(title,a,b) in enumerate(sections):
        x=24+i*312
        if i:body+=f'<path d="M{x-12} 24V222" stroke="{border}"/>'
        body+=text(x+8,45,f'0{i+1} / EXPLORATION',muted,11)
        body+=text(x+8,84,title,fg,18,'font-weight="700"')
        body+=text(x+8,119,a,muted,14)+text(x+8,143,b,muted,14)
        for j in range(6):
            xx=x+12+j*42
            body+=f'<circle cx="{xx}" cy="186" r="4" fill="{accent}" opacity=".25"/>'
        body+=tracer(f'M{x+12} 186h210',blue,9+i*2)
        body+=text(x+8,220,'LEARN / EXPERIMENT / DOCUMENT',accent,10)
    write('focus-desktop',suffix,'Systems, embedded hardware and security learning',body,960,246)
    # Match the information on small screens with a vertical composition.
    body=frame(360,510)
    for i,(title,a,b) in enumerate(sections):
        y=24+i*166
        body+=text(24,y+20,title,accent,16)+text(24,y+56,a,fg,15)+text(24,y+82,b,muted,15)+tracer(f'M24 {y+119}H336',accent,10+i)
    write('focus-mobile',suffix,'Systems, embedded hardware and security learning',body,360,510)

    for name,title,subtitle,description in [
        ('nizaw','Nizaw','LINUX / C++20','System and CLI framework'),
        ('rf','ESP32 RF Suite','ESP32-S3 / DUAL nRF24L01+','2.4 GHz RF analyzer')]:
        body=frame(960,278)+text(32,37,'SELECTED PROJECT / '+('01' if name=='nizaw' else '02'),accent,11,'letter-spacing="2"')
        body+=text(32,93,title,fg,34,'font-weight="700"')+text(32,130,description,muted,17)+text(32,164,subtitle,accent,12)
        body+=rule(32,193,384)+text(32,226,'EXPLORE REPOSITORY  ↗',fg,12)
        body+=f'<path d="M460 28V250" stroke="{border}"/>'
        if name=='nizaw':
            body+=text(494,42,'SYSTEMS / CONCEPTUAL VIEW',muted,10)
            body+=box(508,69,170,44,'COMMAND LINE')+box(730,69,192,44,'C++20 FRAMEWORK')
            body+=box(594,174,240,44,'LINUX SYSTEM')
            for path in ['M678 91H730','M826 113V145H714V174','M594 196H536V113']:
                body+=f'<path d="{path}" fill="none" stroke="{border}"/>'+tracer(path,accent,10)
        else:
            body+=text(494,42,'RF / ILLUSTRATIVE SIGNAL',muted,10)
            for y in (86,119,152,185):body+=rule(500,y,416)
            points=' '.join(f'{500+i*8},{172-((i*17)%67)}' for i in range(53))
            body+=f'<polyline points="{points}" fill="none" stroke="{blue}" stroke-width="1.5" opacity=".65"/>'
            body+=f'<path class="motion" d="M500 66V188" stroke="{accent}" opacity=".5"><animateTransform attributeName="transform" type="translate" from="0 0" to="416 0" dur="9s" repeatCount="indefinite"/></path>'
            body+=text(500,222,'SCAN / WATERFALL / LOG / DIAGNOSTICS',accent,11)
        body+=tracer('M32 255H928',accent,16)
        write('project-'+name+'-desktop',suffix,title+' — '+description+'; illustrative diagram',body,960,278)

    body=frame(960,138)
    labels=[('C++20','SYSTEMS'),('Linux','PLATFORM'),('ESP32-S3','CONTROLLER'),('nRF24L01+','RADIO'),('Arduino','EMBEDDED')]
    for i,(label,category) in enumerate(labels):
        x=24+i*187
        if i:body+=f'<path d="M{x-10} 22V115" stroke="{border}"/>'
        body+=text(x,37,category,muted,10)+text(x,75,label,fg,20)
        body+=tracer(f'M{x} 105h138',accent,9+i)
    write('stack-desktop',suffix,', '.join(x[0] for x in labels),body,960,138)
    body=frame(360,340)
    for i,(label,category) in enumerate(labels):
        y=38+i*62
        body+=text(24,y,label,fg,18)+text(336,y,category,muted,10,'text-anchor="end"')+tracer(f'M24 {y+18}H336',accent,10+i)
    write('stack-mobile',suffix,', '.join(x[0] for x in labels),body,360,340)
