import {BrowserModule} from '@angular/platform-browser';
import {ErrorHandler, NgModule} from '@angular/core';
import {IonicApp, IonicErrorHandler, IonicModule} from 'ionic-angular';
import {SplashScreen} from '@ionic-native/splash-screen';
import {StatusBar} from '@ionic-native/status-bar';

import {MyApp} from './app.component';
import {HomePage} from '../pages/home/home';
import {ArticleProvider} from '../providers/article/article';
import {HttpClientModule} from "@angular/common/http";
import {ShoppingProvider} from '../providers/shopping/shopping';
import {ShoppingPage} from "../pages/shopping/shopping";


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
    ShoppingProvider
  ]
})
export class AppModule {
}
