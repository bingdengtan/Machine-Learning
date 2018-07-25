import { Component, OnInit, ViewChild, TemplateRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';

import { UserService } from '../../services/user.service';
import { ModelService } from '../../services/model.service';
import { ProjectService } from '../../services/project.service';
import { CoreUtils } from '../../utils/core.utils';
import { GridColumn, GridMenu, GridComponent } from '../../components/grid/grid.component';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { ToastrService } from 'ngx-toastr';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
declare var $: any;

interface IModel {
  name: string;
  path: string;
  project: any;
  description: string;
  creation_date: null;
  created_by: string;
  last_updated_date: null;
  last_updated_by: string;
}

@Component({
  selector: 'app-model',
  templateUrl: './model.component.html',
  styleUrls: ['./model.component.scss']
})
export class ModelComponent implements OnInit {
  @ViewChild(GridComponent) gridComponent: GridComponent;
  @ViewChild(ConfirmDialogComponent) confirmDialog: ConfirmDialogComponent;

  title = 'Model Profile';
  restUrl = '';
  gridColumns: any[] = new Array();
  gridActions: any[] = new Array();
  projects: any[] = new Array();
  model: IModel = {name: '', path: '', project: null,
    description: '', creation_date: null, created_by: '', last_updated_date: null, last_updated_by: ''};

  modalRef: BsModalRef;
  confirmDialogTitle: string;
  confirmDialogMessage: string;

  projectSelectedId: string;

  constructor(public coreUtils: CoreUtils,
    public modelService: ModelService,
    public projectService: ProjectService,
    private oidcSecurityService: OidcSecurityService,
    private toastr: ToastrService,
    private modalService: BsModalService
  ) {
    this.confirmDialogTitle = 'Roles Management';
  }

  ngOnInit() {
    window.dispatchEvent(new Event('resize'));
    this.initGrid();
    this.initProjects();
  }

  menuActionNew(): void {
    this.model = {name: '', path: '', project: null,
      description: '', creation_date: null, created_by: '', last_updated_date: null, last_updated_by: ''};
    $('#myModal').modal('show');
  }

  save(): void {
    const $btn = $('#saveButton').button('loading');
    this.modelService.save(this.model).then( response => {
      $btn.button('reset');
      if ($('#myModal').modal('hide')) {
        this.gridComponent.loadGrid(1);
      }
    }).catch(e => {
      $btn.button('reset');
      this.toastr.error(e.error.detail, 'Save Failed');
    });
  }

  menuActionEdit(): void {
    const rows = this.gridComponent.getSelectedRows();
    if (rows.length !== 1) {
      this.toastr.warning('Please select one document to edit.', '', {
        positionClass: 'toast-top-center'
      });
    } else {
      this.model = JSON.parse(JSON.stringify(rows[0]));
      $('#myModal').modal('show');
    }
  }

  menuActionDelete(): void {
    const selectedIds = this.gridComponent.getSelectedIds();
    if (selectedIds.length <= 0 ) {
      this.toastr.warning('Please select document first', '', {
        positionClass: 'toast-top-center'
      });
    } else {
      this.confirmDialogMessage = 'Are you sure to delete the selected document(s)';
      this.confirmDialog.show();
    }
  }

  confirmCallback(confirm): void {
    this.confirmDialog.hide();
    if (confirm) {
      setTimeout(() => {
        this.confirmDeletetion();
      }, 500);
    }
  }

  confirmDeletetion(): void {
    const selectedIds = this.gridComponent.getSelectedIds();
    selectedIds.forEach(async id => {
      await this.modelService.delete(id).then( response => {
          this.toastr.success('Delete completed', '');
          this.gridComponent.loadGrid(1);
      }).catch(e => {
        this.toastr.error(e.error.detail, 'Delete Failed');
      });
    });
  }

  closeConfirmDialog(): void {
    this.modalRef.hide();
  }

  cellClickAction(row): void {
    this.model = JSON.parse(JSON.stringify(row));
    this.model['project'] = this.model['project'].id;
    $('#myModal').modal('show');
  }

  getDateFormat(row, val): String {
    return this.coreUtils.getDateFormat(val);
  }

  initProjects(): void {
    this.projectService.list({pageNumber: 1, pageSize: 100, sortBy: 'name', orderBy: 'asc'}, {})
    .then(projects => {
      this.projects = projects.results.map(project => {
        return {selected: false, id: project.id, name: project.name};
      });
    });
  }

  initGrid(): void {
    this.restUrl = this.modelService.restUrl;

    let nameCol: GridColumn = {title: 'ID', filedName: 'id', width: null, columnFormat: null, display: false,
      click: null,
      sort: {enable: false, sortBy: null}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Project', filedName: 'project.name', width: null, columnFormat: null, display: true,
      click: null,
      sort: {enable: false, sortBy: ''}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Name', filedName: 'name', width: null, columnFormat: null, display: true,
      click: this.cellClickAction.bind(this),
      sort: {enable: true, sortBy: 'name'}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Path', filedName: 'path', width: null, columnFormat: null, display: true,
      click: null,
      sort: {enable: false, sortBy: ''}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Description', filedName: 'description', width: null, columnFormat: null, display: true,
      click: null,
      sort: {enable: false, sortBy: ''}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Creation Date', filedName: 'creation_date', width: null, columnFormat: this.getDateFormat.bind(this),
      display: false,
      click: null,
      sort: {enable: true, sortBy: 'creation_date'}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Creation By', filedName: 'created_by', width: null, columnFormat: null,
      display: false,
      click: null,
      sort: {enable: true, sortBy: 'created_by'}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Last Updated Date', filedName: 'last_updated_date', width: null, columnFormat: this.getDateFormat.bind(this),
      display: true,
      click: null,
      sort: {enable: true, sortBy: 'last_updated_date'}};
    this.gridColumns.push(nameCol);

    nameCol = {title: 'Last Updated By', filedName: 'last_updated_by', width: null, columnFormat: null,
      display: false,
      click: null,
      sort: {enable: true, sortBy: 'last_updated_by'}};
    this.gridColumns.push(nameCol);

    // actions
     let gridMenu: GridMenu;
    gridMenu = {title: 'New', aClass: 'btn-primary', faIcon: 'fa fa-sticky-note-o',
      action: this.menuActionNew.bind(this), subMenus: []};
    this.gridActions.push(gridMenu);

    gridMenu = {title: 'Edit', aClass: 'btn-info', faIcon: 'fa fa-edit',
      action: this.menuActionEdit.bind(this), subMenus: []};
    this.gridActions.push(gridMenu);

    gridMenu = {title: 'Delete', aClass: 'btn-danger', faIcon: 'fa fa-trash',
      action: this.menuActionDelete.bind(this), subMenus: []};
    this.gridActions.push(gridMenu);

    // gridMenu = {title: 'More', aClass: 'btn-primary', faIcon: 'fa fa-trash',
    //   action: null, subMenus: [{title: 'More 1', action: this.menuActionDelete}, {title: 'More 2', action: this.menuActionDelete}]};
    // this.gridActions.push(gridMenu);
  }
}
