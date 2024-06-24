import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import embed from 'vega-embed';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  @ViewChild('container') container!: ElementRef;

  menu: boolean = true;

  constructor(private http: HttpClient) { }

  displayVisulization(chartName: string) {
    this.menu = false;
    this.http.get(`../assets/Altiar visulizations/${chartName}.json`).subscribe(data => {
      embed(this.container.nativeElement, data, { actions: false });
    });
  }

}
