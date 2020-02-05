<template>
  <div>
    <FormSchema ref="formSchema" v-model="model" @submit="submit">
      <button type="submit">Submit</button>
    </FormSchema>
  </div>
</template>

<script>
import FormSchema from '@formschema/native'

export default {
    components: { FormSchema },
    created() {
        this.axios.get('http://localhost:8000/messages/new').then(
            (response) => {
                let schema = JSON.parse(response.data);
                this.$refs.formSchema.load(schema);
            },
            (error) => {
                console.log(error);
            }
        );
    },
    data() {
        return {
            model: {}
        }
    },
    methods: {
        submit (e) {
            e.preventDefault();
            console.log(model);
        }
    }
};
</script>

<style scoped>
</style>
