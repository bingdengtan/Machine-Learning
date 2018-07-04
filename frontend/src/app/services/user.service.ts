import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import 'rxjs/Rx';

import { CoreUtils } from '../utils/core.utils';

@Injectable()
export class UserService {
  restUrl = 'user';
  constructor(public http: HttpClient, public coreUtils: CoreUtils) {
      this.restUrl = environment.api + this.restUrl;
  }

  getUsers(): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.post(this.restUrl + '/list', null)
        .toPromise()
        .then( response => {
          resolve(response);
        })
        .catch(e => {
          reject(e);
        });
    });
  }

  save(user: any): Promise<any> {
    return new Promise((resolve, reject) => {
      let action = 'create';
      if (user._id) {
        action = 'update';
      }

      this.http.post(this.restUrl + '/' + action, {user: user})
        .toPromise()
        .then( response => {
          resolve(response);
        })
        .catch(e => {
          reject(e);
        });
    });
  }

  delete(ids: Array<string>): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.post(this.restUrl + '/delete', {ids: ids})
        .toPromise()
        .then( response => {
          resolve(response);
        })
        .catch(e => {
          reject(e);
        });
    });
  }
}
