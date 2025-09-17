import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Transaction, TransactionService } from './transaction.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h1>My Finance Tracker</h1>

    <form (ngSubmit)="addTransaction()" #txForm="ngForm">
      <input
        [(ngModel)]="newTx.description"
        name="description"
        placeholder="Description"
        required
      />
      <input
        [(ngModel)]="newTx.amount"
        type="number"
        name="amount"
        placeholder="Amount"
        required
      />
      <input
        [(ngModel)]="newTx.category"
        name="category"
        placeholder="Category"
      />
      <select [(ngModel)]="newTx.type" name="type">
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>
      <button type="submit">Add</button>
    </form>

    <ul>
      <li *ngFor="let tx of transactions">
        {{ tx.date }} - {{ tx.description }} ({{ tx.type }}):
        {{ tx.amount }} [{{ tx.category }}]
      </li>
    </ul>
  `,
})
export class AppComponent implements OnInit {
  transactions: Transaction[] = [];
  newTx: Transaction = {
    description: '',
    amount: 0,
    category: '',
    type: 'expense',
  };

  constructor(private txService: TransactionService) {}

  ngOnInit() {
    this.loadTransactions();
  }

  loadTransactions() {
    this.txService.getTransactions().subscribe({
      next: (data) => (this.transactions = data),
      error: () => console.error('Error fetching transactions'),
    });
  }

  addTransaction() {
    this.txService.addTransaction(this.newTx).subscribe({
      next: () => {
        this.newTx = {
          description: '',
          amount: 0,
          category: '',
          type: 'expense',
        };
        this.loadTransactions();
      },
      error: () => console.error('Error adding transaction'),
    });
  }
}
