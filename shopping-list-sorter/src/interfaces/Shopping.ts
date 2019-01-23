import {Article} from "./Article";

export class Shopping {
  private articles : Article[];

  constructor(articles : Article[]){
    this.articles = articles;
  }

  public get_articles() : Article[]{
    return this.articles;
  }
}
