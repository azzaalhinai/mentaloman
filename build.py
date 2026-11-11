"""Generates the static pages. Run: python build.py <folder of the old site> (it reads the legal text and Arabic news from there)."""
import html, json, re, sys
from pathlib import Path

OLD = Path(sys.argv[1]); OUT = Path(__file__).parent
DRIVE = 'https://drive.google.com/file/d/%s/view?usp=sharing'
SOP, NPO = DRIVE % '1HyGzNke408sXkKrh53JZ4xeWUb0WkSJ3', DRIVE % '12xrXO9rFpLMXKvX7ZRHIPaxy2CXpV6gg'
TRAIN1, TRAIN2 = DRIVE % '1yeH0Q0s_hCUqoWCFJDdmLOZspeaX9H0k', DRIVE % '11pE22mypJZ4rKaxkZJVK4gl318pAKb7S'
EMAIL = 'azzaalhinai.moh@gmail.com'
MAP = 'https://www.google.com/maps/d/viewer?mid=1frkJr2AGwxv7CSSsHj_g3TFSi0qYcoUw'
EXT = 'target="_blank" rel="noopener"'
LEAF = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21 3C10 3 4 8 4 15c0 1.500.4 3 1 4l-2 2 1.400 1.400 2-2c1.200.800 2.600 1.100 4 1.100 7 0 10.600-7 10.600-18.500zM8 17c2-4 5-6.500 9-8-3.500 2-6 4.800-7.600 8.600L8 17z"/></svg>'
SOON = '<span class="soon"><span lang="en">Coming soon</span><span lang="ar">قريبًا</span></span>'

def t(en, ar): return f'<span lang="en">{en}</span><span lang="ar">{ar}</span>'
def b(tag, en, ar, attrs=''): return f'<{tag} lang="en" {attrs}>{en}</{tag}><{tag} lang="ar" {attrs}>{ar}</{tag}>'

NAV = [('index.html#about', 'About', 'عن المبادرة'), ('index.html#resources', 'Resources', 'الموارد'), ('index.html#cultural', 'Wellness', 'العافية'),
       ('index.html#stories', 'Stories', 'القصص'), ('index.html#services', 'Services', 'الخدمات'), ('index.html#contact', 'Contact', 'تواصل معنا')]

def page(name, title_en, body, extra=''):
    nav = ''.join(f'<a href="{h}">{t(e, a)}</a>' for h, e, a in NAV)
    links = lambda rows: '<ul>' + ''.join(f'<li><a href="{h}">{t(e, a)}</a></li>' for h, e, a in rows) + '</ul>'
    doc = f'''<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_en} | Dhofar Mental Wellness Initiative</title>
<meta name="description" content="Mental health resources, screening tools and support for Dhofar, Oman.">
<link rel="canonical" href="https://www.mentaloman.net/{"" if name=="index.html" else name}">
<script>(function(){{var s=function(k){{try{{return localStorage.getItem(k)}}catch(e){{}}}},l=s('lang')||(/^ar/i.test(navigator.language)?'ar':'en'),h=document.documentElement;h.lang=l;h.dir=l==='ar'?'rtl':'ltr';h.dataset.theme=s('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@600;700&family=Caveat:wght@400;600&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Aref+Ruqaa:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">{t('Skip to content', 'تخطَّ إلى المحتوى')}</a>
<header class="top"><div class="in">
<a class="logo" href="index.html">{LEAF}{t('Dhofar Wellness', 'عافية ظفار')}</a>
<nav class="nav" aria-label="Main">{nav}</nav>
<div class="tools">
<button class="tool" id="langBtn" type="button"><span lang="en" aria-label="التبديل إلى العربية">ع</span><span lang="ar" aria-label="Switch to English">EN</span></button>
<button class="tool" id="themeBtn" type="button" aria-label="Light or dark mode"><svg class="i-moon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21 14.500A9 9 0 0 1 9.500 3a9 9 0 1 0 11.500 11.500z"/></svg><svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.500"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.400 1.400M17.600 17.600 19 19M5 19l1.400-1.400M17.600 6.400 19 5"/></svg></button>
<button class="tool burger" id="burger" type="button" aria-label="Menu" aria-expanded="false">☰</button>
<a class="btn" href="index.html#contact">{t('Get support', 'اطلب الدعم')}</a>
</div></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="fgrid">
<div><a class="logo" href="index.html">{LEAF}{t('Dhofar Wellness', 'عافية ظفار')}</a>{b('p', 'Promoting mental health awareness and support in Dhofar, Oman.', 'نعزز الوعي بالصحة النفسية ودعمها في ظفار، عُمان.')}
<p><strong>{t('In an emergency, call', 'في حالات الطوارئ، اتصل على')} <a href="tel:9999" dir="ltr">9999</a></strong></p></div>
<div><h3>{t('Explore', 'استكشف')}</h3>{links(NAV[:5])}</div>
<div><h3>{t('Resources', 'الموارد')}</h3>{links([('screening.html', 'Screening tools', 'أدوات الفحص'), ('meditation.html', 'Meditation', 'التأمل'), ('guidelines.html', 'Guidelines', 'الإرشادات'), ('flowcharts.html', 'Flowcharts', 'المخططات'), ('training-materials.html', 'Training', 'التدريب'), ('news.html', 'News', 'الأخبار')])}</div>
<div><h3>{t('Contact', 'تواصل')}</h3><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="https://maps.app.goo.gl/Nxb3UMQnz2cRVhFw8" {EXT}>{t('Salalah, Oman', 'صلالة، عُمان')}</a></li></ul></div>
</div><div class="fend"><span>© 2025 {t('Dhofar Mental Wellness Initiative. All Rights Reserved.', 'مبادرة ظفار للعافية النفسية. جميع الحقوق محفوظة.')}</span>
<span><a href="privacy-policy.html">{t('Privacy Policy', 'سياسة الخصوصية')}</a> · <a href="terms-of-service.html">{t('Terms of Service', 'شروط الخدمة')}</a> · <a href="privacy-policy.html#cookies">{t('Cookies', 'ملفات تعريف الارتباط')}</a></span></div></div></footer>
{extra}<script src="assets/site.js"></script>
</body></html>'''
    (OUT / name).write_text(doc, encoding='utf-8')

