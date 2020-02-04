import Vue from 'vue'
import Manager from './components/Manager'

Vue.config.productionTip = false

new Vue({
  name: 'app',
  el: '#manager',
    components: {
        'messages-manager': Manager
    }
})
