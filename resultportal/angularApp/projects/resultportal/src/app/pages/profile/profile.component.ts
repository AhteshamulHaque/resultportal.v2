import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  name: string = "Nile Krator";
  branch: string = "Computer Science and Engineering"
  resultStatus: boolean = true;

  _listofData;

  listOfData = [
    {
      code: 'CS501',
      subject: 'OPERATING SYSTEM',
      test1: 26.0,
      test2: 17.0,
      assignment: 0.0,
      quiz_avg: 0.0,
      end_sem: 27.0,
      total: 70.0,
      grade: 'B'
    },
    {
      code: 'CS501',
      subject: 'OPERATING SYSTEM',
      test1: 26.0,
      test2: 17.0,
      assignment: 0.0,
      quiz_avg: 0.0,
      end_sem: 27.0,
      total: 70.0,
      grade: 'B'
    },{
      code: 'CS501',
      subject: 'OPERATING SYSTEM',
      test1: 26.0,
      test2: 17.0,
      assignment: 0.0,
      quiz_avg: 0.0,
      end_sem: 27.0,
      total: 70.0,
      grade: 'B'
    }
  ];

  panels = [
    {
      id: 5,
      active: true,
      disabled: false,
      name: "Semester 5",
    },
    {
      id: 4,
      active: false,
      disabled: true,
      name: 'Semester 4',
    },
    {
      id: 3,
      active: false,
      disabled: false,
      name: 'Semester 3',
    }
  ];

  gridStyle = {
    'text-align': 'center'
  };

  constructor() { }

  ngOnInit() {

    this._listofData = [];

    for (let i = 0; i < 5; i++) {
      this._listofData.push({
        name: `Edward King ${i}`,
        age: 32,
        address: `London`
      });
    }

  }

}
