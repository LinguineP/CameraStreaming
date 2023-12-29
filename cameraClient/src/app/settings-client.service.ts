import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, catchError } from 'rxjs';
import { environment } from '../environments/environment';
import { SettingsData } from './models/settings-data.model';

@Injectable({
  providedIn: 'root'
})
export class SettingsService {


    private url = environment.API_URL + '/'+'settings';

    constructor(private http: HttpClient) { 
        
    }

    getData(): Observable<SettingsData> {
        return this.http.get<SettingsData>(`${this.url}`);
    }   
    

  
    updateSettings(alarmFlag: boolean, detectFlag: boolean): Observable<SettingsData> {
        const data = {
            'detect': detectFlag,
            'notify': alarmFlag
        };
    
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
    
        console.log(this.url);
        
        // Make the PUT request
        return this.http.put<SettingsData>(this.url, data, { headers });
    }
    
    updateEmail(email: string, auth: string): Observable<Object> {
        const data = {
            'email': email,
            'auth': auth
        };
    
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
    
        const changeEmailURL = environment.API_URL+'/change_email'
        
        // Make the PUT request
        return this.http.put<Object>(changeEmailURL, data, { headers });
    }


    sendEmail(): Observable<Object> {
        const sendEmailURL = environment.API_URL+'/send_email'
        return this.http.get<Object>(`${sendEmailURL}`);
    }
  
}