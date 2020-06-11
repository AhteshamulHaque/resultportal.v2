import { Component, OnInit } from '@angular/core';

import {
  ChartComponent,
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexDataLabels,
  ApexStroke,
  ApexMarkers,
  ApexYAxis,
  ApexGrid,
  ApexTitleSubtitle,
  ApexLegend
} from "ng-apexcharts";

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  stroke: ApexStroke;
  dataLabels: ApexDataLabels;
  markers: ApexMarkers;
  tooltip: any; // ApexTooltip;
  yaxis: ApexYAxis;
  grid: ApexGrid;
  legend: ApexLegend;
  title: ApexTitleSubtitle;
};


@Component({
  selector: 'app-compare',
  templateUrl: './compare.component.html',
  styleUrls: ['./compare.component.css']
})
export class CompareComponent implements OnInit {

  dataSet;

  public chartOptions: Partial<ChartOptions>;

  subjects;
  constructor() {
    this.subjects = [
      "Computer Science And Engineering",
      "Data Structures And Algorithms",
      "Economics",
      "Lab 1",
      "Lab 2"
    ];
    var _this = this;

    this.chartOptions = {
      series: [
        {
          name: "Anshu Malle",
          data: [45, 52, 38, 24, 33]
        },
        {
          name: "Gurmeet Singh",
          data: [35, 41, 62, 42, 13]
        }
      ],
      chart: {
        toolbar: {
          show: false
        },
        height: 350,
        type: "line"
      },
      dataLabels: {
        enabled: true
      },
      stroke: {
        width: 2,
        // colors: ["#123546", "#865654"],
        curve: "straight",
        dashArray: [0, 5]
      },
      title: {
        text: "",
        align: "center"
      },
      markers: {
        size: 0,
        // colors: ["#123546", "#865654"],
        hover: {
          sizeOffset: 6
        }
      },
      xaxis: {
        labels: {
          trim: true
        },
        categories: ["CS501", "CS502", "CS503", "CS504", "CS505"]
      },
      tooltip: {
        y: [
          {
            title: {
              formatter: function(val, s) {
                return _this.subjects[s.dataPointIndex];
              }
            }
          },
          {
            title: {
              formatter: function(val, s) {
                return _this.subjects[s.dataPointIndex];
              }
            }
          }
        ]
      },
      grid: {
        borderColor: "#eeeeee"
      },
      legend: {
        position: 'top',
        markers: {
          // fillColors: ["#123546", "#865654"],
        }
      }
    };
  }

  ngOnInit() {
    this.dataSet = [];

    this.dataSet = [
      {
        rank: '1',
        name: 'John Brown',
        cgpa: 32,
        roll: '2017UGME034',
        src: 'http://nilekrator.pythonanywhere.com/static/images/9823.jpg'
      },
      {
        rank: '2',
        name: 'Jim Green',
        cgpa: 42,
        roll: '2017UGME034',
        src: 'http://nilekrator.pythonanywhere.com/static/images/9705.jpg'
      },
      {
        rank: '3',
        name: 'This is a very long name to be shown',
        cgpa: 32,
        roll: '2017UGME034',
        src: 'http://nilekrator.pythonanywhere.com/static/images/10299.jpg'
      }
    ];
  }

}
