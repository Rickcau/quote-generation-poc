import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ApiService } from '../../services/api.service';
import { QuoteSummary } from '../../models/quote.model';

@Component({
  selector: 'app-quote-list',
  templateUrl: './quote-list.component.html',
  styleUrl: './quote-list.component.css'
})
export class QuoteListComponent implements OnInit, AfterViewInit {
  displayedColumns: string[] = ['quote_number', 'customer_name', 'status', 'total', 'quote_date'];
  dataSource = new MatTableDataSource<QuoteSummary>([]);
  loading = true;

  @ViewChild(MatSort) sort!: MatSort;

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.apiService.getQuotes().subscribe({
      next: (quotes) => {
        this.dataSource.data = quotes;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  ngAfterViewInit(): void {
    this.dataSource.sort = this.sort;
  }

  onRowClick(quote: QuoteSummary): void {
    this.router.navigate(['/quotes', quote.quote_id]);
  }
}
