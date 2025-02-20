import { Component } from '@angular/core';
import { ProductListComponent } from './components/product-list/product-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ProductListComponent],  // ✅ Ajout du composant ici !
  template: `
    <h1>Welcome to FarmShop</h1>
    <app-product-list></app-product-list> <!-- Affichage des produits -->
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {}
