import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { CommonModule } from '@angular/common'; // ✅ Import de CommonModule
import { FormsModule } from '@angular/forms'; // ✅ Import pour ngModel

// ✅ Définition de l'interface Product pour un typage strict
interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  imageUrl: string;
}

@Component({
  selector: 'app-product-list',
  standalone: true, // ✅ Assure que c'est un composant autonome
  imports: [CommonModule, FormsModule], // ✅ Ajout de CommonModule et FormsModule ici
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit {
  @ViewChild('productSlider', { static: false }) productSlider!: ElementRef;

  products: Product[] = [];
  filteredProducts: Product[] = [];
  searchQuery: string = '';
  selectedCategory: string = '';
  categories: string[] = [];

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.productService.getProducts().subscribe(
      (data: Product[]) => {
        console.log('✅ Données API reçues :', data);
        this.products = data;
        this.filteredProducts = data;

        // ✅ Vérification que category est bien un string avant de l'utiliser
        this.categories = ['Toutes les catégories', ...Array.from(new Set(
          data.map((p: Product) => String(p.category))
        ))];

        console.log('📌 Catégories extraites :', this.categories);
      },
      (error) => {
        console.error('❌ Erreur lors de la récupération des produits:', error);
      }
    );
  }

  /**
   * ✅ Filtrer les produits selon la recherche et la catégorie sélectionnée
   */
  applyFilters(): void {
    console.log('🛠️ Filtrage en cours...');
    console.log('🔍 Recherche :', this.searchQuery);
    console.log('📂 Catégorie :', this.selectedCategory);

    this.filteredProducts = this.products.filter(product => {
      const matchesSearch = this.searchQuery
        ? String(product.name).toLowerCase().includes(this.searchQuery.toLowerCase())
        : true;

      const matchesCategory = this.selectedCategory && this.selectedCategory !== 'Toutes les catégories'
        ? String(product.category) === this.selectedCategory
        : true;

      return matchesSearch && matchesCategory;
    });

    console.log('🎯 Produits après filtrage :', this.filteredProducts);
  }

  onSearch(): void {
    console.log('🔍 Recherche déclenchée avec :', this.searchQuery);
    this.applyFilters();
  }

  onCategoryChange(): void {
    console.log('📂 Changement de catégorie détecté :', this.selectedCategory);
    this.applyFilters();
  }

  /**
   * ✅ Optimisation du rendu des catégories dans *ngFor
   */
  trackByCategory(index: number, category: string): string {
    return category;
  }

  /**
   * ✅ Optimisation du rendu des produits dans *ngFor
   */
  trackByProduct(index: number, product: Product): number {
    return product.id;
  }

  /**
   * ✅ Ajout du défilement horizontal pour les produits en utilisant ViewChild
   */
  scrollLeft(): void {
    if (this.productSlider) {
      this.productSlider.nativeElement.scrollBy({ left: -300, behavior: 'smooth' });
    }
  }

  scrollRight(): void {
    if (this.productSlider) {
      this.productSlider.nativeElement.scrollBy({ left: 300, behavior: 'smooth' });
    }
  }
}