def phero(crumb_en, crumb_ar, h_en, h_ar, lead_en='', lead_ar=''):
    lead = b('p', lead_en, lead_ar, 'class="lead"') if lead_en else ''
    return f'<section class="phero"><div class="wrap"><p class="crumbs"><a href="index.html">{t("Home", "الرئيسية")}</a> / {t(crumb_en, crumb_ar)}</p><h1>{t(h_en, h_ar)}</h1>{lead}</div></section>'

# ---------- home ----------
REEL = [('falls', '50% 55%', 'screening.html', 'Take a self-check', 'ابدأ فحصًا ذاتيًا'), ('cave', '50% 60%', 'meditation.html', 'Breathe and relax', 'تنفّس واسترخِ'),
        ('peaks', '70% 70%', 'guidelines.html', 'Care guidelines', 'إرشادات الرعاية'), ('cliff', '85% 60%', 'flowcharts.html', 'Care flowcharts', 'مخططات الرعاية'),
        ('falls', '12% 45%', 'training-materials.html', 'Training materials', 'مواد التدريب'), ('cave', '75% 75%', 'news.html', 'Mental health news', 'أخبار الصحة النفسية'),
        ('falls', '60% 95%', 'index.html#services', 'Find services', 'ابحث عن الخدمات'), ('cliff', '30% 70%', 'index.html#cultural', 'Wellness practices', 'ممارسات العافية'),
        ('peaks', '20% 80%', 'index.html#stories', 'Community stories', 'قصص المجتمع'), ('falls', '95% 50%', 'index.html#contact', 'Talk to us', 'تحدث إلينا')]
reel = ''.join(f'<a class="rc" href="{h}" draggable="false"><img src="assets/img/{i}.webp" alt="" style="object-position:{p};animation-delay:-{n * 3}s" draggable="false"><b>{t(e, a)}</b><i></i></a>' for n, (i, p, h, e, a) in enumerate(REEL))

RES = [('clinical', 'guidelines.html', 'Healthcare Guidelines', 'الإرشادات الصحية', 'Official guidelines for mental health diagnostics and treatment protocols for practitioners.', 'إرشادات رسمية لتشخيص الصحة النفسية وبروتوكولات العلاج للممارسين.', 'Access guidelines', 'عرض الإرشادات'),
       ('clinical', 'flowcharts.html', 'Care Flowcharts', 'مخططات الرعاية', 'Standardized care pathways and decision-making flowcharts for mental health conditions.', 'مسارات رعاية موحدة ومخططات لاتخاذ القرار في حالات الصحة النفسية.', 'View flowcharts', 'عرض المخططات'),
       ('edu', 'training-materials.html', 'Training Materials', 'مواد التدريب', 'Professional development resources for mental health workers and community supporters.', 'موارد للتطوير المهني للعاملين في الصحة النفسية وداعمي المجتمع.', 'Access training', 'الوصول إلى التدريب'),
       ('edu', None, 'Educational Materials', 'المواد التعليمية', 'Literature, guides and fact sheets about mental health topics relevant to the Dhofar community.', 'منشورات وأدلة وصحائف وقائع عن موضوعات الصحة النفسية التي تهم مجتمع ظفار.', '', ''),
       ('clinical', 'screening.html', 'Assessment Tools', 'أدوات التقييم', 'Screening and assessment instruments you can complete privately in your browser.', 'أدوات فحص وتقييم يمكنك إكمالها بخصوصية في متصفحك.', 'View tools', 'عرض الأدوات'),
       ('well', 'meditation.html', 'Meditation & Relaxation', 'التأمل والاسترخاء', 'Guided meditation recordings, relaxation exercises and stress management techniques.', 'تسجيلات تأمل موجه وتمارين استرخاء وأساليب لإدارة التوتر.', 'Start practice', 'ابدأ التمرين'),
       ('well', '#services', 'Mental Health Services', 'خدمات الصحة النفسية', 'Mental health professionals, facilities and support services in Dhofar.', 'مختصو الصحة النفسية والمرافق وخدمات الدعم في ظفار.', 'Find services', 'ابحث عن الخدمات'),
       ('edu', 'news.html', 'Oman Mental Health Research', 'أبحاث الصحة النفسية في عُمان', 'Publications, research and mental health updates specific to Oman.', 'منشورات وأبحاث ومستجدات الصحة النفسية الخاصة بعُمان.', 'Explore research', 'استكشف الأبحاث')]
def res_card(c, h, te, ta, de, da, ge, ga):
    inner = f'<div class="ico">{te[0]}</div><h3>{t(te, ta)}</h3><p>{t(de, da)}</p>'
    return f'<a class="card rv" data-c="{c}" href="{h}">{inner}<span class="go">{t(ge, ga)}</span></a>' if h else f'<div class="card rv" data-c="{c}">{inner}{SOON}</div>'
chips = lambda rows, target: f'<div class="chips" data-for="{target}">' + ''.join(f'<button class="chip" type="button" data-f="{f}" aria-pressed="{str(i == 0).lower()}">{t(e, a)}</button>' for i, (f, e, a) in enumerate(rows)) + '</div>'

