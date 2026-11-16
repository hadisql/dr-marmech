"""Rebuild the static Arabic page. Fail on any untranslated French text."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = {
    'Le cabinet sur la carte': 'موقع العيادة على الخريطة',
    'Afficher le cabinet sur Google Maps': 'عرض موقع العيادة على Google Maps',
    'Localisation du cabinet du Dr Marmech Ilias à Casablanca sur Google Maps': 'موقع عيادة الدكتور مرمش إلياس بالدار البيضاء على Google Maps',
    'Politique de confidentialité de Google': 'سياسة الخصوصية لدى Google',
    'Ce site ne comporte aucun formulaire de collecte de données, aucun outil de suivi publicitaire et ne dépose aucun cookie applicatif. La carte intégrée est fournie par Google Maps : son chargement peut transmettre des données techniques à Google et permettre l’utilisation de cookies selon vos réglages Google. Les liens externes vous conduisent vers des services qui appliquent leurs propres règles de confidentialité. L’hébergeur peut traiter des journaux techniques de connexion.': 'لا يتضمن هذا الموقع أي استمارة لجمع البيانات أو أداة للتتبع الإعلاني، ولا يضع ملفات تعريف ارتباط خاصة بالتطبيق. الخريطة المضمّنة مقدّمة من Google Maps؛ وقد يؤدي تحميلها إلى إرسال بيانات تقنية إلى Google واستخدام ملفات تعريف ارتباط بحسب إعداداتكم لدى Google. تنقلكم الروابط الخارجية إلى خدمات تطبّق سياسات الخصوصية الخاصة بها. وقد يعالج مزوّد الاستضافة سجلات تقنية للاتصال.',
    'Les extraits d’avis présentés constituent une sélection manuelle de témoignages notés quatre ou cinq étoiles, conservée sur ce site. Ils ne représentent ni l’ensemble des avis ni une mise à jour en temps réel. Les traductions réalisées pour ce site sont signalées et le texte original reste accessible. Les avis sont intégrés directement au site. La carte Google Maps est un contenu externe, soumis à la politique de confidentialité de Google.': 'مقتطفات الآراء المعروضة هي اختيار يدوي من شهادات بتقييم أربع أو خمس نجوم، محفوظة على هذا الموقع. وهي لا تمثّل جميع الآراء ولا تُحدّث بشكل فوري. يُشار إلى الترجمات المنجزة لهذا الموقع ويبقى النص الأصلي متاحاً. الآراء مضمّنة مباشرة في الموقع. أما خريطة Google Maps فهي محتوى خارجي يخضع لسياسة الخصوصية لدى Google.',
    'Découvrez les avis des patients sur la fiche Google Maps du cabinet.': 'اطّلعوا على آراء المرضى على صفحة العيادة في Google Maps.',
    'Résidence Al Manzah, GH1 n°46, 1er étage, appartement n°2, boulevard Abdelkader Sahraoui — Casablanca 20660': 'إقامة المنزه، GH1 رقم 46، الطابق الأول، الشقة رقم 2، شارع عبد القادر الصحراوي — الدار البيضاء 20660',

    'Le Dr Marmech Ilias vous accueille dans son cabinet d’ophtalmologie, au sein de la résidence Al Manzah à Casablanca.': 'يستقبلكم الدكتور مرمش إلياس في عيادته لطب العيون بإقامة المنزه بالدار البيضاء.',
    'LES AVIS GOOGLE': 'الآراء على GOOGLE',
    'Les mots': 'تجارب',
    'des patients.': 'المرضى.',
    'Une sélection d’avis publiés sur Google Maps, pour découvrir l’expérience partagée par les patients.': 'آراء مختارة منشورة على Google Maps للاطّلاع على التجارب التي يشاركها المرضى.',
    'Google Maps': 'Google Maps',
    'Voir tous les avis': 'عرض جميع الآراء',
    'Sélection d’avis Google': 'آراء مختارة من Google',
    'Avis précédent': 'الرأي السابق',
    'Avis suivant': 'الرأي التالي',
    'Voir sur Google Maps': 'عرض على Google Maps',
    'Rendez-vous par WhatsApp': 'حجز موعد عبر WhatsApp',
    'Lundi – vendredi': 'الاثنين – الجمعة',
    'Samedi': 'السبت',
    'Dimanche': 'الأحد',
    'Fermé': 'مغلق',
    'Jours fériés : horaires à confirmer.': 'يُرجى تأكيد أوقات العمل خلال أيام العطل.',
    'Avis Google Maps': 'الآراء على Google Maps',
    'Le médecin au bloc opératoire': 'الطبيب في غرفة العمليات',
    'Le Dr Marmech Ilias au microscope au bloc opératoire': 'الدكتور مرمش إلياس يستخدم المجهر في غرفة العمليات',
    'AU BLOC OPÉRATOIRE': 'في غرفة العمليات',
    'Le bureau du médecin': 'مكتب الطبيب',
    'Vue d’ensemble du bureau du médecin et de l’espace de consultation': 'منظر عام لمكتب الطبيب وفضاء الاستشارة',
    '04 / Le bureau du médecin': '04 / مكتب الطبيب',
    'La salle de consultation': 'غرفة الاستشارة',
    'Fauteuil de consultation et appareils d’examen devant la fenêtre du cabinet': 'كرسي الاستشارة وأجهزة الفحص أمام نافذة العيادة',
    '05 / La salle de consultation': '05 / غرفة الاستشارة',
    'La façade de l’immeuble du cabinet': 'واجهة المبنى الذي توجد به العيادة',
    'Façade de l’immeuble avec l’enseigne du cabinet et l’entrée au numéro 46': 'واجهة المبنى مع لافتة العيادة والمدخل رقم 46',
    'Repérer l’immeuble': 'التعرّف على المبنى',
    'Résidence Al Manzah · Cabinet au 1er étage': 'إقامة المنزه · العيادة بالطابق الأول',
    'Dr Marmech Ilias · Ophtalmologue à Casablanca': 'الدكتور مرمش إلياس · طبيب عيون بالدار البيضاء',
    'Dr Marmech Ilias, ophtalmologue à Casablanca. Découvrez le médecin, le cabinet et les informations pratiques pour votre consultation.': 'الدكتور مرمش إلياس، طبيب عيون بالدار البيضاء. تعرّفوا على الطبيب والعيادة واطّلعوا على المعلومات العملية للتحضير لزيارتكم.',
    'Un regard attentif sur votre vision. Découvrez le médecin et le cabinet.': 'عناية متواصلة بصحة عيونكم. تعرّفوا على الطبيب والعيادة.',
    'Aller au contenu': 'الانتقال إلى المحتوى',
    'Version de présentation': 'نسخة للمعاينة',
    'Informations du cabinet à compléter': 'سيتم استكمال معلومات العيادة',
    'Dr Marmech Ilias, accueil': 'الدكتور مرمش إلياس، الصفحة الرئيسية',
    'Dr Marmech Ilias': 'الدكتور مرمش إلياس',
    'OPHTALMOLOGUE · CASABLANCA': 'طبيب عيون · الدار البيضاء',
    'Navigation principale': 'القائمة الرئيسية',
    'Le médecin': 'الطبيب',
    'Les pratiques': 'مجالات الممارسة',
    'Le cabinet': 'العيادة',
    'Contact & accès': 'التواصل والعنوان',
    'Langue du site': 'لغة الموقع',
    'FR': 'FR',
    'العربية': 'العربية',
    'Ouvrir le menu': 'فتح القائمة',
    'OPHTALMOLOGIE · CASABLANCA': 'طب العيون · الدار البيضاء',
    'Un regard attentif': 'عناية متواصلة',
    'sur': '',
    'votre vision.': 'بصحة عيونكم.',
    'Votre santé visuelle mérite toute notre attention. Découvrez le cabinet et préparez votre prochaine consultation en toute simplicité.': 'صحة عيونكم تستحق كل اهتمامنا. تعرّفوا على العيادة وحضّروا زيارتكم المقبلة بكل سهولة.',
    'Préparer votre visite': 'التحضير للزيارة',
    'Rencontrer le médecin': 'التعرّف على الطبيب',
    'Votre cabinet d’ophtalmologie': 'عيادتكم لطب العيون',
    'à Casablanca, Maroc': 'بالدار البيضاء، المغرب',
    'AU CŒUR DU CABINET': 'من داخل العيادة',
    'Le médecin installé dans son cabinet, à côté du matériel d’examen ophtalmologique': 'الطبيب داخل عيادته بجانب أجهزة فحص العيون',
    'La santé des yeux.': 'صحة العيون.',
    'Une attention au quotidien.': 'اهتمام كل يوم.',
    'UN LIEU, UNE RENCONTRE, UN SUIVI': 'عيادة، لقاء ومتابعة',
    'Un espace dédié à votre santé visuelle.': 'فضاء مخصص لصحة عيونكم.',
    'Découvrir': 'اكتشفوا',
    'Portrait du médecin dans son espace de consultation': 'صورة الطبيب في غرفة الاستشارة',
    'VOTRE MÉDECIN': 'طبيبكم',
    '01 / LE MÉDECIN': '01 / الطبيب',
    'Prendre le temps': 'نخصص الوقت',
    'de': '',
    'bien vous voir.': 'للعناية ببصركم.',
    'Le Dr Marmech Ilias, médecin ophtalmologue, vous accueille dans son cabinet à Casablanca.': 'يستقبلكم الدكتور مرمش إلياس، طبيب العيون، في عيادته بالدار البيضاء.',
    'Ce site vous permet de découvrir les lieux avant votre venue et de retrouver les informations pratiques pour organiser votre consultation.': 'يمكنكم من خلال هذا الموقع التعرّف على العيادة قبل زيارتكم والاطّلاع على المعلومات العملية لتنظيم موعدكم.',
    'Cabinet d’ophtalmologie · Casablanca': 'عيادة طب العيون · الدار البيضاء',
    'Entrer dans le cabinet': 'اكتشفوا العيادة',
    'MÉDECINE & CHIRURGIE DE L’ŒIL': 'طب وجراحة العيون',
    'du cabinet.': 'بالعيادة.',
    'Du suivi de la vision aux soins spécialisés, découvrez les domaines d’activité du Dr Marmech Ilias.': 'من متابعة البصر إلى العلاجات المتخصصة، تعرّفوا على مجالات ممارسة الدكتور مرمش إلياس.',
    'Chirurgie de la cataracte': 'جراحة المياه البيضاء (الجلالة)',
    'Maladies rétiniennes et glaucome': 'أمراض الشبكية وزرق العين',
    'Chirurgie réfractive, laser et strabisme': 'تصحيح البصر بالليزر والحول',
    'Contactologie, OCT et angiographie': 'العدسات اللاصقة، تصوير الشبكية بـ OCT وتصوير الأوعية',
    'Préparer votre consultation': 'التحضير للاستشارة',
    '02 / LA CONSULTATION': '02 / الاستشارة',
    'Votre vision,': 'بصركم،',
    'au centre de l’attention.': 'في صميم اهتمامنا.',
    'Un premier rendez-vous ou un suivi ?': 'زيارة أولى أم موعد للمتابعة؟',
    'Préparez les éléments utiles à votre visite pour faciliter l’échange avec le médecin.': 'حضّروا الوثائق والمعلومات المفيدة لزيارتكم لتسهيل الحوار مع الطبيب.',
    'Faire le point': 'تقييم',
    'sur votre vision': 'حالة بصركم',
    'Notez les changements que vous avez remarqués et les questions que vous souhaitez poser pendant la consultation.': 'دوّنوا التغيّرات التي لاحظتموها والأسئلة التي ترغبون في طرحها أثناء الاستشارة.',
    'Rassembler': 'جمع',
    'vos documents': 'وثائقكم',
    'Pensez à vos ordonnances, vos comptes rendus et vos lunettes actuelles, ainsi qu’aux références de vos lentilles si vous en portez.': 'أحضروا وصفاتكم الطبية وتقاريركم ونظاراتكم الحالية، ومراجع عدساتكم اللاصقة إن كنتم تستعملونها.',
    'Préparer': 'التحضير',
    'votre suivi': 'للمتابعة',
    'Apportez les résultats de vos précédents examens et la liste de vos traitements pour les partager avec votre médecin.': 'أحضروا نتائج فحوصاتكم السابقة ولائحة الأدوية التي تستعملونها لعرضها على الطبيب.',
    'Quelques repères pour venir l’esprit tranquille.': 'إرشادات بسيطة لزيارة مطمئنة.',
    'Voir la liste à emporter': 'الاطّلاع على لائحة ما يجب إحضاره',
    '03 / LE CABINET': '03 / العيادة',
    'Avant votre visite,': 'قبل زيارتكم،',
    'faites connaissance avec les lieux.': 'تعرّفوا على المكان.',
    'Des espaces lumineux, des matières naturelles et une place pour chaque étape de votre visite.': 'فضاءات مضيئة ولمسات طبيعية، ومكان لكل مرحلة من مراحل زيارتكم.',
    'La salle d’attente': 'قاعة الانتظار',
    'Salle d’attente lumineuse avec fauteuils et plantes': 'قاعة انتظار مضيئة تضم مقاعد ونباتات',
    '01 / La salle d’attente': '01 / قاعة الانتظار',
    'L’accueil du cabinet': 'استقبال العيادة',
    'Comptoir d’accueil en bois avec le logo du cabinet': 'مكتب استقبال خشبي يحمل شعار العيادة',
    '02 / L’accueil': '02 / الاستقبال',
    'L’espace d’examen': 'غرفة الفحص',
    'Espace d’examen avec les appareils d’ophtalmologie': 'غرفة الفحص وأجهزة طب العيون',
    '03 / L’espace d’examen': '03 / غرفة الفحص',
    'Le cabinet, en images.': 'العيادة بالصور.',
    'Photographies des lieux et du médecin.': 'صور للعيادة والطبيب.',
    'BON À SAVOIR': 'معلومات مفيدة',
    'Votre visite,': 'زيارتكم،',
    'tout simplement.': 'بكل بساطة.',
    'Les réponses aux questions pratiques': 'أجوبة عن أسئلتكم العملية',
    'avant de venir au cabinet.': 'قبل الحضور إلى العيادة.',
    'Comment prendre rendez-vous ?': 'كيف يمكن حجز موعد؟',
    'Pour convenir d’un rendez-vous, contactez le cabinet au 05 21 44 44 30 ou au 06 63 84 98 48.': 'لحجز موعد، اتصلوا بالعيادة على الرقم 05 21 44 44 30 أو 06 63 84 98 48.',
    'Que faut-il apporter à la consultation ?': 'ما الذي يجب إحضاره للاستشارة؟',
    'Vos lunettes, les références de vos lentilles, vos ordonnances et les résultats de vos examens précédents. Pensez aussi à la liste de vos traitements en cours et à vos documents de couverture médicale, si vous en disposez.': 'نظاراتكم ومراجع عدساتكم اللاصقة ووصفاتكم الطبية ونتائج فحوصاتكم السابقة. أحضروا أيضاً لائحة أدويتكم الحالية ووثائق التغطية الصحية إن توفرت لديكم.',
    'Où trouver le cabinet ?': 'أين توجد العيادة؟',
    'Le cabinet se situe à la résidence Al Manzah, GH1 n°46, 1er étage, appartement n°2, boulevard Abdelkader Sahraoui, à Casablanca. Retrouvez le lien de recherche de l’adresse ci-dessous.': 'توجد العيادة بإقامة المنزه، GH1 رقم 46، الطابق الأول، الشقة رقم 2، شارع عبد القادر الصحراوي، الدار البيضاء. تجدون رابط البحث عن العنوان أدناه.',
    '04 / CONTACT & ACCÈS': '04 / التواصل والعنوان',
    'Au plaisir': 'يسعدنا',
    'vous accueillir.': 'استقبالكم.',
    'Retrouvez les informations utiles': 'اطّلعوا على المعلومات المفيدة',
    'pour organiser votre venue au cabinet.': 'لتنظيم زيارتكم للعيادة.',
    'Nous trouver': 'عنوان العيادة',
    'Résidence Al Manzah, GH1 n°46, 1er étage, appartement n°2, boulevard Abdelkader Sahraoui — Casablanca': 'إقامة المنزه، GH1 رقم 46، الطابق الأول، الشقة رقم 2، شارع عبد القادر الصحراوي — الدار البيضاء',
    'Adresse précise à renseigner': 'سيتم استكمال العنوان التفصيلي',
    'Rechercher l’adresse': 'البحث عن العنوان',
    'Nous contacter': 'تواصلوا معنا',
    'Appeler le cabinet': 'الاتصال بالعيادة',
    'Prendre rendez-vous': 'حجز موعد',
    'Les coordonnées seront ajoutées prochainement.': 'ستُضاف معلومات التواصل قريباً.',
    'Les horaires': 'أوقات العمل',
    'Horaires à confirmer': 'أوقات العمل قيد التأكيد',
    'À confirmer auprès du cabinet.': 'يرجى التأكد من أوقات العمل بالاتصال بالعيادة.',
    '· Dr Marmech Ilias': '· الدكتور مرمش إلياس',
    'Mentions légales & confidentialité': 'المعلومات القانونية والخصوصية',
    'Revenir en haut de page': 'العودة إلى أعلى الصفحة',
    'Fermer': 'إغلاق',
    'AVANT DE VENIR': 'قبل الحضور',
    'Votre liste': 'لائحة',
    'à emporter.': 'ما يجب إحضاره.',
    'Quelques éléments utiles pour votre consultation :': 'بعض العناصر المفيدة لاستشارتكم:',
    'Vos lunettes et les références de vos lentilles': 'نظاراتكم ومراجع عدساتكم اللاصقة',
    'Vos ordonnances et comptes rendus précédents': 'وصفاتكم الطبية وتقاريركم السابقة',
    'La liste de vos traitements en cours': 'لائحة الأدوية التي تستعملونها حالياً',
    'Vos documents de couverture médicale': 'وثائق التغطية الصحية',
    'Les questions que vous souhaitez poser au médecin': 'الأسئلة التي ترغبون في طرحها على الطبيب',
    'Pour toute consigne propre à votre rendez-vous, contactez le cabinet.': 'للحصول على تعليمات خاصة بموعدكم، يرجى التواصل مع العيادة.',
    'C’est noté': 'حسناً',
    'Photographie du cabinet agrandie': 'صورة مكبّرة للعيادة',
    'Fermer la photographie': 'إغلاق الصورة',
    'INFORMATIONS DU SITE': 'معلومات الموقع',
    'Mentions légales': 'المعلومات القانونية',
    '& confidentialité.': 'والخصوصية.',
    'Éditeur du site': 'مسؤول الموقع',
    'Dr Marmech Ilias — Résidence Al Manzah, GH1 n°46, 1er étage, appartement n°2, boulevard Abdelkader Sahraoui, Casablanca. Téléphone : 05 21 44 44 30 / 06 63 84 98 48. E-mail : dr.marmech@outlook.com.': 'الدكتور مرمش إلياس — إقامة المنزه، GH1 رقم 46، الطابق الأول، الشقة رقم 2، شارع عبد القادر الصحراوي، الدار البيضاء. الهاتف: 05 21 44 44 30 / 06 63 84 98 48. البريد الإلكتروني: dr.marmech@outlook.com.',
    'Hébergement': 'استضافة الموقع',
    'Ce site est hébergé par Cloudflare Pages, un service de Cloudflare, Inc.': 'تتم استضافة هذا الموقع عبر Cloudflare Pages، وهي خدمة تقدمها Cloudflare, Inc.',
    'Politique de confidentialité de Cloudflare': 'سياسة الخصوصية لدى Cloudflare',
    'Ce site est hébergé par GitHub Pages, un service de GitHub, Inc.': 'تتم استضافة هذا الموقع عبر GitHub Pages، وهي خدمة تقدمها GitHub, Inc.',
    'Politique de confidentialité de GitHub': 'سياسة الخصوصية لدى GitHub',
    'Les coordonnées de l’hébergeur devront être renseignées lors du choix de l’hébergement définitif.': 'ستُضاف بيانات مزوّد الاستضافة عند اختيار الاستضافة النهائية للموقع.',
    'Vie privée': 'الخصوصية',
    'Ce site ne comporte aucun formulaire de collecte de données, aucun outil de suivi publicitaire et ne dépose aucun cookie applicatif. Les liens externes, lorsqu’ils sont renseignés, vous conduisent vers des services qui appliquent leurs propres règles de confidentialité. L’hébergeur peut traiter des journaux techniques de connexion.': 'لا يتضمن هذا الموقع أي استمارة لجمع البيانات أو أداة للتتبع الإعلاني، ولا يضع ملفات تعريف ارتباط خاصة بالتطبيق. عند فتح الروابط الخارجية، تنتقلون إلى خدمات تطبّق سياسات الخصوصية الخاصة بها. قد يعالج مزوّد الاستضافة سجلات تقنية للاتصال.',
    'Contenu du site': 'محتوى الموقع',
    'Les informations présentées sont générales et ne remplacent pas une consultation médicale. Les photographies et le logo ont été fournis pour la réalisation de ce site.': 'المعلومات المعروضة عامة ولا تعوّض الاستشارة الطبية. تم توفير الصور والشعار لإنجاز هذا الموقع.',
}


class ArabicPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def translate(self, value):
        stripped = value.strip()
        if stripped in TRANSLATIONS:
            return value[:len(value) - len(value.lstrip())] + TRANSLATIONS[stripped] + value[len(value.rstrip()):]
        if any(c.isalpha() for c in stripped):
            raise ValueError(f'Missing Arabic translation: {stripped!r}')
        return value

    def handle_decl(self, decl):
        self.parts.append(f'<!{decl}>')

    def handle_starttag(self, tag, attrs):
        original = self.get_starttag_text()
        for key, value in attrs:
            if value and (key in ('alt', 'aria-label', 'data-caption', 'title') or key == 'content' and value in TRANSLATIONS):
                original = original.replace('"' + escape(value, quote=True) + '"', '"' + escape(self.translate(value), quote=True) + '"')
                original = original.replace('"' + value + '"', '"' + escape(self.translate(value), quote=True) + '"')
        if tag == 'html':
            original = original.replace('lang="fr"', 'lang="ar" dir="rtl"')
        if tag == 'iframe' and 'data-cabinet-map' in dict(attrs):
            original = original.replace('hl=fr', 'hl=ar')
        if tag == 'link' and dict(attrs).get('rel') == 'canonical':
            value = dict(attrs)['href']
            original = original.replace(value, value + 'ar.html')
        if tag == 'meta' and dict(attrs).get('property') == 'og:url':
            value = dict(attrs)['content']
            original = original.replace(value, value + 'ar.html')
        if tag == 'meta' and dict(attrs).get('property') == 'og:locale':
            original = original.replace('fr_MA', 'ar_MA')
        if tag == 'a' and dict(attrs).get('hreflang') in ('fr', 'ar'):
            original = original.replace(' aria-current="page"', '')
            if dict(attrs).get('hreflang') == 'ar':
                original = original[:-1] + ' aria-current="page">'
        self.parts.append(original)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')

    def handle_data(self, data):
        self.parts.append(escape(self.translate(data), quote=False))

    def handle_entityref(self, name):
        self.parts.append(f'&{name};')

    def handle_charref(self, name):
        self.parts.append(f'&#{name};')

    def handle_comment(self, data):
        self.parts.append(f'<!--{data}-->')


if __name__ == '__main__':
    page = ArabicPage()
    page.feed((ROOT / 'dist/index.html').read_text())
    (ROOT / 'dist/ar.html').write_text(''.join(page.parts))
    print('Arabic page generated; all text and accessible labels translated.')
