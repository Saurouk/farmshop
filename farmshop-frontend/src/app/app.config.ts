import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router'; // ❌ Suppression de `withDebug`
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient()
  ]
};