PRACTICE = [('Mindfulness & Meditation', 'اليقظة الذهنية والتأمل', 'Traditional meditation techniques adapted to address contemporary mental health challenges.', 'أساليب تأمل تقليدية مُكيَّفة لمواجهة تحديات الصحة النفسية المعاصرة.'),
            ('Community Gatherings', 'اللقاءات المجتمعية', 'Structured social engagement activities that foster connection and belonging.', 'أنشطة اجتماعية منظمة تعزز التواصل والانتماء.'),
            ('Nature Immersion', 'الانغماس في الطبيعة', "Therapeutic practices that utilize Dhofar's natural landscape for mental restoration.", 'ممارسات علاجية تستفيد من طبيعة ظفار لاستعادة الصفاء الذهني.'),
            ('Creative Expression', 'التعبير الإبداعي', 'Art therapy incorporating traditional Omani artistic elements and patterns.', 'علاج بالفن يوظف العناصر والزخارف الفنية العُمانية التقليدية.')]
STORY = [('The cultural wellness program helped me reconnect with traditional practices while addressing my anxiety. The blend of old and new approaches created a comfortable path to healing.', 'ساعدني برنامج العافية الثقافية على إعادة التواصل مع الممارسات التقليدية أثناء التعامل مع قلقي. وقد صنع المزج بين القديم والجديد طريقًا مريحًا للتعافي.', 'Fatima', 'فاطمة', 'Program Participant', 'مشاركة في البرنامج'),
         ('After struggling with isolation during the pandemic, the community support group became my lifeline. The facilitators understood our cultural context while offering effective coping strategies.', 'بعد معاناتي مع العزلة أثناء الجائحة، أصبحت مجموعة الدعم المجتمعي طوق نجاة لي. فهم الميسرون سياقنا الثقافي وقدموا استراتيجيات فعالة للتأقلم.', 'Ahmed', 'أحمد', 'Support Group Member', 'عضو مجموعة دعم'),
         ('As a parent, I was worried about discussing mental health with my children. The family workshop gave me the vocabulary and confidence to have these important conversations in a culturally appropriate way.', 'كنت قلقة بصفتي أمًا من الحديث مع أطفالي عن الصحة النفسية. منحتني ورشة الأسرة المفردات والثقة لإجراء هذه الأحاديث المهمة بطريقة تناسب ثقافتنا.', 'Layla', 'ليلى', 'Workshop Participant', 'مشاركة في الورشة')]

