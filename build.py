import json,os
BASE="https://YOUR-PROJECT.vercel.app"  # <-- UPDATE after first deploy, then re-run: python3 build.py
T={ # slug:(h1,in,out,title,desc,intro)
"jfif-to-png":("Free JFIF to PNG Converter Online","jfif","png","JFIF to PNG Converter Online Free | PixelConvert","Convert JFIF to PNG online for free with PixelConvert. Convert multiple images in your browser, preview results, and download PNG files securely without uploading images.","Convert JFIF images to PNG online for free. Upload one image or multiple images, convert them instantly in your browser, and download your PNG files. No account or software installation required."),
"jpg-to-png":("JPG to PNG Converter","jpg","png","JPG to PNG Converter - Free Online | PixelConvert","Convert JPG and JPEG images to PNG online for free. Fast, private conversion in your browser with batch support and ZIP download.","Convert JPG or JPEG images to PNG in your browser. Upload several files at once and download them individually or as a ZIP."),
"png-to-jpg":("PNG to JPG Converter","png","jpg","PNG to JPG Converter - Free Online | PixelConvert","Convert PNG images to JPG online for free. Transparent areas become white. Private, in-browser conversion with batch and ZIP download.","Convert PNG images to JPG in your browser. Transparent areas are replaced with a white background."),
"webp-to-png":("WebP to PNG Converter","webp","png","WebP to PNG Converter - Free Online | PixelConvert","Convert WebP images to PNG online for free. Transparency is preserved. Private, in-browser conversion with batch and ZIP download.","Convert WebP images to PNG in your browser, keeping transparency. Nothing is uploaded."),
"jfif-to-jpg":("JFIF to JPG Converter","jfif","jpg","JFIF to JPG Converter - Free Online | PixelConvert","Convert JFIF files to JPG online for free. Re-encodes images in your browser with batch support and ZIP download.","Convert JFIF files to standard JPG images in your browser. No uploads, no account."),
}
FAQ=[("What is a JFIF file?","JFIF (JPEG File Interchange Format) is a container format for JPEG-compressed images. Many programs and some devices save images as .jfif, but not every app can open them."),
("How do I convert JFIF to PNG?","Select or drop your JFIF files, keep PNG as the output format, click Convert Images, then download each file or all as a ZIP."),
("Is PixelConvert free?","Yes. There is no account, subscription or watermark."),
("Can I convert multiple images?","Yes. Add as many files as your device can handle and convert them one after another."),
("Are my images uploaded?","No. Conversion runs in your browser and image data is not intentionally sent to any server."),
("Does converting an image reduce its file size?","Not necessarily. PNG is lossless and is often larger than JPG or JFIF files."),
("Why might a conversion fail?","The file may be corrupted, not really an image, unsupported by your browser, or too large for your device's memory."),
("Can I use PixelConvert on mobile?","Yes. It works in modern mobile browsers, though very large images may fail on low-memory phones.")]
RELATED=[("jpg-to-png","JPG to PNG Converter"),("png-to-jpg","PNG to JPG Converter"),("webp-to-png","WebP to PNG Converter"),("jfif-to-jpg","JFIF to JPG Converter")]
def ld(o):return '<script type="application/ld+json">'+json.dumps(o)+'</script>'
def head(title,desc,path):
    u=BASE+path
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{u}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#2563EB">
<meta property="og:type" content="website"><meta property="og:site_name" content="PixelConvert"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{u}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<link rel="stylesheet" href="/assets/css/style.css">'''
HDR='''</head><body%s><div id="pre" aria-hidden="true"><i></i>PixelConvert</div>
<header><div class="w bar"><a class="logo" href="/"><img src="/favicon.svg" alt="PixelConvert logo" width="28" height="28">PixelConvert</a>
<button id="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav id="nav" aria-label="Main"><a href="/">Home</a><a href="/jpg-to-png/">Image Converter</a><a href="/about">About</a><a href="/#faq">FAQ</a></nav></div></header><main class="w">'''
def faq():
    return '<section id="faq"><h2>Frequently asked questions</h2>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)+'</section>'
