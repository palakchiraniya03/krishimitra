export interface KnowledgeDoc {
  id: string;
  text: string;
}

function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2);
}

function termFrequency(tokens: string[]): Record<string, number> {
  const tf: Record<string, number> = {};
  for (const t of tokens) tf[t] = (tf[t] || 0) + 1;
  const total = tokens.length;
  for (const t in tf) tf[t] = tf[t] / total;
  return tf;
}

function inverseDocFrequency(docsTokens: string[][]): Record<string, number> {
  const N = docsTokens.length;
  const df: Record<string, number> = {};
  for (const tokens of docsTokens) {
    const seen = new Set(tokens);
    for (const t of seen) df[t] = (df[t] || 0) + 1;
  }
  const idf: Record<string, number> = {};
  for (const t in df) idf[t] = Math.log(N / df[t]) + 1;
  return idf;
}

function tfidfVector(tf: Record<string, number>, idf: Record<string, number>): Record<string, number> {
  const vec: Record<string, number> = {};
  for (const t in tf) vec[t] = tf[t] * (idf[t] ?? 0);
  return vec;
}

function cosineSimilarity(a: Record<string, number>, b: Record<string, number>): number {
  let dot = 0, normA = 0, normB = 0;
  const allTerms = new Set([...Object.keys(a), ...Object.keys(b)]);
  for (const t of allTerms) {
    const va = a[t] || 0;
    const vb = b[t] || 0;
    dot += va * vb;
    normA += va * va;
    normB += vb * vb;
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

export function searchKnowledge(query: string, docs: KnowledgeDoc[]): { id: string; score: number }[] {
  const docsTokens = docs.map((d) => tokenize(d.text));
  const idf = inverseDocFrequency(docsTokens);
  const docVectors = docsTokens.map((tokens) => tfidfVector(termFrequency(tokens), idf));

  const queryTokens = tokenize(query);
  const queryVector = tfidfVector(termFrequency(queryTokens), idf);

  const scored = docs.map((d, i) => ({
    id: d.id,
    score: cosineSimilarity(queryVector, docVectors[i]),
  }));

  return scored.sort((a, b) => b.score - a.score);
}