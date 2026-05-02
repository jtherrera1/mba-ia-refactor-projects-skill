const UserModel = require('../models/userModel');

async function deleteUser(req, res, next) {
    try {
        await UserModel.deleteById(req.params.id);
        res.json({ msg: 'Usuário deletado com sucesso.' });
    } catch (err) {
        next(err);
    }
}

module.exports = { deleteUser };
