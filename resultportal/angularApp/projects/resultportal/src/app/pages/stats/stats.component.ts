import { Component, ViewChild, OnInit } from "@angular/core";

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
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit {

  ngOnInit() {
  }

  marks = {
    4: '4',
    10: '10'
  };

  @ViewChild("chart", {static: true}) chart: ChartComponent;
  public chartOptions: Partial<ChartOptions>;

  constructor() {
    this.chartOptions = {
      series: [
        {
          name: "SGPA",
          data: [4.5, 5.2, 3.8, 2.4, 3.3]
        },
        {
          name: "CGPA",
          data: [3.5, 4.1, 6.2, 4.2, 1.3]
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
        enabled: false
      },
      stroke: {
        width: 2,
        // colors: ["#123546", "#865654"],
        curve: "straight",
        dashArray: [0, 8]
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
        categories: [
          "Semester 1",
          "Semester 2",
          "Semester 3",
          "Semester 4",
          "Semester 5"
        ]
      },
      tooltip: {
        y: [
          {
            title: {
              formatter: function(val) {
                return val;
              }
            }
          },
          {
            title: {
              formatter: function(val) {
                return val;
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

}
