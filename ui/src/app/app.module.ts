import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { QuoteListComponent } from './components/quote-list/quote-list.component';
import { QuotePreviewComponent } from './components/quote-preview/quote-preview.component';
import { QuoteEditorComponent } from './components/quote-editor/quote-editor.component';
import { TemplateSelectorComponent } from './components/template-selector/template-selector.component';
import { TemplateBuilderComponent } from './components/template-builder/template-builder.component';

@NgModule({
  declarations: [
    AppComponent,
    QuoteListComponent,
    QuotePreviewComponent,
    QuoteEditorComponent,
    TemplateSelectorComponent,
    TemplateBuilderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
