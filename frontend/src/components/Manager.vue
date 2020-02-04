<template>
    <div>
      <v-form v-model="formValid">
        <schema
            :schema="schema"
            :model="dataObject"
            :options="options"
            @error="showError"
            @change="showChange"
            @input="showInput" />
      </v-form>
  </div>
</template>

<script>
import VJsonschemaForm from '@koumoul/vuetify-jsonschema-form'
import '@koumoul/vuetify-jsonschema-form/dist/main.css'

export default {
    components: {
        schema: VJsonschemaForm
    },
    mounted () {
        this.axios.get('http://localhost:8000/messages/new').then(
            (response) => {
                console.log(response.data);
                this.schema = JSON.parse(response.data);
            },
            (error) => {
                console.log(error);
            }
        );
    },
    data() {
        return {
            schema: {},
            dataObject: {},
            formValid: false,
            options: {
                debug: false,
                disableAll: false,
                autoFoldObjects: true
            }
        }
    },
    methods: {
        showError(err) {
            window.alert(err)
        },
        showChange(e) {
            console.log('"change" event', e)
        },
        showInput(e) {
            console.log('"input" event', e)
        }
    }
};
</script>

<style scoped>
</style>
