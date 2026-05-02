const UserModel = require('../models/userModel');
const CourseModel = require('../models/courseModel');
const EnrollmentModel = require('../models/enrollmentModel');
const PaymentModel = require('../models/paymentModel');
const AuditModel = require('../models/auditModel');
const { hashPassword } = require('../utils/crypto');

async function processCheckout({ name, email, password, courseId, cardNumber }) {
    const course = await CourseModel.findActiveById(courseId);
    if (!course) {
        throw Object.assign(new Error('Curso não encontrado'), { status: 404 });
    }

    let user = await UserModel.findByEmail(email);
    if (!user) {
        const hash = hashPassword(password || '');
        const result = await UserModel.create(name, email, hash);
        user = { id: result.lastID };
    }

    const cardStatus = cardNumber.startsWith('4') ? 'PAID' : 'DENIED';
    if (cardStatus === 'DENIED') {
        throw Object.assign(new Error('Pagamento recusado'), { status: 400 });
    }

    const enrollment = await EnrollmentModel.create(user.id, courseId);
    await PaymentModel.create(enrollment.lastID, course.price, cardStatus);
    await AuditModel.log(`Checkout curso ${courseId} por usuário ${user.id}`);

    return { enrollmentId: enrollment.lastID };
}

module.exports = { processCheckout };
