import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { IconsProviderModule } from './icons-provider.module';
import { NgZorroAntdModule, NZ_I18N, en_US } from 'ng-zorro-antd';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';

// ng-ant components
import { NzCardModule } from 'ng-zorro-antd/card';

// apexcharts
import { NgApexchartsModule } from 'ng-apexcharts';

// Components imports
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { RankComponent } from './pages/rank/rank.component';
import { CompareComponent } from './pages/compare/compare.component';
import { StatsComponent } from './pages/stats/stats.component';
import { BatchlistComponent } from './pages/college/batchlist/batchlist.component';
import { YearlistComponent } from './pages/college/yearlist/yearlist.component';
import { RanklistComponent } from './pages/college/ranklist/ranklist.component';
import { CollegeComponent } from './pages/college/college.component';

registerLocaleData(en);


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    ProfileComponent,
    RankComponent,
    CompareComponent,
    StatsComponent,
    YearlistComponent,
    BatchlistComponent,
    RanklistComponent,
    CollegeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    IconsProviderModule,
    NgZorroAntdModule,
    FormsModule,
    HttpClientModule,
    NzCardModule,
    NgApexchartsModule,
  ],
  providers: [{ provide: NZ_I18N, useValue: en_US }],
  bootstrap: [AppComponent]
})
export class AppModule { }
