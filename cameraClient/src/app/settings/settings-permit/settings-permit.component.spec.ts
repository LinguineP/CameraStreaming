import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SettingsPermitComponent } from './settings-permit.component';

describe('SettingsPermitComponent', () => {
  let component: SettingsPermitComponent;
  let fixture: ComponentFixture<SettingsPermitComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SettingsPermitComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SettingsPermitComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
