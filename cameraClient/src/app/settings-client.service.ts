import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SettingsService {


    private url = environment.API_URL + '/settings';

    constructor(private http: HttpClient) { 
        
    }

    getEmployee(): Observable<any> {
        return this.http.get(`${this.url}`);
    }

  

    updateSettings(alarmFlag:Boolean,detectFlag:boolean): Observable<Object> { 
       
        const data={
            'detect':detectFlag,
            'notify':alarmFlag
        }
        
        const headers = new HttpHeaders({
                'Content-Type': 'application/json'
        });

                    // Make the PUT request
        return this.http.put<any>(this.url, data, { headers });
    }

  
}