import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-batchlist',
  templateUrl: './batchlist.component.html',
  styleUrls: ['./batchlist.component.css']
})
export class BatchlistComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  panels = [
    {
      active: true,
      name: ' M.C.A',
      branch: [
        { course: 'UG', branchInitials: 'CSE', branchName: 'Computer Science and Engineering' },
        { course: 'PG', branchInitials: 'ME', branchName: 'Mechanical Engineering' },
        { course: 'UG', branchInitials: 'EEE', branchName: 'Electrical Engineering' }
      ]
    },
    {
      active: false,
      name: 'CEP',
      branch: [
        { course: 'UG', branchInitials: 'CSE', branchName: 'Computer Science and Engineering' },
        { course: 'PG', branchInitials: 'ME', branchName: 'Mechanical Engineering' },
        { course: 'UG', branchInitials: 'EEE', branchName: 'Electrical Engineering' }
      ]
    },
    {
      active: false,
      name: 'B.Tech (Hons.)',
      branch: [
        { course: 'UG', branchInitials: 'CSE', branchName: 'Computer Science and Engineering' },
        { course: 'PG', branchInitials: 'ME', branchName: 'Mechanical Engineering' },
        { course: 'UG', branchInitials: 'EEE', branchName: 'Electrical Engineering' }
      ]
    }
  ];

}