home = f'''
<section class="hero"><div class="frame">
<p class="badge">{t('Mental Health in Oman', 'الصحة النفسية في عُمان')}</p>
<h1><span lang="en"><span class="l">Inspiring a Culture of</span><span class="l l2">Mental Wellness in Oman</span></span><span lang="ar"><span class="l">نُلهم ثقافة</span><span class="l l2">العافية النفسية في عُمان</span></span></h1>
<p class="sub"><span lang="en"><span class="l">Breaking barriers and building hope. Find resources, self-care</span><span class="l">strategies and scientific learning, thoughtfully tailored</span><span class="l">to help you stay resilient.</span></span><span lang="ar"><span class="l">نكسر الحواجز ونبني الأمل. اكتشف موارد واستراتيجيات للعناية بالذات</span><span class="l">ومواد علمية أُعدّت بعناية لتناسب احتياجاتك</span><span class="l">وتساعدك على الصمود.</span></span></p>
<svg class="doodle deco abs" style="--x:263;--y:377;width:calc(46*var(--u));height:calc(44*var(--u))" viewBox="0 0 46 44" aria-hidden="true"><path d="M14 4 4 40"/><path d="M38 4 28 40"/></svg>
<div class="hand deco abs" style="--x:1212;--y:310;transform:rotate(16deg)" aria-hidden="true">{t('Breathe<br>with Dhofar', 'تنفّس<br>مع ظفار')}</div>
<svg class="doodle deco abs" style="--x:1215;--y:395;width:calc(130*var(--u));height:calc(120*var(--u))" viewBox="0 0 130 120" aria-hidden="true"><path d="M78 4C122 28 118 72 42 106"/><path d="M60 88 42 106 68 112"/></svg>
<div class="stage" aria-label="Featured sections">{reel}</div>
<div class="ring"><a class="btn" href="screening.html">{t('Take a self-check', 'ابدأ فحصًا ذاتيًا')}</a></div>
<div class="hand zero abs" style="--x:470;--y:937;transform:rotate(24deg)">{t('Free &amp; private', 'مجاني وخاص')}</div>
<svg class="doodle deco abs" style="--x:560;--y:925;width:calc(58*var(--u));height:calc(40*var(--u))" viewBox="0 0 58 40" aria-hidden="true"><path d="M4 30C20 34 38 28 52 12"/><path d="M36 12 52 12 52 28"/></svg>
</div></section>

<section id="about"><div class="wrap split">
<div class="shot rv"><img src="assets/img/cliff.webp" alt="Mist over the sea beside a coastal cliff" loading="lazy"></div>
<div class="rv"><span class="eyebrow">{t('About our initiative', 'عن مبادرتنا')}</span>
<h2>{t('Breaking barriers, building hope', 'نكسر الحواجز ونبني الأمل')}</h2>
{b('p', 'We are here to uplift and support you. We recognize the unique challenges you face and the toll they can take on your mental well-being. Discover resources, self-care strategies, educational materials and scientific lectures, all thoughtfully tailored to help you stay resilient while continuing to deliver exceptional care.', 'نحن هنا لدعمك ورفع معنوياتك. ندرك التحديات الفريدة التي تواجهها وأثرها في صحتك النفسية. اكتشف الموارد واستراتيجيات العناية بالذات والمواد التعليمية والمحاضرات العلمية، وقد أُعدّت جميعها بعناية لتساعدك على الصمود ومواصلة تقديم رعاية متميزة.', 'class="lead"')}
{b('p', 'Founded by mental health professionals and community leaders, our initiative bridges traditional cultural practices with modern psychological approaches.', 'أسس مبادرتنا مختصون في الصحة النفسية وقادة مجتمعيون، وهي تربط الممارسات الثقافية التقليدية بالأساليب النفسية الحديثة.', 'class="lead"')}
<div class="feats">
<div class="feat"><h3>{t('Community support', 'الدعم المجتمعي')}</h3><p>{t('Building networks of care within neighborhoods', 'بناء شبكات رعاية داخل الأحياء')}</p></div>
<div class="feat"><h3>{t('Professional care', 'الرعاية المهنية')}</h3><p>{t('Access to qualified mental health practitioners', 'الوصول إلى ممارسين مؤهلين في الصحة النفسية')}</p></div>
<div class="feat"><h3>{t('Education', 'التثقيف')}</h3><p>{t('Raising awareness through workshops and programs', 'رفع الوعي عبر الورش والبرامج')}</p></div>
</div></div></div></section>

<section id="resources" style="padding-top:0"><div class="wrap">
<div class="head"><div><span class="eyebrow">{t('Resources &amp; services', 'الموارد والخدمات')}</span><h2>{t('Support, in one place', 'الدعم في مكان واحد')}</h2></div>
{chips([('all', 'All', 'الكل'), ('clinical', 'Clinical', 'سريرية'), ('edu', 'Educational', 'تعليمية'), ('well', 'Wellness', 'العافية')], '#resGrid .card')}</div>
<div class="grid" id="resGrid">{''.join(res_card(*r) for r in RES)}</div></div></section>

<section id="cultural" class="dark"><img src="assets/img/falls.webp" alt="" loading="lazy"><div class="wrap"><span class="eyebrow">{t('Wellness practices', 'ممارسات العافية')}</span>
<h2 style="max-width:20ch">{t('Elevating mental health through professional excellence and modern care', 'الارتقاء بالصحة النفسية عبر التميز المهني والرعاية الحديثة')}</h2>
<div class="practice">{''.join(f'<div class="rv"><span>0{i + 1}</span><h3>{t(a, b_)}</h3><p>{t(c, d)}</p></div>' for i, (a, b_, c, d) in enumerate(PRACTICE))}</div></div></section>

<section id="stories"><div class="wrap"><div class="head"><div><span class="eyebrow">{t('Success stories', 'قصص نجاح')}</span><h2>{t('Journeys of growth and healing', 'رحلات من النمو والتعافي')}</h2></div></div>
<div class="grid">{''.join(f'<figure class="card rv" style="margin:0"><blockquote>{t(q, qa)}</blockquote><figcaption class="who">{t(n, na)}<small>{t(r, ra)}</small></figcaption></figure>' for q, qa, n, na, r, ra in STORY)}</div>
{b('p', 'Illustrative stories.', 'قصص توضيحية.', 'class="tag"')}</div></section>

<section id="services" style="padding-top:0"><div class="wrap"><div class="head"><div><span class="eyebrow">{t('Mental health services', 'خدمات الصحة النفسية')}</span><h2>{t('Find support near you', 'ابحث عن الدعم بالقرب منك')}</h2>
{b('p', 'Hospitals, clinics, support groups and school counseling across Dhofar. Select a location on the map to learn more.', 'مستشفيات وعيادات ومجموعات دعم وإرشاد مدرسي في أنحاء ظفار. اختر موقعًا على الخريطة لمعرفة المزيد.', 'class="lead"')}</div>
<a class="btn ghost" href="{MAP}" {EXT}>{t('Open full map', 'افتح الخريطة كاملة')}</a></div>
<div class="map rv"><iframe src="https://www.google.com/maps/d/embed?mid=1frkJr2AGwxv7CSSsHj_g3TFSi0qYcoUw&amp;ehbc=2E312F" title="Map of mental health services in Dhofar" loading="lazy"></iframe></div></div></section>

<section id="contact" style="padding-top:0"><div class="wrap">
<div class="sos rv"><strong>{t('In a crisis or emergency?', 'في أزمة أو حالة طارئة؟')}</strong><span>{t('Call the Royal Oman Police or go to the nearest emergency department.', 'اتصل بشرطة عُمان السلطانية أو توجّه إلى أقرب قسم طوارئ.')}</span><a class="num" href="tel:9999">9999</a></div>
<div class="split" style="align-items:start"><div class="rv"><span class="eyebrow">{t('Contact us', 'تواصل معنا')}</span><h2>{t('Reach out for information or support', 'تواصل معنا للمعلومات أو الدعم')}</h2>
<div class="docs" style="margin-top:22px"><a href="https://maps.app.goo.gl/Nxb3UMQnz2cRVhFw8" {EXT}>{t('Directorate General of Health Services, Dhofar Governorate, Salalah', 'المديرية العامة للخدمات الصحية بمحافظة ظفار، صلالة')}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<form class="card rv" id="contactForm" data-to="{EMAIL}" style="align-items:stretch">
<label>{t('Your name', 'اسمك')}<input name="name" required autocomplete="name"></label><label>{t('Your email', 'بريدك الإلكتروني')}<input name="email" type="email" required autocomplete="email" dir="ltr"></label>
<label>{t('Subject', 'الموضوع')}<input name="subject" required></label><label>{t('Message', 'الرسالة')}<textarea name="message" rows="5" required></textarea></label>
<button class="btn" type="submit">{t('Open in my email app', 'افتح في تطبيق البريد')}</button></form></div></div></section>'''
page('index.html', 'Home', home)

