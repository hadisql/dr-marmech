// Synthetic layout fixtures, never included in dist/.
export function demoReviews(language = 'fr') {
  const ar = language === 'ar';
  return {
    demo: true,
    selectedOn: '2026-11-16',
    reviews: Array.from({length: 3}, (_, i) => ({
      rating: i === 1 ? 4 : 5,
      text: ar
        ? 'هذا نص افتراضي لاختبار عرض الآراء فقط، ولا يمثّل تجربة مريض. يتيح التحقق من اتجاه الكتابة والمسافات بين عناصر البطاقة.'
        : 'Ceci est un texte fictif pour vérifier la présentation des avis. Il ne décrit aucune expérience de patient. Cette carte permet de contrôler les espacements, la date, les liens et la lisibilité du contenu sur un petit écran. Un texte plus long permet aussi de tester le bouton de lecture.',
      textAr: 'هذا نص افتراضي لاختبار عرض الآراء فقط، ولا يمثّل تجربة مريض.',
      publishTime: `2026-11-${10 + i}T10:00:00Z`,
      sourceUrl: 'https://maps.google.com/',
      author: {name: ar ? `ملف افتراضي ${i + 1}` : `Profil de démonstration ${i + 1}`},
    })),
  };
}
