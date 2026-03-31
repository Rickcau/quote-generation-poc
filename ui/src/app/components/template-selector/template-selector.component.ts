import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { TemplateSummary } from '../../models/quote.model';

@Component({
  selector: 'app-template-selector',
  templateUrl: './template-selector.component.html',
  styleUrl: './template-selector.component.css'
})
export class TemplateSelectorComponent implements OnInit {
  templates: TemplateSummary[] = [];
  @Input() selectedKey: string = '';
  @Output() templateChanged = new EventEmitter<string>();

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getTemplates().subscribe(templates => {
      this.templates = templates;
      if (!this.selectedKey && templates.length > 0) {
        const def = templates.find(t => t.is_default) || templates[0];
        this.selectedKey = def.template_key;
        this.templateChanged.emit(this.selectedKey);
      }
    });
  }

  onSelectionChange(key: string): void {
    this.selectedKey = key;
    this.templateChanged.emit(key);
  }
}