# ---------- guidelines ----------
GEN = [('Patient-Centered Care', 'الرعاية المتمحورة حول المريض', "Practitioners should prioritize patient-centered approaches that respect individual needs, preferences and cultural backgrounds.", 'ينبغي للممارسين تقديم الأساليب المتمحورة حول المريض التي تحترم احتياجات الفرد وتفضيلاته وخلفيته الثقافية.',
        [("Involve patients in treatment planning and decision-making", 'إشراك المرضى في تخطيط العلاج واتخاذ القرار'), ("Respect patients' autonomy and preferences", 'احترام استقلالية المرضى وتفضيلاتهم'), ('Consider family dynamics within cultural context', 'مراعاة ديناميكيات الأسرة ضمن السياق الثقافي')]),
       ('Confidentiality and Privacy', 'السرية والخصوصية', 'Maintaining confidentiality is essential to trust and ethical practice, while balancing cultural expectations and safety concerns.', 'الحفاظ على السرية أساس الثقة والممارسة الأخلاقية، مع الموازنة بين التوقعات الثقافية واعتبارات السلامة.',
        [('Secure storage of patient information', 'تخزين معلومات المرضى بأمان'), ('Clear communication about confidentiality limits', 'التواصل الواضح بشأن حدود السرية'), ('Culturally sensitive approach to family involvement', 'نهج مراعٍ للثقافة في إشراك الأسرة')])]
DIAG = [('Depression', 'الاكتئاب', 'PHQ-9 (Omani version), Beck Depression Inventory', 'PHQ-9 (النسخة العمانية)، مقياس بيك للاكتئاب', 'Consider somatic expressions of distress common in Omani culture', 'مراعاة التعبيرات الجسدية عن الضيق الشائعة في الثقافة العمانية'),
        ('Anxiety Disorders', 'اضطرابات القلق', 'GAD-7 (Omani version), Hamilton Anxiety Rating Scale', 'GAD-7 (النسخة العمانية)، مقياس هاملتون للقلق', 'Address religious and cultural expressions of anxiety', 'التعامل مع التعبيرات الدينية والثقافية عن القلق'),
        ('Trauma-Related Disorders', 'الاضطرابات المرتبطة بالصدمات', 'PCL-5 (Adapted), Trauma Symptom Inventory', 'PCL-5 (مُكيَّف)، قائمة أعراض الصدمة', 'Consider collective trauma experiences and community resilience factors', 'مراعاة تجارب الصدمة الجماعية وعوامل صمود المجتمع')]
def support():
    return f'''<section style="padding-top:0"><div class="wrap"><div class="card rv" style="padding:clamp(26px,5vw,56px)"><h2>{t('Implementation support', 'دعم التطبيق')}</h2>
{b('p', 'Our team offers training, consultation and ongoing support for mental health practitioners in the Dhofar region.', 'يقدم فريقنا التدريب والاستشارات والدعم المستمر لممارسي الصحة النفسية في منطقة ظفار.', 'class="lead"')}
<div class="btns"><a class="btn" href="index.html#contact">{t('Request training', 'اطلب تدريبًا')}</a><a class="btn ghost" href="index.html#contact">{t('Schedule consultation', 'حدد موعد استشارة')}</a></div></div></div></section>'''
guide = phero('Guidelines', 'الإرشادات', 'Healthcare Guidelines', 'الإرشادات الصحية', 'Official guidelines for mental health practitioners in Dhofar, aligned with international standards and culturally adapted for the Omani context.', 'إرشادات رسمية لممارسي الصحة النفسية في ظفار، متوافقة مع المعايير الدولية ومُكيَّفة ثقافيًا للسياق العماني.') + f'''
<section><div class="wrap"><div class="head"><h2>{t('Documents', 'الوثائق')}</h2></div><div class="docs rv">
<a href="{SOP}" {EXT}>{t('Standing Operating Procedures (SOP) and Checklist for Mental Health Services 2021', 'إجراءات التشغيل الموحدة وقائمة التحقق لخدمات الصحة النفسية 2021')}</a>
<a href="{NPO}" {EXT}>{t('NPO in Mental Health', 'NPO في الصحة النفسية')}</a>
<div class="d">{t('Guideline for Management of Mental Disorders in Primary Health Care 2020', 'دليل التعامل مع الاضطرابات النفسية في الرعاية الصحية الأولية 2020')}{SOON}</div>
<div class="d">{t('Treatment Approaches', 'أساليب العلاج')}{SOON}</div>
<div class="d">{t('Emergency Procedures', 'إجراءات الطوارئ')}{SOON}</div>
</div></div></section>
<section id="general" style="padding-top:0"><div class="wrap"><h2>{t('General guidelines', 'الإرشادات العامة')}</h2><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
{''.join(f'<div class="card rv"><h3>{t(a, b_)}</h3><p>{t(c, d)}</p><ul>' + ''.join(f'<li>{t(x, y)}</li>' for x, y in li) + '</ul></div>' for a, b_, c, d, li in GEN)}</div></div></section>
<section id="diagnostic" style="padding-top:0"><div class="wrap"><h2>{t('Diagnostic protocols', 'بروتوكولات التشخيص')}</h2>{b('p', 'Culturally adapted screening and assessment approaches.', 'أساليب فحص وتقييم مُكيَّفة ثقافيًا.', 'class="lead"')}
<div class="scroll rv"><table class="table"><thead><tr><th>{t('Condition', 'الحالة')}</th><th>{t('Recommended tools', 'الأدوات الموصى بها')}</th><th>{t('Cultural adaptations', 'التكييفات الثقافية')}</th></tr></thead><tbody>
{''.join(f'<tr><td>{t(a, b_)}</td><td>{t(c, d)}</td><td>{t(e, f)}</td></tr>' for a, b_, c, d, e, f in DIAG)}</tbody></table></div></div></section>''' + support()
page('guidelines.html', 'Healthcare Guidelines', guide)

