const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "^/api/*": {
        target: "http://localhost:5000",
      },
      "^/socket.io/*": {
        target: "http://localhost:5000",
      },
    },
  },
});
