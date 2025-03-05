const bridgeService = require('../../services/bridgeService');

exports.deposit = async (req, res) => {
    const { amount } = req.body;
    const userAddress = req.user.address; // Assuming user address is available in req.user

    try {
        const receipt = await bridgeService.deposit(userAddress, amount);
        res.status(200).json({ message: 'Deposit successful', receipt });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

exports.withdraw = async (req, res) => {
    const { amount } = req.body;
    const userAddress = req.user.address;

    try {
        const receipt = await bridgeService.withdraw(userAddress, amount);
        res.status(200).json({ message: 'Withdrawal successful', receipt });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

exports.bridge = async (req, res) => {
    const { amount, targetChain } = req.body;
    const userAddress = req.user.address;

    try {
        const receipt = await bridgeService.bridge(userAddress, amount, targetChain);
        res.status(200).json({ message: 'Bridging successful', receipt });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
