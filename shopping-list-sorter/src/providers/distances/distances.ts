import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Distance} from "../../interfaces/Distance";

/*
  Generated class for the DistancesProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class DistancesProvider {

  constructor(public http: HttpClient) {
    //https://renaudcosta.pythonanywhere.com/distances
    console.log('Hello DistancesProvider Provider');
  }

  async post(distances: Distance[]): Promise<void> {
    const request = {token: "wakandaforeva", distances: distances};
    await this.http.post<void>("https://renaudcosta.pythonanywhere.com/distances", request).toPromise();
  }

}
