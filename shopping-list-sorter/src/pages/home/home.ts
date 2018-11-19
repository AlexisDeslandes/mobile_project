import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import {Article} from "../../interfaces/Article";
import {ArticleProvider} from "../../providers/article/article";


@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  articles: Article[];

  constructor(public navCtrl: NavController, private article_provider : ArticleProvider) {

  }

  async ionViewDidLoad(){
    this.articles = await this.article_provider.get();
  }

}
