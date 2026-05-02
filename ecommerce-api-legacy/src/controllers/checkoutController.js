const { processCheckout } = require('../services/checkoutService');

async function checkout(req, res, next) {
    const { usr: name, eml: email, pwd: password, c_id: courseId, card: cardNumber } = req.body;

    if (!name || !email || !courseId || !cardNumber) {
        return res.status(400).json({ error: 'Bad Request' });
    }

    try {
        const result = await processCheckout({ name, email, password, courseId, cardNumber });
        res.status(200).json({ msg: 'Sucesso', enrollment_id: result.enrollmentId });
    } catch (err) {
        next(err);
    }
}

module.exports = { checkout };
