import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Shopping} from "../../interfaces/Shopping";

/*
  Generated class for the ShoppingProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class ShoppingProvider {


  constructor(public http: HttpClient) {

  }

  async post(shopping : Shopping){
    return await this.http.post<Shopping>("https://renaudcosta.pythonanywhere.com/shopping",shopping).toPromise();
  }

}
