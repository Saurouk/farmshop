import { Component } from '@angular/core';
import { RouterModule } from '@angular/router'; // ✅ Ajout de RouterModule pour le routing

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule], // ✅ Utilisation du RouterModule pour gérer le routage
  template: `
    <header class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <a class="navbar-brand" routerLink="/">FarmShop</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" routerLink="/">Accueil</a></li>
            <li class="nav-item"><a class="nav-link" routerLink="/products">Produits</a></li>
            <li class="nav-item"><a class="nav-link" routerLink="/blog">Blog</a></li>
            <li class="nav-item"><a class="nav-link" routerLink="/contact">Contact</a></li>
            <li class="nav-item"><a class="nav-link btn btn-primary text-white ms-3" routerLink="/login">Connexion</a></li>
          </ul>
        </div>
      </div>
    </header>

    <!-- Contenu dynamique -->
    <main class="container mt-4">
      <router-outlet></router-outlet>  <!-- ✅ Zone où s'affichent les composants des routes -->
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3 mt-4">
      <div class="container">
        <p>© 2024 FarmShop - Tous droits réservés</p>
        <ul class="list-inline">
          <li class="list-inline-item"><a href="/cgv" class="text-white">CGV</a></li>
          <li class="list-inline-item"><a href="/politique" class="text-white">Politique de confidentialité</a></li>
          <li class="list-inline-item"><a href="/contact" class="text-white">Contact</a></li>
        </ul>
      </div>
    </footer>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {}
