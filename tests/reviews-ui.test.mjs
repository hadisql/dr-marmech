import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {parseHTML} from 'linkedom';
import {mountReviews} from '../dist/reviews.js';
import {demoReviews} from './fixtures.mjs';
import productionData from '../dist/reviews-data.js';

async function page(ar = false) {
  const {document, window} = parseHTML(await readFile(new URL(`../dist/${ar ? 'ar' : 'index'}.html`, import.meta.url), 'utf8'));
  return {root: document.querySelector('[data-reviews]'), document, window};
}

for (const ar of [false, true]) test(`${ar ? 'Arabic' : 'French'} static carousel renders source, date and keyboard controls`, async () => {
  const {root, document, window} = await page(ar);
  mountReviews(root, {data: demoReviews()});
  assert.equal(root.querySelectorAll('.review-card').length, 3);
  assert.equal(root.querySelector('[data-review-demo]').hidden, false);
  assert.equal(root.querySelector('[data-reviews-controls]').hidden, false);
  assert.equal(root.querySelector('.maps-attribution').textContent, 'Google Maps');
  assert.equal(root.querySelector('[data-review-prev]').disabled, true);
  const event = new window.Event('keydown', {bubbles: true});
  event.key = ar ? 'ArrowLeft' : 'ArrowRight';
  root.querySelector('[data-reviews-track]').dispatchEvent(event);
  assert.equal(root.querySelector('[data-review-prev]').disabled, false);
  if (ar) {
    const original = demoReviews().reviews[0].text;
    root.querySelector('.review-original').click();
    assert.equal(root.querySelector('.review-text').textContent, original);
    assert.equal(root.querySelector('.review-translation').hidden, true);
  } else {
    const toggle = root.querySelector('.review-expand');
    toggle.click();
    assert.equal(toggle.getAttribute('aria-expanded'), 'true');
  }
  assert.equal(document.documentElement.lang, ar ? 'ar' : 'fr');
});

test('review text cannot inject markup; ratings under four and unsafe links are filtered', async () => {
  const {root} = await page();
  const data = demoReviews();
  data.reviews[0].text = '<img src=x onerror=alert(1)>';
  data.reviews[1].rating = 3;
  data.reviews[2].sourceUrl = 'https://google.com.evil.example/';
  mountReviews(root, {data});
  assert.equal(root.querySelectorAll('.review-card').length, 1);
  assert.equal(root.querySelector('.review-text').textContent, data.reviews[0].text);
  assert.equal(root.querySelector('.review-text img'), null);
});

test('empty selection retains the Google Maps fallback without fake reviews or global rating', async () => {
  const {root} = await page();
  mountReviews(root, {data: {reviews: []}});
  assert.equal(root.querySelector('[data-reviews-track]').hidden, true);
  assert.ok(root.querySelector('[data-reviews-status]').textContent.length);
  assert.equal(root.querySelector('.reviews-topline a').href, 'https://maps.app.goo.gl/wWAsAZMqj17nAnie6');
  assert.equal(root.querySelector('[data-google-rating]'), null);
});

test('desktop navigation stops when the last card is already visible', async () => {
  const {root} = await page();
  mountReviews(root, {data: demoReviews()});
  const track = root.querySelector('[data-reviews-track]');
  Object.defineProperty(track, 'clientWidth', {value: 622});
  track.children[0].getBoundingClientRect = () => ({width: 300});
  root.querySelector('[data-review-next]').click();
  assert.equal(root.querySelector('[data-review-next]').disabled, true);
});

test('published data never contains demo fixtures; attributions are complete when entries exist', () => {
  assert.notEqual(productionData.demo, true);
  for (const review of productionData.reviews) {
    assert.ok(review.text && review.author?.name && review.sourceUrl);
    assert.ok(review.rating >= 4 && review.rating <= 5);
    assert.doesNotMatch(review.text, /fictif|Synthetic layout/);
  }
});
