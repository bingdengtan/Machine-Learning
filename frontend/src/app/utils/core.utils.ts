import {Injectable} from '@angular/core';
import * as moment from 'moment';

export interface IPager {
    pageNumber: number;
    pageSize: number;
    sortBy: string;
    orderBy: string;
}

@Injectable()
export class CoreUtils {
    static FORMAT_DATE = 'YYYY-MM-DD';
    static FORMAT_DATE_TIME = 'YYYY-MM-DD HH:mm:ss';

    getAppHostName(): String {
        return location.protocol + '//' + location.hostname;
    }

    getDateFormat(date): String {
        let val;
        // date = moment.utc(date);
        date = moment(date);
        if (date.isValid) {
            val = date.format(CoreUtils.FORMAT_DATE_TIME);
        }
        return val;
    }
}
