import Vue from 'vue'
import app from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from "./routers";
import store from './store'

Vue.config.productionTip = false


new Vue ({
    render: h => h(app),
    router:router,
    store:store
}).$mount('#app')

