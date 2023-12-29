import { Component } from '@angular/core';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms'
import {  NgClass } from '@angular/common';
import { SettingsService } from '../../settings-client.service';
import { SettingsData } from '../../models/settings-data.model';


@Component({
  selector: 'app-settings-panel',
  standalone: true,
  imports: [FormsModule,NgClass,ReactiveFormsModule],
  templateUrl: './settings-panel.component.html',
  styleUrl: './settings-panel.component.css'
})
export class SettingsPanelComponent {

  detectionFlag: boolean = false;
  alarmFlag: boolean = false;
  emailForm: FormGroup;

  constructor(private settingsCli:SettingsService,private fb: FormBuilder){
    this.getSettings();
    this.emailForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      auth: ['', [Validators.required, Validators.minLength(6)]]
    });
    
  }

  submitForm() {
     console.log(this.emailForm.value);
     this.emailForm.reset();

    // You can handle the form submission logic here
  }

  toggleEvent(e:Event,toggleId:string){
      
      if(toggleId=='alarm'){
        
        this.alarmFlag=!this.alarmFlag
        //console.log(this.alarmFlag)

      }
      if(toggleId=='detection'){
        this.detectionFlag=!this.detectionFlag;
        //console.log(this.detectionFlag)
      }
      
      this.updateSettings();
  }




  updateSettings(){
    
    this.settingsCli.updateSettings(this.alarmFlag,this.detectionFlag).subscribe(
      (data: SettingsData) => {
        console.log(data.detection)
        this.alarmFlag=data.notify;
        this.detectionFlag=data.detection;
        
      } );
  }

  getSettings(){
    
    this.settingsCli.getData().subscribe(
      (data: SettingsData) => {
        console.log(data)
        
        this.alarmFlag=data.notify;
        this.detectionFlag=data.detection;
      }
    );
  }
  
  updateEmail(email:string,auth:string){
    this.settingsCli.updateEmail(email,auth).subscribe();
  }


  sendEmail(){
    this.settingsCli.sendEmail().subscribe();

  }
  

}
