import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './login/login.component';
import  { ProfileComponent } from './pages/profile/profile.component';
import { RankComponent } from './pages/rank/rank.component';
import { CompareComponent } from './pages/compare/compare.component';
import { StatsComponent } from './pages/stats/stats.component';
import { BatchlistComponent } from './pages/college/batchlist/batchlist.component';
import { YearlistComponent } from './pages/college/yearlist/yearlist.component';
import { RanklistComponent } from './pages/college/ranklist/ranklist.component';
import { CollegeComponent } from './pages/college/college.component';

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: '/profile' },
  { path: 'login', pathMatch: 'full', component: LoginComponent },
  { path: 'profile',  component: ProfileComponent },
  { path: 'rank',  component: RankComponent },
  { path: 'compare',  component: CompareComponent },
  { path: 'stats',  component: StatsComponent },
  { 
    path: 'college', component: CollegeComponent,
    children: [
      { path: '', component: YearlistComponent },
      { path: ':year', component: BatchlistComponent },
      { path: ':year/:course/:branchInitials', component: RanklistComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
