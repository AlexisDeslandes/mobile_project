import {Component} from '@angular/core';
import {AlertController, IonicPage, NavController, NavParams} from 'ionic-angular';
import {Shopping} from "../../interfaces/Shopping";
import {IPedometerData, Pedometer} from "@ionic-native/pedometer";

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
  index: number;
  step_counter: number = 0;
  total_before: number = 0;
  precedent_article_count: number = 0;

  constructor(public navCtrl: NavController, public navParams: NavParams,
              private alert_ctrl: AlertController, private pedometer: Pedometer) {
    this.shopping = this.navParams.get('shopping');
    this.index = 0;
    this.current_article = this.shopping.get_articles()[this.index];
    this.pedometer.startPedometerUpdates().subscribe((data: IPedometerData) => {
      console.log(data.numberOfSteps);
      this.step_counter = data.numberOfSteps - this.total_before;
    });
  }

  ionViewDidLoad() {

  }

  async set_precedent_article() {
    this.precedent_article_count += 1;
    await this.pedometer.stopPedometerUpdates();
    this.current_article = this.shopping.get_articles()[--this.index];
  }

  set_next_article() {
    if (this.precedent_article_count > 0) {
      this.precedent_article_count -= 1;
      if (this.precedent_article_count === 0) {
        this.pedometer.startPedometerUpdates().subscribe((data: IPedometerData) => {
          this.step_counter = data.numberOfSteps - this.total_before;
        })
      }
    }
    this.total_before += this.step_counter;
    this.current_article = this.shopping.get_articles()[++this.index];
  }

  async finish_shopping() {
    const alert = this.alert_ctrl.create({
      title: 'Liste de course',
      message: 'La liste de course est terminée',
      buttons: [{text: 'Ok'}]
    });
    await alert.present();
    await this.navCtrl.pop()
  }
}