# ---------- flowcharts ----------
CH = [('chart-pharma', 'Psychopharmacology Pocket Guide for Primary Care', 'دليل الجيب للأدوية النفسية في الرعاية الأولية', 'A quick reference for primary care physicians on psychotropic medication selection, dosing, monitoring and side effects.', 'مرجع سريع لأطباء الرعاية الأولية حول اختيار الأدوية النفسية وجرعاتها ومتابعتها وآثارها الجانبية.'),
      ('chart-5step', '5-Step Approach Flowchart', 'مخطط النهج ذي الخطوات الخمس', 'A structured five-step methodology for systematic mental health assessment in clinical practice.', 'منهجية منظمة من خمس خطوات للتقييم المنهجي للصحة النفسية في الممارسة السريرية.'),
      ('chart-integration', 'Integration of Mental Health at Primary Care', 'دمج الصحة النفسية في الرعاية الأولية', 'A framework for integrating mental health services into primary healthcare, adapted for the Omani healthcare system.', 'إطار لدمج خدمات الصحة النفسية في الرعاية الصحية الأولية، مُكيَّف للنظام الصحي العماني.')]
flow = phero('Flowcharts', 'المخططات', 'Care Flowcharts', 'مخططات الرعاية', 'Step-by-step care pathways for clinical decision-making. Select a flowchart to view it full screen.', 'مسارات رعاية خطوة بخطوة لاتخاذ القرار السريري. اختر مخططًا لعرضه بملء الشاشة.') + f'''
<section><div class="wrap"><div class="grid">{''.join(f'<button class="card chart rv" type="button"><img src="assets/img/{i}.webp" alt="{e}" loading="lazy"><div><h3>{t(e, a)}</h3><p>{t(d, da)}</p><span class="go">{t("View full", "عرض كامل")}</span></div></button>' for i, e, a, d, da in CH)}</div></div></section>''' + support()
page('flowcharts.html', 'Care Flowcharts', flow, f'<dialog aria-label="Flowchart"><header><button class="btn ghost" type="button">{t("Close", "إغلاق")}</button></header><img alt=""></dialog>')

# ---------- training ----------
TR = [(TRAIN1, 'Professional Development Guide', 'دليل التطوير المهني', 'Comprehensive training for mental health professionals working in Oman, including cultural considerations, best practices and intervention techniques.', 'تدريب شامل لمختصي الصحة النفسية العاملين في عُمان، يشمل الاعتبارات الثقافية وأفضل الممارسات وأساليب التدخل.'),
      (TRAIN2, 'Community Support Training', 'تدريب الدعم المجتمعي', 'Train and empower non-specialists, extend the reach of mental health initiatives and build more resilient communities.', 'تدريب غير المتخصصين وتمكينهم، وتوسيع نطاق مبادرات الصحة النفسية، وبناء مجتمعات أكثر صمودًا.'),
      (None, 'Mental Health First Aid', 'الإسعافات الأولية النفسية', 'Basic training on providing initial help to people experiencing mental health problems or crises until professional help is received.', 'تدريب أساسي على تقديم المساعدة الأولية لمن يعانون مشكلات أو أزمات نفسية إلى أن يتلقوا المساعدة المهنية.'),
      (None, 'Cultural Competency Training', 'تدريب الكفاءة الثقافية', 'Delivering culturally appropriate mental health support in the Omani context, addressing local customs and practices.', 'تقديم دعم نفسي مناسب ثقافيًا في السياق العماني، مع مراعاة العادات والممارسات المحلية.')]
TIPS = [('Allocate dedicated time to go through the materials completely', 'خصص وقتًا لمراجعة المواد كاملة'), ('Take notes on important concepts and techniques', 'دوّن المفاهيم والأساليب المهمة'), ('Practice the skills with colleagues or in a supervised setting', 'تدرب على المهارات مع الزملاء أو تحت الإشراف'), ('Revisit the materials regularly to reinforce your learning', 'راجع المواد بانتظام لترسيخ التعلم'), ('Reach out to us with any questions or for additional support', 'تواصل معنا لأي استفسار أو دعم إضافي')]
train = phero('Training', 'التدريب', 'Training Materials', 'مواد التدريب', 'Resources for professionals, community supporters and anyone interested in mental health education in Oman.', 'موارد للمختصين وداعمي المجتمع وكل من يهتم بالتثقيف في الصحة النفسية في عُمان.') + f'''
<section><div class="wrap"><div class="grid">{''.join((f'<a class="card rv" href="{h}" {EXT}><h3>{t(e, a)}</h3><p>{t(d, da)}</p><span class="go">{t("Access training", "الوصول إلى التدريب")}</span></a>' if h else f'<div class="card rv"><h3>{t(e, a)}</h3><p>{t(d, da)}</p>{SOON}</div>') for h, e, a, d, da in TR)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="card rv" style="padding:clamp(26px,5vw,56px)"><h2>{t('How to use these materials', 'كيفية استخدام هذه المواد')}</h2><ul>{''.join(f'<li>{t(x, y)}</li>' for x, y in TIPS)}</ul>
{b('p', 'Interested in group sessions or custom training? We would love to hear from you.', 'هل تهتم بجلسات جماعية أو تدريب مخصص؟ يسعدنا تواصلك معنا.')}<a class="btn" href="index.html#contact">{t('Contact us', 'تواصل معنا')}</a></div></div></section>'''
page('training-materials.html', 'Training Materials', train)

