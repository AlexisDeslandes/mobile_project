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

  async post(shopping: Distance[]): Promise<void> {
    const promises: Promise<void>[] = [];
    shopping.forEach(elem => promises.push(this.http.post<void>("https://renaudcosta.pythonanywhere.com/distances", elem).toPromise()));
    await Promise.all(promises);
  }

}
