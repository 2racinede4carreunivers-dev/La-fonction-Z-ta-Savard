/**
 * GabrielMarkdown - Composant de rendu Markdown ameliore pour Gabriel
 * Avec styles elegants, couleurs et espacement optimal
 */
import React, { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';

// Composants personnalises definis en dehors du composant principal
const MarkdownH1 = ({ children }) => (
  <h1 className="text-2xl font-bold text-amber-400 mb-4 mt-6 pb-2 border-b border-amber-500/30">
    {children}
  </h1>
);

const MarkdownH2 = ({ children }) => (
  <h2 className="text-xl font-semibold text-emerald-400 mb-3 mt-5">
    {children}
  </h2>
);

const MarkdownH3 = ({ children }) => (
  <h3 className="text-lg font-semibold text-cyan-400 mb-2 mt-4">
    {children}
  </h3>
);

const MarkdownH4 = ({ children }) => (
  <h4 className="text-base font-medium text-purple-400 mb-2 mt-3">
    {children}
  </h4>
);

const MarkdownParagraph = ({ children }) => (
  <p className="text-slate-200 mb-4 leading-relaxed">
    {children}
  </p>
);

const MarkdownStrong = ({ children }) => (
  <strong className="font-bold text-amber-300">
    {children}
  </strong>
);

const MarkdownEmphasis = ({ children }) => (
  <em className="italic text-cyan-300">
    {children}
  </em>
);

const MarkdownCode = ({ inline, children }) => {
  if (inline) {
    return (
      <code className="bg-slate-800 text-green-400 px-1.5 py-0.5 rounded text-sm font-mono">
        {children}
      </code>
    );
  }
  return (
    <code className="block bg-slate-900 text-green-400 p-4 rounded-lg my-4 overflow-x-auto font-mono text-sm leading-relaxed whitespace-pre-wrap">
      {children}
    </code>
  );
};

const MarkdownPre = ({ children }) => (
  <pre className="bg-slate-900 border border-slate-700 rounded-lg my-4 overflow-x-auto">
    {children}
  </pre>
);

const MarkdownUl = ({ children }) => (
  <ul className="list-none space-y-2 mb-4 ml-2">
    {children}
  </ul>
);

const MarkdownOl = ({ children }) => (
  <ol className="list-decimal list-inside space-y-2 mb-4 ml-2 text-slate-200">
    {children}
  </ol>
);

const MarkdownLi = ({ children }) => (
  <li className="text-slate-200 flex items-start gap-2">
    <span className="text-emerald-400 mt-1">•</span>
    <span className="flex-1">{children}</span>
  </li>
);

const MarkdownHr = () => (
  <hr className="border-t border-slate-600 my-6" />
);

const MarkdownBlockquote = ({ children }) => (
  <blockquote className="border-l-4 border-amber-500 pl-4 py-2 my-4 bg-slate-800/50 rounded-r-lg italic text-slate-300">
    {children}
  </blockquote>
);

const MarkdownLink = ({ href, children }) => (
  <a href={href} className="text-cyan-400 hover:text-cyan-300 underline" target="_blank" rel="noopener noreferrer">
    {children}
  </a>
);

// Objet de configuration des composants (stable)
const markdownComponents = {
  h1: MarkdownH1,
  h2: MarkdownH2,
  h3: MarkdownH3,
  h4: MarkdownH4,
  p: MarkdownParagraph,
  strong: MarkdownStrong,
  em: MarkdownEmphasis,
  code: MarkdownCode,
  pre: MarkdownPre,
  ul: MarkdownUl,
  ol: MarkdownOl,
  li: MarkdownLi,
  hr: MarkdownHr,
  blockquote: MarkdownBlockquote,
  a: MarkdownLink,
};

const GabrielMarkdown = ({ content }) => {
  // Pre-traitement du contenu pour s'assurer des sauts de ligne
  const processedContent = useMemo(() => {
    if (!content) return '';
    
    return content
      // Ajouter des sauts de ligne avant les titres s'ils n'existent pas
      .replace(/([^\n])(\n?)(#{1,6}\s)/g, '$1\n\n$3')
      // Ajouter des sauts de ligne apres les titres
      .replace(/(#{1,6}\s[^\n]+)(\n?)([^\n#])/g, '$1\n\n$3')
      // S'assurer que --- sont sur leur propre ligne
      .replace(/([^\n])(---)/g, '$1\n\n$2')
      .replace(/(---)([^\n])/g, '$1\n\n$2')
      // Ajouter des espaces avant les listes
      .replace(/([^\n-])(\n?)(- )/g, '$1\n\n$3')
      // Ajouter des espaces avant les blocs de code
      .replace(/([^\n`])(\n?)(```)/g, '$1\n\n$3')
      .replace(/(```)(\n?)([^\n`])/g, '$1\n$3')
      // Ajouter espace apres **texte**
      .replace(/(\*\*[^*]+\*\*)([^\s\n*])/g, '$1 $2');
  }, [content]);

  return (
    <div className="gabriel-markdown-content" data-testid="gabriel-markdown">
      <ReactMarkdown components={markdownComponents}>
        {processedContent}
      </ReactMarkdown>
    </div>
  );
};

export default GabrielMarkdown;