# ---------- meditation ----------
BEN = [('Stress reduction', 'تخفيف التوتر', 'Helps lower stress hormone levels and creates a sense of calm.', 'يساعد على خفض هرمونات التوتر ويمنح إحساسًا بالهدوء.'), ('Anxiety management', 'إدارة القلق', 'Techniques to manage anxiety and worry through mindful awareness.', 'أساليب لإدارة القلق عبر الوعي اليقظ.'), ('Improved sleep', 'نوم أفضل', 'Helps quiet the mind and prepare the body for restful sleep.', 'يساعد على تهدئة الذهن وتهيئة الجسم لنوم مريح.'), ('Enhanced mood', 'مزاج أفضل', 'Regular practice can help improve overall emotional well-being.', 'تساعد الممارسة المنتظمة على تحسين الصحة العاطفية عمومًا.')]
VID = [('tF1xYcMj0Tk', 'Calming Meditation Practice', 'تمرين تأمل مهدئ', 'A guided meditation focusing on breath awareness and relaxation.', 'تأمل موجه يركز على الوعي بالتنفس والاسترخاء.'), ('EbMWfKS0W6Q', 'Mindfulness for Anxiety', 'اليقظة الذهنية للقلق', 'Grounding and present-moment awareness techniques to help manage anxiety.', 'أساليب للتركيز والوعي باللحظة الحاضرة للمساعدة على إدارة القلق.'), ('vTIxOw2XMe8', 'Evening Relaxation Session', 'جلسة استرخاء مسائية', 'A gentle practice for the evening wind-down that prepares you for restful sleep.', 'تمرين لطيف لنهاية اليوم يهيئك لنوم مريح.')]
med = phero('Meditation', 'التأمل', 'Meditation &amp; Relaxation', 'التأمل والاسترخاء', 'Simple guided practices that can help reduce stress and anxiety and fit into your daily routine.', 'تمارين موجهة بسيطة تساعد على تخفيف التوتر والقلق ويمكن إدراجها في روتينك اليومي.') + f'''
<section><div class="wrap"><div class="grid">{''.join(f'<div class="card rv"><h3>{t(a, b_)}</h3><p>{t(c, d)}</p></div>' for a, b_, c, d in BEN)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(320px,1fr))">{''.join(f'<article class="card vcard rv"><iframe class="video" src="https://www.youtube-nocookie.com/embed/{v}" title="{e}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe><div><h3>{t(e, a)}</h3><p>{t(d, da)}</p></div></article>' for v, e, a, d, da in VID)}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="card rv" style="padding:clamp(26px,5vw,56px)"><h2>{t('Practice tips', 'نصائح للممارسة')}</h2>{b('p', 'Practice regularly in a quiet, comfortable space. Start with a few minutes each day and gradually increase your time. Meditation is a skill that improves with consistency.', 'مارس بانتظام في مكان هادئ ومريح. ابدأ ببضع دقائق يوميًا وزد الوقت تدريجيًا. التأمل مهارة تتحسن بالمواظبة.', 'class="lead"')}
<div class="btns"><a class="btn" href="index.html#resources">{t('Explore more resources', 'استكشف المزيد من الموارد')}</a><a class="btn ghost" href="index.html#contact">{t('Contact us', 'تواصل معنا')}</a></div></div></div></section>'''
page('meditation.html', 'Meditation & Relaxation', med)

# ---------- news ----------
src = (OLD / 'news.html').read_text(encoding='utf8')
en, ar = {}, {}
for k, v in re.findall(r'"(news_(?:title|excerpt)_\d)": "([^"]+)"', src):
    (ar if re.search('[؀-ۿ]', v) else en)[k] = v
NEWS = [('initiative', 'May 12, 2023', 'falls'), ('services', 'April 28, 2023', 'cave'), ('services', 'April 15, 2023', 'cliff'), ('research', 'March 30, 2023', 'peaks'), ('services', 'March 15, 2023', 'falls'), ('education', 'February 28, 2023', 'cave'), ('services', 'February 10, 2023', 'cliff'), ('education', 'January 25, 2023', 'peaks')]
LAB = {'initiative': ('Initiative', 'مبادرة'), 'services': ('Services', 'خدمات'), 'research': ('Research', 'أبحاث'), 'education': ('Education', 'تعليم')}
cards = ''.join(f'''<article class="card vcard rv" data-c="{c}"><img src="assets/img/{i}.webp" alt="" loading="lazy" style="width:100%;aspect-ratio:16/9;object-fit:cover;object-position:{20 + n * 10}% {30 + n * 7}%"><div><span class="soon" style="display:inline-block;margin-bottom:10px">{t(*LAB[c])}</span><p style="font-size:14px;margin:0 0 6px" dir="ltr" lang="en">{d}</p><h3>{t(en[f"news_title_{n + 1}"], ar[f"news_title_{n + 1}"])}</h3><p>{t(en[f"news_excerpt_{n + 1}"], ar[f"news_excerpt_{n + 1}"])}</p></div></article>''' for n, (c, d, i) in enumerate(NEWS))
news = phero('News', 'الأخبار', 'Mental Health News in Oman', 'أخبار الصحة النفسية في عُمان', 'Updates and developments in mental health initiatives across Oman.', 'مستجدات مبادرات الصحة النفسية في أنحاء عُمان.') + f'''
<section><div class="wrap"><div class="head">{chips([('all', 'All news', 'كل الأخبار'), ('initiative', 'Initiatives', 'المبادرات'), ('services', 'Services', 'الخدمات'), ('research', 'Research', 'الأبحاث'), ('education', 'Education', 'التعليم')], '#newsGrid .card')}</div><div class="grid" id="newsGrid">{cards}</div></div></section>'''
page('news.html', 'Mental Health News', news)

