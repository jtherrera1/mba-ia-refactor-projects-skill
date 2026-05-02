const { db } = require('../database');

const EnrollmentModel = {
    create: (userId, courseId) =>
        db.run('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId]),

    findByCourse: (courseId) =>
        db.all('SELECT * FROM enrollments WHERE course_id = ?', [courseId]),
};

module.exports = EnrollmentModel;
