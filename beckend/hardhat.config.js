require('@nomiclabs/hardhat-ethers');
require('dotenv').config();

module.exports = {
  solidity: "0.8.27",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配置
    }
  }
};