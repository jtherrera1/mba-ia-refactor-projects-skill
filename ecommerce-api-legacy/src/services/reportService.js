const { db } = require('../database');

async function getFinancialReport() {
    const rows = await db.all(`
        SELECT
            c.id     AS course_id,
            c.title  AS course,
            u.name   AS student,
            p.amount AS paid,
            p.status
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        LEFT JOIN users u       ON u.id = e.user_id
        LEFT JOIN payments p    ON p.enrollment_id = e.id
    `);

    const reportMap = {};
    for (const row of rows) {
        if (!reportMap[row.course_id]) {
            reportMap[row.course_id] = { course: row.course, revenue: 0, students: [] };
        }
        if (row.student) {
            if (row.status === 'PAID') reportMap[row.course_id].revenue += row.paid;
            reportMap[row.course_id].students.push({ student: row.student, paid: row.paid || 0 });
        }
    }

    return Object.values(reportMap);
}

module.exports = { getFinancialReport };
