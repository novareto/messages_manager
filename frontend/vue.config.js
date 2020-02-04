// vue.config.js
module.exports = {
    filenameHashing: false,
    devServer: {
        port: 8091,
        disableHostCheck: true
    },
    configureWebpack: {
        resolve: {
            alias: {
                'vue$': 'vue/dist/vue.esm.js'
            }
        }
    }
}
