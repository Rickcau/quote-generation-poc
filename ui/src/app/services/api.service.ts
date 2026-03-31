import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { QuoteSummary, QuoteDetail, TemplateSummary, TemplateDetail } from '../models/quote.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = '/api';

  constructor(private http: HttpClient) {}

  getQuotes(): Observable<QuoteSummary[]> { return this.http.get<QuoteSummary[]>(`${this.base}/quotes`); }
  getQuote(id: number): Observable<QuoteDetail> { return this.http.get<QuoteDetail>(`${this.base}/quotes/${id}`); }
  updateQuote(id: number, data: any): Observable<any> { return this.http.put(`${this.base}/quotes/${id}`, data); }
  getTemplates(): Observable<TemplateSummary[]> { return this.http.get<TemplateSummary[]>(`${this.base}/templates`); }
  getTemplate(id: number): Observable<TemplateDetail> { return this.http.get<TemplateDetail>(`${this.base}/templates/${id}`); }
  createTemplate(data: any): Observable<any> { return this.http.post(`${this.base}/templates`, data); }
  updateTemplate(id: number, data: any): Observable<any> { return this.http.put(`${this.base}/templates/${id}`, data); }
  deleteTemplate(id: number): Observable<any> { return this.http.delete(`${this.base}/templates/${id}`); }
  previewDocument(data: any): Observable<string> { return this.http.post(`${this.base}/documents/preview`, data, { responseType: 'text' as any }); }
  renderDocument(data: any): Observable<Blob> { return this.http.post(`${this.base}/documents/render`, data, { responseType: 'blob' }); }
  previewTemplate(data: any): Observable<string> { return this.http.post(`${this.base}/templates/preview`, data, { responseType: 'text' as any }); }
}
