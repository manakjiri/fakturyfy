import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


// Vuetify
import 'vuetify/styles'
import { createVuetify} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        },
    },
    theme: {
        defaultTheme: 'dark',
    }
    
})
  

const app = createApp(App)

app.use(router)
app.use(vuetify)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
    // Handle the error globally
    console.error("Global error:", err);
    console.log("Vue instance:", instance);
    console.log("Error info:", info);

    // Add code for UI notifications, reporting or other error handling logic
};


app.mount('#app')
