import {Component, ElementRef, ViewChild} from '@angular/core';
import {Card, NavController} from 'ionic-angular';
import {Article} from "../../interfaces/Article";
import {ArticleProvider} from "../../providers/article/article";
import {Shopping} from "../../interfaces/Shopping";
import {ProcessProvider} from "../../providers/shopping/process";
import {ShoppingPage} from "../shopping/shopping";


@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  @ViewChild("maListe") myList : ElementRef;
  @ViewChild("searchResult") searchResult : ElementRef;

  articles: Article[];
  my_articles: Article[] = [];
  articles_filtered: Article[];
  search: string = "";

  constructor(public navCtrl: NavController, private article_provider: ArticleProvider,
              private shopping_provider: ProcessProvider) {
  }

  async ionViewDidLoad() {
    this.articles = await this.article_provider.get();
    this.articles_filtered = JSON.parse(JSON.stringify(this.articles));
  }

  search_items(event): void {
    let item_name: string = event.target.value;
    item_name = item_name.toLowerCase();

    this.articles_filtered = this.articles
      .filter(article => article.nom.toLowerCase().includes(item_name));
  }

  add_to_list(article: Article): void {
    this.my_articles.push(article);
    this.articles.splice(Article.index_of(this.articles, article), 1);
    this.articles_filtered.splice(Article.index_of(this.articles_filtered, article), 1);
    this.make_my_list_appear();
    this.resetSearch();
  }

  remove_from_list(article: Article): void {
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

  async start_shopping(): Promise<void> {
    const shopping: Shopping = new Shopping(this.my_articles);
    let articles_result: Article[] = await this.shopping_provider.post(shopping);
    articles_result = articles_result.filter(elem => elem.id !== 1);
    const shopping_sorted: Shopping = new Shopping(articles_result);
    await this.navCtrl.push(ShoppingPage, {shopping: shopping_sorted});
  }

  make_my_list_disapear() {
    this.myList.nativeElement.style.display = "None";
    this.searchResult.nativeElement.style.height = "50vh";
  }

  make_my_list_appear() {
    this.myList.nativeElement.style.display = "block";
    this.searchResult.nativeElement.style.height = "30vh";
  }

  resetSearch(){
    this.search = "";
    this.articles_filtered = JSON.parse(JSON.stringify(this.articles));
  }
}
