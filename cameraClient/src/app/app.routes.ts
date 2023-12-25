import { Routes } from '@angular/router';
import { MonitoringComponent } from './monitoring/monitoring.component';
import { SettingsComponent } from './settings/settings.component';
import { SettingsPanelComponent } from './settings/settings-panel/settings-panel.component';

export const routes: Routes = [
    {path:'',component:MonitoringComponent},
    {path:'settings',component:SettingsComponent, children: [
        {path: 'settings-panel',component: SettingsPanelComponent,outlet:"settingsRouterOutlet" }
      ]}
 
    
];
