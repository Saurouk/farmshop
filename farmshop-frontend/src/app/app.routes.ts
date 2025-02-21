import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./components/home/home.component').then(m => m.HomeComponent) }, // Accueil
  { path: 'products', loadComponent: () => import('./components/product-list/product-list.component').then(m => m.ProductListComponent) }, // Produits
  { path: 'blog', loadComponent: () => import('./components/blog/blog.component').then(m => m.BlogComponent) }, // Blog
  { path: 'contact', loadComponent: () => import('./components/contact/contact.component').then(m => m.ContactComponent) }, // Contact
  { path: 'login', loadComponent: () => import('./components/login/login.component').then(m => m.LoginComponent) }, // Connexion
  { path: '**', redirectTo: '', pathMatch: 'full' } // Redirection vers l'accueil en cas d'erreur
];
