import {BrowserModule} from '@angular/platform-browser';
import {ErrorHandler, NgModule} from '@angular/core';
import {IonicApp, IonicErrorHandler, IonicModule} from 'ionic-angular';
import {SplashScreen} from '@ionic-native/splash-screen';
import {StatusBar} from '@ionic-native/status-bar';

import {MyApp} from './app.component';
import {HomePage} from '../pages/home/home';
import {ArticleProvider} from '../providers/article/article';
import {HttpClientModule} from "@angular/common/http";
import {ProcessProvider} from '../providers/shopping/process';
import {ShoppingPage} from "../pages/shopping/shopping";
import {Pedometer} from "@ionic-native/pedometer";
import { DistancesProvider } from '../providers/distances/distances';


@NgModule({
  declarations: [
    MyApp,
    HomePage,
    ShoppingPage
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    IonicModule.forRoot(MyApp)
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage,
    ShoppingPage
  ],
  providers: [
    StatusBar,
    HttpClientModule,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    ArticleProvider,
    ProcessProvider,
    Pedometer,
    DistancesProvider
  ]
})
export class AppModule {
}
