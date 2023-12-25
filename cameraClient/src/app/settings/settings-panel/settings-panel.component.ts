import { Component } from '@angular/core';
import {FormsModule} from '@angular/forms'
import {  NgClass } from '@angular/common';
import { SettingsService } from '../../settings-client.service';


@Component({
  selector: 'app-settings-panel',
  standalone: true,
  imports: [FormsModule,NgClass],
  templateUrl: './settings-panel.component.html',
  styleUrl: './settings-panel.component.css'
})
export class SettingsPanelComponent {

  detectionFlag: boolean = false;
  alarmFlag: boolean = false;

  toggleEvent(e:Event,toggleId:string){
      
      if(toggleId=='alarm'){
        
        this.alarmFlag=!this.alarmFlag
        console.log(this.alarmFlag)

      }
      if(toggleId=='detection'){
        this.detectionFlag=!this.detectionFlag;
        console.log(this.detectionFlag)
      }
      this.updateSettings();
      
    
  }

  updateSettings(){
    this.settingsCli.updateSettings(this.alarmFlag,this.detectionFlag)
  }
 
  constructor(private settingsCli:SettingsService){
    
  }

}
