import {Article} from "./Article";

export class ProcessAnswer {
  private distance: number;
  public articles: Article[];

  public constructor(distance: number, articles: Article[]) {
    this.distance = distance;
    this.articles = articles;
  }
}
