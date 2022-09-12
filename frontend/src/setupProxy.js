const { createProxyMiddleware } = require('http-proxy-middleware');
const proxy = {
    // target: "http://api.synestify.com",
    target: "http://127.0.0.1:5000",
    changeOrigin: true
}

module.exports = function(app) {
  app.use(
    '/status',
    createProxyMiddleware(proxy)
  );
  app.use(
    '/genres',
    createProxyMiddleware(proxy)
  );
  app.use(
    '/analysis',
    createProxyMiddleware(proxy)
  );
};