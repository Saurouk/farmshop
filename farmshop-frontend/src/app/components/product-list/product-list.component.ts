import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  imageUrl: string;
}

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit, AfterViewInit {
  @ViewChild('productSlider', { static: false }) productSlider!: ElementRef;

  products: Product[] = [];
  filteredProducts: Product[] = [];
  searchQuery: string = '';
  selectedCategory: string = '';
  categories: string[] = [];

  constructor(private productService: ProductService, private router: Router) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  ngAfterViewInit(): void {
    if (this.productSlider) {
      console.log('✅ Slider détecté:', this.productSlider.nativeElement);
    }
  }

  loadProducts(): void {
    this.productService.getProducts().subscribe(
      (data: Product[]) => {
        console.log('✅ Données API reçues :', data);
        this.products = data;
        this.filteredProducts = data;

        // ✅ Correction de la duplication de "Toutes les catégories"
        const uniqueCategories = Array.from(new Set(data.map(p => p.category))).filter(Boolean);
        this.categories = uniqueCategories;

        console.log('📌 Catégories extraites :', this.categories);
      },
      (error) => {
        console.error('❌ Erreur lors de la récupération des produits:', error);
      }
    );
  }

  applyFilters(): void {
    this.filteredProducts = this.products.filter(product => {
      const matchesSearch = this.searchQuery
        ? product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        : true;

      const matchesCategory = this.selectedCategory !== ''
        ? product.category === this.selectedCategory
        : true;

      return matchesSearch && matchesCategory;
    });

    console.log('🎯 Produits après filtrage :', this.filteredProducts);
  }

  onSearch(): void {
    this.applyFilters();
  }

  onCategoryChange(): void {
    this.applyFilters();
  }

  trackByCategory(index: number, category: string): string {
    return category;
  }

  trackByProduct(index: number, product: Product): number {
    return product.id;
  }

  /**
   * ✅ Correction du bouton "Voir plus" : Navigation correcte
   */
  viewProductDetails(productId: number): void {
    this.router.navigate(['/product-detail', productId]);
  }

  /**
   * ✅ Correction du défilement horizontal des produits
   */
  scrollLeft(): void {
    if (this.productSlider?.nativeElement) {
      this.productSlider.nativeElement.scrollBy({ left: -300, behavior: 'smooth' });
    }
  }

  scrollRight(): void {
    if (this.productSlider?.nativeElement) {
      this.productSlider.nativeElement.scrollBy({ left: 300, behavior: 'smooth' });
    }
  }
}
