import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-ranklist',
  templateUrl: './ranklist.component.html',
  styleUrls: ['./ranklist.component.css']
})
export class RanklistComponent implements OnInit {
  
  dataSet;
  
  constructor() { }

  ngOnInit() {

    this.dataSet = [
      {
        rank: '1',
        name: 'John Brown',
        roll: '2017UGME034',
        src: 'http://nilekrator.pythonanywhere.com/static/images/9823.jpg',
        cgpa: 9.6
      },
      {
        rank: '2',
        name: 'Jim Green',
        roll: '2017UGME034',
        src: 'http://nilekrator.pythonanywhere.com/static/images/9705.jpg',
        cgpa: 9.6
      },
      {
        rank: '3',
        name: 'This is a very long name to be shown',
        roll: '2017UGME034',
        src: 'http://nilekrator.pythonanywhere.com/static/images/10299.jpg',
        cgpa: 9.6
      }
    ];

  }

}
