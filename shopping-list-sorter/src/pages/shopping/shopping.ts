import {ChangeDetectorRef, Component} from '@angular/core';
import {Alert, AlertController, NavController, NavParams, Platform} from 'ionic-angular';
import {Shopping} from "../../interfaces/Shopping";
import {IPedometerData, Pedometer} from "@ionic-native/pedometer";
import {Article} from "../../interfaces/Article";
import {Distance} from "../../interfaces/Distance";
import {DistancesProvider} from "../../providers/distances/distances";

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
  current_article: Article;
  private distances: Distance[] = [];
  index: number;
  step_counter: number = 0;

  constructor(public navCtrl: NavController, public navParams: NavParams,
              private alert_ctrl: AlertController, private pedometer: Pedometer,
              private refdect: ChangeDetectorRef, private distances_provider: DistancesProvider) {
    this.shopping = this.navParams.get('shopping');
    this.index = 0;
    this.current_article = this.shopping.get_articles()[this.index];
    this.pedometer.startPedometerUpdates().subscribe((data: IPedometerData) => {
      this.step_counter = data.numberOfSteps;
      this.refdect.detectChanges();
    });
  }

  async set_next_article() {
    const articles: Article[] = this.shopping.get_articles();
    let start_id: number;
    if (this.index === 0) {
      start_id = 1;
    } else {
      start_id = articles[this.index - 1].id;
    }
    this.distances.push(new Distance(start_id, this.current_article.id, this.step_counter));
    this.step_counter = 0;
    await this.pedometer.stopPedometerUpdates();
    this.pedometer.startPedometerUpdates().subscribe((data: IPedometerData) => {
      this.step_counter = data.numberOfSteps;
      this.refdect.detectChanges();
    });
    this.current_article = articles[++this.index];
  }

  async set_next_article_alert() {
    const alert: Alert = this.alert_ctrl.create({
      title: "Etes-vous sûr ?",
      buttons: [{
        text: "Oui", handler: () => {
          this.set_next_article();
        }
      }, {
        text: "Non", handler: () => {
        }
      }]
    });
    await alert.present();
  }

  async finish_shopping() {
    const previous_article: Article = this.shopping.get_articles()[this.index - 1];
    this.distances.push(new Distance(previous_article.id, this.current_article.id, this.step_counter));
    this.distances_provider.post(this.distances);
    const alert = this.alert_ctrl.create({
      title: 'Liste de course',
      message: "La liste de course est terminée.",
      //message: this.distances.map(elem => elem.to_string()).join(),
      buttons: [{text: 'Ok'}]
    });
    await alert.present();
    await this.navCtrl.pop();
  }
}
