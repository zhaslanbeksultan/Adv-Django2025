const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: {
        port: 5173,
    },
  transpileDependencies: true
})
