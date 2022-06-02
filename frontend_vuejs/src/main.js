import Vue from 'vue';
import App from './App.vue';
import router from './Routes';
import store from './store/index';
import vuetify from './plugins/vuetify';
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import Axios from "axios";



Vue.use(Toast,{
  timeout: 2000,
});

Vue.prototype.$http = Axios;

Axios.defaults.headers.common = {
  "Content-Type": "application/json;charset=UTF-8",
  "Access-Control-Allow-Origin": "*"
}
Axios.defaults.baseURL = (process.env.API_PATH !== 'production') ? 'http://127.0.0.1:8000/api/' : '';


Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App), store
}).$mount('#app')
