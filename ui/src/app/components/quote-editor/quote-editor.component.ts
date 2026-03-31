import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api.service';
import { QuoteDetail } from '../../models/quote.model';

@Component({
  selector: 'app-quote-editor',
  templateUrl: './quote-editor.component.html',
  styleUrl: './quote-editor.component.css'
})
export class QuoteEditorComponent implements OnInit {
  @Input() quote!: QuoteDetail;
  @Input() selectedTemplate: string = 'formal';
  @Output() saved = new EventEmitter<void>();
  @Output() cancelled = new EventEmitter<void>();

  form!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      notes: [this.quote.notes || ''],
      regulatory_notes: [this.quote.regulatory_notes || ''],
      line_items: this.fb.array(
        this.quote.line_items.map(item =>
          this.fb.group({
            line_item_id: [item.line_item_id],
            service_description: [item.service_description],
            quantity: [item.quantity],
            unit_price: [item.unit_price]
          })
        )
      )
    });
  }

  get lineItems(): FormArray {
    return this.form.get('line_items') as FormArray;
  }

  save(): void {
    const val = this.form.value;
    const update: any = {};
    if (val.notes !== this.quote.notes) update.notes = val.notes;
    if (val.regulatory_notes !== this.quote.regulatory_notes) update.regulatory_notes = val.regulatory_notes;

    const editedItems = val.line_items
      .filter((item: any, i: number) => {
        const orig = this.quote.line_items[i];
        return item.service_description !== orig.service_description ||
               item.quantity !== orig.quantity ||
               item.unit_price !== orig.unit_price;
      })
      .map((item: any) => ({
        line_item_id: item.line_item_id,
        service_description: item.service_description,
        quantity: item.quantity,
        unit_price: item.unit_price
      }));

    if (editedItems.length > 0) update.line_items = editedItems;

    this.apiService.updateQuote(this.quote.quote_id, update).subscribe({
      next: () => {
        this.snackBar.open('Quote updated', 'OK', { duration: 3000 });
        this.saved.emit();
      },
      error: () => {
        this.snackBar.open('Failed to update quote', 'OK', { duration: 3000 });
      }
    });
  }

  cancel(): void {
    this.cancelled.emit();
  }
}
