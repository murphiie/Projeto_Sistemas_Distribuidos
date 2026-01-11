use newsflow;

db.articles.insertMany([
  {
    title: "Governo anuncia nova política econômica",
    content: "O governo anunciou novas medidas para controle da inflação...",
    author: "Agência Brasil",
    category: "Política",
    created_at: new Date()
  },
  {
    title: "Final do campeonato termina em empate",
    content: "A grande final do campeonato terminou empatada em 2 a 2...",
    author: "Redação Esportes",
    category: "Esportes",
    created_at: new Date()
  },
  {
    title: "Nova inteligência artificial revoluciona mercado",
    content: "Uma nova IA promete transformar diversos setores da indústria...",
    author: "Tech News",
    category: "Tecnologia",
    created_at: new Date()
  },
  {
    title: "Projeto de lei gera debates no congresso",
    content: "O novo projeto de lei está gerando intensos debates...",
    author: "Jornal Nacional",
    category: "Política",
    created_at: new Date()
  },
  {
    title: "Time local conquista vitória histórica",
    content: "O time local venceu uma partida histórica...",
    author: "Esporte Total",
    category: "Esportes",
    created_at: new Date()
  }
]);
