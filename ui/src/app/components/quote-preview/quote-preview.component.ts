import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ApiService } from '../../services/api.service';
import { QuoteDetail } from '../../models/quote.model';

@Component({
  selector: 'app-quote-preview',
  templateUrl: './quote-preview.component.html',
  styleUrl: './quote-preview.component.css'
})
export class QuotePreviewComponent implements OnInit {
  quote: QuoteDetail | null = null;
  previewHtml: SafeHtml = '';
  selectedTemplate: string = 'formal';
  loading = true;
  editing = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.apiService.getQuote(id).subscribe({
      next: (quote) => {
        this.quote = quote;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  onTemplateChanged(templateKey: string): void {
    this.selectedTemplate = templateKey;
    this.loadPreview();
  }

  loadPreview(): void {
    if (!this.quote) return;
    this.apiService.previewDocument({
      quote_id: this.quote.quote_id,
      template_key: this.selectedTemplate
    }).subscribe(html => {
      this.previewHtml = this.sanitizer.bypassSecurityTrustHtml(html);
    });
  }

  toggleEdit(): void {
    this.editing = !this.editing;
  }

  downloadPdf(): void {
    if (!this.quote) return;
    this.apiService.renderDocument({
      quote_id: this.quote.quote_id,
      template_key: this.selectedTemplate,
      format: 'pdf'
    }).subscribe(blob => {
      this.triggerDownload(blob, `${this.quote!.quote_number}.pdf`);
    });
  }

  downloadDocx(): void {
    if (!this.quote) return;
    this.apiService.renderDocument({
      quote_id: this.quote.quote_id,
      template_key: this.selectedTemplate,
      format: 'docx'
    }).subscribe(blob => {
      this.triggerDownload(blob, `${this.quote!.quote_number}.docx`);
    });
  }

  private triggerDownload(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  goBack(): void {
    this.router.navigate(['/']);
  }
}
