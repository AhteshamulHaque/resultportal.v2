import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-yearlist',
  templateUrl: './yearlist.component.html',
  styleUrls: ['./yearlist.component.css']
})
export class YearlistComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  data = [
    '2015',
    '2016',
    '2017',
    '2018',
    '2019',
  ];

}
