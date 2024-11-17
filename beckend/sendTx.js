const { ethers } = require('hardhat');
const fs = require('fs');

async function main() {
    // 读取 output.json 文件
    const data = JSON.parse(fs.readFileSync('output.json', 'utf8'));

    // 验证 JSON 数据完整性
    if (!data.to || !data.amount) {
        throw new Error('Missing required fields in output.json: "to" and "amount"');
    }

    // 获取合适的网络 provider
    const provider = new ethers.providers.JsonRpcProvider(process.env.SEPOLIA_URL);

    // 使用私钥创建钱包对象
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

    // 设定交易参数
    const tx = {
        to: data.to, // 从 output.json 获取接收方地址
        value: ethers.utils.parseEther(data.amount.toString()), // 从 output.json 获取发送金额
        gasLimit: 21000, // 固定 gas 上限
    };

    // 发起交易
    console.log('Sending transaction:', tx);
    const transaction = await wallet.sendTransaction(tx);

    // 等待交易确认
    const receipt = await transaction.wait();
    console.log('Transaction successful with hash:', receipt.transactionHash);
    
// // kinto：
    // // 调用 Kinto 的 API 发起交换交易
    // const kintoApiUrl = "https://api.kinto.xyz/v1/swap";
    // try {
    //     const response = await axios.post(kintoApiUrl, swapData, {
    //         headers: {
    //             'Authorization': `Bearer ${process.env.KINTO_API_KEY}`,
    //             'Content-Type': 'application/json',
    //         },
    //     });

    //     // 输出 Kinto API 返回的结果
    //     console.log('Kinto transaction response:', response.data);
    // } catch (error) {
    //     console.error('Error during Kinto API call:', error.response ? error.response.data : error.message);
    // }

}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
