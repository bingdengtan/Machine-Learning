import { Injectable, Injector } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { HttpErrorResponse } from '@angular/common/http/src/response';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    private oidcSecurityService: OidcSecurityService;

    constructor(private injector: Injector, private router: Router) {
    }

    private handleAuthError(err: HttpErrorResponse): Observable<any> {
        // handle your auth error or rethrow
        if (err.status === 401 || err.status === 403) {
            // navigate /delete cookies or whatever
            this.router.navigateByUrl(`/unauthorized`);
        }
        return Observable.throw(err);
    }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        let requestToForward = req;

        if (this.oidcSecurityService === undefined) {
            this.oidcSecurityService = this.injector.get(OidcSecurityService);
        }
        if (this.oidcSecurityService !== undefined) {
            const token = this.oidcSecurityService.getToken();
            if (token !== '') {
                const tokenValue = 'Bearer ' + token;
                requestToForward = req.clone({ setHeaders: { 'Authorization': tokenValue} });
            }
        } else {
            console.log('OidcSecurityService undefined: NO auth header!');
        }
        return next.handle(requestToForward).catch( err => this.handleAuthError(err));
    }
}
