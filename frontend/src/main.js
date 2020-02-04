import Vue from 'vue'
import Manager from './components/Manager'
import axios from 'axios'
import VueAxios from 'vue-axios'
import vuetify from '@/plugins/vuetify'


Vue.use(VueAxios, axios)
Vue.config.productionTip = false


new Vue({
    vuetify,
    components: {
        'messages-manager': Manager
    }
}).$mount('#manager')
