import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Article} from "../../interfaces/Article";

/*
  Generated class for the ArticleProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class ArticleProvider {

  constructor(public http: HttpClient) {

  }

  async get(): Promise<Article[]> {
    return await this.http.get<Article[]>("https://renaudcosta.pythonanywhere.com/articles").toPromise();
  }

}
