module.exports = {
    port: parseInt(process.env.PORT, 10) || 3000,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || '',
    adminToken: process.env.ADMIN_TOKEN || 'dev-admin-token',
};
