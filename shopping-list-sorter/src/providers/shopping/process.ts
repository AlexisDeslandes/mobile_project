import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Shopping} from "../../interfaces/Shopping";
import {Article} from "../../interfaces/Article";

/*
  Generated class for the ProcessProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class ProcessProvider {


  constructor(public http: HttpClient) {

  }

  async post(shopping: Shopping): Promise<Article[]> {
    const ids: number[] = shopping.get_articles().map(elem => elem.id);
    const request = {token: "wakandaforeva", articles: ids};
    return await this.http.post<Article[]>("https://renaudcosta.pythonanywhere.com/processs", request).toPromise();
  }

}
