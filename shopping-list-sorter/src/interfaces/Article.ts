export class Article {
  public id: number;
  public nom: string;

  public constructor(id: number, nom: string) {
    this.id = id;
    this.nom = nom;
  }

  static index_of(articles: Article[], article: Article) {
    for (let i = 0; i < articles.length; i++) {
      if (articles[i].id === article.id) return i;
    }
    return -1;
  }

}
