const { db } = require('../database');

const PaymentModel = {
    create: (enrollmentId, amount, status) =>
        db.run('INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
            [enrollmentId, amount, status]),

    findByEnrollment: (enrollmentId) =>
        db.get('SELECT amount, status FROM payments WHERE enrollment_id = ?', [enrollmentId]),
};

module.exports = PaymentModel;
