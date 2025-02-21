import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'http://127.0.0.1:8000/api/products/';

  constructor(private http: HttpClient) {}

  /**
   * Récupérer les produits avec option de recherche et filtrage par catégorie
   */
  getProducts(searchQuery: string = '', category: string = ''): Observable<any> {
    let params = new HttpParams();

    if (searchQuery) {
      params = params.set('search', searchQuery);
    }

    if (category) {
      params = params.set('category__name', category);
    }

    return this.http.get<any>(this.apiUrl, { params });
  }
}
