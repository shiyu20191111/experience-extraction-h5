const localtunnel = require('localtunnel');

(async () => {
  const tunnel = await localtunnel({ subdomain: 'chaoai-cti-h5', port: 8080 });

  console.log('=== 公网访问链接 ===');
  console.log(tunnel.url);
  console.log('====================');
  console.log('');
  console.log('移动端和PC端均可通过上方链接访问');
  console.log('按 Ctrl+C 停止服务');

  tunnel.on('close', () => {
    console.log('隧道已关闭');
  });
})();
