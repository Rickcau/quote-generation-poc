import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { QuoteListComponent } from './components/quote-list/quote-list.component';
import { QuotePreviewComponent } from './components/quote-preview/quote-preview.component';
import { TemplateBuilderComponent } from './components/template-builder/template-builder.component';

const routes: Routes = [
  { path: '', component: QuoteListComponent },
  { path: 'quotes/:id', component: QuotePreviewComponent },
  { path: 'templates/builder', component: TemplateBuilderComponent },
  { path: 'templates/builder/:id', component: TemplateBuilderComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
