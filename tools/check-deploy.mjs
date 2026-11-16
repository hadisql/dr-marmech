import data from '../dist/reviews-data.js';
if (!/^\d{4}-\d{2}-\d{2}$/.test(data.selectedOn || '') || data.reviews.length < 2) {
  console.error('Publication bloquée : compléter la sélection datée avec au moins deux extraits d’avis vérifiés.');
  process.exit(1);
}
