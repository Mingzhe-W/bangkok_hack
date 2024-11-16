// todo: read from, to, value from python output
// todo: execute: npx hardhat run sendTx.js --network sepolia in terminal
async function main() {
    const { ethers } = require('hardhat');

    // 获取合适的网络 provider
    const provider = new ethers.providers.JsonRpcProvider(process.env.SEPOLIA_URL);

    // 使用私钥创建钱包对象
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

    // 设定交易参数
    const tx = {
        to: '0xb18E350DFa4063317849Dd0c76cE9c0eB7b2cc5c', // 接收方地址
        value: ethers.utils.parseEther('0.01'), // 发送的以太数量，0.01ETH
        gasLimit: 21000, // 固定 gas 上限
    };

    // 发起交易
    const transaction = await wallet.sendTransaction(tx);

    // 等待交易确认
    const receipt = await transaction.wait();
    console.log('Transaction successful with hash:', receipt.transactionHash);
}
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
