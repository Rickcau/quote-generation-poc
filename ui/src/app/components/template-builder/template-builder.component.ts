import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api.service';
import { TemplateSectionConfig } from '../../models/quote.model';

interface SectionItem {
  section_type: string;
  label: string;
  enabled: boolean;
  sort_order: number;
  config: any;
}

@Component({
  selector: 'app-template-builder',
  templateUrl: './template-builder.component.html',
  styleUrl: './template-builder.component.css'
})
export class TemplateBuilderComponent implements OnInit {
  templateId: number | null = null;
  templateName: string = '';
  templateKey: string = '';
  isSystem: boolean = false;
  colorScheme: string = '#1a365d';
  fontFamily: string = 'Calibri';
  previewHtml: SafeHtml = '';

  colorOptions = [
    { label: 'Blue', value: '#1a365d' },
    { label: 'Teal', value: '#0d9488' },
    { label: 'Green', value: '#166534' },
    { label: 'Red', value: '#991b1b' },
    { label: 'Purple', value: '#6b21a8' }
  ];

  fontOptions = ['Calibri', 'Arial', 'Georgia', 'Roboto'];

  sections: SectionItem[] = [
    { section_type: 'header', label: 'Header', enabled: true, sort_order: 1, config: null },
    { section_type: 'summary', label: 'Summary', enabled: true, sort_order: 2, config: null },
    { section_type: 'line_items', label: 'Line Items', enabled: true, sort_order: 3, config: null },
    { section_type: 'regulatory', label: 'Regulatory Notes', enabled: true, sort_order: 4, config: null },
    { section_type: 'terms', label: 'Terms & Conditions', enabled: true, sort_order: 5, config: null },
    { section_type: 'signature', label: 'Signature Block', enabled: true, sort_order: 6, config: null }
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService,
    private sanitizer: DomSanitizer,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.templateId = Number(idParam);
      this.apiService.getTemplate(this.templateId).subscribe(t => {
        this.templateName = t.template_name;
        this.templateKey = t.template_key;
        this.isSystem = t.is_system;
        if (t.style_config) {
          this.colorScheme = t.style_config.color_scheme || '#1a365d';
          this.fontFamily = t.style_config.font_family || 'Calibri';
        }
        if (t.sections && t.sections.length > 0) {
          this.sections = t.sections.map(s => ({
            section_type: s.section_type,
            label: s.label,
            enabled: s.enabled,
            sort_order: s.sort_order,
            config: s.config
          }));
        }
        this.loadPreview();
      });
    } else {
      this.loadPreview();
    }
  }

  moveUp(index: number): void {
    if (index <= 0) return;
    [this.sections[index], this.sections[index - 1]] = [this.sections[index - 1], this.sections[index]];
    this.updateSortOrders();
    this.loadPreview();
  }

  moveDown(index: number): void {
    if (index >= this.sections.length - 1) return;
    [this.sections[index], this.sections[index + 1]] = [this.sections[index + 1], this.sections[index]];
    this.updateSortOrders();
    this.loadPreview();
  }

  toggleSection(index: number): void {
    this.sections[index].enabled = !this.sections[index].enabled;
    this.loadPreview();
  }

  private updateSortOrders(): void {
    this.sections.forEach((s, i) => s.sort_order = i + 1);
  }

  loadPreview(): void {
    this.apiService.previewTemplate({
      sections: this.sections,
      style_config: { color_scheme: this.colorScheme, font_family: this.fontFamily }
    }).subscribe(html => {
      this.previewHtml = this.sanitizer.bypassSecurityTrustHtml(html);
    });
  }

  save(): void {
    const data: any = {
      template_name: this.templateName,
      template_key: this.templateKey || this.templateName.toLowerCase().replace(/\s+/g, '_'),
      style_config: { color_scheme: this.colorScheme, font_family: this.fontFamily },
      sections: this.sections
    };

    const obs = this.templateId
      ? this.apiService.updateTemplate(this.templateId, data)
      : this.apiService.createTemplate(data);

    obs.subscribe({
      next: () => {
        this.snackBar.open('Template saved', 'OK', { duration: 3000 });
        if (!this.templateId) this.router.navigate(['/']);
      },
      error: () => {
        this.snackBar.open('Failed to save template', 'OK', { duration: 3000 });
      }
    });
  }

  deleteTemplate(): void {
    if (!this.templateId || this.isSystem) return;
    this.apiService.deleteTemplate(this.templateId).subscribe({
      next: () => {
        this.snackBar.open('Template deleted', 'OK', { duration: 3000 });
        this.router.navigate(['/']);
      }
    });
  }
}
