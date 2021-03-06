import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

import { BasicModelService } from './basic.model.service';
import { CoreUtils, IPager } from '../utils/core.utils';

@Injectable()
export class ProjectService extends BasicModelService {
  constructor(public http: HttpClient, public coreUtils: CoreUtils) {
    super(http, coreUtils);
    this.restUrl = environment.api + 'adm/project/';
  }
}
