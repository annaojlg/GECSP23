const XYZCoin = artifacts.require("XYZCoin");
const truffleAssert = require("truffle-assertions");

contract("XYZCoin", async accounts => {

    // test cases for part (h)
    it("should set the token name correctly", async() => {
        let xyzCoinInstance = await XYZCoin.deployed();
        assert.equal(await xyzCoinInstance.name(), "XYZCoin");
    });

    it("should initialize the owner balance", async () => {
        let xyzCoinInstance = await XYZCoin.deployed();
        let balance0 = await xyzCoinInstance.balanceOf(accounts[0]);
        let totalSupply = await xyzCoinInstance.totalSupply();

        assert.equal(balance0.toNumber(), totalSupply.toNumber());
    });

    it("should be able to transfer tokens", async() => {
        let xyzCoinInstance = await XYZCoin.deployed();
        const amount = 50;
        let balance0 = await xyzCoinInstance.balanceOf(accounts[0]);
        let balance1 = await xyzCoinInstance.balanceOf(accounts[1]);
        await xyzCoinInstance.transfer(accounts[1], amount, { from: accounts[0] });
        
        assert.equal(await xyzCoinInstance.balanceOf(accounts[0]), balance0.toNumber() - amount);
        assert.equal(await xyzCoinInstance.balanceOf(accounts[1]), balance1.toNumber() + amount);
    });

    const allowanceAmount = 20;

    it("should be able to set and read allowance", async () => {
        let xyzCoinInstance = await XYZCoin.deployed();
        await xyzCoinInstance.approve(accounts[2], allowanceAmount, { from: accounts[0] });

        assert.equal(await xyzCoinInstance.allowance(accounts[0], accounts[2],), allowanceAmount);
        assert.equal(await xyzCoinInstance.allowance(accounts[0], accounts[1],), 0);
    });

    it("should be able to transfer on behalf of other accounts", async () => {
        let xyzCoinInstance = await XYZCoin.deployed();
        let balance0 = await xyzCoinInstance.balanceOf(accounts[0]);
        let balance3 = await xyzCoinInstance.balanceOf(accounts[3]);
        await xyzCoinInstance.transferFrom(accounts[0], accounts[3], allowanceAmount, { from: accounts[2] });

        assert.equal(await xyzCoinInstance.allowance(accounts[0], accounts[2],), 0);
        assert.equal(await xyzCoinInstance.balanceOf(accounts[0]), balance0.toNumber() - allowanceAmount);
        assert.equal(await xyzCoinInstance.balanceOf(accounts[3]), balance3.toNumber() + allowanceAmount);
    });

    // test cases for part (i)
    it("should throw if balance is not enough when transferring tokens using transfer()", async() => {
        const amount = 5000;
        let xyzCoinInstance = await XYZCoin.deployed();
        let balance0 = await xyzCoinInstance.balanceOf(accounts[0]);
        let balance1 = await xyzCoinInstance.balanceOf(accounts[1]);
        await truffleAssert.reverts(xyzCoinInstance.transfer(accounts[1], amount, { from: accounts[0] }));

        assert.equal(await xyzCoinInstance.balanceOf(accounts[0]), balance0.toNumber());
        assert.equal(await xyzCoinInstance.balanceOf(accounts[1]), balance1.toNumber());
    });

    it("should throw if an unauthorized transferFrom happens", async() => {
        const amount = 10;
        let xyzCoinInstance = await XYZCoin.deployed();
        let balance0 = await xyzCoinInstance.balanceOf(accounts[0]);
        let balance1 = await xyzCoinInstance.balanceOf(accounts[1]);
        await truffleAssert.reverts(xyzCoinInstance.transferFrom(accounts[1], accounts[2], amount, { from: accounts[2] }));

        assert.equal(await xyzCoinInstance.balanceOf(accounts[0]), balance0.toNumber());
        assert.equal(await xyzCoinInstance.balanceOf(accounts[1]), balance1.toNumber());
    });

    it("should fire transfer event for transfer() (even for 0 transfers)", async() => {
        const amount = 10;
        let xyzCoinInstance = await XYZCoin.deployed();
        let tx = await xyzCoinInstance.transfer(accounts[1], amount, { from: accounts[0] });
        truffleAssert.eventEmitted(tx, 'Transfer', (ev) => {
            return ev._from === accounts[0] && ev._to === accounts[1] && ev._value.toNumber() === amount;
        });

        let tx2 = await xyzCoinInstance.transfer(accounts[1], 0, { from: accounts[0] });
        truffleAssert.eventEmitted(tx2, 'Transfer', (ev) => {
            return ev._from === accounts[0] && ev._to === accounts[1] && ev._value.toNumber() === 0;
        });
    });

    it("should fire Transfer event for transferFrom() (even for 0 transfers)", async() => {
        const amount = 10;
        let xyzCoinInstance = await XYZCoin.deployed();
        await xyzCoinInstance.approve(accounts[1], amount, { from: accounts[0] });

        let tx = await xyzCoinInstance.transferFrom(accounts[0], accounts[2], amount, { from: accounts[1] });
        truffleAssert.eventEmitted(tx, 'Transfer', (ev) => {
            return ev._from === accounts[0] && ev._to === accounts[2] && ev._value.toNumber() === amount;
        });

        let tx2 = await xyzCoinInstance.transferFrom(accounts[0], accounts[3], 0, { from: accounts[4] });
        truffleAssert.eventEmitted(tx2, 'Transfer', (ev) => {
            return ev._from === accounts[0] && ev._to === accounts[3] && ev._value.toNumber() === 0;
        });
    });

    it("should fire Apporval event when setting an allowance", async() => {
        const amount = 10;
        let xyzCoinInstance = await XYZCoin.deployed();
        let tx = await xyzCoinInstance.approve(accounts[1], amount, { from: accounts[0] });

        truffleAssert.eventEmitted(tx, 'Approval', (ev) => {
            return ev._owner === accounts[0] && ev._spender === accounts[1] && ev._value.toNumber() === amount;
        });
    });
});