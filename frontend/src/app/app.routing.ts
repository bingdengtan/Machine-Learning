import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { AuthorizationGuard } from './services/authorization.guard';

import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { HomeComponent } from './pages/home/home.component';
import { UnauthorizedComponent } from './pages/unauthorized/unauthorized.component';
import { StarterComponent } from './pages/starter/starter.component';
import { ForbiddenComponent } from './pages/forbidden/forbidden.component';
import { AuthorizedComponent } from './pages/authorized/authorized.component';
import { RoleComponent } from './pages/role/role.component';
import { UserComponent } from './pages/user/user.component';
import { ModelComponent } from './pages/model/model.component';
import { ProjectComponent } from './pages/project/project.component';

@NgModule({
  imports: [
    RouterModule.forRoot([
      { path: '', redirectTo: 'starter', pathMatch: 'full' },
      { path: 'starter', component: StarterComponent},
      { path: 'authorized', component: AuthorizedComponent},
      { path: 'unauthorized', component: UnauthorizedComponent },
      { path: 'forbidden', component: ForbiddenComponent },
      { path: 'dashboard', component: DashboardComponent,
        children: [
          { path: 'home', component: HomeComponent, canActivate: [AuthorizationGuard] },
          { path: 'adm/project', component: ProjectComponent, canActivate: [AuthorizationGuard] },
          { path: 'adm/model', component: ModelComponent, canActivate: [AuthorizationGuard] },
          { path: 'adm/input', component: ModelComponent, canActivate: [AuthorizationGuard] },
          { path: 'adm/output', component: ModelComponent, canActivate: [AuthorizationGuard] },
          { path: 'adm/roles', component: RoleComponent, canActivate: [AuthorizationGuard] },
          { path: 'adm/users', component: UserComponent, canActivate: [AuthorizationGuard]}
        ]
      }
    ])
  ],
  declarations: [],
  exports: [RouterModule]
})

export class AppRoutingModule {}
