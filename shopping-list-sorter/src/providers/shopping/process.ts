import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Shopping} from "../../interfaces/Shopping";
import {Article} from "../../interfaces/Article";
import {ProcessAnswer} from "../../interfaces/ProcessAnswer";

/*
  Generated class for the ProcessProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class ProcessProvider {


  constructor(public http: HttpClient) {

  }

  async post(shopping: Shopping): Promise<ProcessAnswer> {
    const ids: number[] = shopping.get_articles().map(elem => elem.id);
    const request = {token: "wakandaforeva", articles: ids};
    return await this.http.post<ProcessAnswer>("https://renaudcosta.pythonanywhere.com/process", request).toPromise();
  }

}
