import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync('assets/js/user.js', 'utf8');
const moduleSource = source
  .replace(/export function /g, 'function ')
  .replace(/export const /g, 'const ')
  .replace(/export default /g, '');
const context = {
  console,
  Math,
  localStorage: {
    getItem() { return null; },
    setItem() {},
    removeItem() {},
  },
};
vm.createContext(context);
vm.runInContext(`${moduleSource}\nthis.selectSmartPaper = selectSmartPaper;`, context);

const bank = JSON.parse(fs.readFileSync('data/cha_questions.json', 'utf8'));
const papers = Array.from({ length: 20 }, () => context.selectSmartPaper(bank, null, 150, 'cha'));
for (const [index, paper] of papers.entries()) {
  if (paper.length !== 150) throw new Error(`Paper ${index + 1} has ${paper.length} questions`);
  const ids = new Set(paper.map((question) => question.id));
  if (ids.size !== 150) throw new Error(`Paper ${index + 1} repeats question IDs`);
  const signatures = new Set(paper.map((question) => [
    question.stem,
    ...(question.options || []),
    question.correctIndex,
  ].map((value) => String(value ?? '').trim().toLowerCase().replace(/\s+/g, ' ')).join('|')));
  if (signatures.size !== 150) throw new Error(`Paper ${index + 1} repeats full question signatures`);
}
console.log(`Generated ${papers.length} CHA papers with 150 unique questions each`);