CONV='''<section class="card" id="converter" aria-label="Image converter"><div id="drop" class="drop"><p class="big">Drop your images here</p><p>or choose files from your device</p>
<button class="btn" id="pick" type="button">Select Images</button><input id="file" type="file" multiple hidden aria-label="Select images"></div>
<div class="ctl"><label>Input format<select id="in"><option value="any">Auto-detect</option><option value="jfif">JFIF</option><option value="jpg">JPG / JPEG</option><option value="png">PNG</option><option value="webp">WebP</option></select></label>
<label>Output format<select id="out"><option value="png">PNG</option><option value="jpg">JPG / JPEG</option><option value="webp">WebP</option></select></label>
<button class="btn" id="go" type="button">Convert Images</button><button class="btn s" id="clr" type="button" hidden>Clear All</button></div>
<p class="note" id="jnote" hidden>JPG does not support transparency. Transparent areas will be filled with white.</p>
<progress id="prog" hidden aria-label="Conversion progress"></progress><div id="status" role="status" aria-live="polite"></div><ul id="list"></ul>
<div class="row"><button class="btn" id="zip" type="button" hidden>Download All as ZIP</button><button class="btn s" id="more" type="button" hidden>Convert More Images</button></div>
<p class="priv">Your images stay on your device. Very large images may fail on low-memory devices.</p></section>'''
FOOT='''</main><footer><div class="w"><a href="/">Home</a><a href="/about">About</a><a href="/privacy">Privacy Policy</a><a href="/#faq">FAQ</a><p>© PixelConvert. Free browser-based image converter.</p></div></footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js" defer></script><script src="/assets/js/app.js" defer></script></body></html>'''
def w(path,s):
    os.makedirs(os.path.dirname(path) or '.',exist_ok=True);open(path,'w').write(s)
def tool(slug):
    h1,i,o,title,desc,intro=T[slug];home=slug=="jfif-to-png";path="/" if home else f"/{slug}/"
    steps='<h2>How it works</h2><ol><li>Select or drop your images.</li><li>Choose the output format.</li><li>Click Convert Images and download your files.</li></ol>'
    rel='<h2>Related tools</h2><ul>'+''.join(f'<li><a href="/{s}/">{n}</a></li>' for s,n in RELATED if s!=slug)+('' if home else '<li><a href="/">JFIF to PNG Converter</a></li>')+'</ul>'
    fmts='<h2>Supported formats</h2><p>Input: JFIF, JPG, JPEG, PNG and WebP, where your browser can decode them. Output: PNG, JPG or WebP. PNG files can be larger than the originals, and PNG keeps transparency.</p>'
    priv='<h2>Privacy</h2><p>Images are decoded and converted locally in your browser and are not intentionally uploaded. See the <a href="/privacy">Privacy Policy</a>.</p>'
    g=[{"@context":"https://schema.org","@type":"WebApplication","name":h1,"url":BASE+path,"applicationCategory":"MultimediaApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}]
    if home:
        g.append({"@context":"https://schema.org","@type":"WebSite","name":"PixelConvert","url":BASE+"/"})
        g.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]})
    else:
        g.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":h1,"item":BASE+path}]})
    body=head(title,desc,path)+''.join(ld(x) for x in g)+HDR%f' data-in="{i}" data-out="{o}"'+f'<section class="hero"><h1>{h1}</h1><p>{intro}</p><p class="priv">Your images stay on your device.</p></section>'+CONV+fmts+steps+priv+rel+faq()+FOOT
    w("index.html" if home else f"{slug}/index.html",body)
for s in T:tool(s)
def page(file,path,title,desc,h1,html):
    w(file,head(title,desc,path)+HDR%''+f'<section class="hero"><h1>{h1}</h1></section>{html}'+FOOT)
page("about.html","/about","About PixelConvert | Free Browser-Based Image Converter","Learn how PixelConvert converts images locally in your browser without uploading them.","About PixelConvert",'<p>PixelConvert is a free image converter for JFIF, JPG, PNG and WebP files. It was built to be simple, fast and private.</p><h2>How it works</h2><p>Your browser decodes the image, draws it on a canvas and re-encodes it in the format you choose. The result is a real converted file, not a renamed one. All of this happens on your device.</p><h2>Limits</h2><p>Browsers differ in the formats they can decode and export. Very large images depend on your device memory and may fail.</p>')
page("privacy.html","/privacy","Privacy Policy | PixelConvert","How PixelConvert handles your images and data.","Privacy Policy",'<p>Images you select are processed locally in your browser and are not intentionally uploaded to any server by PixelConvert.</p><h2>Third-party resources</h2><p>The ZIP feature loads the JSZip library from the cdnjs content delivery network (Cloudflare). Loading it may expose your IP address and browser details to that provider. The site is hosted on a static hosting provider (such as Vercel), which may keep standard server logs.</p><h2>What we do not add</h2><p>PixelConvert does not include analytics, advertising scripts, tracking pixels or cookies by default. Any change would be reflected on this page.</p>')
w("404.html",head("Page Not Found | PixelConvert","The page you requested could not be found.","/404").replace('<link rel="canonical"','<link rel="canonical"')+HDR%''+'<section class="hero"><h1>Page not found</h1><p>The page you are looking for does not exist. <a href="/">Go to the JFIF to PNG converter</a>.</p></section>'+FOOT)
paths=["/"]+[f"/{s}/" for s in T if s!="jfif-to-png"]+["/about","/privacy"]
w("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f"<url><loc>{BASE}{p}</loc></url>" for p in paths)+'</urlset>')
w("robots.txt",f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
w("vercel.json",json.dumps({"cleanUrls":True,"redirects":[{"source":"/jfif-to-png","destination":"/","permanent":True},{"source":"/jfif-to-png/","destination":"/","permanent":True}]},indent=2))
