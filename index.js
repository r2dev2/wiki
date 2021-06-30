const toJson = r => r.json();
const emptyArr = () => [];

const getArticles = (() => {
  let articles = [];

  return async () => {
    if (articles.length) return articles;
    return articles = await fetch('./articles.json')
      .then(toJson)
      .catch(emptyArr);
  };
})();

const articleNameToArticle = name => ({
  name: name.toLowerCase(),
  href: `./en/${name.replaceAll(" ", "_")}.html`
});

const matchRecommends = (() => {
  let articles = [];
  let previousQuery = null;

  return async query => {
    query = query.toLowerCase();
    if (!query.startsWith(previousQuery)) {
      articles = await getArticles();
    }
    previousQuery = query;
    return articles
      .filter(art => art.toLowerCase().includes(query))
      .map(articleNameToArticle);
  };
})();
