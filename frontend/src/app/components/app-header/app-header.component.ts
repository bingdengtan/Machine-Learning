import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { EventsService } from '../../services/events.service';
import { CoreService } from '../../services/core.service';

@Component({
  selector: 'app-app-header',
  templateUrl: './app-header.component.html',
  styleUrls: ['./app-header.component.scss']
})
export class AppHeaderComponent implements OnInit {
  username = '';
  email = '';
  location = '';
  title = '';

  constructor(private authService: AuthService,
    private eventsService: EventsService,
    private coreService: CoreService,
  ) {
      this.coreService.getAppConfig('header_title').then( title => {
        this.title = title;
      });
    }

  ngOnInit() {

  }

  logout(): void {
    this.authService.revokeToken();
    this.authService.removeRedirectUrl();
  }

  private setUserData() {
    this.username = sessionStorage.getItem('userData')['username'];
  }
}