# ---------- screening ----------
TOOLS = [('phq4', 'PHQ-4', 'Brief screener for both depression and anxiety symptoms.', 'فحص سريع لأعراض الاكتئاب والقلق.', '~1 minute', 'نحو دقيقة'), ('phq9', 'PHQ-9', 'Screens for presence and severity of depression.', 'يفحص وجود الاكتئاب وشدته.', '~3 minutes', 'نحو 3 دقائق'), ('gad7', 'GAD-7', 'Screens for presence and severity of anxiety.', 'يفحص وجود القلق وشدته.', '~2 minutes', 'نحو دقيقتين')]
scr = phero('Screening', 'الفحص', 'Mental Health Screening Tools', 'أدوات فحص الصحة النفسية', 'These tools are not diagnostic, but can indicate when further evaluation may be beneficial.', 'هذه الأدوات ليست تشخيصية، لكنها قد تشير إلى متى يكون التقييم الإضافي مفيدًا.') + f'''
<section><div class="wrap steps"><p class="sos" style="font-size:15.5px">{t('Your privacy matters: everything is processed in your browser. Nothing is stored or sent to us.', 'خصوصيتك مهمة: تجري المعالجة كلها في متصفحك، ولا يُخزَّن أي شيء أو يُرسل إلينا.')}</p>
<div id="picker"><h2>{t('Select an assessment', 'اختر تقييمًا')}</h2><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(210px,1fr))">{''.join(f'<button class="card" type="button" data-tool="{k}"><div class="ico" style="width:auto;padding:0 12px">{n}</div><p>{t(d, da)}</p><span class="go">{t(m, ma)}</span></button>' for k, n, d, da, m, ma in TOOLS)}</div></div>
<div id="app" aria-live="polite"></div>
<div class="card" style="margin-top:34px"><h3>{t('Professional guidance', 'إرشاد مهني')}</h3><p>{t('These tools do not replace professional evaluation. If you or someone you know is having mental health difficulties, please reach out to a qualified healthcare provider.', 'لا تُغني هذه الأدوات عن التقييم المهني. إذا كنت أنت أو أحد معارفك تواجهون صعوبات نفسية، فيُرجى التواصل مع مقدم رعاية صحية مؤهل.')}</p>
<div class="btns"><a class="btn" href="index.html#services">{t('Find services', 'ابحث عن الخدمات')}</a><a class="btn ghost" href="index.html#contact">{t('Contact us', 'تواصل معنا')}</a></div></div></div></section>'''
page('screening.html', 'Screening Tools', scr, '<script src="assets/screening-data.js"></script><script src="assets/screening.js"></script>')

# ---------- legal: English text kept verbatim from the old site ----------
def legal(old, new, title, title_ar, summary_ar):
    s = (OLD / old).read_text(encoding='utf8')
    s = re.sub(r'<(script|style)[\s\S]*?</\1>|<footer[\s\S]*', '', s)
    s = s[s.index('Effective Date'):]
    s = s[:s.rindex('Back to Home')]
    s = s[:s.rindex('<a ')]
    s = re.sub(r'<i [^>]*></i>', '', s)
    s = re.sub(r'</?(div|section|main|span|article)\b[^>]*>', '', s)
    s = re.sub(r'<(?!a\b)(\w+)\b[^>]*>', r'<\1>', s)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>', r'<a href="\1">', s)
    s = re.sub(r'<h2>(\s*7\. Cookies)', r'<h2 id="cookies">\1', s)
    body = phero(title, title_ar, title, title_ar) + f'''<section><div class="wrap prose">
<div lang="ar"><p class="sos">ملخص بالعربية. النص الإنجليزي أدناه هو النص المعتمد.</p>{summary_ar}<hr style="margin:40px 0;border:0;border-top:1px solid var(--line)"></div>
<div dir="ltr" style="text-align:left"><p>{s}</div>
<a class="btn" href="index.html" style="margin-top:24px">{t('Back to home', 'العودة إلى الرئيسية')}</a></div></section>'''
    page(new, title, body)

legal('privacy-policy.html', 'privacy-policy.html', 'Privacy Policy', 'سياسة الخصوصية', f'''<p>نلتزم بحماية خصوصيتك والتعامل مع بياناتك بمسؤولية وفق قانون حماية البيانات الشخصية العماني (المرسوم السلطاني 6/2022).</p><ul><li>قد نجمع البيانات التي تقدمها طوعًا، مثل الاسم والبريد الإلكتروني، وبيانات استخدام غير شخصية.</li><li>نستخدم البيانات لتشغيل الموقع وتحسينه والرد على استفساراتك، ولا نبيع بياناتك الشخصية.</li><li>لك حق الوصول إلى بياناتك وتصحيحها ومحوها وتقييد معالجتها والاعتراض عليها ونقلها وسحب موافقتك.</li><li>الموقع غير موجَّه لمن هم دون 18 عامًا.</li></ul><p>للتواصل: <a href="mailto:{EMAIL}">{EMAIL}</a></p>''')
legal('terms-of-service.html', 'terms-of-service.html', 'Terms of Service', 'شروط الخدمة', f'''<p class="alert"><strong>إخلاء مسؤولية طبية:</strong> محتوى هذا الموقع لأغراض معلوماتية وتثقيفية فقط، ولا يُعد نصيحة طبية أو تشخيصًا أو علاجًا. إذا كنت تمر بأزمة نفسية أو حالة طارئة، فاتصل بشرطة عمان السلطانية على 9999 أو توجّه إلى أقرب قسم طوارئ فورًا.</p><ul><li>باستخدامك الموقع فإنك توافق على هذه الشروط وعلى سياسة الخصوصية.</li><li>يجب استخدام الموقع لأغراض مشروعة وشخصية وغير تجارية.</li><li>يخضع الموقع لقوانين سلطنة عُمان وتختص بنزاعاته محاكمها.</li></ul><p>للتواصل: <a href="mailto:{EMAIL}">{EMAIL}</a></p>''')
print('built')
