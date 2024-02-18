document.addEventListener('DOMContentLoaded', function () {
    var contract=new web3.eth.Contract(abi,address);
    const voteButtons = document.querySelectorAll('.btn-primary');
    voteButtons.forEach((button, index) => {
        button.addEventListener('click', async function () {
            try {
                // Request accounts from MetaMask
                const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                const account = accounts[0];

                const parameter = index;
                await contract.methods.castVote(parameter).send({ from: account });

                console.log(`Vote cast for candidate ${parameter} by account ${account}`);
            } catch (error) {
                console.error('Error casting vote:', error);
            }
        });
    });
});