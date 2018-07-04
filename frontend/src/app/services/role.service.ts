import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import 'rxjs/Rx';

import { CoreUtils, IPager } from '../utils/core.utils';

@Injectable()
export class RoleService {
  restUrl = 'role';
  constructor(public http: HttpClient, public coreUtils: CoreUtils) {
      this.restUrl = environment.api + this.restUrl;
  }

  save(role: any): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.post(this.restUrl + '/create', role)
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

  list(pager: IPager, query: any): Promise<any> {
    const data = pager;
    data['query'] = query;

    return new Promise((resolve, reject) => {
      this.http.post(this.restUrl + '/list', data)
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
