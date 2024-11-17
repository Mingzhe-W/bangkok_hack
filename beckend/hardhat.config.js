require('@nomiclabs/hardhat-ethers');
require('dotenv').config();

module.exports = {
  solidity: "0.8.27",
  networks: {
    sepolia: {
      url: process.env.ALCHEMY_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配置
    },
    morphl2: {
      url: 'https://rpc-quicknode-holesky.morphl2.io',
      accounts: process.env.PRIVATE_KEY !== undefined ? [process.env.PRIVATE_KEY] : [],
      gasPrice: 2000000000
    },
    scrollSepolia: {
      url: "https://sepolia-rpc.scroll.io/" || "",
      accounts:
        process.env.PRIVATE_KEY !== undefined ? [process.env.PRIVATE_KEY] : [],
    },
    polygonpos: {
      url: process.env.ALCHEMY_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配
    },
    mantle: {
      url: process.env.ALCHEMY_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配
    },
    basesepolia: {
      url: process.env.ALCHEMY_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配
    },
    lineasepolia: {
      url: process.env.ALCHEMY_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配
    },
    unichainsepolia: {
      url: process.env.ALCHEMY_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配
    },
    genosissepolia: {
      url: process.env.ALCHEMY_URL, // 在 .env 文件中配置
      accounts: [process.env.PRIVATE_KEY] // 在 .env 文件中配
    },
  }
};