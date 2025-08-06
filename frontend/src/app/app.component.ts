import { Component } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HttpClientModule],
  template: `<h1>{{ message }}</h1>`,
})
export class AppComponent {
  message = 'FastAPI + Angular!';
}
