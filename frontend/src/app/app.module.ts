import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpModule } from '@angular/http';
import { NgModule, APP_INITIALIZER } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LocationStrategy, HashLocationStrategy } from '@angular/common';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AuthModule,
  OidcSecurityService,
  OpenIDImplicitFlowConfiguration,
  OidcConfigService,
  AuthWellKnownEndpoints
} from 'angular-auth-oidc-client';
import { NgxBootstrapModule } from './utils/ngxBootstrap.module';

import { AppRoutingModule } from './app.routing';
import { environment } from '../environments/environment';
import { AppComponent } from './app.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { AppHeaderComponent } from './components/app-header/app-header.component';
import { AppFooterComponent } from './components/app-footer/app-footer.component';
import { AppLeftSideComponent } from './components/app-left-side/app-left-side.component';
import { AppControlSidebarComponent } from './components/app-control-sidebar/app-control-sidebar.component';
import { HomeComponent } from './pages/home/home.component';
import { UnauthorizedComponent } from './pages/unauthorized/unauthorized.component';
import { StarterComponent } from './pages/starter/starter.component';
import { AuthorizedComponent } from './pages/authorized/authorized.component';
import { ForbiddenComponent } from './pages/forbidden/forbidden.component';
import { RoleComponent } from './pages/role/role.component';
import { UserComponent } from './pages/user/user.component';
import { GridComponent } from './components/grid/grid.component';

import { AuthService } from './services/auth.service';
import { UserService } from './services/user.service';
import { RoleService } from './services/role.service';
import { EventsService } from './services/events.service';
import { CoreService } from './services/core.service';
import { CoreUtils } from './utils/core.utils';
import { AuthorizationGuard } from './services/authorization.guard';
import { AuthInterceptor } from './services/authInterceptor.service';
import { ConfirmDialogComponent } from './components/confirm-dialog/confirm-dialog.component';

export function loadConfig(oidcConfigService: OidcConfigService) {
  return () => oidcConfigService.load(`${window.location.origin}/assets/data/oidc.config${environment.production ? '.prod' : ''}.json`);
}

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    AppHeaderComponent,
    AppFooterComponent,
    AppLeftSideComponent,
    AppControlSidebarComponent,
    HomeComponent,
    UnauthorizedComponent,
    StarterComponent,
    AuthorizedComponent,
    ForbiddenComponent,
    RoleComponent,
    UserComponent,
    GridComponent,
    ConfirmDialogComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule,
    NgxBootstrapModule,
    AuthModule.forRoot()
  ],
  providers: [
    // {provide: LocationStrategy, useClass: HashLocationStrategy},
    OidcConfigService,
    AuthService,
    CoreService,
    RoleService,
    AuthorizationGuard,
    UserService,
    CoreUtils,
    EventsService,
    {
        provide: APP_INITIALIZER, useFactory: loadConfig, deps: [OidcConfigService], multi: true
    },
    {
      provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(
    private oidcSecurityService: OidcSecurityService,
    private oidcConfigService: OidcConfigService,
  ) {
      this.oidcConfigService.onConfigurationLoaded.subscribe(() => {

        const openIDImplicitFlowConfiguration = new OpenIDImplicitFlowConfiguration();
        openIDImplicitFlowConfiguration.stsServer = this.oidcConfigService.clientConfiguration.stsServer;
        openIDImplicitFlowConfiguration.redirect_url = this.oidcConfigService.clientConfiguration.redirect_url;
        // The Client MUST validate that the aud (audience) Claim contains its client_id value registered at the Issuer
        // identified by the iss (issuer) Claim as an audience.
        // The ID Token MUST be rejected if the ID Token does not list the Client as a valid audience,
        // or if it contains additional audiences not trusted by the Client.
        openIDImplicitFlowConfiguration.trigger_authorization_result_event =
          this.oidcConfigService.clientConfiguration.trigger_authorization_result_event;
        openIDImplicitFlowConfiguration.client_id = this.oidcConfigService.clientConfiguration.client_id;
        openIDImplicitFlowConfiguration.response_type = this.oidcConfigService.clientConfiguration.response_type;
        openIDImplicitFlowConfiguration.scope = this.oidcConfigService.clientConfiguration.scope;
        openIDImplicitFlowConfiguration.post_logout_redirect_uri = this.oidcConfigService.clientConfiguration.post_logout_redirect_uri;
        openIDImplicitFlowConfiguration.start_checksession = this.oidcConfigService.clientConfiguration.start_checksession;
        openIDImplicitFlowConfiguration.silent_renew = this.oidcConfigService.clientConfiguration.silent_renew;
        openIDImplicitFlowConfiguration.silent_renew_url = this.oidcConfigService.clientConfiguration.silent_renew_url;
        openIDImplicitFlowConfiguration.post_login_route = this.oidcConfigService.clientConfiguration.startup_route;
        // HTTP 403
        openIDImplicitFlowConfiguration.forbidden_route = this.oidcConfigService.clientConfiguration.forbidden_route;
        // HTTP 401
        openIDImplicitFlowConfiguration.unauthorized_route = this.oidcConfigService.clientConfiguration.unauthorized_route;
        openIDImplicitFlowConfiguration.log_console_warning_active = this.oidcConfigService.clientConfiguration.log_console_warning_active;
        openIDImplicitFlowConfiguration.log_console_debug_active = this.oidcConfigService.clientConfiguration.log_console_debug_active;
        // id_token C8: The iat Claim can be used to reject tokens that were issued too far away from the current time,
        // limiting the amount of time that nonces need to be stored to prevent attacks.The acceptable range is Client specific.
        openIDImplicitFlowConfiguration.max_id_token_iat_offset_allowed_in_seconds =
            this.oidcConfigService.clientConfiguration.max_id_token_iat_offset_allowed_in_seconds;

        const authWellKnownEndpoints = new AuthWellKnownEndpoints();
        // authWellKnownEndpoints.setWellKnownEndpoints(this.oidcConfigService.wellKnownEndpoints);
        // console.log(authWellKnownEndpoints.revocation_endpoint);
        authWellKnownEndpoints.issuer = this.oidcConfigService.clientConfiguration.stsServer;
        authWellKnownEndpoints.jwks_uri = this.oidcConfigService.clientConfiguration.stsServer + '/.well-known/openid-configuration/jwks';
        authWellKnownEndpoints.authorization_endpoint = this.oidcConfigService.clientConfiguration.stsServer + '/connect/authorize';
        authWellKnownEndpoints.token_endpoint = this.oidcConfigService.clientConfiguration.stsServer + '/connect/token';
        authWellKnownEndpoints.userinfo_endpoint = this.oidcConfigService.clientConfiguration.stsServer + '/connect/userinfo';
        authWellKnownEndpoints.end_session_endpoint = this.oidcConfigService.clientConfiguration.stsServer + '/connect/endsession';
        authWellKnownEndpoints.check_session_iframe = this.oidcConfigService.clientConfiguration.stsServer + '/connect/checksession';
        authWellKnownEndpoints.revocation_endpoint = this.oidcConfigService.clientConfiguration.stsServer + '/connect/revocation';
        authWellKnownEndpoints.introspection_endpoint = this.oidcConfigService.clientConfiguration.stsServer + '/connect/introspect';

        this.oidcSecurityService.setupModule(openIDImplicitFlowConfiguration, authWellKnownEndpoints);
    });

    console.log('APP STARTING');
  }

}
