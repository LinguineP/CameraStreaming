import { Component, OnInit } from '@angular/core';
import { SseService } from '../sse-client.service';
import { StreamData } from '../models/stream-data.model';
import { Subscriber, Subscription } from 'rxjs';


@Component({
  selector: 'app-monitoring',
  standalone: true,
  imports: [],
  templateUrl: './monitoring.component.html',
  styleUrl: './monitoring.component.css'
})
export class MonitoringComponent {

  picString:string='';
  lockStatus:string='';
  doorStatus:string='';
  serviceSubscription?:Subscription;

  constructor(private sseService: SseService) { }

  ngOnInit() {
        
      this.serviceSubscription=this.sseService.createEventSource('listen').subscribe(
          (data: StreamData) => {
            //console.log('Message received: ' + .message);
            this.picString=data.img
            this.doorStatus=data.lock;
            this.lockStatus=data.door;
            
          }
      );
  }

  ngOnDestroy(){
    this.serviceSubscription?.unsubscribe();
  }


}
