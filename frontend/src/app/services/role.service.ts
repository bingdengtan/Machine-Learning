import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import 'rxjs/Rx';

import { CoreUtils, IPager } from '../utils/core.utils';

@Injectable()
export class RoleService {
  restUrl = 'role/';
  constructor(public http: HttpClient, public coreUtils: CoreUtils) {
      this.restUrl = environment.api + this.restUrl;
  }

  save(role: any): Promise<any> {
    return new Promise((resolve, reject) => {
      if (role.id) {
        this.http.put(this.restUrl + role.id + '/', role)
          .toPromise()
          .then( response => {
            resolve(response);
          })
          .catch(e => {
            reject(e);
          });
      } else {
        this.http.post(this.restUrl, role)
        .toPromise()
        .then( response => {
          resolve(response);
        })
        .catch(e => {
          reject(e);
        });
      }
    });
  }

  async delete(id: string): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.delete(this.restUrl + id, {})
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
    const urlParameters = CoreUtils.prototype.getQueryPagination(pager, query);
    console.log(urlParameters);
    return new Promise((resolve, reject) => {
      this.http.get(this.restUrl + urlParameters)
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
