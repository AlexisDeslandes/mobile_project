import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Article} from "../../interfaces/Article";
import {ArticleProvider} from "../../providers/article/article";


@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  articles: Article[];
  my_articles: Article[] = [];
  articles_filtered: Article[];

  constructor(public navCtrl: NavController, private article_provider: ArticleProvider) {

  }

  async ionViewDidLoad() {
    this.articles = await this.article_provider.get();
    this.articles_filtered = JSON.parse(JSON.stringify(this.articles));
  }

  search_items(event) {
    let item_name: string = event.target.value;
    item_name = item_name.toLowerCase();

    this.articles_filtered = this.articles
      .filter(article => article.nom.toLowerCase().includes(item_name));
  }

  add_to_list(article: Article): void {
    this.my_articles.push(article);
    this.articles.splice(Article.index_of(this.articles, article), 1);
    this.articles_filtered.splice(Article.index_of(this.articles_filtered, article), 1);
  }

  remove_from_list(article: Article) {
    const sort = (articles: Article[]) => {
      return articles.sort((a, b) => {
        if (a.nom < b.nom) return -1;
        else if (a.nom > b.nom) return 1;
        return 0;
      });
    };
    this.my_articles.splice(Article.index_of(this.my_articles, article), 1);
    this.articles.push(article);
    this.articles_filtered.push(article);
    this.articles = sort(this.articles);
    this.articles_filtered = sort(this.articles_filtered);
  }

  start_shopping() {
    //todo start shopping
  }
}
