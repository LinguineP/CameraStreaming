import { Routes } from '@angular/router';
import { MonitoringComponent } from './monitoring/monitoring.component';
import { SettingsComponent } from './settings/settings.component';

export const routes: Routes = [
    {path:'',component:MonitoringComponent},
    {path:'settings',component:SettingsComponent}  
];
