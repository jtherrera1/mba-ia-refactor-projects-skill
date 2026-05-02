const { db } = require('../database');

const CourseModel = {
    findActiveById: (id) =>
        db.get('SELECT * FROM courses WHERE id = ? AND active = 1', [id]),

    findAll: () =>
        db.all('SELECT * FROM courses', []),
};

module.exports = CourseModel;
