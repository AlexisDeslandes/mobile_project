import {Component} from '@angular/core';
import {AlertController, IonicPage, NavController, NavParams} from 'ionic-angular';
import {Shopping} from "../../interfaces/Shopping";

/**
 * Generated class for the ShoppingPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-shopping',
  templateUrl: 'shopping.html',
})
export class ShoppingPage {

  shopping: Shopping;
  current_article: any;
  index : number;

  constructor(public navCtrl: NavController, public navParams: NavParams,
              private alert_ctrl : AlertController) {
    this.shopping = this.navParams.get('shopping');
    this.index = 0;
    this.current_article = this.shopping.get_articles()[this.index];
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ShoppingPage');
  }

  set_precedent_article() {
    this.current_article = this.shopping.get_articles()[--this.index];
  }

  set_next_article(){
    this.current_article = this.shopping.get_articles()[++this.index];
  }

  async finish_shopping() {
    const alert = this.alert_ctrl.create({
      title:'Liste de course',
      message:'La liste de course est terminée',
      buttons:[{text:'Ok'}]
    });
    await alert.present();
    await this.navCtrl.pop()
  }
}
