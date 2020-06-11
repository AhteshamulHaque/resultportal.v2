import { NgModule } from '@angular/core';

import { ProfileRoutingModule } from './profile-routing.module';

import { ProfileComponent } from './profile.component';


@NgModule({
  imports: [ProfileRoutingModule],
  declarations: [ProfileComponent],
  exports: [ProfileComponent]
})
export class ProfileModule { }
