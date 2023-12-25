import { Component } from '@angular/core';
import { Router, RouterOutlet,ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.css'
})
export class SettingsComponent {

    constructor(private router:Router,private route:ActivatedRoute){

    }

    goToSettingsPanel() {
      this.router.navigate( ['/settings','settings-panel']);
      
    }

    ngOnInit(){

      this.goToSettingsPanel()
    }


}
