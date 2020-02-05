import Vue from 'vue'
import Manager from './components/Manager'
import axios from 'axios'
import VueAxios from 'vue-axios'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import SchemaJsonVue from 'schema-json-vue'

Vue.use(ElementUI)
Vue.use(SchemaJsonVue)
Vue.use(VueAxios, axios)
Vue.config.productionTip = false

new Vue({
    components: {
        'messages-manager': Manager
    }
}).$mount('#manager')
