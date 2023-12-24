import { Observable } from "rxjs";
import { environment } from "../environments/environment";
import { StreamData } from "./models/stream-data.model";
import { Injectable } from "@angular/core";


@Injectable({providedIn: 'root',})
export class SseService {

    constructor() { }

    createEventSource(topic: string): Observable<StreamData> {
      
      let eventSource = new EventSource(environment.API_URL + '/'+topic);
      

      return new Observable(observer => {
        eventSource.addEventListener('frame', function(event) {
            const streamData: StreamData = JSON.parse(event.data);  
            observer.next(streamData);
        });

        return () => {
            console.log('Closing event source...');
            eventSource.close();
        }

      });
   }

  
}